"""Data v2.1: the note package behind each visit (issue 57; schema in docs/data_v2_1.md).

For every visit the generator also writes a templated note, who signed it and when, the orders and results it refers to, and an
EHR audit-trail row (returned only on a second-tier request). Honest providers write notes from the visit's facts with natural
variation; some honest providers use fixed templates and copy forward (a benign baseline, so similarity alone is not a tell). A
cloning provider's note for an upgraded visit reuses a high-level template, claims the inflated MDM elements and a repeated time
statement, and does NOT gain the orders, results or diagnoses the claim lacks. Every signal is a probability scaled by
`clone_signal_strength`; at 0 a cloner's notes look like honest ones except for the inflated claimed levels.

Own random stream, so claims and the records universe are identical to data v2.0 for the same seed and settings.
"""
import numpy as np

import generate_synthetic as g1

NAMES = {code: name for name, code in g1.CONDITIONS}
NAMES.update({code: name for name, code in g1.ACUTE_DX})
NAMES.update({"Z09": "annual follow-up"})
HPI = ["{age}-year-old {sex} here for {reason}.", "Patient, {age}, {sex}, presents with {reason}.", "{age} y/o {sex} seen for {reason}; no new complaints otherwise.",
       "Returns for {reason}. {age}-year-old {sex}.", "{sex} aged {age}, {reason}; symptoms discussed.", "Follow-up visit for {reason}, {age} year old {sex}."]
EXAM = ["Vitals reviewed. Heart regular, lungs clear. Abdomen soft.", "Exam unremarkable apart from the complaint.", "General: well appearing. Cardiac and respiratory exam normal.",
        "Focused exam of the affected area; otherwise normal.", "Alert and oriented. No acute distress.", "Exam consistent with the history."]
PLAN = ["{p}: continue current regimen.", "{p}: counselled on diet and activity; recheck in 3 months.", "{p}: stable today, no change.",
        "{p}: adjusted therapy, follow up in 6 weeks.", "{p}: reviewed with patient; return if worse.", "{p}: monitor."]
HIGH_HPI = "Patient with multiple active chronic conditions presents for comprehensive review of complex medical problems."
HIGH_EXAM = "Detailed multisystem examination performed."
HIGH_PLAN = ("Reviewed prior labs and outside records. Ordered additional labs and tests. Prescription drug management performed. "
             "Discussed risks and benefits of treatment options at length.")
SEXES = {"F": "female", "M": "male"}
NOTE_COLS = ["note_id", "claim_id", "member_id", "rendering_npi", "service_date", "note_text", "problems_addressed", "problems_level", "data_level",
             "risk_level", "documented_minutes", "time_statement", "outside_records_reviewed", "independent_historian"]
AUTH_COLS = ["note_id", "status", "signed_by_npi", "signed_date", "method", "signature_text", "amended", "amended_date"]
ORDER_COLS = ["order_id", "note_id", "claim_id", "order_type", "code", "ordered_date", "ordered_by_npi", "signed"]
RESULT_COLS = ["order_id", "result_present", "result_date"]
AUDIT_COLS = ["note_id", "created_ts", "last_edited_ts", "edit_count", "copy_paste_events", "template_id"]
LAB_NAMES = {"80053": "comprehensive metabolic panel", "85025": "complete blood count"}


def _iso(d, days=0):
    from datetime import timedelta
    return (d + timedelta(days=int(days))).isoformat()


class NoteGen:
    def __init__(self, seed, strength=0.7, honest_template_share=0.10, honest_copy_forward=0.10, late_honest=0.05, unsigned_honest=0.015):
        self.rng = np.random.default_rng([seed, 17])
        self.strength, self.hts, self.hcf, self.late, self.unsigned = strength, honest_template_share, honest_copy_forward, late_honest, unsigned_honest
        self.prov = {}
        self.notes, self.auth, self.orders, self.results, self.audit, self.cloned = [], [], [], [], [], []
        self.n_order = 0

    def _state(self, npi, clones):
        if npi not in self.prov:
            r = self.rng
            self.prov[npi] = {"template": (not clones) and r.random() < self.hts, "hpi": int(r.integers(len(HPI))), "exam": int(r.integers(len(EXAM))),
                              "plan": int(r.integers(len(PLAN))), "minutes": int(r.integers(32, 48)), "tid": f"T{len(self.prov):04d}",
                              "prev": {}}
        return self.prov[npi]

    def _signal(self):
        return self.rng.random() < self.strength

    def add_visit(self, claim_id, claim, member, P, L, B, els_doc, els_true, minutes, tlevel, lab_code, service_date, dx):
        """claim: unused hook; member: dict with sex and birth_year; P: provider state dict; els_doc/els_true: documented and true MDM
        elements; minutes: documented minutes or ''; lab_code: lab CPT on the claim or None; dx: ICD-10 codes on the claim."""
        r, npi = self.rng, P["npi"]
        st = self._state(npi, P["clones"])
        cloned = bool(P["clones"] and B > L)
        signal_here = cloned and self._signal()
        age = 2024 - member["birth_year"]
        sex = SEXES.get(member["sex"], "patient")
        names = [NAMES.get(c, c) for c in dx]
        # problems the note addresses: honest notes follow the level; a cloned note addresses only what the claim shows
        need = {0: 1, 1: 1, 2: 1, 3: 2, 4: 3}[min(els_true[0], 4)]
        n_addr = min(len(dx), need + (1 if r.random() < 0.3 else 0))
        n_addr = max(1, n_addr)
        addressed = dx[:n_addr]
        # text
        reason = names[-1] if names else "follow-up"
        minutes_text = ""
        tstyle = "none"
        mins = minutes
        if minutes != "":
            tstyle = "total" if r.random() < 0.8 else "face_to_face"
            if signal_here and r.random() < 0.8:
                mins = st["minutes"]                             # the same time statement again and again
            minutes_text = (f" Total time on the date of the encounter: {mins} minutes." if tstyle == "total"
                            else f" Face-to-face time with the patient: {mins} minutes.")
        if signal_here:
            lines = [HIGH_HPI, HIGH_EXAM, " ".join(PLAN[st["plan"]].format(p=n) for n in [NAMES.get(c, c) for c in addressed]), HIGH_PLAN + minutes_text]
            template_id = st["tid"] + "H"
        else:
            if st["template"]:
                hpi_i, exam_i, plan_i = st["hpi"], st["exam"], st["plan"]
            else:
                hpi_i, exam_i, plan_i = int(r.integers(len(HPI))), int(r.integers(len(EXAM))), int(r.integers(len(PLAN)))
            hpi = HPI[hpi_i].format(age=age, sex=sex, reason=reason)
            exam = EXAM[exam_i]
            plan = " ".join(PLAN[plan_i].format(p=NAMES.get(c, c)) for c in addressed)
            if member["member_id"] in st["prev"] and r.random() < self.hcf:        # honest copy-forward from the patient's own last note
                hpi, exam = st["prev"][member["member_id"]]
            st["prev"][member["member_id"]] = (hpi, exam)
            extra = ""
            if lab_code:
                extra = f" Ordered {LAB_NAMES.get(lab_code, 'labs')}; results reviewed."
            lines = [hpi, exam, plan + extra + minutes_text]
            template_id = st["tid"] if st["template"] else f"V{int(r.integers(1, 40)):03d}"
        nid = f"N{claim_id[1:]}"
        outside = bool((not signal_here) and els_true[1] >= 2 and not lab_code and r.random() < 0.4)
        self.notes.append({"note_id": nid, "claim_id": claim_id, "member_id": member["member_id"], "rendering_npi": npi,
                           "service_date": service_date.isoformat(), "note_text": " ".join(lines), "problems_addressed": ";".join(addressed),
                           "problems_level": els_doc[0], "data_level": els_doc[1], "risk_level": els_doc[2],
                           "documented_minutes": mins, "time_statement": tstyle, "outside_records_reviewed": int(outside),
                           "independent_historian": int((not signal_here) and r.random() < 0.05)})
        # authentication
        u = r.random()
        bad = (0.04 if signal_here else self.unsigned)
        if u < bad / 2:
            status = "unsigned"
        elif u < bad:
            status = "illegible"
        else:
            status = "signed" if r.random() < 0.72 else "e_signed"
        if signal_here and r.random() < 0.65:
            lag = int(r.integers(4, 31))
        else:
            lag = 0 if r.random() < 0.78 else (int(r.integers(1, 4)) if r.random() < 0.75 else int(r.integers(4, 15)))
            if r.random() < self.late * 0.2:
                lag = int(r.integers(15, 40))
        self.auth.append({"note_id": nid, "status": status, "signed_by_npi": npi, "signed_date": "" if status == "unsigned" else _iso(service_date, lag),
                          "method": "handwritten" if status in ("signed", "illegible") else "electronic",
                          "signature_text": "" if status != "e_signed" else f"Electronically signed by provider {npi}",
                          "amended": 0, "amended_date": ""})
        # orders and results: only what the claim shows (real labs), never inflated
        if lab_code:
            self.n_order += 1
            oid = f"O{self.n_order:08d}"
            self.orders.append({"order_id": oid, "note_id": nid, "claim_id": claim_id, "order_type": "lab", "code": lab_code,
                                "ordered_date": service_date.isoformat(), "ordered_by_npi": npi, "signed": int(r.random() < 0.92)})
            present = r.random() < 0.88
            self.results.append({"order_id": oid, "result_present": int(present), "result_date": _iso(service_date, int(r.integers(0, 3))) if present else ""})
        # audit trail
        copy_events = int(r.poisson(6 if signal_here else 0.8))
        created_lag = lag if (signal_here and lag > 3) else 0
        self.audit.append({"note_id": nid, "created_ts": f"{_iso(service_date, created_lag)}T{int(r.integers(8, 19)):02d}:{int(r.integers(0, 60)):02d}",
                           "last_edited_ts": f"{_iso(service_date, lag)}T{int(r.integers(8, 19)):02d}:{int(r.integers(0, 60)):02d}",
                           "edit_count": int(r.integers(1, 4)), "copy_paste_events": copy_events, "template_id": template_id})
        if cloned:
            self.cloned.append({"claim_id": claim_id, "signal_applied": signal_here})

"""Draws docs/images/audit_postpay_zoom.svg: stages 5 to 7 of the commercial postpay audit, today and with this repository. Hand-written SVG, no libraries. Usage: python docs/make_audit_zoom.py"""
import os

LAB = 250
CW = 262
BH = 62
LH = 76
NCOL = 7
LANES = ["Provider (practice, billing office)", "Payer: payment integrity analyst", "Payer: coder, nurse, clinician", "Payer: legal, medical director", "Payer: finance and recovery", "Payer: SIU (fraud)", None]
COLS = ["5 Screen", "5 Request", "5 Chart review", "5-6 Estimate, findings", "6 Demand", "7 Dispute, appeal", "7 Collect, fees"]
G, Y, B, R = "#bfe3c6", "#fdf0b8", "#cfd8ee", "#e8e8e8"


def panel(title, sub, last_lane, boxes, arrows, y0, o):
    """boxes: id -> (lane, col, text, fill, dashed); arrows: (from, to, kind) kind in main, dash, red"""
    W = LAB + NCOL * CW + 10
    o.append(f'<text x="10" y="{y0 + 24}" font-size="24" font-weight="bold">{title}</text><text x="10" y="{y0 + 46}" fill="#444">{sub}</text>')
    top = y0 + 92
    for i, c in enumerate(COLS):
        x = LAB + i * CW
        o.append(f'<rect x="{x}" y="{top - 24}" width="{CW}" height="{7 * LH + 24}" fill="{"#f4f9f5" if i % 2 else "#fafafa"}" stroke="#ddd"/><text x="{x + CW / 2}" y="{top - 8}" text-anchor="middle" font-weight="bold" font-size="15">{c}</text>')
    lanes = LANES[:6] + [last_lane]
    for j, l in enumerate(lanes):
        y = top + j * LH
        o.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="#aaa"/><text x="8" y="{y + LH / 2 + 5}" font-weight="bold" font-size="14">{l}</text>')
    o.append(f'<line x1="0" x2="{W}" y1="{top + 7 * LH}" y2="{top + 7 * LH}" stroke="#aaa"/>')
    pos = {}
    for k, (lane, col, text, fill, dash) in boxes.items():
        x = LAB + col * CW + 10
        y = top + lane * LH + (LH - BH) / 2
        pos[k] = (x, y, CW - 20, BH)
        d = ' stroke-dasharray="5 3"' if dash else ""
        o.append(f'<rect x="{x}" y="{y}" width="{CW - 20}" height="{BH}" rx="7" fill="{fill}" stroke="#444"{d}/>')
        lines = text.split("|")
        y1 = y + BH / 2 - (len(lines) - 1) * 8 + 5
        for n, t in enumerate(lines):
            o.append(f'<text x="{x + (CW - 20) / 2}" y="{y1 + n * 16}" text-anchor="middle" font-size="13.5">{t}</text>')
    for a, b, kind in arrows:
        xa, ya, wa, ha = pos[a]
        xb, yb, wb, hb = pos[b]
        col = {"main": "#222", "dash": "#666", "red": "#c0392b"}[kind]
        dash = ' stroke-dasharray="6 4"' if kind != "main" else ""
        if abs(xa - xb) < 5:                                           # same column: vertical
            y_s, y_e = (ya + ha, yb) if yb > ya else (ya, yb + hb)
            d = f"M{xa + wa / 2},{y_s} L{xb + wb / 2},{y_e}"
        else:
            xs, xe = xa + wa, xb
            ys, ye = ya + ha / 2, yb + hb / 2
            xm = xe - 10                                               # vertical run in the gap before the target column
            d = f"M{xs},{ys} L{xm},{ys} L{xm},{ye} L{xe},{ye}"
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"{dash} marker-end="url(#ah{kind})"/>')
    return top + 7 * LH


def main():
    W = LAB + NCOL * CW + 10
    o = [f'<defs>' + "".join(f'<marker id="ah{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for k, c in (("main", "#222"), ("dash", "#666"), ("red", "#c0392b"))) + '</defs>']
    o.append('<rect width="100%" height="100%" fill="#fff"/>')
    o.append('<text x="10" y="30" font-size="30" font-weight="bold">Stages 5 to 7 of the commercial postpay audit: today and with this repository</text>')
    o.append('<text x="10" y="54" fill="#444" font-size="15">Yellow = the provider. Blue = payer staff. Green = software in this repository (simulated; it does not send letters or findings). Dashed grey = vendor, optional. Red dashed = dispute and appeal. People still sign the list and the demand.</text>')
    today = {
        "t_sig": (5, 0, "SIU: tips, complaints,|referrals", B, False),
        "t_fraud": (5, 1, "Fraud cases: referral to|state or law enforcement", B, False),
        "t_scr": (1, 0, "Screen paid claims,|pick providers (peers, tips)", B, False),
        "t_req": (1, 1, "Draft records request,|choose sample of claims", B, False),
        "t_pr1": (0, 1, "Receives request|(30 to 45 days to answer)", Y, False),
        "t_pr2": (0, 2, "Assembles and sends charts|(manual, fax or portal)", Y, False),
        "t_cod": (2, 2, "Code each chart; nurse, then|physician review (10-15/hour)", B, False),
        "t_ven3": (6, 2, "Vendor reviews, extrapolates|(15% to 30% of recovery)", R, True),
        "t_est": (1, 3, "Extrapolate the sample|to all the provider's claims", B, False),
        "t_meet": (2, 3, "Findings meeting, written|findings (2 to 4 weeks)", B, False),
        "t_md": (3, 3, "Medical director|signs off findings", B, False),
        "t_not": (4, 4, "Overpayment notice,|settlement offer", B, False),
        "t_prd": (0, 4, "Repays, or disputes|within 30 days", Y, False),
        "t_dis": (0, 5, "Dispute, appeal;|may leave the network", Y, False),
        "t_leg": (3, 5, "Legal and medical director|answer (30 days)", B, False),
        "t_off": (4, 6, "Offset on later 835s;|books the recovery", B, False),
        "t_ref": (0, 6, "Refund or offset|taken from payments", Y, False),
        "t_inv": (6, 6, "Vendor invoice:|contingency fee", R, True),
    }
    t_arrows = [("t_sig", "t_scr", "main"), ("t_sig", "t_fraud", "main"), ("t_scr", "t_req", "main"), ("t_req", "t_pr1", "main"), ("t_pr1", "t_pr2", "main"), ("t_pr2", "t_cod", "main"), ("t_cod", "t_est", "main"),
                ("t_ven3", "t_est", "dash"), ("t_est", "t_meet", "main"), ("t_meet", "t_md", "main"), ("t_md", "t_not", "main"), ("t_not", "t_prd", "main"), ("t_prd", "t_dis", "red"), ("t_dis", "t_leg", "red"),
                ("t_leg", "t_off", "red"), ("t_not", "t_off", "main"), ("t_off", "t_ref", "main"), ("t_off", "t_inv", "dash")]
    y = panel("Today", "Humans do every hand-off. Most of the cost is chart review and the chain of sign-offs; a vendor, if used, takes a share of the recovery.", "Vendor (optional)", today, t_arrows, 70, o)
    proj = {
        "p_sig": (5, 0, "SIU: tips, complaints,|referrals", B, False),
        "p_fraud": (5, 5, "Fraud cases: referral|(unchanged)", B, False),
        "p_scr": (6, 0, "Statistical screen and volume|lane (30+ visits in a day)", G, False),
        "p_list": (1, 1, "Reviews and approves|the list (a person)", B, False),
        "p_req": (6, 1, "Chooses whom to ask and how|many charts; writes the request", G, False),
        "p_pr": (0, 2, "Receives request,|sends charts", Y, False),
        "p_rd": (6, 2, "Reads each chart by rule; a|model only where rules are silent", G, False),
        "p_est": (6, 3, "Lower-bound estimate; demand|only if it covers its cost", G, False),
        "p_chk": (2, 3, "Reviews cases the rules|cannot decide", B, False),
        "p_pkt": (1, 3, "Approves and signs|the demand (a person)", B, False),
        "p_not": (4, 4, "Notice and settlement|(unchanged)", B, False),
        "p_prd": (0, 4, "Repays, or disputes", Y, False),
        "p_dis": (0, 5, "Dispute, appeal;|may leave the network", Y, False),
        "p_leg": (3, 5, "Legal and medical director|answer (unchanged)", B, False),
        "p_off": (4, 6, "Offset on later 835s", B, False),
        "p_ref": (0, 6, "Refund or offset|taken from payments", Y, False),
    }
    p_arrows = [("p_sig", "p_scr", "main"), ("p_sig", "p_fraud", "main"), ("p_scr", "p_list", "main"), ("p_list", "p_req", "main"), ("p_req", "p_pr", "main"), ("p_pr", "p_rd", "main"), ("p_rd", "p_est", "main"),
                ("p_est", "p_chk", "main"), ("p_chk", "p_pkt", "main"), ("p_pkt", "p_not", "main"), ("p_not", "p_prd", "main"), ("p_prd", "p_dis", "red"), ("p_dis", "p_leg", "red"), ("p_leg", "p_off", "red"),
                ("p_not", "p_off", "main"), ("p_off", "p_ref", "main")]
    y2 = panel("With this repository", "Software screens, chooses whom to ask, reads charts by rule and estimates; a person approves the list and signs the demand. Everything downstream of the demand is unchanged.", "This repository (software)", proj, p_arrows, y + 20, o)
    H = int(y2 + 40)
    o.append(f'<text x="10" y="{H - 14}" fill="#444" font-size="13">Steps and timings: docs/audit_actors_research.md. Dollars: docs/audit_in_context.md. A simplification: not every path is drawn. The lower panel is what the simulation does, not a deployed product.</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">' + "\n".join(o) + "</svg>"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "audit_postpay_zoom.svg")
    open(out, "w").write(svg)
    print("wrote", out, W, H)


if __name__ == "__main__":
    main()

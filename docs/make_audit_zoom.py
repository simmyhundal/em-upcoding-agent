"""Draws docs/images/audit_postpay_zoom.svg from docs/diagram_src/audit_workflow.csv, the single source of truth for the postpay audit diagram (one row per box: panel, id, lane,
column, copy, colour kind, counterpart in the other panel, next steps with arrow style). To change the diagram, edit the CSV and rerun. Hand-written SVG, no libraries. Usage: python docs/make_audit_zoom.py"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LAB, CW, BH, LH = 250, 262, 62, 76
COLS = ["Screen", "Request", "Chart review", "Estimate, findings", "Demand", "Dispute, appeal", "Collect, fees"]
LANES = ["Provider", "Payer: payment integrity analyst", "Payer: coder, nurse, clinician", "Payer: legal, medical director", "Payer: finance and recovery", None, "Payer: SIU"]
LAST = {"today": "Vendor (optional)", "agent": "PI Agent (software)"}
KINDS = {  # kind -> (fill, dashed, label in the key)
    "provider": ("#fdf0b8", False, "Provider"),
    "payer": ("#d3dcf0", False, "Payer staff, step as today"),
    "payer_changed": ("#7f9be0", False, "Payer staff, step changed by PI Agent"),
    "software": ("#bfe3c6", False, "PI Agent (software)"),
    "vendor": ("#e8e8e8", True, "Vendor (optional)"),
}
ARROW = {"main": "#222", "dash": "#666", "red": "#c0392b"}
TITLES = {"today": ("Today", "People do every hand-off; the chart review and sign-offs carry most of the cost."),
          "agent": ("With PI Agent", "Software screens, requests, reads and estimates; people approve the list and sign the demand.")}


def load():
    rows = list(csv.DictReader(open(os.path.join(HERE, "diagram_src", "audit_workflow.csv"))))
    for r in rows:
        r["lane"], r["col"] = int(r["lane"]), int(r["col"])
        r["next"] = [tuple((x.split(":") + ["main", ""])[:3]) for x in r["next"].split(";") if x]
    return rows


def panel(panel_name, rows, y0, o):
    W = LAB + len(COLS) * CW + 10
    title, sub = TITLES[panel_name]
    o.append(f'<text x="10" y="{y0 + 24}" font-size="24" font-weight="bold">{title}</text><text x="10" y="{y0 + 46}" fill="#444">{sub}</text>')
    top = y0 + 92
    for i, c in enumerate(COLS):
        x = LAB + i * CW
        o.append(f'<rect x="{x}" y="{top - 24}" width="{CW}" height="{7 * LH + 24}" fill="{"#f4f9f5" if i % 2 else "#fafafa"}" stroke="#ddd"/><text x="{x + CW / 2}" y="{top - 8}" text-anchor="middle" font-weight="bold" font-size="15">{c}</text>')
    for j, l in enumerate(LANES[:5] + [LAST[panel_name], LANES[6]]):
        y = top + j * LH
        o.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="#aaa"/><text x="8" y="{y + LH / 2 + 5}" font-weight="bold" font-size="14">{l}</text>')
    o.append(f'<line x1="0" x2="{W}" y1="{top + 7 * LH}" y2="{top + 7 * LH}" stroke="#aaa"/>')
    mine = [r for r in rows if r["panel"] == panel_name]
    pos = {}
    for r in mine:
        x, y = LAB + r["col"] * CW + 10, top + r["lane"] * LH + (LH - BH) / 2
        pos[r["id"]] = (x, y, CW - 20, BH)
        fill, dashed, _ = KINDS[r["kind"]]
        d = ' stroke-dasharray="5 3"' if dashed else ""
        txt = "#fff" if r["kind"] == "payer_changed" else "#111"
        o.append(f'<rect x="{x}" y="{y}" width="{CW - 20}" height="{BH}" rx="7" fill="{fill}" stroke="#444"{d}/>')
        words, lines, cur = r["copy"].split(), [], ""
        for w in words:                                                    # wrap at about 32 characters
            if len(cur) + len(w) + 1 > 32 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        y1 = y + BH / 2 - (len(lines) - 1) * 8 + 5
        for n, t in enumerate(lines):
            o.append(f'<text x="{x + (CW - 20) / 2}" y="{y1 + n * 16}" text-anchor="middle" font-size="13.5" fill="{txt}">{t}</text>')
    for r in mine:
        for tgt, kind, flag in r["next"]:
            xa, ya, wa, ha = pos[r["id"]]
            xb, yb, wb, hb = pos[tgt]
            dash = ' stroke-dasharray="6 4"' if kind != "main" else ""
            if flag == "L":                                                # same column, routed through the gap on the left
                xg = xa - 5
                d = f"M{xa},{ya + ha / 2} L{xg},{ya + ha / 2} L{xg},{yb + hb / 2} L{xb},{yb + hb / 2}"
            elif abs(xa - xb) < 5:
                ys, ye = (ya + ha, yb) if yb > ya else (ya, yb + hb)
                d = f"M{xa + wa / 2},{ys} L{xb + wb / 2},{ye}"
            else:
                xs, xe, ys, ye = xa + wa, xb, ya + ha / 2, yb + hb / 2
                xm = xe - 10                                                # vertical run in the gap before the target column
                d = f"M{xs},{ys} L{xm},{ys} L{xm},{ye} L{xe},{ye}"
            o.append(f'<path d="{d}" fill="none" stroke="{ARROW[kind]}" stroke-width="2"{dash} marker-end="url(#ah{kind})"/>')
    return top + 7 * LH


def key(y, o):
    x = 10
    o.append(f'<text x="{x}" y="{y + 4}" font-weight="bold" font-size="14">Key</text>')
    x = 60
    for k, (fill, dashed, label) in KINDS.items():
        d = ' stroke-dasharray="5 3"' if dashed else ""
        o.append(f'<rect x="{x}" y="{y - 12}" width="26" height="18" rx="4" fill="{fill}" stroke="#444"{d}/><text x="{x + 34}" y="{y + 3}" font-size="14">{label}</text>')
        x += 56 + 8 * len(label)
    for label, col, dash in (("Step", "#222", ""), ("Optional (vendor)", "#666", "6 4"), ("Dispute and appeal", "#c0392b", "6 4")):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<line x1="{x}" x2="{x + 34}" y1="{y - 3}" y2="{y - 3}" stroke="{col}" stroke-width="2"{da}/><text x="{x + 42}" y="{y + 3}" font-size="14">{label}</text>')
        x += 60 + 8 * len(label)


def main():
    rows = load()
    W = LAB + len(COLS) * CW + 10
    o = ['<defs>' + "".join(f'<marker id="ah{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for k, c in ARROW.items()) + '</defs>',
         '<rect width="100%" height="100%" fill="#fff"/>', '<text x="10" y="30" font-size="30" font-weight="bold">The postpay audit: today and with PI Agent</text>']
    key(62, o)
    y = panel("today", rows, 76, o)
    y2 = panel("agent", rows, y + 20, o)
    H = int(y2 + 40)
    o.append(f'<text x="10" y="{H - 14}" fill="#444" font-size="13">A simplification: not every path is drawn. PI Agent is simulated on synthetic claims.</text>')
    open(os.path.join(HERE, "images", "audit_postpay_zoom.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">' + "\n".join(o) + "</svg>")
    print("wrote svg", W, H)


if __name__ == "__main__":
    main()

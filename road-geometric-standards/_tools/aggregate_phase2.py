#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 2 aggregation: read every _content__*.json under free/** and mixed/**,
emit CONTENT_VERIFICATION.md and content_summary.json. Print non-CONFIRMED items."""
import os, sys, json, io
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"D:\My Drive\Nauka\standardi\road-geometric-standards"
def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")

recs = []
for sub in ("free", "mixed"):
    for dp, _, fs in os.walk(os.path.join(ROOT, sub)):
        for f in fs:
            if f.startswith("_content__") and f.endswith(".json"):
                try:
                    d = json.load(open(os.path.join(dp, f), encoding="utf-8"))
                except Exception as e:
                    d = {"file": f, "verdict": "PARSE_ERROR", "notes": str(e)}
                d["_folder"] = rel(dp)
                recs.append(d)
recs.sort(key=lambda r: (r.get("_folder", ""), r.get("file", "")))

def keypages(r):
    cats = r.get("categories", {})
    parts = []
    for short, c in (("DS","DESIGN_SPEED"),("SD","SIGHT_DISTANCE"),("HOR","HORIZONTAL"),
                     ("VER","VERTICAL"),("SE","SUPERELEVATION"),("CS","CROSS_SECTION")):
        v = cats.get(c, {})
        if v.get("hit"): parts.append(f"{short}:p{v.get('page')}")
    return " ".join(parts) if parts else "—"

# CONTENT_VERIFICATION.md
m = io.StringIO()
m.write("# CONTENT_VERIFICATION — geometric-content check of every downloaded PDF (Phase 2)\n\n")
m.write("Verdict rule: CONFIRMED = >=4 categories incl. design-speed or sight-distance · "
        "PARTIAL = 2-3 · NO_GEOMETRY <=1 · NEEDS_OCR = image-only scan. "
        "Coverage of 6 concept categories matched in each doc's own language + English.\n\n")
m.write("| File | ISO3 | Lang | Verdict | N/6 | Key pages | Refetch hint |\n")
m.write("|---|---|---|---|---|---|---|\n")
for r in recs:
    nN = r.get("categories_hit_verified", r.get("categories_hit", 0))
    m.write("| {f} | {iso} | {lg} | {v} | {n}/6 | {kp} | {rf} |\n".format(
        f=r.get("file",""), iso=r.get("iso3",""), lg=r.get("lang",""),
        v=r.get("verdict",""), n=nN, kp=keypages(r),
        rf=(r.get("refetch_hint","") or "—")))
with open(os.path.join(ROOT, "CONTENT_VERIFICATION.md"), "w", encoding="utf-8") as fh:
    fh.write(m.getvalue())

# content_summary.json
counts = Counter(r.get("verdict","?") for r in recs)
nonconf = [{"file": r.get("file"), "iso3": r.get("iso3"), "verdict": r.get("verdict"),
            "refetch_hint": r.get("refetch_hint",""), "notes": r.get("notes","")}
           for r in recs if r.get("verdict") != "CONFIRMED"]
summary = {"total_pdfs": len(recs), "by_verdict": dict(counts),
           "confirmed": counts.get("CONFIRMED",0), "partial": counts.get("PARTIAL",0),
           "no_geometry": counts.get("NO_GEOMETRY",0), "needs_ocr": counts.get("NEEDS_OCR",0),
           "non_confirmed": nonconf}
with open(os.path.join(ROOT, "content_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=2, ensure_ascii=False)

print(json.dumps({k: summary[k] for k in ("total_pdfs","by_verdict")}, indent=2, ensure_ascii=False))
print("\nNon-CONFIRMED:")
for x in nonconf:
    print(f"  [{x['verdict']}] {x['iso3']} {x['file']}")
    print(f"        -> {x['refetch_hint'] or x['notes'][:120]}")

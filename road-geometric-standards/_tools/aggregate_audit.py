#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggregate _audit/<ISO3>.json -> AUDIT.md + audit_summary.json."""
import os, json, sys, io
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\My Drive\Nauka\standardi\road-geometric-standards"
AUD = os.path.join(ROOT, "_audit")
DATE = "2026-06-14"

recs = []
for f in sorted(os.listdir(AUD)):
    if f.endswith(".json"):
        try:
            recs.append(json.load(open(os.path.join(AUD, f), encoding="utf-8-sig")))
        except Exception as e:
            print("parse error", f, e)

order = {"COMPLETE": 0, "ADEQUATE_CORE": 1, "PARTIAL": 2, "FRAGMENT": 3}
recs.sort(key=lambda r: (order.get(r.get("verdict"), 9), r.get("iso3", "")))

def is_free(m):  return "free" in (m.get("free_or_paid", "") or "").lower()
def is_paid(m):  return "paid" in (m.get("free_or_paid", "") or "").lower()

from collections import Counter
vc = Counter(r.get("verdict", "?") for r in recs)

m = io.StringIO()
m.write("# AUDIT — kompletnost preuzetih standarda po zemlji\n\n")
m.write(f"Datum: {DATE}. Auditovano {len(recs)} zemalja (po jedan agent po zemlji, samo zvanični izvori).\n\n")
m.write("**Verdikt:** "
        + " · ".join(f"{k}={vc.get(k,0)}" for k in ["COMPLETE","ADEQUATE_CORE","PARTIAL","FRAGMENT"]) + "\n\n")
m.write("Legenda verdikta: COMPLETE = ništa bitno ne fali · ADEQUATE_CORE = jezgro pokriveno, manje praznine · "
        "PARTIAL = bitni delovi nedostaju · FRAGMENT = samo mali deo.\n\n")

m.write("## Pregled\n\n")
m.write("| ISO3 | Zemlja | Verdikt | Izdanje aktuelno? | # fali | Ključno što fali |\n")
m.write("|---|---|---|---|---|---|\n")
for r in recs:
    miss = r.get("missing", []) or []
    ed = "da" if r.get("current_edition_ok") else "**NE**"
    key = (r.get("key_missing") or "; ".join(x.get("doc","") for x in miss) or "—")
    if len(key) > 130: key = key[:127] + "…"
    m.write(f"| {r.get('iso3','')} | {r.get('country','')} | {r.get('verdict','')} | {ed} | {len(miss)} | {key} |\n")

# Free actionable gaps
m.write("\n## Besplatne praznine — preporučeno skinuti (Faza 0d)\n\n")
m.write("| ISO3 | Dokument | Zašto bitno | URL |\n|---|---|---|---|\n")
free_count = 0
for r in recs:
    for x in (r.get("missing", []) or []):
        if is_free(x):
            free_count += 1
            why = (x.get("why_essential","") or "")[:90]
            m.write(f"| {r.get('iso3','')} | {x.get('doc','')} | {why} | {x.get('url','')} |\n")
if free_count == 0: m.write("| — | (nema besplatnih praznina) | | |\n")

# Paid / restricted gaps
m.write("\n## Plaćene / restriktivne praznine\n\n")
m.write("| ISO3 | Dokument | Zašto bitno | Izvor |\n|---|---|---|---|\n")
paid_count = 0
for r in recs:
    for x in (r.get("missing", []) or []):
        if is_paid(x) and not is_free(x):
            paid_count += 1
            why = (x.get("why_essential","") or "")[:90]
            m.write(f"| {r.get('iso3','')} | {x.get('doc','')} | {why} | {x.get('url','')} |\n")
if paid_count == 0: m.write("| — | (nema) | | |\n")

# Edition-superseded flags
m.write("\n## Zastarela izdanja (provera/zamena)\n\n")
sup = [r for r in recs if not r.get("current_edition_ok")]
if sup:
    for r in sup:
        m.write(f"- **{r.get('iso3')}** — {(r.get('notes','') or r.get('note',''))[:260]}\n")
else:
    m.write("- (sva izdanja aktuelna)\n")

with open(os.path.join(ROOT, "AUDIT.md"), "w", encoding="utf-8") as fh:
    fh.write(m.getvalue())

summary = {"date": DATE, "audited": len(recs), "by_verdict": dict(vc),
           "free_gaps": free_count, "paid_gaps": paid_count,
           "superseded_edition": [r.get("iso3") for r in sup]}
json.dump(summary, open(os.path.join(ROOT, "audit_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(json.dumps(summary, ensure_ascii=False, indent=2))

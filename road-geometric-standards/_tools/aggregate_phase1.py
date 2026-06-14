#!/usr/bin/env python3
"""Phase 1 aggregation: read every _result.json, emit MANIFEST.md, BUY_LIST.md,
summary.json, download.log. Single-writer step (no worker write races)."""
import os, json, io

ROOT = r"D:\My Drive\Nauka\standardi\road-geometric-standards"

def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")

records, logs = [], []
for dirpath, dirs, files in os.walk(ROOT):
    if "_tools" in rel(dirpath).split("/"):
        continue
    if "_result.json" in files:
        p = os.path.join(dirpath, "_result.json")
        try:
            with open(p, encoding="utf-8-sig") as f:
                rec = json.load(f)
        except Exception as e:
            rec = {"_parse_error": str(e), "country": "?", "standard": "?"}
        rec["_folder"] = rel(dirpath)
        rec["_has_tobuy"] = os.path.exists(os.path.join(dirpath, "TO_BUY.md"))
        records.append(rec)
    if "_log.txt" in files:
        lp = os.path.join(dirpath, "_log.txt")
        try:
            with open(lp, encoding="utf-8", errors="replace") as f:
                logs.append((rel(dirpath), f.read()))
        except Exception as e:
            logs.append((rel(dirpath), f"<<could not read _log.txt: {e}>>"))

records.sort(key=lambda r: r.get("_folder", ""))

def g(r, k, d=""): return r.get(k, d) if r.get(k, d) not in (None,) else d
def short(s, n=12): return (s[:n] if s else "")
def base(f):
    f = g(r, "file")
    return os.path.basename(f) if f else ""

# ---------- MANIFEST.md ----------
m = io.StringIO()
m.write("# MANIFEST — national road geometric-design standards (Phase 1)\n\n")
m.write(f"Total items: {len(records)}\n\n")
m.write("| ISO3 | Country | Standard | Status | Result | File | Pages | Size (KB) | SHA-256 (short) | Source |\n")
m.write("|---|---|---|---|---|---|---|---|---|---|\n")
for r in records:
    f = g(r, "file"); fb = os.path.basename(f) if f else ""
    kb = g(r, "bytes", 0)
    kb = f"{round(int(kb)/1024):,}" if isinstance(kb, (int, float)) and kb else ""
    src = g(r, "source_url") or g(r, "store_url")
    m.write("| {iso} | {ctry} | {std} | {st} | {res} | {file} | {pg} | {kb} | {sha} | {src} |\n".format(
        iso=g(r, "iso3"), ctry=g(r, "country"), std=g(r, "standard").replace("|", "/"),
        st=g(r, "status"), res=g(r, "result"), file=fb, pg=g(r, "pages", ""),
        kb=kb, sha=short(g(r, "sha256")), src=src))
with open(os.path.join(ROOT, "MANIFEST.md"), "w", encoding="utf-8") as fh:
    fh.write(m.getvalue())

# ---------- BUY_LIST.md ----------
buy = [r for r in records if g(r, "status") in ("paid", "mixed") or r.get("_has_tobuy")]
b = io.StringIO()
b.write("# BUY_LIST — paid & mixed-paid items\n\n")
b.write("Prices are in mixed currencies (USD/CAD/EUR/INR/JPY/RMB) — see per-currency notes at bottom; "
        "no single cross-currency total is meaningful. Nothing was purchased.\n\n")
b.write("| ISO3 | Country | Standard | Item / order code | Price (as listed/surveyed) | Store URL | Note |\n")
b.write("|---|---|---|---|---|---|---|\n")
for r in buy:
    price = g(r, "price") or "(see TO_BUY.md)"
    store = g(r, "store_url") or g(r, "source_url")
    note = "paid title" if g(r, "status") == "paid" else "mixed: free core retrieved, paid part flagged"
    b.write("| {iso} | {ctry} | {std} | {code} | {price} | {store} | {note} |\n".format(
        iso=g(r, "iso3"), ctry=g(r, "country"), std=g(r, "standard").replace("|", "/"),
        code="(see TO_BUY.md)", price=price, store=store, note=note))
b.write("\n> Each item's TO_BUY.md in its folder carries the exact item/order code(s) and why it is paid.\n")
with open(os.path.join(ROOT, "BUY_LIST.md"), "w", encoding="utf-8") as fh:
    fh.write(b.getvalue())

# ---------- summary.json ----------
from collections import Counter
res_counts = Counter(g(r, "result", "unknown") for r in records)
st_counts = Counter(g(r, "status", "unknown") for r in records)
summary = {
    "total_items": len(records),
    "by_result": dict(res_counts),
    "by_status": dict(st_counts),
    "retrieved": res_counts.get("retrieved", 0),
    "paywalled": res_counts.get("paywalled", 0),
    "needs_manual": res_counts.get("needs_manual", 0),
    "failed": res_counts.get("failed", 0),
    "buy_list_items": len(buy),
}
with open(os.path.join(ROOT, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=2, ensure_ascii=False)

# ---------- download.log ----------
with open(os.path.join(ROOT, "download.log"), "w", encoding="utf-8") as fh:
    for folder, text in sorted(logs):
        fh.write(f"\n===== {folder} =====\n")
        fh.write(text.rstrip() + "\n")

print(json.dumps(summary, indent=2, ensure_ascii=False))
print("\nRecords:", len(records), "| logs:", len(logs), "| buy items:", len(buy))

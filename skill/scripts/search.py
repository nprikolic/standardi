#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""world-road-design-standards — v0 live search over the PDF corpus.

This is the NACRT (draft) retrieval tool: it extracts text on demand with pdftotext,
caches it, and searches multilingual concept terms (from reference/glossary.json) across
the corpus. To be replaced in Faza 1-3 by a proper text index + normalized parameter DB.

Usage:
  python search.py --concept WEAVING                 # all hits for a concept, every standard
  python search.py --concept SUPERELEVATION --iso3 ESP
  python search.py --grep "vitoperenje"              # free-text substring
  python search.py --list-concepts
Options:
  --max N        max snippets printed per file (default 5)
  --context N    snippet chars on each side (default 90)
"""
import os, sys, json, subprocess, argparse, re

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
CORPUS = os.path.abspath(os.path.join(SKILL, "..", "road-geometric-standards"))
GLOSSARY = os.path.join(SKILL, "reference", "glossary.json")
CACHE = os.path.join(SKILL, ".textcache")

def load_glossary():
    with open(GLOSSARY, encoding="utf-8") as f:
        return json.load(f)["concepts"]

def iso3_of(folder):
    rp = os.path.join(folder, "_result.json")
    if os.path.exists(rp):
        try:
            return json.load(open(rp, encoding="utf-8-sig")).get("iso3", "") or "MODEL"
        except Exception:
            pass
    return "MODEL"

def find_pdfs(iso3_filter=None):
    out = []
    for sub in ("free", "mixed", "paid"):
        base = os.path.join(CORPUS, sub)
        if not os.path.isdir(base):
            continue
        for dp, _, fs in os.walk(base):
            iso = iso3_of(dp)
            if iso3_filter and iso.upper() != iso3_filter.upper():
                continue
            for fn in fs:
                if fn.lower().endswith(".pdf"):
                    out.append((iso, dp, os.path.join(dp, fn)))
    return out

def get_pages(pdf):
    rel = os.path.relpath(pdf, CORPUS).replace("\\", "_").replace("/", "_")
    cp = os.path.join(CACHE, rel + ".txt")
    if os.path.exists(cp) and os.path.getmtime(cp) >= os.path.getmtime(pdf):
        txt = open(cp, encoding="utf-8", errors="replace").read()
    else:
        try:
            r = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", pdf, "-"],
                               capture_output=True, timeout=600)
            txt = r.stdout.decode("utf-8", "replace")
        except Exception as e:
            return None, f"pdftotext failed: {e}"
        os.makedirs(CACHE, exist_ok=True)
        open(cp, "w", encoding="utf-8").write(txt)
    return txt.split("\f"), ""

def search_terms(pages, terms, context):
    hits = []
    for i, pg in enumerate(pages):
        low = pg.lower()
        for t in terms:
            tl = t.lower()
            start = 0
            while True:
                k = low.find(tl, start)
                if k < 0:
                    break
                a = max(0, k - context); b = min(len(pg), k + len(t) + context)
                snip = re.sub(r"\s+", " ", pg[a:b]).strip()
                hits.append((i + 1, t, snip))
                start = k + len(tl)
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept"); ap.add_argument("--grep")
    ap.add_argument("--iso3"); ap.add_argument("--max", type=int, default=5)
    ap.add_argument("--context", type=int, default=90)
    ap.add_argument("--list-concepts", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    gloss = load_glossary()
    if a.list_concepts:
        print("Concepts:", ", ".join(gloss.keys())); return
    if a.concept:
        c = a.concept.upper()
        if c not in gloss:
            print(f"Unknown concept '{c}'. Available: {', '.join(gloss)}"); sys.exit(2)
        terms = sorted({t for lang in gloss[c].values() if isinstance(lang, list) for t in lang}, key=len, reverse=True)
        label = f"concept {c}"
    elif a.grep:
        terms = [a.grep]; label = f"grep '{a.grep}'"
    else:
        ap.print_help(); return

    pdfs = find_pdfs(a.iso3)
    print(f"# Search: {label}  | corpus PDFs scanned: {len(pdfs)}"
          + (f" (iso3={a.iso3})" if a.iso3 else "") + "\n")
    total_files = 0
    for iso, dp, pdf in sorted(pdfs):
        pages, err = get_pages(pdf)
        if pages is None:
            print(f"  ! {os.path.basename(pdf)}: {err}"); continue
        hits = search_terms(pages, terms, a.context)
        if not hits:
            continue
        total_files += 1
        std = os.path.basename(dp)
        print(f"## {iso}  {std}/{os.path.basename(pdf)}  — {len(hits)} hit(s)")
        seen_pages = set()
        shown = 0
        for pg, term, snip in hits:
            key = (pg, term)
            if key in seen_pages:
                continue
            seen_pages.add(key)
            print(f"   p.{pg:>4}  [{term}]  …{snip}…")
            shown += 1
            if shown >= a.max:
                print(f"   … (+{len(hits)-shown} more hits)"); break
        print()
    print(f"# Files with hits: {total_files}/{len(pdfs)}")

if __name__ == "__main__":
    main()

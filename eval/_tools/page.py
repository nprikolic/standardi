#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print the verbatim text of one corpus page — for grounding/quoting.

Usage:
  python eval/_tools/page.py "<doc_id>" <page>
  python eval/_tools/page.py "<doc_id>" <page> --find "substring"   # show match context
Use the exact doc_id printed by query.py (folder::pdfstem).
"""
import sys, argparse
import lib  # noqa: E402  (same dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc_id")
    ap.add_argument("page", type=int)
    ap.add_argument("--find", help="highlight context around a substring")
    ap.add_argument("--max", type=int, default=2500)
    a = ap.parse_args()
    txt = lib.page_text(a.doc_id, a.page)
    if not txt:
        print(f"(no text for {a.doc_id} p.{a.page} — check doc_id / page / NEEDS_OCR)")
        return
    if a.find:
        low = txt.lower(); k = low.find(a.find.lower())
        if k < 0:
            print(f"(substring not found on this page)\n--- full page ---")
            print(txt[:a.max]); return
        s = max(0, k - 200); e = min(len(txt), k + len(a.find) + 200)
        print(f"FOUND at offset {k}:\n…{txt[s:e]}…")
    else:
        print(txt[:a.max] + ("\n…[truncated]" if len(txt) > a.max else ""))


if __name__ == "__main__":
    main()

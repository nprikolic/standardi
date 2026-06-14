#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ANTI-FABRICATION GATE: verify every ground-truth quote is LITERALLY on its page.

For each question's expected[{doc_id,page,quote}], load the verbatim page text and
require the quote (split on ellipsis into fragments) to appear as a substring after
whitespace+unicode normalisation. Checks page and page±1. Reports PASS/FAIL.

Silent questions (is_silent) are reported as MANUAL (negative claims verified by hand).
Exit code != 0 if any non-silent expected fails — so a bad ground-truth can't slip in.
"""
import os, sys, re, json, unicodedata, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib                                                    # noqa: E402
import yaml                                                   # noqa: E402


def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def fragments(quote):
    parts = re.split(r"…+|\.\.\.+|\[\.\.\.\]", quote)
    return [p for p in (f.strip() for f in parts) if len(p) >= 4]


def check_quote(doc_id, page, quote):
    """Return (ok, found_page, missing_fragment)."""
    frs = fragments(quote)
    if not frs:
        return False, None, "(empty/too-short quote)"
    for pg in (page, page - 1, page + 1):
        txt = norm(lib.page_text(doc_id, pg))
        if not txt:
            continue
        if all(norm(fr) in txt for fr in frs):
            return True, pg, None
    # find which fragment is missing on the nominal page
    txt = norm(lib.page_text(doc_id, page))
    miss = next((fr for fr in frs if norm(fr) not in txt), frs[0])
    return False, None, miss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", default=os.path.join(lib.EVAL, "questions.yaml"))
    a = ap.parse_args()
    with open(a.questions, encoding="utf-8") as f:
        qs = yaml.safe_load(f)
    npass = nfail = nmanual = 0
    fails = []
    for q in qs:
        qid = q["qid"]
        if q.get("is_silent"):
            nmanual += 1
            print(f"  MANUAL  {qid:<8} silent/negative — verify by hand")
            continue
        exp = q.get("expected") or []
        if not exp:
            nfail += 1; fails.append((qid, "no expected"));
            print(f"  FAIL    {qid:<8} non-silent but no expected"); continue
        for i, e in enumerate(exp):
            ok, fp, miss = check_quote(e["doc_id"], int(e["page"]), e.get("quote", ""))
            if ok:
                npass += 1
                tag = "" if fp == int(e["page"]) else f" (found on p.{fp}, declared p.{e['page']})"
                print(f"  PASS    {qid:<8} {e['doc_id'].split('::')[-1][:32]} p.{e['page']}{tag}")
            else:
                nfail += 1; fails.append((qid, miss[:60]))
                print(f"  FAIL    {qid:<8} {e['doc_id'].split('::')[-1][:32]} p.{e['page']} "
                      f"-- missing: «{miss[:60]}»")
    print(f"\n  {npass} PASS · {nfail} FAIL · {nmanual} MANUAL(silent)")
    if fails:
        print("  FAILURES:")
        for qid, why in fails:
            print(f"    {qid}: {why}")
        sys.exit(1)


if __name__ == "__main__":
    main()

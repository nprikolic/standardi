#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the 6 retrieval systems over eval/questions.yaml. Deterministic; idempotent.

Writes eval/runs/<system>/<qid>.json  (skip if present unless --force).
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib                                                    # noqa: E402
import yaml                                                   # noqa: E402

EVAL = lib.EVAL
RUNS = os.path.join(EVAL, "runs")


def load_questions():
    with open(os.path.join(EVAL, "questions.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args()
    qs = load_questions()
    n = 0
    for q in qs:
        qid = q["qid"]
        for s in lib.RETRIEVAL_SYSTEMS:
            d = os.path.join(RUNS, s)
            os.makedirs(d, exist_ok=True)
            out = os.path.join(d, f"{qid}.json")
            if os.path.exists(out) and not a.force:
                continue
            res = lib.retrieve(s, q, limit=a.limit)
            res["qid"] = qid
            with open(out, "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=1)
            n += 1
    print(f"wrote {n} retrieval run files for {len(qs)} questions "
          f"x {len(lib.RETRIEVAL_SYSTEMS)} systems")


if __name__ == "__main__":
    main()

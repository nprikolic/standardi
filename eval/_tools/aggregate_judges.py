#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggregate the blind 3-judge panel (majority vote), de-anonymise via judge_key,
compute per-system answer accuracy. Writes eval/answer_metrics.json + console table."""
import os, sys, json
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib                                                    # noqa: E402
import yaml                                                   # noqa: E402

EVAL = lib.EVAL

J1 = {"P001":{"A":"missing","B":"missing","C":"partially","D":"correct","E":"missing"},"PB03":{"A":"partially","B":"partially","C":"partially","D":"missing","E":"partially"},"PC01":{"A":"missing","B":"missing","C":"partially","D":"missing","E":"correct"},"PD06":{"A":"correct","B":"correct","C":"missing","D":"missing","E":"correct"},"PD01":{"A":"wrong","B":"correct","C":"correct","D":"missing","E":"missing"},"PA07":{"A":"missing","B":"partially","C":"missing","D":"missing","E":"missing"},"SF02":{"A":"wrong","B":"missing","C":"missing","D":"missing","E":"missing"},"SH01":{"A":"correct","B":"correct","C":"missing","D":"correct","E":"missing"},"SI02":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL01":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL03":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL04":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"}}
J2 = {"P001":{"A":"missing","B":"missing","C":"partially","D":"partially","E":"missing"},"PB03":{"A":"partially","B":"partially","C":"partially","D":"missing","E":"partially"},"PC01":{"A":"missing","B":"missing","C":"partially","D":"missing","E":"correct"},"PD06":{"A":"correct","B":"correct","C":"missing","D":"missing","E":"correct"},"PD01":{"A":"wrong","B":"correct","C":"correct","D":"missing","E":"missing"},"PA07":{"A":"missing","B":"partially","C":"missing","D":"missing","E":"missing"},"SF02":{"A":"wrong","B":"missing","C":"missing","D":"missing","E":"missing"},"SH01":{"A":"correct","B":"correct","C":"missing","D":"correct","E":"missing"},"SI02":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL01":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL03":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL04":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"}}
J3 = {"P001":{"A":"missing","B":"missing","C":"wrong","D":"partially","E":"missing"},"PB03":{"A":"partially","B":"partially","C":"partially","D":"missing","E":"partially"},"PC01":{"A":"missing","B":"missing","C":"partially","D":"missing","E":"correct"},"PD06":{"A":"correct","B":"correct","C":"missing","D":"missing","E":"correct"},"PD01":{"A":"wrong","B":"correct","C":"correct","D":"missing","E":"missing"},"PA07":{"A":"missing","B":"partially","C":"missing","D":"missing","E":"missing"},"SF02":{"A":"partially","B":"missing","C":"missing","D":"missing","E":"missing"},"SH01":{"A":"correct","B":"correct","C":"missing","D":"correct","E":"missing"},"SI02":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL01":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL03":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"},"SIL04":{"A":"correct","B":"correct","C":"correct","D":"correct","E":"correct"}}

RANK = {"correct": 0, "partially": 1, "missing": 2, "wrong": 3, "hallucinated_citation": 4}
INV = {v: k for k, v in RANK.items()}


def majority(votes):
    c = Counter(votes)
    top, n = c.most_common(1)[0]
    if n >= 2:
        return top
    return INV[sorted(RANK[v] for v in votes)[1]]   # 3-way split -> median severity


def main():
    key = json.load(open(os.path.join(EVAL, "judge_key.json"), encoding="utf-8"))
    qs = {q["qid"]: q for q in yaml.safe_load(open(os.path.join(EVAL, "questions.yaml"), encoding="utf-8"))}
    per_sys = defaultdict(lambda: Counter())
    per_sys_silent = defaultdict(lambda: Counter())
    per_q = {}
    for qid in J1:
        silent = bool(qs[qid].get("is_silent"))
        per_q[qid] = {}
        for lab in J1[qid]:
            v = majority([J1[qid][lab], J2[qid][lab], J3[qid][lab]])
            sysname = key[qid][lab]
            per_q[qid][sysname] = v
            (per_sys_silent if silent else per_sys)[sysname][v] += 1

    def acc(counter):
        n = sum(counter.values())
        if not n:
            return None
        # answer-correct% = correct + 0.5*partially
        return round((counter["correct"] + 0.5 * counter["partially"]) / n, 3)

    systems = ["S0", "S1", "S2", "S3", "S4"]
    out = {"subset_n_nonsilent": 9, "subset_n_silent": 3, "per_system": {}, "per_question": per_q}
    print(f"{'sys':<5}{'corr':>5}{'part':>5}{'wrong':>6}{'halluc':>7}{'miss':>5} | {'ans-acc%':>8}  (non-silent, n=9)")
    for s in systems:
        c = per_sys[s]
        print(f"{s:<5}{c['correct']:>5}{c['partially']:>5}{c['wrong']:>6}{c['hallucinated_citation']:>7}{c['missing']:>5} | {str(acc(c)):>8}")
        out["per_system"][s] = {"nonsilent": dict(c), "ans_acc_nonsilent": acc(c),
                                "silent": dict(per_sys_silent[s]), "silent_correct": per_sys_silent[s]["correct"]}
    print(f"\nSILENT controls (n=3) — 'correct' = properly declined / out-of-scope; 'hallucinated_citation'/'wrong' = invented a value:")
    for s in systems:
        c = per_sys_silent[s]
        print(f"  {s}: correct={c['correct']}  wrong={c['wrong']}  hallucinated={c['hallucinated_citation']}")
    json.dump(out, open(os.path.join(EVAL, "answer_metrics.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nwrote {os.path.join(EVAL, 'answer_metrics.json')}")


if __name__ == "__main__":
    main()

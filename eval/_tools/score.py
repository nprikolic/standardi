#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic retrieval scoring vs frozen ground-truth.

Hit = retrieved doc_id == expected doc_id AND |page - expected.page| <= 1,
within top-k (k=10). No LLM, no self-scoring.

Outputs:
  eval/benchmark.csv   — one row per (qid, system): recall@10, rr, p@10, first_hit_rank
  eval/metrics.json    — aggregates per system, and breakdowns (concept/lang/primary)
"""
import os, sys, json, csv, argparse
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib                                                    # noqa: E402
import yaml                                                   # noqa: E402

EVAL = lib.EVAL
RUNS = os.path.join(EVAL, "runs")
K = 10
PAGE_TOL = 1


def load_questions():
    with open(os.path.join(EVAL, "questions.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_run(system, qid):
    p = os.path.join(RUNS, system, f"{qid}.json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def is_hit(hit, expected):
    for e in expected:
        if hit["doc_id"] == e["doc_id"] and abs(int(hit["page"]) - int(e["page"])) <= PAGE_TOL:
            return True
    return False


def score_one(run, expected):
    """Return (recall@k, reciprocal_rank, precision@k, first_hit_rank|None)."""
    hits = run["retrieved"][:K]
    first = None
    nhit = 0
    for h in hits:
        if is_hit(h, expected):
            nhit += 1
            if first is None:
                first = h["rank"]
    recall = 1.0 if first is not None else 0.0
    rr = (1.0 / first) if first else 0.0
    p_at_k = nhit / float(K)
    return recall, rr, p_at_k, first


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.path.join(EVAL, "benchmark.csv"))
    ap.add_argument("--metrics", default=os.path.join(EVAL, "metrics.json"))
    a = ap.parse_args()
    qs = load_questions()
    # retrieval is scored only on non-silent questions (silent => no ground-truth doc)
    scored_qs = [q for q in qs if not q.get("is_silent")]
    silent_qs = [q for q in qs if q.get("is_silent")]

    rows = []                       # csv rows
    # agg[system] -> list of (recall, rr, p)
    agg = defaultdict(list)
    by_concept = defaultdict(lambda: defaultdict(list))   # concept->system->list
    by_lang = defaultdict(lambda: defaultdict(list))      # lang->system->list
    primary = defaultdict(list)                           # system->list (DRAINAGE_MIN_GRADE)

    for q in scored_qs:
        qid = q["qid"]; expected = q.get("expected") or []
        concept = q.get("concept", "?"); lang = q.get("lang", "?")
        is_primary = (concept == "DRAINAGE_MIN_GRADE") or (q.get("topic") == "primary")
        for s in lib.RETRIEVAL_SYSTEMS:
            run = load_run(s, qid)
            if run is None:
                continue
            recall, rr, p_at_k, first = score_one(run, expected)
            rows.append({"qid": qid, "system": s, "concept": concept, "lang": lang,
                         "topic": q.get("topic", ""), "is_primary": int(is_primary),
                         "recall_at_10": recall, "reciprocal_rank": round(rr, 4),
                         "precision_at_10": round(p_at_k, 3),
                         "first_hit_rank": first if first else ""})
            agg[s].append((recall, rr, p_at_k))
            by_concept[concept][s].append((recall, rr, p_at_k))
            by_lang[lang][s].append((recall, rr, p_at_k))
            if is_primary:
                primary[s].append((recall, rr, p_at_k))

    # write csv
    with open(a.csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "system", "concept", "lang", "topic",
                                          "is_primary", "recall_at_10", "reciprocal_rank",
                                          "precision_at_10", "first_hit_rank"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    def summarize(d):
        return {s: {"n": len(v),
                    "recall@10": round(mean(x[0] for x in v), 4),
                    "MRR": round(mean(x[1] for x in v), 4),
                    "P@10": round(mean(x[2] for x in v), 4)}
                for s, v in d.items()}

    metrics = {
        "k": K, "page_tolerance": PAGE_TOL,
        "n_questions_total": len(qs),
        "n_scored_retrieval": len(scored_qs),
        "n_silent": len(silent_qs),
        "overall": summarize(agg),
        "primary_DRAINAGE_MIN_GRADE": summarize(primary),
        "by_concept": {c: summarize(d) for c, d in sorted(by_concept.items())},
        "by_lang": {lg: summarize(d) for lg, d in sorted(by_lang.items())},
    }
    with open(a.metrics, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    # console summary
    print(f"Scored {len(scored_qs)} retrieval questions ({len(silent_qs)} silent excluded)\n")
    hdr = f"{'system':<6} {'n':>3} {'recall@10':>10} {'MRR':>7} {'P@10':>7}"
    print("OVERALL"); print(hdr)
    for s in lib.RETRIEVAL_SYSTEMS:
        m = metrics["overall"].get(s)
        if m:
            print(f"{s:<6} {m['n']:>3} {m['recall@10']:>10} {m['MRR']:>7} {m['P@10']:>7}")
    print("\nPRIMARY (DRAINAGE_MIN_GRADE)"); print(hdr)
    for s in lib.RETRIEVAL_SYSTEMS:
        m = metrics["primary_DRAINAGE_MIN_GRADE"].get(s)
        if m:
            print(f"{s:<6} {m['n']:>3} {m['recall@10']:>10} {m['MRR']:>7} {m['P@10']:>7}")
    print(f"\nwrote {a.csv} and {a.metrics}")


if __name__ == "__main__":
    main()

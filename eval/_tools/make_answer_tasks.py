#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build per-question answer tasks for the (bounded) answer-accuracy layer.

For each qid in the subset and each retrieval system, gather the top-5 retrieved
passages (doc_id, page, verbatim text) so an answerer agent can answer ONLY from
them. S0 (raw-LLM) gets no passages. Output: eval/answer_tasks/<qid>.json
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib                                                    # noqa: E402
import yaml                                                   # noqa: E402

EVAL = lib.EVAL
RUNS = os.path.join(EVAL, "runs")
OUT = os.path.join(EVAL, "answer_tasks")
ANSWER_SYSTEMS = ["S1", "S2", "S3", "S4"]   # S0 handled separately (no retrieval)
TOPN = 5
SNIP = 700

SUBSET = ["P001", "PB03", "PC01", "PD06", "PD01", "PA07",
          "SF02", "SH01", "SI02", "SIL01", "SIL03", "SIL04"]


def main():
    os.makedirs(OUT, exist_ok=True)
    qs = {q["qid"]: q for q in yaml.safe_load(open(os.path.join(EVAL, "questions.yaml"), encoding="utf-8"))}
    for qid in SUBSET:
        q = qs[qid]
        task = {"qid": qid, "question_en": q["question_en"],
                "question_local": q.get("question_local", ""),
                "is_silent": bool(q.get("is_silent")), "systems": {}}
        for s in ANSWER_SYSTEMS:
            run = json.load(open(os.path.join(RUNS, s, f"{qid}.json"), encoding="utf-8"))
            passages = []
            for h in run["retrieved"][:TOPN]:
                txt = lib.page_text(h["doc_id"], h["page"])
                txt = " ".join(txt.split())[:SNIP]
                passages.append({"doc_id": h["doc_id"], "page": h["page"], "text": txt})
            task["systems"][s] = passages
        json.dump(task, open(os.path.join(OUT, f"{qid}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    print(f"wrote {len(SUBSET)} answer tasks to {OUT}")
    print("subset:", ", ".join(SUBSET))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble agent answers -> eval/answers.json, then build BLIND judge tasks.

Blind = candidates are shuffled and relabelled A..E; the judge never sees which
system produced an answer. Deterministic shuffle (qid-seeded) since no RNG.
Output: eval/answers.json, eval/judge_tasks/<qid>.json, eval/judge_key.json
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib                                                    # noqa: E402
import yaml                                                   # noqa: E402

EVAL = lib.EVAL

# ---- S0 raw-LLM answers (no retrieval; from memory) -------------------------
S0 = {
 "P001": {"answer": "Min longitudinal grade set by drainage; ~0.5% for road in cut with ditch (uncertain).", "cite": "Pravilnik 50/11 (no page)", "confident": False},
 "PB03": {"answer": "Vector sum of longitudinal + relative grade kept above a min resultant (~0.5%); min long. grade at runoff ~0.7% (uncertain).", "cite": "RAL Germany (no page)", "confident": False},
 "PC01": {"answer": "Min 0.5% on curbed pavements; may reduce to 0.3% on a properly sloped paved surface.", "cite": "AASHTO Green Book (no page)", "confident": True},
 "PD06": {"answer": "Asphalt-/cement-concrete pavements: cross slope ~1.5-2.0% (uncertain).", "cite": "KOR Rules Art. 28 (no page)", "confident": False},
 "PD01": {"answer": "Min longitudinal grade of the profile at a runoff ~0.5% (uncertain).", "cite": "VGU Sweden (no page)", "confident": False},
 "PA07": {"answer": "Min longitudinal gradient ~0.5%, reducible to ~0.3% (or 0% with special drainage) (uncertain).", "cite": "WR-D-22-2 Poland (no page)", "confident": False},
 "SF02": {"answer": "Approx Rmin: 40:45 / 50:75 / 60:120 / 70:175 / 80:240 / 90:335 / 100:435 / 110:540 / 120:700 / 130:900 m (uncertain).", "cite": "SRDM (no page)", "confident": False},
 "SH01": {"answer": "Maximum superelevation 8% (7% for some road groups).", "cite": "Norma 3.1-IC (no page)", "confident": True},
 "SI02": {"answer": "Desirable minimum weaving length 2 km (absolute min ~1 km) (uncertain).", "cite": "TII / DMRB (no page)", "confident": False},
 "SIL01": {"answer": "Not specified: 120 km/h is outside the LVRR low-volume scope; no value exists.", "cite": "AFG LVRR Vol 2 (no page)", "confident": True},
 "SIL03": {"answer": "Not specified: CD 109 is an alignment standard; surface-course thickness is in pavement-design docs (e.g. CD 226).", "cite": "DMRB CD 109 (no page)", "confident": True},
 "SIL04": {"answer": "Not specified: 50/11 governs roads, not tram/railway track radii.", "cite": "Pravilnik 50/11 (no page)", "confident": True},
}

# ---- retrieval-system answers (strictly from each system's passages) --------
# Collected verbatim from answerer agents AW1..AW4.
RET = {
 "P001": {
   "S1": {"found": False}, "S2": {"found": False},
   "S3": {"found": True, "answer": "Per Pravilnik 50/11, min iN determined from drainage condition; min iN=0% allowed if crossfall drains; cut/ditch branch truncated in passage.", "doc": "SRB_Pravilnik-50-11::SRB_Pravilnik-50-11_full", "page": 63},
   "S4": {"found": False}},
 "PB03": {
   "S1": {"found": False, "answer": "RAL p.46: 'To ensure adequate carriageway drainage, the differ-' — value truncated in passage.", "doc": "DEU_FGSV::RAL_FGSV201_Rural-Roads_EN_2012-tr2024", "page": 46},
   "S2": {"found": False, "answer": "RAL p.46 difference rule present but specific value truncated.", "doc": "DEU_FGSV::RAL_FGSV201_Rural-Roads_EN_2012-tr2024", "page": 46},
   "S3": {"found": False},
   "S4": {"found": False, "answer": "RAL p.46 difference rule present but specific value truncated.", "doc": "DEU_FGSV::RAL_FGSV201_Rural-Roads_EN_2012-tr2024", "page": 46}},
 "PC01": {
   "S1": {"found": False}, "S2": {"found": False}, "S3": {"found": False},
   "S4": {"found": True, "answer": "Green Book: desirable min grade 0.3% minimum (0.5% for curbed) — curbed clause partly truncated.", "doc": "USA_AASHTO-Green-Book::AASHTO_Green_Book_7th_2018", "page": 600}},
 "PD06": {
   "S1": {"found": False},
   "S2": {"found": True, "answer": "Art. 28: lane cross slope for asphalt-/cement-concrete pavements is 1.5% to 2.0%.", "doc": "KOR_Road-Structure-Rules::KOR_Road-Structure-Rules-Commentary_2021", "page": 221},
   "S3": {"found": False},
   "S4": {"found": True, "answer": "Art. 28: lane cross slope for asphalt-/cement-concrete pavements is 1.5% to 2.0%.", "doc": "KOR_Road-Structure-Rules::KOR_Road-Structure-Rules-Commentary_2021", "page": 49}},
 "PD01": {
   "S1": {"found": False},
   "S2": {"found": True, "answer": "Skevningsövergang placed where profile-plane longitudinal grade >= 1.0%; not where < 0.5%.", "doc": "SWE_VGU::VGU_Krav_med_radstext_TRVINFRA-00396_v1_0", "page": 309},
   "S3": {"found": False},
   "S4": {"found": True, "answer": "Skevningsövergang placed where profile-plane longitudinal grade >= 1.0% to ensure drainage.", "doc": "SWE_VGU::VGU_Krav_med_radstext_TRVINFRA-00396_v1_0", "page": 309}},
 "PA07": {"S1": {"found": False}, "S2": {"found": False}, "S3": {"found": False}, "S4": {"found": False}},
 "SF02": {"S1": {"found": False}, "S2": {"found": False}, "S3": {"found": False}, "S4": {"found": False}},
 "SH01": {
   "S1": {"found": False},
   "S2": {"found": True, "answer": "Tabla 4.4: peralte maximo 8.00% (Groups 1&2) and 7.00% (Group 3).", "doc": "ESP_Norma-3.1-IC::BOE-A-2016-2217_Norma-3.1-IC-Trazado", "page": 38},
   "S3": {"found": False},
   "S4": {"found": True, "answer": "Tabla 4.4: peralte maximo 8.00% (Groups 1&2) and 7.00% (Group 3).", "doc": "ESP_Norma-3.1-IC::BOE-A-2016-2217_Norma-3.1-IC-Trazado", "page": 38}},
 "SI02": {
   "S1": {"found": True, "answer": "Desirable Minimum weaving length between grade separated junctions = 2km.", "doc": "IRL_TII-junctions::DN-GEO-03060-03", "page": 145},
   "S2": {"found": True, "answer": "Desirable Minimum weaving length = 2km.", "doc": "IRL_TII-junctions::DN-GEO-03060-03", "page": 145},
   "S3": {"found": True, "answer": "Desirable Minimum weaving length = 2km.", "doc": "IRL_TII-junctions::DN-GEO-03060-03", "page": 145},
   "S4": {"found": True, "answer": "Desirable Minimum weaving length = 2km.", "doc": "IRL_TII-junctions::DN-GEO-03060-03", "page": 145}},
 "SIL01": {"S1": {"found": False}, "S2": {"found": False}, "S3": {"found": False}, "S4": {"found": False}},
 "SIL03": {"S1": {"found": False}, "S2": {"found": False}, "S3": {"found": False}, "S4": {"found": False}},
 "SIL04": {"S1": {"found": False}, "S2": {"found": False}, "S3": {"found": False}, "S4": {"found": False}},
}

SUBSET = ["P001", "PB03", "PC01", "PD06", "PD01", "PA07", "SF02", "SH01", "SI02", "SIL01", "SIL03", "SIL04"]
ANSWER_SYSTEMS = ["S0", "S1", "S2", "S3", "S4"]


def candidate(qid, sysname):
    if sysname == "S0":
        d = S0[qid]
        return {"answer": d["answer"], "citation": d["cite"]}
    d = RET[qid].get(sysname, {"found": False})
    if not d.get("found") and "answer" not in d:
        return {"answer": "NOT FOUND IN PASSAGES (system reported no answer)", "citation": "(none)"}
    cite = f"{d['doc']} p.{d['page']}" if d.get("doc") else "(none)"
    return {"answer": d.get("answer", "NOT FOUND IN PASSAGES"), "citation": cite}


def main():
    qs = {q["qid"]: q for q in yaml.safe_load(open(os.path.join(EVAL, "questions.yaml"), encoding="utf-8"))}
    answers = {}
    os.makedirs(os.path.join(EVAL, "judge_tasks"), exist_ok=True)
    key = {}
    for qid in SUBSET:
        q = qs[qid]
        answers[qid] = {s: candidate(qid, s) for s in ANSWER_SYSTEMS}
        # deterministic shuffle of labels via qid hash
        order = sorted(ANSWER_SYSTEMS, key=lambda s: hashlib.md5((qid + s).encode()).hexdigest())
        labels = ["A", "B", "C", "D", "E"]
        cand_block = []
        key[qid] = {}
        for lab, s in zip(labels, order):
            c = answers[qid][s]
            cand_block.append({"label": lab, "answer": c["answer"], "citation": c["citation"]})
            key[qid][lab] = s
        gt = q.get("expected") or []
        task = {
            "qid": qid,
            "question": q["question_en"],
            "is_silent": bool(q.get("is_silent")),
            "ground_truth": ([{"doc_id": e["doc_id"], "page": e["page"], "value": e["value"], "quote": e["quote"]} for e in gt]
                             if gt else "NO VALUE EXISTS IN THE CORPUS — correct answer = state it is not specified/out of scope."),
            "candidates": cand_block,
        }
        json.dump(task, open(os.path.join(EVAL, "judge_tasks", f"{qid}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    json.dump(answers, open(os.path.join(EVAL, "answers.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(key, open(os.path.join(EVAL, "judge_key.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote answers.json, {len(SUBSET)} judge tasks, judge_key.json")


if __name__ == "__main__":
    main()

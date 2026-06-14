# Phase-5 Benchmark Report — Retrieval & Answer accuracy across world road-geometric-design standards

**Date:** 2026-06-14 · **Corpus:** 83 docs / 12,036 pages, multilingual · **Index:** `corpus/index.sqlite` (FTS5/bm25)
**Questions:** 77 (35 primary `DRAINAGE_MIN_GRADE`, 37 secondary, 5 silent/negative) · **Ground-truth:** built from the corpus *before* running any system, every quote verified literally on its cited page, then **frozen**.

> ### ⚠️ Headline finding (read this first)
> **The pre-registered hypothesis — that concept-mapping + a multilingual glossary (`query.py --concept`, system "S3") beats keyword/RAG baselines — is NOT supported. It is decisively *refuted*.** Concept-only retrieval is the **worst** real system (recall@10 = 0.13 vs 0.86 for a plain native-language keyword baseline). The benchmark did its job: it caught a design flaw in the skill's retrieval layer *before* publication. The remainder of this report documents the result faithfully, diagnoses the cause, and converts it into concrete fixes (Phase 6). Per the anti-fabrication mandate, no number here was tuned to make our own system look better — and where our system loses, it is stated plainly.

---

## 1. Systems under test

Retrieval is **100% deterministic** (pure SQLite/FTS5; scored by code against frozen ground-truth — no LLM self-scoring). k = 10. A retrieved page is a *hit* iff `doc_id` matches and `|page − expected.page| ≤ 1`.

| ID | What it does | Query construction |
|----|--------------|--------------------|
| **S0** | raw-LLM, no retrieval | — (parametric memory; measures hallucination) |
| **S1** | naïve English keyword | tokens of `question_en` → FTS bm25 |
| **S2** | generic RAG, native language, **no glossary** | tokens of `question_local`+`question_en` → FTS bm25 |
| **S3** | **SKILL as literally specified** (`query.py --concept`) | concept → all multilingual glossary terms → FTS bm25 |
| **S3a** | ablation: concept, English glossary terms only | concept(en) → FTS bm25 |
| **S3b** | ablation: no concept mapping (free terms) | tokens of `question_en`+`question_local` → FTS bm25 (≡ S2 by construction) |
| **S3c** | ablation: concept terms, **LIKE** (no bm25 ranking) | concept terms → SQL LIKE, ordered by doc/page |
| **S4** | *principled* skill (added post-hoc as a **new** system, not a tweak to S3) | question tokens **∪** glossary terms → FTS bm25 |
| **S1g** | isolates glossary cross-language value | `question_en` tokens **∪** glossary terms → FTS bm25 |

S4 and S1g were added **after** seeing S3 fail, to answer the *real* question ("is the multilingual glossary worth anything when used correctly?"). They are new systems evaluated on the unchanged, frozen questions — **not** edits to S3 or to the glossary, and the questions were never changed to favour any system (anti-overfitting rule).

---

## 2. Main results — retrieval (deterministic, all 72 non-silent questions)

| System | Recall@10 | MRR | P@10 |
|--------|:---------:|:---:|:----:|
| S2 generic-RAG (native language) | **0.861** | **0.619** | 0.125 |
| S3b (≡ S2) | 0.861 | 0.619 | 0.125 |
| **S4 question + glossary** | 0.792 | 0.613 | 0.111 |
| S1g (EN question + glossary) | 0.417 | 0.282 | 0.051 |
| S1 naïve English keyword | 0.431 | 0.284 | 0.054 |
| **S3 SKILL (concept-only)** | **0.125** | 0.041 | 0.017 |
| S3a (concept, EN only) | 0.083 | 0.032 | 0.010 |
| S3c (concept, LIKE) | 0.000 | 0.000 | 0.000 |

### Primary subset — `DRAINAGE_MIN_GRADE` (35 questions, the PhD core)

| System | Recall@10 | MRR | P@10 |
|--------|:---------:|:---:|:----:|
| S2 / S3b | 0.914 | 0.706 | 0.114 |
| **S4 question + glossary** | **0.914** | **0.741** | 0.111 |
| S1g | 0.600 | — | — |
| S1 | 0.514 | 0.330 | 0.063 |
| S3 / S3a | 0.143 | 0.05 | 0.017 |
| S3c | 0.000 | 0.000 | 0.000 |

**On the primary topic, S4 ties S2 on recall and slightly *beats* it on MRR (0.741 vs 0.706)** — i.e., glossary expansion ranks the right page marginally higher *only* when it is already combined with the question's own words. The glossary alone (S3) is near-useless.

---

## 3. Root-cause diagnosis — why S3 fails (the mandated investigation)

The prompt says: if our system *dominates* ~100%, treat it as a red flag and investigate. The same skepticism was applied to the inverse — S3 *losing* ~everywhere — and the cause is concrete and verified:

**`query.py --concept` ignores the question.** It builds one fixed 60-term OR-query from the concept's glossary and returns the same pages for *every* question of that concept. Verified directly:

```
S3 top-5 for three DIFFERENT primary questions (Serbian / Spanish / Korean):
  P001 (sr): SRDM p.85, SRDM p.84, Pravilnik p.63, SRDM p.97, AGRD03 p.230
  PB05 (es): SRDM p.85, SRDM p.84, Pravilnik p.63, SRDM p.97, AGRD03 p.230   ← identical
  PD06 (ko): SRDM p.85, SRDM p.84, Pravilnik p.63, SRDM p.97, AGRD03 p.230   ← identical
S2 (native question) for the same three: Serbian / Spanish / Korean pages respectively (correct).
```

S3 is a concept **browser**, not a per-question **retriever**. It only "hits" when the answer page happens to be one of the globally densest concept pages — which, because the glossary has the most Serbian terms, is biased toward Serbian docs. That is why S3's only non-trivial recall (0.14) is on the primary topic and concentrated on Serbian questions.

Three corollaries, all empirically confirmed:
- **S3a < S3** (English-only glossary, 0.08): drops the Serbian terms that gave S3 its few hits.
- **S3c = 0** (LIKE, concept terms): no bm25 ranking → the same broad term set returns an arbitrary, useless order.
- **S3b = S2 exactly** (0.861): removing concept-mapping reduces the "skill" to a generic native-language keyword search — i.e., the concept layer contributes *nothing positive*.

---

## 4. Does the multilingual glossary add value? (per-language, the core PhD question)

Recall@10 by source language (S1 = EN question; S1g = EN question + glossary; S2 = native question; S4 = native question + glossary; S3 = concept-only):

| lang | n | S1 | S1g | S2 | S4 | S3 |
|------|--:|---:|----:|---:|---:|---:|
| de | 5 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| en | 19 | 1.00 | **0.79** | 1.00 | 0.79 | 0.16 |
| es | 7 | 0.00 | 0.00 | 0.71 | 0.86 | 0.29 |
| fr | 1 | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 |
| hr | 4 | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 |
| it | 5 | 0.20 | 0.20 | 1.00 | 1.00 | 0.00 |
| **ja** | **3** | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** |
| ko | 4 | 0.25 | 0.25 | 1.00 | 0.75 | 0.00 |
| pl | 5 | 0.00 | 0.00 | 0.80 | 0.80 | 0.00 |
| pt | 3 | 0.67 | 0.67 | 0.67 | 1.00 | 0.33 |
| sl | 4 | 0.25 | 0.25 | 1.00 | 1.00 | 0.00 |
| sr | 7 | 0.00 | **0.43** | 0.57 | 0.43 | 0.43 |
| sv | 3 | 0.00 | 0.00 | 1.00 | 0.67 | 0.00 |
| zh | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |

**Findings:**
1. **The glossary as flat OR-expansion does NOT deliver cross-language value.** Compare S1 (0.43) vs S1g (0.42): adding all 14 languages of synonyms to an English query barely moves non-English recall, and it *hurts* English (1.00 → 0.79) by diluting bm25 precision. The single language it helped (sr: 0.00 → 0.43) is the over-represented one.
2. **The dominant success factor is querying in the document's own language** (S2). Where the question is asked in the target language, recall is 0.7–1.0 across the board.
3. **Adding the glossary to a native-language query (S4) is net slightly negative** (0.79 vs S2 0.86): it helps `es`/`pt` but hurts `en`/`ko`/`sv`/`vertical`/`weaving` via noise. It is *not* a free win.
4. **Japanese = 0% for every system.** True CJK phrase retrieval fails under FTS5 `unicode61` tokenisation (the documented limitation). `zh` only scores 1.00 because those questions target the *English* JTG D20 translation; genuine Chinese-script retrieval is untested/unsupported here.

By concept (recall@10): see `eval/metrics.json`. Pattern is uniform — S2/S3b best, S4 close, S3/S3a/S3c near-zero. S4 underperforms S2 specifically on `VERTICAL` (0.43 vs 0.71) and `WEAVING` (0.33 vs 0.67).

---

## 5. Answer accuracy (bounded blind-judge sub-study)

**Scope (logged, not hidden):** the answer layer covers a **12-question subset** (9 non-silent across sr/de/en/ko/sv/pl/es + 3 silent), and the **5 most informative systems** {S0, S1, S2, S3, S4}. S3a/S3b/S3c are omitted here because S3b≡S2, S3a≈S3, S3c is degenerate. This is a *demonstration*, not full coverage of all 77×7; treat the percentages as indicative (small N).

Method: answers generated strictly from each system's top-5 passages (S0 from memory, no retrieval). Judged by a **blind 3-judge panel** (candidates shuffled to A–E; judges never told which system; each judge independently opened the cited page with `page.py` to confirm; majority vote). Anonymisation key in `eval/judge_key.json`; raw answers in `eval/answers.json`.

**Answer-correct%** = (correct + 0.5·partial)/n.

| System | correct | partial | wrong | halluc-cite | missing | **Answer-correct%** (n=9) |
|--------|:------:|:------:|:----:|:-----------:|:------:|:----:|
| S0 raw-LLM | 4 | 3 | 2 | 0 | 0 | **0.611** |
| S4 question+glossary | 4 | 2 | 0 | 0 | 3 | 0.556 |
| S2 native RAG | 4 | 1 | 0 | 0 | 4 | 0.500 |
| S1 EN keyword | 1 | 1 | 0 | 0 | 7 | 0.167 |
| S3 concept-only | 1 | 1 | 0 | 0 | 7 | 0.167 |

**Silent/negative controls (n=3): every system scored 3/3 "correctly declined" — zero fabricated values, zero hallucinated citations, including S0.**

**Interpretation (carefully):**
- The grounded systems track their retrieval quality: S4≈S2 > S1≈S3. Confirms retrieval drives answers.
- **S0 (raw-LLM) scores *highest* on this subset (0.611) — but this is a trap, not a win for "no retrieval".** The subset includes globally famous standards (AASHTO Green Book, Norma 3.1-IC) the model has memorised, so it gets partial credit cheaply. Critically, **S0 produced 2 confidently *wrong* values** (e.g. P001: claimed "~0.5%" min grade in cut; the actual Pravilnik rule is `≥0.8(1.0)%` via `iN − irv ≥ min ihid`) and it cites **no verifiable page**. The grounded systems produced **0 wrong** answers — when retrieval fails they return "not found" (fail-safe), whereas the raw LLM fails *confident-and-wrong* (fail-dangerous). For a safety-critical reference tool, the latter is the more serious failure mode.
- **Hallucinated-citation rate = 0% for all systems** on this subset (every cited page was verified to contain the claim).
- Caveat/artefact: my answer-task prep truncated passages to 700 chars, which cut off the value on 2 items (PB03, PC01) where retrieval had actually succeeded — depressing S1/S2/S4 "correct" counts. The retrieval table (§2) is unaffected.

---

## 6. Error analysis — where the systems miss

- **S3 / S3a / S3c (the skill as specified):** miss almost everything because retrieval is question-independent (§3). Not fixable by glossary edits; needs a different query construction.
- **S4 misses (15):** the 3 Japanese questions (CJK/FTS), plus `SF01, SF03, SG05, SG07, SH04, SH07, SI03, SI07` — cases where the 60 glossary terms outvote the specific question terms in bm25 and push the target below rank 10. This is the *cost* of naïve expansion.
- **S2 primary misses (3):** `P001` (target = Pravilnik p.63, but the equivalent rule on SRDM pages ranked higher — answer still derivable, retrieval "miss" is page-exact strictness), `PA07` (sibling WR-D documents outranked WR-D-22-2), `PD03` (BRA IPR-740 p.292). These are near-misses, not topical failures.
- **Universal CJK failure (ja):** confirms the corpus note that CJK *phrase* MATCH is unreliable under `unicode61`; the remedy is the `--grep`/LIKE path per token, not FTS phrases.

---

## 7. Threats to validity (mandatory)

1. **Conflict of interest.** One model family built the corpus tooling, wrote the questions, generated answers, and judged. Mitigations applied: retrieval scored by *code* (no LLM scoring); ground-truth frozen before systems ran and quote-verified on-page; blind, shuffled judging; adversarial "default to wrong/missing"; silent controls. Residual risk remains and is acknowledged.
2. **Question→page vocabulary leakage favours the *winners*, not S3.** Questions were authored by agents that read the target page and naturally reused its wording. This inflates S1/S2/S3b/S4 (which query with question words) and gives **S2's 0.86 an optimistic tilt**. It does *not* help S3 (which ignores the question). So the *gap* S2≫S3 is real, but S2's absolute level is likely an overestimate of real-user performance. A truly clean design needs questions written independently of the target page.
3. **The benchmark under-tests the glossary's intended use-case.** Because each question's `question_local` is in the target document's language, S2 already has the right-language terms, leaving little headroom for the glossary. The scenario the glossary is *for* — a query in language X seeking a target in language Y≠X — is under-sampled. The S1 vs S1g comparison is the only clean isolation, and there the glossary did not help. **Verdict on the glossary is therefore "no demonstrated value here", not "proven useless everywhere".** Phase 6 should add explicit cross-language questions.
4. **Small N for answer accuracy** (9 non-silent + 3 silent, 5 systems) and a small silent-control set (5 total). Percentages are indicative; the safe reading is the *qualitative* one (grounded = fail-safe, raw-LLM = fail-dangerous-but-fluent).
5. **CJK / NEEDS_OCR limits.** Japanese FTS retrieval is unsupported (0% all systems); 4 NEEDS_OCR docs were excluded from ground-truth; `zh` results lean on the English JTG D20 translation.
6. **Judge subjectivity** on the partial/correct boundary; mitigated by the 3-judge majority (judges agreed on ~92% of candidate verdicts).

---

## 8. Conservative verdict

- **Is the S3-vs-baseline difference real and large?** Yes — S3 is *worse* than the baselines by a wide, robust margin (0.13 vs 0.86), well outside small-N noise, and mechanistically explained (§3). This direction is the opposite of the project's hope and is reported as such.
- **Does concept-mapping + multilingual glossary beat keyword/RAG?** **No, not as currently implemented.** Concept-only retrieval (S3) fails; glossary-as-OR-expansion (S4, S1g) does not beat plain native-language retrieval (S2) and can hurt it.
- **What *does* work?** Querying with the user's actual question terms in the document's language (S2). The skill's value, if any, is not in its current retrieval design.
- **Is anything salvageable for the skill?** Possibly — S4 slightly improved *ranking* (MRR) on the primary topic, hinting that *targeted* (not flat) glossary expansion could help. That is a Phase-6 hypothesis, not a Phase-5 result.

---

## 9. Auditability

- Raw per-question retrieval scores: **`eval/benchmark.csv`** (one row per question×system). Aggregates: **`eval/metrics.json`**.
- Frozen questions + verified quotes: **`eval/questions.yaml`** (re-checkable with `python eval/_tools/verify_groundtruth.py`).
- Raw retrieval runs: **`eval/runs/<system>/<qid>.json`**. Answer sub-study: **`eval/answers.json`**, **`eval/answer_metrics.json`**, blind key **`eval/judge_key.json`**.
- **≥10% manual-review sample** (verify by hand against the cited page): `P001` (sr), `PB01` (de), `PC02` (en), `PD06` (ko), `PA02` (hr), `SF09` (it), `SG02` (ja), `SI04` (it) — 8/77 ≈ 10.4%, spanning Cyrillic/Latin/CJK. All 5 silent items (`SIL01–05`) carry a recorded `negative_basis` (corpus LIKE-count) and should be hand-confirmed.

Full reproduction: `python eval/_tools/verify_groundtruth.py && python eval/_tools/run_retrieval.py --force && python eval/_tools/score.py`.

---
*Companion: `eval/glossary_improvements.md` — concrete glossary/term and retrieval-design changes for Phase 6 (forward-looking; deliberately NOT applied-and-re-measured on this frozen set).*

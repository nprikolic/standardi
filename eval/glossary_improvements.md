# Glossary & retrieval-design improvements (input to Phase 6)

Derived from the Phase-5 benchmark misses. **These are proposals for future work — deliberately NOT applied to `glossary.json` and re-measured on the same frozen question set** (anti-overfitting rule, BENCHMARK_PROMPT §5). They must be validated on a *new* question set.

The benchmark's central lesson is **architectural, not lexical**: the biggest win is not "more glossary terms" but "use the glossary differently". Ordered by expected impact.

---

## A. Retrieval architecture (highest impact — fixes the actual failure)

1. **Never retrieve by concept terms alone.** `query.py --concept` returns the same pages for every question of a concept (recall@10 = 0.13). The skill's retriever must combine the **user's question terms** with the glossary, not replace them. Minimum viable fix: `S4 = tokens(question) ∪ glossary(concept)`. Recommended: **the question terms carry primary weight; glossary terms are a secondary, boosted-but-not-dominating expansion.**

2. **Make glossary expansion language-targeted, not flat.** Adding all 14 languages of synonyms to every query (S1g, S4) dilutes bm25 precision and *hurt* English recall (1.00 → 0.79). Detect the query language and/or the candidate document language, and expand **only** with the relevant language(s)' synonyms (plus English as lingua franca). This should recover the cross-language value that the flat OR-expansion failed to deliver.

3. **Weight/boost instead of OR-flatten.** In FTS5, prefer scoring that does not let 60 broad terms outvote 3 specific ones. Options: per-term bm25 weighting (`bm25(pages_fts, w1, w2, …)`), a two-stage retrieve-then-rerank, or boosting exact question phrases above glossary synonyms.

4. **Route CJK through LIKE/`--grep`, not FTS phrase MATCH.** Japanese scored **0% on every system** — `unicode61` cannot phrase-match CJK. For `lang ∈ {ja, zh, ko}` (and any CJK query token), retrieve via per-term LIKE and rank by term-hit count or a CJK-aware tokenizer (e.g. an `icu`/trigram FTS tokenizer if the SQLite build allows).

---

## B. Concrete glossary term fixes (from observed misses)

Verified gaps where the agent's expected term was absent and a different on-page term was the real one:

| Concept | Lang | Add / fix | Evidence |
|---|---|---|---|
| VERTICAL / DRAINAGE_MIN_GRADE | sv | **`längslutning`**, **`vattenavrinning`** (NOT `minimilutning` — 0 hits in VGU) | PD-agent: `minimilutning` returned nothing; the Swedish term used is `längslutning` |
| DRAINAGE_MIN_GRADE | de | **`resultierende neigung`**, **`anrampungsneigung`**, `REwS` (resultant-slope rule) | RAL p.46 "resultant slope p ≥ 0.5%"; RAA p.42 "relative grade" |
| DRAINAGE_MIN_GRADE | en | **`relative grade`**, **`false channel`**, `constructable grade`, `edge-of-pavement grade` | CD109 p.24 "false channel paths"; AGRD03 p.230 "minimum constructable grade"; Green Book p.285 |
| DRAINAGE_MIN_GRADE | hr/sl/pl | **`rigol`/`koritnica`** (gutter), **`jarek`/`jarak`** (ditch), `rezultantni nagib` | NN-110 p.18; SLO Pravilnik p.28; WR-D-22-2 p.47 |
| SUPERELEVATION | es | **`bombeo`** (already present — keep), **`peralte máximo`** | Norma 3.1-IC p.38/p.53 |
| VERTICAL | ko | ensure **`종단경사`**, **`횡단경사`**, `변화 비율` (rate-of-change/K) — drop `최소 종단경사` (0 hits as a phrase) | KOR Rules Art.25/27/28 |
| VERTICAL | ja | **`縦断勾配`**, **`縦断曲線`**, **`横断勾配`**, `片勾配` (retrieve via LIKE — see A.4) | Road Structure Ordinance Art.19/22 |
| HORIZONTAL | it | **`parametro A`**, `Amin = 0,021·Vp²`-style phrasing; `raggio minimo` | DM 6792 p.66/p.73 |
| WEAVING/MERGE | various | **`carril de trenzado`**, `corsia di intreccio`, `faixa de desaceleração`, `traka za preplitanje` | ESP OC-32 p.499; BRA IPR-718 p.264; SRB SRDM5-2 p.15 |

(S4 specifically *under*performed S2 on `VERTICAL` and `WEAVING` — those concepts' glossary entries are the noisiest and should be the first to get language-targeted/weighted treatment, not merely enlarged.)

---

## C. Corpus / OCR gaps (block coverage, not glossary)

- **`CHN_JTG-D20::JTG_D20-2017_full` and `CHN_JTG-B01::JTG_B01-2014` have no extractable CJK text** (image-only/un-OCR'd). Chinese-script retrieval is therefore impossible; all `zh` benchmark hits rely on the English translation `JTG_D20-2017_EN`. Re-OCR these for genuine Chinese coverage.
- The 4 NEEDS_OCR docs (BRA IPR-706, CHN JTG D20-full, CHN JTG B01, ZAF UTG7) remain unusable for ground-truth.
- ZAF TRH17-1988 is OCR-garbled enough that clean verbatim quotes could not be extracted (noted by the PD agent).

---

## D. Benchmark-design fixes for a fair Phase-6 re-test

The current set cannot fairly judge the glossary's headline value (Threats §2–3). For a clean re-measurement:

1. **Add cross-language questions:** question phrased in language X, target document in language Y≠X (e.g., an English question whose only answer is in the Korean or German standard). This is the scenario the multilingual glossary exists for and is the only way to prove/disprove its value.
2. **Author questions independently of the target page** (e.g., have one agent write the question from a topic prompt, a *different* agent locate+verify the page) to remove question→page vocabulary leakage that currently inflates question-term retrievers.
3. **Expand the silent/negative set** (currently 5) and include *near-miss* negatives (value exists for a neighbouring speed/road-class but not the asked one) to stress fail-safe behaviour.
4. **Add a CJK-native sub-track** scored with the LIKE/`--grep` retriever so CJK is evaluated on a path that can actually work.
5. **Full answer-accuracy coverage** (all questions × the meaningful systems) rather than the 12-question demonstration used here, with longer passage windows (the 700-char truncation cost real "correct" credit).

---

### Bottom line
The Phase-5 evidence does **not** justify shipping concept-only retrieval, and does **not** (yet) justify the multilingual glossary as a flat query expansion. The actionable Phase-6 work is to (i) re-architect the skill's retriever to question-terms-plus-targeted-expansion with CJK via LIKE, and (ii) build a leakage-free, cross-language question set to test whether the glossary then earns its keep.

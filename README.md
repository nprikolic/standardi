# standardi — World Road Geometric Design Standards

A research corpus and a multilingual retrieval **skill** for comparing **national road geometric-design
standards** across the world (horizontal/vertical alignment, sight distance, cross-section, superelevation,
at-grade junctions and grade-separated interchanges/weaving), with the end goal of a **gap-analysis of the
Serbian standard** (Pravilnik 50/11) against international practice.

> Built with Claude Code. Working language of the notes is Serbian; see [TODO.md](TODO.md) for the plan and
> [PUBLICATION_ASSESSMENT.md](PUBLICATION_ASSESSMENT.md) for the publishability review.

## Status (2026-06-14)
- **Corpus:** 44 items / 86 PDFs / ~545 MB — **~19–21 countries** with substantive standards
  (36 retrieved · 7 paywalled-flagged · 1 needs_manual).
- **Content-verified:** 70 CONFIRMED / 6 PARTIAL / 3 NO_GEOMETRY / 4 NEEDS_OCR (of 83 PDFs).
- **Per-country completeness audit:** 3 COMPLETE, 10 ADEQUATE_CORE, 6 PARTIAL (19 countries).
- **Skill:** draft v0.3 — concept taxonomy + multilingual glossary (9 concepts × ~14 languages, incl.
  Cyrillic/CJK) + a working live-search tool.
- **Phase 5 (benchmark): DONE** — 77 grounded, quote-verified questions; 8 retrieval systems scored by code
  + a blind 3-judge answer sub-study. See [eval/BENCHMARK_REPORT.md](eval/BENCHMARK_REPORT.md).
  **⚠️ Key (negative) finding:** *concept-only* retrieval (`search.py --concept`, the skill's intended design)
  **fails** — recall@10 = 0.13 vs **0.86** for a plain native-language keyword search — because `--concept`
  ignores the question and returns the same pages for every question of a concept. The multilingual glossary
  as flat query-expansion adds no net value, and Japanese (CJK) FTS retrieval is 0%. The retriever must be
  re-architected (question terms + targeted glossary expansion; CJK via `--grep`) before publication
  (fixes in [eval/glossary_improvements.md](eval/glossary_improvements.md)).
- **Next:** retriever redesign + a leakage-free cross-language re-test, then Phase 6 (Serbian-standard gap-analysis).

Countries with standards: GBR, IRL, ESP, ITA, SWE, POL, KOR, BRA, ZAF, NZL, MWI, AFG, SRB, HRV, SVN, DEU,
USA, AUS, CHN, JPN (+ FRA partial). Flagged-only (no file): CAN, IND, NLD, MEX. Plus model standards
(TRL ORN 6, World Bank TP-496, SADC LVSR).

## Layout
```
road-geometric-standards/
  free/ paid/ mixed/ references/       # one folder per standard/item (+ _result.json, _log.txt)
  _audit/                              # per-country completeness audit (_audit/<ISO3>.json)
  _tools/                             # validate_pdf.py, aggregate_*.py, phase2_verify.py, ...
  MANIFEST.md  BUY_LIST.md  AUDIT.md  GAP_FILL.md
  summary.json  content_summary.json  CONTENT_VERIFICATION.md  download.log
skill/
  SKILL.md  NACRT.md  reference/ (taxonomy, glossary.json, standards-index, answer-format)  scripts/search.py
eval/                                  # Phase 5 benchmark
  questions.yaml  benchmark.csv  metrics.json  BENCHMARK_REPORT.md  glossary_improvements.md
  _tools/ (lib.py, run_retrieval.py, score.py, verify_groundtruth.py, page.py, ...)  runs/<system>/<qid>.json
TODO.md  PUBLICATION_ASSESSMENT.md
```

## Important — PDFs are not tracked
The standard PDFs (~545 MB, and several are **copyrighted/paid** — AASHTO, FGSV, Austroads) are
**gitignored** and are **not redistributed**. Only metadata is committed: each item's `_result.json`
records the official source URL, SHA-256, size and page count, so the corpus is reproducible from official
sources. The raw download/HTML staging folder (`manual-download/`) is also gitignored.

## Using the skill (v0 live search)
```
cd skill/scripts
python search.py --list-concepts
python search.py --concept WEAVING            # browse: all pages about a concept across standards
python search.py --concept SUPERELEVATION --iso3 ESP
python search.py --grep "vitoperenje"         # literal/CJK substring — most reliable for a specific term
```
Requires Python 3 + `pypdf` and Poppler (`pdftotext`). See `skill/SKILL.md` for the answer workflow.

> **Note (Phase 5):** `--concept` is a concept *browser*, not a per-question retriever — it returns the same
> pages regardless of the specific question. For a specific value, combine the concept with the question's own
> terms (and the document's language), and prefer `--grep` for an exact term, especially CJK. See
> [eval/BENCHMARK_REPORT.md](eval/BENCHMARK_REPORT.md) §3.

## Tooling
`validate_pdf.py` (magic-byte/size/page validation), `aggregate_phase1.py` / `aggregate_phase2.py`
(manifests + content summary), `phase2_verify.py` (multilingual concept matching), `aggregate_audit.py`
(audit roll-up). All under `road-geometric-standards/_tools/`.

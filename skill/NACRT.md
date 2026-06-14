# NACRT skilla — status i šta dalje

Ovo je **draft (v0.3)** skilla `world-road-design-standards`. Korpus (~19–21 zemlja, 86 PDF), audit (19 zemalja)
i popunjavanje praznina (raskrsnice/čvorovi, vitoperenje) su GOTOVI. Ostaje normalizovana baza vrednosti (Faza 3),
benchmark (Faza 5) i analiza SRB (Faza 6) — vidi `../TODO.md`.

## Šta je GOTOVO u nacrtu
- [x] `SKILL.md` — opis/trigeri (SR+EN), workflow, format, ograničenja
- [x] `reference/concept-taxonomy.md` — 9 pojmova (6 osnovnih + WEAVING, MERGE_DIVERGE, INTERCHANGE) + SR/HR/SL termini
- [x] `reference/glossary.json` — višejezični termini (~14 jezika uklj. SR ćirilica + de/pl stemovi) za retrieval
- [x] `reference/standards-index.md` — inventar korpusa mapiran na pojmove (+ šta nedostaje)
- [x] `reference/answer-format.md` — format odgovora + 2 kanonska primera (weaving, vitoperenje)
- [x] `scripts/search.py` — **funkcionalna v0 pretraga** uživo nad korpusom (pdftotext + višejezični termini, keš)
- [x] Demo provereno: `--concept WEAVING` nalazi GBR CD122 (170), IRL DN-GEO-03035/60, ESP trenzado, KOR 엇갈림, CHN

## Šta OSTAJE (kasnije, na poseban zahtev)
- [x] **Korpus (delom)**: dodati SRB (Pravilnik 50/11, ćirilica), HRV (NN 110/2001 render iz HTML), SVN
      (Pravilnik o projektiranju cest); pribavljeni DEU FGSV RAA/RAL/RASt i USA AASHTO (licencirano)
- [x] **Korpus (audit + gap-fill)**: 19 zemalja auditovano (`AUDIT.md`); besplatne praznine + AUS/NZL/SVN/HRV rešeni (`GAP_FILL.md`). Ostaje samo MEX (needs_manual) + plaćene (CAN/IND/NLD, CHN D21, JPN JRA, ZAF SANRAL, MWI SATCC, DEU FGSV 242) + OCR (opciono)
- [ ] **Faza 1**: ekstrakcija teksta po stranama u `corpus/text/`, OCR, normalizacija jedinica u SI, full-text indeks (FTS5)
- [ ] **Faza 2**: dopuniti glosar/ontologiju kroz evaluaciju (sinonimi, inflekcija)
- [ ] **Faza 3**: `kb/<id>.yaml` fact-sheets (normalizovane vrednosti + citat) i `kb/compare/<pojam>.md` matrice
- [ ] **Faza 5**: `eval/questions.yaml` banka pitanja + merenje retrieval/tačnosti
- [ ] **Faza 6**: `ANALIZA_SRB.md` — najproblematičnije tačke srpskog standarda + predlozi prema svetu (cilj projekta)
- [ ] Zameniti `search.py` v0 indeksiranom pretragom; dodati pretragu nad `kb/` vrednostima

## Kako se koristi sada (v0)
```
cd skill/scripts
python search.py --list-concepts
python search.py --concept WEAVING
python search.py --concept SUPERELEVATION --iso3 ESP
python search.py --grep "vitoperenje"
```
Skill čita reference fajlove i koristi `search.py` da nađe tačne strane, pa sastavlja uporedni odgovor sa citatima.

## Poznata ograničenja v0
- Nema normalizovanih vrednosti — broj uvek potvrditi na citiranoj strani.
- Skenirani dokumenti se ne pretražuju (NEEDS_OCR).
- Plaćeni/nedostajući standardi nisu pokriveni — za njih reci da nedostaju.

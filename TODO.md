# TODO — Skill „World Road Geometric Design Standards"

> **Cilj:** *skill* koji poznaje svetske standarde za geometrijsko projektovanje puteva i odgovara na
> duboka, uporedna pitanja sa tačnim citatima (standard · član/tačka · strana · jedinice u SI).
>
> **PRIMARNO istraživačko pitanje:** kako standardi regulišu **minimalni podužni nagib** i **minimalnu rampu
> vitoperenja** za autoputne profile — **iz uslova ODVODNJAVANJA** (mali/nulti poprečni nagib blizu tačaka
> infleksije / na deonici vitoperenja; rezultujući nagib ivice mora ostati dovoljan da voda otiče).
> **Sekundarno:** preplitanje (weaving), denivelisane raskrsnice, ostali geometrijski elementi.
>
> **Krajnji cilj:** gap-analiza srpskog standarda (Pravilnik 50/11) prema svetskoj praksi (Faza 6),
> fokus na min. podužne nagibe + rampu vitoperenja iz odvodnjavanja.

---

## TRENUTNO STANJE (ažurirano 2026-06-14)
- [x] **Korpus: 44 stavke / 86 PDF / 545 MB** — `road-geometric-standards/` (`MANIFEST.md`)
  - rezultat: **36 retrieved · 7 paywalled · 1 needs_manual** (samo MEX)
  - **~19–21 zemlja** sa supstancijalnim standardom (21 sa fajlom; FRA = samo corrigendum, JPN = samo tekst zakona)
- [x] **Sadržajna verifikacija (83 PDF):** **70 CONFIRMED · 6 PARTIAL · 3 NO_GEOMETRY · 4 NEEDS_OCR** (`CONTENT_VERIFICATION.md`)
- [x] **Audit kompletnosti (19 zemalja):** 3 COMPLETE, 10 ADEQUATE_CORE, 6 PARTIAL (`AUDIT.md`)
- [x] **Popunjavanje praznina** (raskrsnice/čvorovi, vitoperenje) odrađeno (`GAP_FILL.md`)
- [x] **Nacrt skilla v0.3** (`skill/`): SKILL.md + taksonomija pojmova + višejezični glosar (9 pojmova × ~14 jezika, uklj. ćirilica/CJK) + indeks standarda + format odgovora + **funkcionalna `scripts/search.py`**
- [x] **Ocena publikabilnosti** (`PUBLICATION_ASSESSMENT.md`): trenutno je *instrument*, ne *rezultat*; Građevinar realan tek uz Fazu 6; AI-venue tek uz Fazu 5 benchmark.
- [x] Git: sve metapodatke push-ovano na `nprikolic/standardi`; PDF-ovi gitignored (provenijencija/SHA u MANIFEST).

> **Faze 0, 1, 2 (seed), 4 (nacrt) su URAĐENE.** Ostaju: **Faza 3** (baza vrednosti), **Faza 5** (benchmark),
> **Faza 6** (analiza SRB = cilj). Korpus NE mora biti 100% pre nastavka (arhitektura je aditivna — vidi „Proces/strategija").

---

## FAZA 0 — Korpus  ✅ (gotovo, osim sitnih ostataka)
- [x] 0a. SRB / HRV / SVN ručno preuzeti i ubačeni (CONFIRMED)
- [x] 0b. Proširenje na raskrsnice/čvorove + poprečni profil/vitoperenje (UK CD122, IRL DN-GEO-03060/03035, DEU RAA, USA AASHTO…)
- [x] 0c. AUS AGRD03 Part 3 (ručno, login) ubačen · DEU/USA pribavljeni
- [x] 0d. Besplatne praznine iz audita skinute + 2 zastarela izdanja osvežena (SWE TRVINFRA-00396, HRV NN 90/2022+154/2024)
- [ ] **Ostatak (ne blokira):** MEX Manual 2018 (gov server bio dole) · OCR za skenirane (BRA IPR-706, CHN kineski, CHN B01, ZAF UTG7 — `tesseract` nije instaliran; pokriveno alternativama) · plaćene na BUY_LIST (CAN/IND/NLD, CHN D21, JPN JRA, ZAF SANRAL, MWI SATCC, DEU FGSV 242)

## FAZA 2 — Taksonomija + glosar  ✅ (seed gotov)
- [x] Taksonomija (9 pojmova) → `skill/reference/concept-taxonomy.md`
- [x] Višejezični glosar → `skill/reference/glossary.json` (uklj. SR ćirilica, DE, PL stemovi)
- [ ] Produbiti: „pojam → tačan član/strana" mapa po standardu (preklapa se sa Fazom 3)

## FAZA 4 — SKILL (nacrt)  ✅ → v0.3
- [x] `skill/SKILL.md` (trigeri SR+EN, workflow, format, ograničenja) + reference + `search.py`
- [ ] Migrirati u pravu instaliranu skill formu (`skill-creator`) kad baza vrednosti (Faza 3) sazri

---

## PREOSTALE FAZE

### FAZA 1 — Pretprocesiranje (🤖)  ✅ GOTOVO (2026-06-14)
- [x] Tekst po stranama → `corpus/text/*.jsonl` (**83 docs, 12.036 strana, 36.7M znakova, 0 grešaka**)
- [x] **SQLite FTS5 indeks** `corpus/index.sqlite` (12.036 page-redova) + query alat `_tools/query.py` (`--concept`/`--iso3`/`--lang`/`--grep`, bm25). Izveštaj: `PHASE1_REPORT.md`
- [x] Jezik po dokumentu (iso3→lang); UTF-8 (ćirilica/CJK) provereno
- [ ] OCR za 4 skenirana (BRA IPR-706, CHN JTG D20-full, CHN JTG B01, ZAF UTG7) — `tesseract` nije instaliran → pending (alternativni izvori pokrivaju)
- [ ] Normalizacija jedinica u SI → prebačeno u Fazu 3 (traži strukturisanu ekstrakciju)
- Napomena: `corpus/` je gitignored (pun tekst, uklj. copyrighted); regenerabilno preko `_tools/phase1_preprocess.py`.

### FAZA 3 — Strukturirana baza vrednosti (🤖)
- [ ] `kb/<id>.yaml` fact-sheets: normalizovane vrednosti po pojmu + citat (vrednost, jedinica, V, član, strana)
- [ ] `kb/compare/<pojam>.md` komparativne matrice (npr. e_max po klasi; min dužina prepleta vs brzina/protok)
- [ ] Eksplicitno beležiti „nem" (standard ne propisuje X) — ključno za Fazu 6

### FAZA 5 — Evaluacija / benchmark (🤖)  ← diže rad ka AI/computing venue
- [ ] Banka ≥50 pitanja (uklj. 2 kanonska), svako sa tačnim citiranim odgovorom
- [ ] Izmeri retrieval vs baseline (keyword / generički-RAG / goli-LLM) + ablacija glosara/taksonomije
- [ ] Iteriraj glosar gde promaši (inflekcija, sinonimi peralte/dévers/vitoperenje)

### FAZA 6 — Analiza srpskog standarda (👤 cilj)  ← diže rad ka Građevinaru — OBAVEZNO
- [ ] Po pojmu uporediti **SRB (Pravilnik 50/11 + SRDM)** sa korpusom: najproblematičnije tačke + šta NEDOSTAJE
- [ ] Za svaku: predlog unapređenja sa **bezbednosnim/operating-speed rationale** + citat kako rade drugi
- [ ] Uokviriti kao **generalizabilan, reproducibilan okvir** (Srbija kao primer), razgraničen od DRI/SRDM harmonizacije
- [ ] Izlaz: `ANALIZA_SRB.md` (tema · SRB · drugi · problem · predlog · izvor)
- [ ] **Preporuka:** prvo *suženo* na **minimalni podužni nagib + min. rampa vitoperenja iz odvodnjavanja** (najjači korpus: DE RAA/RAL, US AASHTO pogl.3–4, UK CD109, ES 3.1-IC, IT DM6792, SE VGU, PL WR-D-22-2, SRB Pravilnik 50/11 + SRDM) → nacrt rada za Građevinar

---

## PUBLIKACIJA (iz `PUBLICATION_ASSESSMENT.md`)
- **Sada (instrument):** nije publikabilno samo po sebi.
- **+ Faza 6 (scoped):** solidan **Građevinar** (Scopus/SCIE) „comparative / subject-review" rad. AI-deo ide samo kao metod.
- **+ Faza 5 benchmark:** AI/NLP doprinos → **ASCE J. Computing in Civil Eng** / Automation in Construction.
- **+ bezbednosni rationale + generalizabilan okvir:** ka TRR / Accident Analysis & Prevention / Baltic JRBE.
- **Disertacija:** kumulativna teza 3 rada (metod → svetska uporedba → unapređenje SRB).
- Pri pisanju: **zamrzni korpus** u snapshot + citiraj („N standarda, stanje [datum]").

## PROCES / STRATEGIJA (zašto ne čekati „sve")
- Skill je **aditivan**: nov standard = drop PDF + `_result.json` + re-run; `search.py` ga pokupi automatski. Ne kvari ništa.
- **Analiza vodi prikupljanje**, ne obrnuto: Faza 6 pokaže koje rupe su važne → tek tad ciljano dopuni.
- Veličina korpusa ≠ kvalitet rada; recenzenti nagrađuju dubinu uporedbe + gap-analizu.

---

## Struktura foldera (stanje)
```
standardi/
  README.md
  TODO.md                         # ovaj fajl
  PUBLICATION_ASSESSMENT.md       # ocena publikabilnosti
  road-geometric-standards/       # ✅ korpus (PDF gitignored)
    free/ paid/ mixed/ references/ _audit/ _tools/
    MANIFEST.md BUY_LIST.md AUDIT.md GAP_FILL.md summary.json content_summary.json CONTENT_VERIFICATION.md download.log
  skill/                          # ✅ nacrt v0.3
    SKILL.md NACRT.md reference/ scripts/search.py
  corpus/   # ⏳ Faza 1 (tekst/OCR/indeks)
  kb/       # ⏳ Faza 3 (fact-sheets + komparativne matrice)
  eval/     # ⏳ Faza 5 (banka pitanja)
  ANALIZA_SRB.md                  # ⏳ Faza 6 (finalni deliverable)
```

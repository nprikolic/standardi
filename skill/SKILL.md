---
name: world-road-design-standards
description: >-
  Uporedni odgovori o geometrijskom projektovanju puteva kroz SVETSKE standarde (sa citatima:
  standard · član/tačka · strana · jedinice u SI). Trigeruj na pitanja koja porede ili traže kako
  više nacionalnih standarda rešava neki geometrijski element — u srpskom ili engleskom:
  „kako svetski standardi hendluju…", „uporedi sa drugim standardima", „šta kažu strani standardi o…",
  „koji je max/min … u svetu". PRIMARNI FOKUS: minimalni podužni nagib (minimum longitudinal gradient) +
  minimalna rampa vitoperenja iz uslova ODVODNJAVANJA (drainage; mali/nulti poprečni nagib na vitoperenju).
  Ostale teme: preplitanje / weaving / dužina prepleta, denivelisane raskrsnice /
  petlje / interchange, ulivna/izlivna traka (merge/diverge, traka za ubrzanje/usporenje, rampe, nos),
  vitoperenje / razvoj poprečnog nagiba / superelevation runoff, max superelevacija e_max, projektna/
  računska brzina (design speed), preglednost (zaustavna/preticajna, sight distance), R_min / poluprečnik /
  klotoida / prelazna krivina (horizontal alignment), niveleta / podužni nagib / vertikalne krivine /
  K-vrednosti (vertical alignment), poprečni profil / širina trake / kolovoz (cross-section). Korpus pokriva
  SRB, HRV, SVN, GBR, IRL, ESP, ITA, SWE, POL, KOR, BRA, ZAF, NZL, CHN, JPN, DEU (RAA/RAL/RASt),
  USA (AASHTO Green Book) + model standardi; preostaje pribaviti CAN/IND/NLD (plaćeno) i MEX/AUS (needs_manual).
  NE koristi za: čisto srpski upit bez poređenja (→ pravilnik-reference);
  komande u GCM-u (→ gcm-d-reference).
---

# World Road Geometric Design Standards

> **STATUS: NACRT (v0.3).** Korpus ~19–21 zemlja (86 PDF, uklj. raskrsnice/čvorove + vitoperenje), audit i
> popunjavanje praznina gotovi. Normalizovana baza vrednosti (Faza 3), benchmark (Faza 5) i analiza SRB
> (Faza 6) tek predstoje (vidi [NACRT.md](NACRT.md)). Do tada radi preko `scripts/search.py`
> (pretraga uživo nad PDF korpusom) + reference fajlova.

## Čemu služi
Odgovara na **uporedna** pitanja o geometrijskom projektovanju puteva: „kako više svetskih standarda
rešava element X" i „koje su konkretne vrednosti/metode i u čemu se razlikuju". Svaki odgovor **mora**
da citira: *standard · član/tačka/tabela · strana · jedinica (u SI)*.

## Kada DA / kada NE
- **DA**: poređenje 2+ standarda; „šta kažu strani standardi o…"; tražene konkretne granične vrednosti
  ili metodologija (preplitanje, vitoperenje, rampe, e_max, K, preglednost, R_min, poprečni profil).
- **NE**:
  - čisto srpski upit bez poređenja → **`pravilnik-reference`** (Pravilnik 50/11)
  - kako uraditi nešto u softveru GCM → **`gcm-d-reference`**

## Korpus
Inventar i mapiranje „koji standard pokriva koji pojam" je u [reference/standards-index.md](reference/standards-index.md).
Sirovi PDF-ovi i manifesti su u `../road-geometric-standards/` (`MANIFEST.md`, `CONTENT_VERIFICATION.md`).

## Workflow (kako da odgovoriš)
1. **Klasifikuj pitanje** → mapiraj na jedan ili više **pojmova** iz
   [reference/concept-taxonomy.md](reference/concept-taxonomy.md)
   (npr. „dužina prepleta" → `WEAVING`; „nagib krovastog vitoperenja na ulivnoj traci" → `SUPERELEVATION` + `MERGE_DIVERGE`).
2. **Nađi izvore** → iz `standards-index.md` izaberi standarde koji pokrivaju pojam; pokreni
   `python scripts/search.py --concept <POJAM> [--iso3 XXX]` da dobiješ tačne strane i isečke
   (skripta koristi višejezične termine iz [reference/glossary.json](reference/glossary.json),
   pa hvata i ne-engleske dokumente).
3. **Izvuci vrednost/pravilo** sa tačnom stranom; **normalizuj jedinice u SI** (m, %, km/h), uz original.
4. **Sastavi uporedni odgovor** po formatu iz [reference/answer-format.md](reference/answer-format.md):
   kratka uporedna tabela + narativ + citati. **Eksplicitno reci gde standard ćuti** o pojmu.
5. **Caveat o izdanju**: navedi izdanje/reviziju i datum; označi ako je vrednost iz superseded izdanja
   ili iz prevoda (npr. JTG D20 EN), ili ako je dokument skeniran/NEEDS_OCR (vrednosti nepouzdane bez OCR).

## Alati
- `scripts/search.py` — v0 pretraga uživo nad korpusom (pdftotext na zahtev + višejezični termini).
  Primeri:
  - `python scripts/search.py --concept WEAVING` → sve pojave prepleta kroz korpus (standard, strana, isečak)
  - `python scripts/search.py --concept SUPERELEVATION --iso3 ESP`
  - `python scripts/search.py --grep "vitoperenje"` (slobodan tekst)

## Ograničenja (budi iskren u odgovoru)
- v0 nema normalizovanu bazu vrednosti — neke odgovore moraš da potvrdiš čitanjem citirane strane.
- Skenirani dokumenti (BRA IPR-706, CHN kineski JTG D20) su `NEEDS_OCR` → ne pretražuju se dok se ne OCR-uju;
  za njih koristi alternativu (BRA→IPR-740, CHN→EN izdanje).
- Pribavljeni plaćeni standardi: **DEU FGSV RAA/RAL/RASt** i **USA AASHTO Green Book** SU u korpusu (paid/, licencirano —
  PDF-ovi su gitignored). Još nisu pribavljeni: **CAN TAC, IND IRC, NLD CROW** + JRA komentar (vidi
  `../road-geometric-standards/BUY_LIST.md`) — za njih reci da nedostaju, ne nagađaj vrednosti.

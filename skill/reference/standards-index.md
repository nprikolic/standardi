# Indeks standarda → pokriveni pojmovi

Status v0.2. „Pojmovi" su orijentir za retrieval; tačnu stranu uvek potvrdi sa `scripts/search.py`.
Jezik = jezik dokumenta (search hvata termine na tom jeziku + en). Fajlovi su u
`../road-geometric-standards/free|mixed|paid/<folder>/`. Sadržajni status: vidi `CONTENT_VERIFICATION.md`.

## U korpusu (pretraživo)
| ISO3 | Standard (primarni fajl) | Jezik | Pojmovi (jako) | Napomena |
|---|---|---|---|---|
| **SRB** | **Pravilnik 50/11** (pun tekst, ćirilica) | sr | SVE (granični elementi) + WEAVING (преплит), INTERCHANGE | **referentni za Fazu 6**; ćirilica |
| **HRV** | **NN 110/2001** (render sa zakon.hr) | hr | SVE; 24 tabele kao tekst | iz HTML → PDF (Edge) |
| **SVN** | **Pravilnik o projektiranju cest** (NPB) | sl | SVE | folder label SLO_ |
| **DEU** | **FGSV RAA** motorways (+ RAL rural, RASt urban), EN | de | SVE + WEAVING (Verflechtung), MERGE_DIVERGE, SUPERELEVATION (Verwindung) | acquired; licencirano (paid/) |
| **USA** | **AASHTO Green Book** 7th 2018 | en | SVE + WEAVING (pogl. 10), SUPERELEVATION (pogl. 3), INTERCHANGE | acquired; licencirano (paid/) |
| GBR | DMRB **CD 122** grade separated junctions | en | WEAVING, MERGE_DIVERGE, INTERCHANGE, SUPERELEVATION | „weaving section length" tabele |
| GBR | DMRB **CD 109** highway link design | en | DESIGN_SPEED, HORIZONTAL, VERTICAL, SIGHT, CROSS_SECTION | osnovna trasa |
| GBR | DMRB **CD 127** cross-sections / **CD 116** roundabouts / **CD 123** at-grade | en | CROSS_SECTION, INTERCHANGE, MERGE_DIVERGE | |
| IRL | TII **DN-GEO-03060** junctions (Rev03, 2023) | en | INTERCHANGE, WEAVING (§7.9), MERGE_DIVERGE | aktuelni |
| IRL | TII **DN-GEO-03035** layout of GSJ (withdrawn) | en | WEAVING (vrednosti: „min weaving = 2 km") | istorijski detalj |
| IRL | TII **DN-GEO-03031** rural link design (v12) | en | DESIGN_SPEED, HORIZONTAL, VERTICAL, SIGHT, SUPERELEVATION, CROSS_SECTION | |
| ESP | **Norma 3.1-IC Trazado** | es | SVE + SUPERELEVATION (peralte), WEAVING (trenzado §8.6), MERGE_DIVERGE | vrlo kompletan |
| ITA | **DM 6792/2001** + annex | it | DESIGN_SPEED, HORIZONTAL (clotoide), VERTICAL, SUPERELEVATION, CROSS_SECTION, SIGHT | tabele u aneksu |
| SWE | **VGU** (Krav/Begrepp/Råd/Grundvärden) | sv | SVE + SUPERELEVATION (skevning) | višetomni |
| POL | **WR-D-22-2** kształtowanie geometryczne | pl | HORIZONTAL, VERTICAL, CROSS_SECTION, SUPERELEVATION, DESIGN_SPEED, SIGHT | inflekcija — koristi stem termine |
| POL | **Dz.U. 2022/1518** rozporządzenie | pl | SIGHT, HORIZONTAL, VERTICAL, CROSS_SECTION | propis |
| KOR | **Road Structure Rules — Commentary 2021** | ko | SVE + WEAVING (엇갈림), INTERCHANGE (입체교차) | 735 str. |
| BRA | **IPR-740** travessias urbanas | pt | SUPERELEVATION, CROSS_SECTION, WEAVING (entrelaçamento), MERGE_DIVERGE | |
| ZAF | **TRH17** rural roads | en | DESIGN_SPEED, HORIZONTAL, VERTICAL, SIGHT, SUPERELEVATION, CROSS_SECTION | 1988 |
| NZL | **NZTA SHGDM** (part 4 horiz, 5 vert, 6 x-sec) | en | SVE alignment + CROSS_SECTION, SUPERELEVATION | NZ uz Austroads |
| MWI | **LVR Manual Vol 2** / AFG **LVRR Vol 2** | en | geometric (low-volume) | |
| CHN | **JTG D20-2017 (EN)** | en | SVE + WEAVING, INTERCHANGE, MERGE_DIVERGE | zvanični EN prevod |
| JPN | **道路構造令** (law text) | ja | definicije + osnovne vrednosti | detalji u plaćenom JRA komentaru |
| MODEL | TRL **ORN 6**, WB **TP 496**, SADC **LVSR** | en | osnovni geometrijski elementi | model standardi |

> **Pokrivenost kanonskih pitanja:** WEAVING (preplitanje) → SRB, GBR CD122, IRL, ESP, KOR, CHN, **DEU RAA**, **USA AASHTO pogl.10**.
> Vitoperenje na ulivnoj/izlivnoj traci → **DEU RAA/RAS-Q (Verwindung/Anrampung)**, **USA AASHTO pogl.3**, ESP, ITA, GBR CD122. Oba pitanja sada imaju jake izvore.

## Skenirano — NEEDS_OCR (nije pretraživo; ima CONFIRMED zamenu)
| ISO3 | Fajl | Zamena (pretraživa) |
|---|---|---|
| BRA | IPR-706 rural geometric | IPR-740 (CONFIRMED) |
| CHN | JTG D20 (kineski) | JTG D20 EN (CONFIRMED) |

## Još nedostaje (reci da nedostaje — ne nagađaj)
| ISO3 | Standard | Status | Šta donosi |
|---|---|---|---|
| MEX | Manual de Proyecto Geométrico 2018 | needs_manual (gov server) | es korpus |
| AUS | AGRD Part 3/4 | needs_manual (login) | x-sec/weaving (Austroads) |
| CAN | TAC GDG | plaćeno — kupiti | severnoamerička praksa |
| IND | IRC:73/86/66 | plaćeno — kupiti | indijska serija |
| NLD | CROW (ASVV/HWO) | plaćeno — kupiti | holandska praksa |

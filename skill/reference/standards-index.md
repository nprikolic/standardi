# Indeks standarda → pokriveni pojmovi

Status v0.1. „Pojmovi" su orijentir za retrieval; tačnu stranu uvek potvrdi sa `scripts/search.py`.
Legenda jezika = jezik dokumenta (search hvata termine na tom jeziku + en). Fajlovi su u
`../road-geometric-standards/free|mixed/<folder>/`.

## U korpusu (pretraživo)
| ISO3 | Standard (primarni fajl) | Jezik | Pojmovi (jako) | Napomena |
|---|---|---|---|---|
| GBR | DMRB **CD 122** grade separated junctions | en | WEAVING, MERGE_DIVERGE, INTERCHANGE, SUPERELEVATION | „weaving section length" tabele; jak za petlje |
| GBR | DMRB **CD 109** highway link design | en | DESIGN_SPEED, HORIZONTAL, VERTICAL, SIGHT, CROSS_SECTION | osnovna trasa |
| GBR | DMRB **CD 127** cross-sections | en | CROSS_SECTION | |
| GBR | DMRB **CD 116** roundabouts / **CD 123** at-grade | en | INTERCHANGE, MERGE_DIVERGE | kružne/površinske |
| IRL | TII **DN-GEO-03060** junctions (Rev03, 2023) | en | INTERCHANGE, WEAVING (§7.9), MERGE_DIVERGE | aktuelni |
| IRL | TII **DN-GEO-03035** layout of GSJ (withdrawn 2017) | en | WEAVING (vrednosti!), MERGE_DIVERGE | „Desirable Min weaving = 2 km" tabele |
| IRL | TII **DN-GEO-03031** rural link design (v12) | en | DESIGN_SPEED, HORIZONTAL, VERTICAL, SIGHT, SUPERELEVATION, CROSS_SECTION | |
| ESP | **Norma 3.1-IC Trazado** | es | SVE: + SUPERELEVATION (peralte), WEAVING (trenzado §8.6), MERGE_DIVERGE | vrlo kompletan |
| ITA | **DM 6792/2001** + annex | it | DESIGN_SPEED, HORIZONTAL (clotoide), VERTICAL, SUPERELEVATION, CROSS_SECTION, SIGHT | tabele u aneksu |
| SWE | **VGU** (Krav/Begrepp/Råd/Grundvärden) | sv | SVE: + SUPERELEVATION (skevning) | višetomni |
| POL | **WR-D-22-2** kształtowanie geometryczne | pl | HORIZONTAL, VERTICAL, CROSS_SECTION, SUPERELEVATION (pochylenie poprzeczne), DESIGN_SPEED, SIGHT | inflekcija — koristi stem termine |
| POL | **Dz.U. 2022/1518** rozporządzenie | pl | SIGHT, HORIZONTAL, VERTICAL, CROSS_SECTION | propis |
| KOR | **Road Structure Rules — Commentary 2021** | ko | SVE: + WEAVING (엇갈림), INTERCHANGE (입체교차) | 735 str., sve vrednosti |
| BRA | **IPR-740** travessias urbanas | pt | SUPERELEVATION, CROSS_SECTION, WEAVING (entrelaçamento), MERGE_DIVERGE | |
| ZAF | **TRH17** rural roads | en | DESIGN_SPEED, HORIZONTAL, VERTICAL, SIGHT, SUPERELEVATION, CROSS_SECTION | 1988 |
| NZL | **NZTA SHGDM** (part 4 horiz, 5 vert, 6 x-sec) | en | SVE alignment + CROSS_SECTION, SUPERELEVATION | NZ uz Austroads |
| MWI | **LVR Manual Vol 2** | en | geometric (low-volume) | |
| AFG | **LVRR Vol 2** | en | geometric (low-volume) | |
| CHN | **JTG D20-2017 (EN)** | en | SVE: + WEAVING, INTERCHANGE, MERGE_DIVERGE | zvanični EN prevod |
| JPN | **道路構造令** (law text) | ja | definicije + osnovne vrednosti | detalji u plaćenom JRA komentaru |
| MODEL | TRL **ORN 6**, WB **TP 496**, SADC **LVSR** | en | osnovni geometrijski elementi | model standardi |

## Skenirano — NEEDS_OCR (nije pretraživo dok se ne OCR-uje)
| ISO3 | Fajl | Alternativa |
|---|---|---|
| BRA | IPR-706 rural geometric | koristi IPR-740 |
| CHN | JTG D20 (kineski) | koristi JTG D20 EN |

## Nedostaje u korpusu (reci da nedostaje — ne nagađaj)
| ISO3 | Standard | Status | Šta donosi |
|---|---|---|---|
| **SRB** | Pravilnik 50/11 | čeka 👤 manuelni download | referentni za Fazu 6 (analiza) |
| **HRV** | NN 110/2001 (+ Smjernice) | čeka 👤 | poređenje |
| **SLO** | Pravilnik o projektiranju cest + TSC | čeka 👤 | poređenje |
| MEX | Manual de Proyecto Geométrico 2018 | needs_manual (server) | es korpus |
| AUS | AGRD Part 3/4 | needs_manual (login) | jak za x-sec/weaving |
| USA | AASHTO Green Book | plaćeno | ch.3 superelevacija, ch.10 weaving/petlje |
| DEU | FGSV **RAA** (autoput), RAS-Q, RAL, RASt | plaćeno | najjači za Verflechtung (weaving) i Verwindung (vitoperenje) |
| CAN | TAC GDG | plaćeno | |
| IND | IRC:73/86/66 | plaćeno | |
| NLD | CROW (ASVV/HWO) | plaćeno | |

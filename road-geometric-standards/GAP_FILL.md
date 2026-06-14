# GAP_FILL — popunjavanje praznina iz audita (2026-06-14)

Posle audita ([AUDIT.md](AUDIT.md)) skinute su besplatne dopune (background agenti, samo zvanični izvori,
sve validirano). Korpus: **44 stavke / 79 PDF / 515 MB**; sadržajno **65 CONFIRMED, 5 PARTIAL, 2 NO_GEOMETRY, 4 NEEDS_OCR**.

## Skinuto besplatno (validirano)
| ISO3 | Dokument | str. | napomena |
|---|---|---|---|
| IRL | DN-GEO-03036 Cross Sections and Headroom (Rev09, 2023) | 55 | poprečni profil — popunjava jedinu rupu |
| IRL | DMURS (urbani dizajn, v1.1 2019) | 165 | urbano |
| ITA | DM 19/04/2006 Intersezioni (a raso/rotatorie/svincoli/zone di scambio) | 28 | raskrsnice — bila rupa |
| ITA | DM 22/04/2004 n.67/S (izmena DM 6792/2001) | 2 | obavezujuća izmena |
| ESP | OC 32/2012 Guía de Nudos Viarios | 549 | dizajn raskrsnica/čvorova |
| BRA | IPR-718 Manual de Projeto de Interseções (2005) | 530 | raskrsnice/petlje/preplitanje |
| KOR | 도로용량편람 (KHCM) 2013 | 702 | Ch.3 weaving (엇갈림) kapacitet/dužina |
| SRB | SRDM 4-0 Projektni elementi puta | 116 | detaljni geometrijski priručnik |
| SRB | SRDM 5-1 / 5-2 / 5-3 (raskrsnice u nivou / denivelisane / kružne) | 41/42/66 | detalji čvorova |
| SWE | **TRVINFRA-00396** Krav v1.0 (2025) + Grundvärden TRV 2024:148 | 721/58 | AKTUELNO izdanje (zamenjuje 2022) |
| ZAF | TRH26 (RCAM, 2012) + UTG1 (urb. arterijale) | 89/76 | klasifikacija + urbano |
| ZAF | UTG7 (urb. kolektori, skeniran) | 44 | NEEDS_OCR |
| HRV | NN 154/2024 (izmena) + Smjernice kružna raskrižja (Hrvatske ceste) | 2/81 | izmena + kružne |
| POL | WR-D-31-1/2/3 (skrzyżowania) + WR-D-32-1/2 (węzły) | 71/99/72/59/96 | **ceo blok raskrsnica/čvorova** — bila velika rupa |
| POL | WR-D-22-1 (wymagania) + WR-D-22-4 (katalog przekrojów) + WR-D-21 (skrajnia) | 43/35/45 | 22-4 = katalog (NO_GEOMETRY, crteži) |
| SVN | TSC 03.341 + TSPI 03.244 + 03.245 (krožna križišča) | 39/60/30 | kružne raskrsnice |
| CHN | **JTG B01-2014** Technical Standard of Highway Engineering | 115 | klase/brzine/profil — našao BESPLATNO (skeniran, NEEDS_OCR) |

## Još needs_manual (besplatno, ali ne automatski)
- **NZL** — TM2501/2502/2503 (NZTA supplementi): Incapsula bot-zid blokira curl; URL-ovi poznati (vidi NZL `_log.txt`) → treba browser.
- **SVN** — TSC 03.300:2002 i TSC 03.200:2003 (jezgro vrednosti/preglednost): zvanično nedostupni (samo neoficijelni mirrori) → ne skidamo.
- **HRV** — NN 90/2022 (izmena): Narodne novine samo HTML; mogu renderovati Edge-om kao glavni HRV doc.
- (od ranije) **MEX** Manual 2018, **AUS** AGRD03.

## Plaćeno → na BUY_LIST
- **CHN** JTG/T D21-2014 (petlje); **JPN** JRA komentar; **ZAF** SANRAL GDM; **MWI** SATCC trunk-roads; **DEU** FGSV 242 (kružne, dopunski).
- (od ranije: CAN TAC, IND IRC, NLD CROW; DEU RAA/RAL/RASt i USA AASHTO su PRIBAVLJENI.)

> Rezultat: skoro sve besplatne praznine zatvorene (raskrsnice/čvorovi koji su falili kod POL, ITA, ESP, BRA, IRL, SRB, KOR, SVN);
> 2 zastarela izdanja osvežena (SWE, HRV). Ostaje 6 needs_manual besplatnih + plaćene na listi.

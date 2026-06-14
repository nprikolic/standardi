# Format odgovora + uporedni primeri

## Pravila formata
1. **Uporedna tabela prva** — jedan red = jedan standard; kolone = traženi parametar(i) + jedinica (SI).
2. **Narativ** — sličnosti/razlike, uslovi (klasa puta, projektna brzina), pristup (deterministički vs. proračun protoka).
3. **Citati uz svaku vrednost** — `standard · član/tačka/tabela · strana`. Nikad vrednost bez izvora.
4. **Eksplicitan „nem"** — ako standard ne propisuje pojam, napiši to (ne ostavljaj prazno bez objašnjenja).
5. **Caveat** — izdanje/revizija + datum; označi prevod (npr. JTG D20 EN), superseded izdanje, ili NEEDS_OCR.
6. Ako nešto zavisi od **plaćenog/nedostajućeg** standarda (CAN/IND/NLD…), reci da nedostaje — **ne nagađaj broj**.

> **Retrieval (nalaz Faze 5):** `--concept` je *pregledač* — dobar da vidiš KOJI standardi pokrivaju pojam, ali vraća
> iste strane za svako pitanje. Za TAČNU vrednost suzi: `--iso3`/`--lang` + reči iz pitanja, a za tačan/CJK termin
> `--grep "<termin>"`. Uvek potvrdi vrednost na citiranoj strani. (`../eval/BENCHMARK_REPORT.md` §3–4)

---

## Primer 1 — „Kako svetski standardi hendluju minimalnu dužinu prepleta na denivelisanim raskrsnicama?"
**Pojmovi:** `WEAVING` (+ `INTERCHANGE`). **Pokreni:** `python scripts/search.py --concept WEAVING`

Skica odgovora (vrednosti potvrditi na citiranoj strani):

| Standard | Pristup | Min. dužina prepleta | Izvor |
|---|---|---|---|
| IRL TII DN-GEO-03035 | determinističko, po tipu puta | Rural Motorway/Type 1: **poželjni min = 2 km** | DN-GEO-03035 Rev05, §… str. 27 |
| IRL TII DN-GEO-03060 | proračun preplitanja za urbane autoputeve | po §7.9 (formula/tabele) | DN-GEO-03060 Rev03, §7.9 |
| GBR DMRB CD 122 | „weaving section length" + razmak čvorova | tabela/formula | CD 122 v1.1.1, str. 2 (sadržaj) → poglavlje weaving |
| ESP 3.1-IC | carriles de trenzado | §8.6 (dispozicija/dimenzije) | BOE-A-2016-2217, §8.6, str. 5/94 |
| CHN JTG D20-2017 (EN) | kapacitet zone preplitanja | §3.5 (capacity of interchange) | JTG D20 EN, str. 27 |
| KOR Commentary | 엇갈림 구간 (zona preplitanja) | pogl. 4 | Commentary 2021, str. ~139 |
| DEU RAA | Verflechtungsstrecke (po brzini/protoku) | **u korpusu** (paid/, licencirano, gitignored) — potvrdi stranu | RAA_FGSV202_Motorways_EN |
| USA AASHTO | weaving length (ch. 10) | **u korpusu** (paid/, licencirano, gitignored) — potvrdi stranu | AASHTO Green Book 7th (2018) |

Narativ: razdvojiti standarde koji daju **fiksnu graničnu dužinu** (npr. TII 2 km poželjni min) od onih koji
traže **proračun na osnovu protoka** (DN-GEO-03060 §7.9, JTG D20 kapacitet). Nemački RAA i AASHTO (najreferentniji
za autoputeve) **jesu u korpusu** (licencirani, PDF gitignored) — vrednosti pročitati sa strane, ne nagađati.

---

## Primer 2 — „Max nagib krovastog vitoperenja pri odvajanju ulivne/izlivne trake na profilu autoputa?"
**Pojmovi:** `SUPERELEVATION` (+ `MERGE_DIVERGE`, `CROSS_SECTION`).
**Pokreni:** `python scripts/search.py --concept SUPERELEVATION --iso3 ESP` (pa GBR, ITA, SWE…)

| Standard | Relevantni parametar | Vrednost | Izvor |
|---|---|---|---|
| ESP 3.1-IC | transición del peralte / bombeo; carriles de cambio de velocidad | po tabeli (zavisi od V, širine) | BOE-A-2016-2217, §… (peralte) |
| GBR DMRB CD 122 | superelevation na merge/diverge, ivična linija | poglavlje merges/diverges | CD 122 v1.1.1 |
| ITA DM 6792/2001 | sopraelevazione / pendenza trasversale; rampa | aneks tabele | DM 6792, aneks str. 69-77 |
| SWE VGU | skevning / skevningsutjämning | Krav/Grundvärden | VGU 2022:001 |
| DEU RAA | Verwindung/Anrampung — **maks. nagib ivice** na rampama | **u korpusu** (paid/, licencirano) — RAA p.42/46 daje „relative grade / resultant slope p≥0.5%" | RAA_FGSV202_Motorways_EN |
| USA AASHTO | superelevation runoff, max relative gradient (ch. 3) | **u korpusu** (paid/, licencirano) — Green Book p.285 (min profile/edge grade) | AASHTO Green Book 7th (2018) |

Napomena: „krovasto vitoperenje na ulivnoj/izlivnoj traci autoputa" je najpreciznije obrađeno u **nemačkom RAA**
i **AASHTO** (max relative gradient / Anrampungsneigung) — **oba su sada u korpusu** (licencirana, PDF gitignored;
v. konkretne strane potvrđene u Fazi 5: `../eval/questions.yaml` PB02–PB04, PC02). Vrednosti pročitati sa strane.

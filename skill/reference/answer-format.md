# Format odgovora + uporedni primeri

## Pravila formata
1. **Uporedna tabela prva** — jedan red = jedan standard; kolone = traženi parametar(i) + jedinica (SI).
2. **Narativ** — sličnosti/razlike, uslovi (klasa puta, projektna brzina), pristup (deterministički vs. proračun protoka).
3. **Citati uz svaku vrednost** — `standard · član/tačka/tabela · strana`. Nikad vrednost bez izvora.
4. **Eksplicitan „nem"** — ako standard ne propisuje pojam, napiši to (ne ostavljaj prazno bez objašnjenja).
5. **Caveat** — izdanje/revizija + datum; označi prevod (npr. JTG D20 EN), superseded izdanje, ili NEEDS_OCR.
6. Ako nešto zavisi od **plaćenog/nedostajućeg** standarda (AASHTO, RAA…), reci da nedostaje — **ne nagađaj broj**.

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
| **DEU RAA** | Verflechtungsstrecke (po brzini/protoku) | **NEDOSTAJE — plaćeno** | flag u BUY_LIST |
| **USA AASHTO** | weaving length (ch. 10) | **NEDOSTAJE — plaćeno** | flag u BUY_LIST |

Narativ: razdvojiti standarde koji daju **fiksnu graničnu dužinu** (npr. TII 2 km poželjni min) od onih koji
traže **proračun na osnovu protoka** (DN-GEO-03060 §7.9, JTG D20 kapacitet). Naglasiti da nemački RAA i AASHTO
(najreferentniji za autoputeve) trenutno nisu u korpusu.

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
| **DEU RAA / RAS-Q** | Verwindung/Anrampung — **maks. nagib ivice** na rampama | **NEDOSTAJE — plaćeno** (najmerodavniji) | BUY_LIST |
| **USA AASHTO** | superelevation runoff, max relative gradient (ch. 3) | **NEDOSTAJE — plaćeno** | BUY_LIST |

Napomena: baš „krovasto vitoperenje na ulivnoj/izlivnoj traci autoputa" je najpreciznije obrađeno u
**nemačkom RAA/RAS-Q** i **AASHTO** (max relative gradient / Anrampungsneigung) — oba su plaćena i nisu u
korpusu. Iz besplatnog korpusa daj ESP/ITA/SWE/UK vrednosti i jasno označi taj jaz.

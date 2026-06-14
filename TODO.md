# TODO — Skill „World Road Geometric Design Standards"

> **Cilj:** izgraditi *skill* koji dobro poznaje svetske standarde za geometrijsko projektovanje
> puteva i ume da odgovara na duboka, uporedna pitanja sa tačnim citatima (standard · član/tačka · strana · jedinice).
>
> **Tip pitanja koji skill MORA da rešava (kanonski primeri):**
> 1. „Kako svetski standardi hendluju **minimalnu dužinu prepleta** na denivelisanim raskrsnicama?"
> 2. „Koji je **maksimalni nagib krovastog vitoperenja** pri odvajanju ulivne/izlivne trake na profilu autoputa?"
>
> Ova pitanja su uporedna (više standarda odjednom), tematski uska i traže konkretne
> vrednosti/metodologiju + razliku između standarda + gde je neki standard „nem".

---

## Trenutno stanje (gotovo)
- [x] Korpus v0: 17 besplatnih standarda preuzeto i validirano (35 PDF, ~202 MB) — `road-geometric-standards/`
- [x] 6 plaćenih + 2 mixed flag-ovano (`BUY_LIST.md`, `TO_BUY.md`)
- [x] Sadržajna verifikacija po fajlu (`CONTENT_VERIFICATION.md`) — 32 CONFIRMED / 1 PARTIAL / 2 NEEDS_OCR
- [x] Višejezični glosar-seed (6 kategorija × 11 jezika) postoji u `_tools/phase2_verify.py`

---

## FAZA 0 — Kompletiranje korpusa
> Bez pravog korpusa skill ne može da odgovori na primer-pitanja. Ovo je preduslov za sve ostalo.

### 0a. Manuelni download (👤 ti) — OBAVEZNO
- [x] 👤 **Srpski** standard — Pravilnik (Sl. glasnik RS **50/11**), pun tekst (ćirilica, 143 str.) →
      `free/SRB_Pravilnik-50-11/`. CONFIRMED 6/6. (Kopija sa SSRN; verifikovati protiv Sl. glasnika.)
- [x] 👤 **Hrvatski** standard — Pravilnik (NN 110/2001) → `free/HRV_NN-110-2001/`. HTML sa zakon.hr
      renderovan u PDF (24 tabele kao tekst). CONFIRMED 6/6. (Skenirani original u `references/`.)
      Opciono kasnije: *Smjernice za projektiranje* (Hrvatske ceste / IGH).
- [x] 👤 **Slovenački** standard — *Pravilnik o projektiranju cest* (NPB) → `free/SLO_Pravilnik-projektiranje-cest/`.
      CONFIRMED 6/6. Opciono kasnije: **TSC** serija 03.2xx (DRSI/DARS).
- [x] 🤖 Ubačeni u korpus + `_result.json` + validacija + sadržajna provera (isti pipeline)

### 0b. Ciljano proširenje korpusa (👤+🤖) — da bi primer-pitanja imala izvor
> Trenutni korpus pokriva *trasu*. Treba dodati **raskrsnice/petlje** i **poprečni profil/vitoperenje**.
- [x] Denivelisane raskrsnice / preplitanje:
      DMRB **CD 122** (besplatno, ubačeno) + TII **DN-GEO-03060/03035** (besplatno, ubačeno);
      **RAA** (Autobahnen) i **AASHTO pogl. 10** — PRIBAVLJENO (paid/, licencirano). Austroads Part 4 = login-gated (needs_manual).
- [x] Poprečni profil + razvoj vitoperenja:
      **RAA / RAS-Q** i **AASHTO pogl. 3** PRIBAVLJENO; španska 3.1-IC (imamo). Austroads Part 3 = login-gated.
- [x] 🤖 Besplatni ubačeni; plaćeni DEU/USA pribavljeni i sadržajno potvrđeni (CONFIRMED).

### 0c. Rešiti zaostatke iz Faze 1/2
- [ ] 👤 **MEX** (needs_manual) — preuzeti Manual 2018 kad srpski/MX server proradi (URL u `summary.json`)
- [ ] 👤 **AUS AGRD03** (needs_manual) — besplatno ali iza login-a; skinuti uz besplatan Austroads nalog
- [ ] 🤖/👤 **OCR** za skenirane: BRA **IPR-706**, CHN **JTG D20 (kineski)**.
      Potreban `tesseract` + jezički paketi (`por`, `chi_sim`) — trenutno NISU instalirani.
      (Pokrivenost za BRA/CHN već postoji preko IPR-740 / EN izdanja — OCR je „nice to have".)
- [x] 🤖 **Plaćeni — pribavljeno:** DEU FGSV (RAA/RAL/RASt) i USA AASHTO Green Book (licencirano, paid/).
      **Preostaje:** CAN TAC, IND IRC, NLD CROW (vidi `BUY_LIST.md`).

---

### 0d. Popunjavanje praznina iz audita (vidi `road-geometric-standards/AUDIT.md`)
> Audit 19 zemalja (2026-06-14): **3 COMPLETE, 10 ADEQUATE_CORE, 6 PARTIAL** · 34 besplatne praznine, 6 plaćenih, 4 zastarela izdanja.
- [ ] 🤖 Skinuti **34 besplatne praznine** (prioritet: raskrsnice/čvorovi koji fale kod POL, ITA, ESP, BRA, IRL, SVN, SRB, KOR). URL-ovi u AUDIT.md.
- [ ] 👤/🤖 Zameniti **zastarela izdanja**: SWE → TRVINFRA-00396; HRV → pročišćeni NN (izmene 90/2022 + 154/2024 — naš render je original); NZL → Austroads AGRD; ZAF (po potrebi).
- [ ] 🤖 Plaćene/restriktivne praznine (CHN JTG B01/D21, JPN JRA komentar, ZAF SANRAL, MWI SATCC, DEU FGSV 242) — na BUY_LIST/odluku.

---

## FAZA 1 — Pretprocesiranje korpusa (🤖)
- [ ] Ekstrakcija teksta **po stranama** (čuvati broj strane) za svaki PDF → `corpus/text/<id>/pNNN.txt`
- [ ] OCR za skenirane (zavisi od 0c); jezik-svestan (`-l por/chi_sim/...`)
- [ ] Detekcija jezika po dokumentu; UTF-8 svuda (CJK/dijakritika)
- [ ] Normalizacija jedinica → sve u **metrički SI** (m, %, km/h), uz čuvanje originala
- [ ] Sirov full-text indeks (npr. SQLite FTS5 ili jednostavan invertovani indeks) za narativna pitanja

---

## FAZA 2 — Ontologija pojmova + višejezični glosar (🤖, jezgro kvaliteta)
> Ovo je „mozak" pretrage: pitanje → pojam → tačan član u svakom standardu, bez obzira na jezik.
- [ ] **Taksonomija pojmova** geometrijskog projektovanja (hijerarhija), npr.:
      `trasa u planu` (R_min, klotoida A, dužina prave/luka, vitoperenje) ·
      `niveleta` (max nagib, vertikalne krivine K, konkavna/konveksna) ·
      `poprečni profil` (širina trake/kolovoza, bankina, popr. nagib) ·
      `preglednost` (zaustavna, preticajna) ·
      `vitoperenje/superelevacija` (max e, max nagib ivice/rampe, razvoj na ulivnoj/izlivnoj traci) ·
      `denivelisane raskrsnice` (rampe, **preplitanje/weaving**, ubrzavajuće/usporavajuće trake, nos/gore) ·
      `projektne brzine i klase puta`
- [ ] **Višejezični glosar** pojam → termin po jeziku (proširiti seed iz `phase2_verify.py`;
      dodati SR/HR/SL termine: *vitoperenje, preplitanje, ulivna/izlivna traka, prelazna krivina, niveleta…*)
- [ ] **Mapa „pojam → lokacija"**: za svaki standard, koje poglavlje/član/tabela pokriva koji pojam
      (omogućava precizan citat strane)

---

## FAZA 3 — Strukturirana baza znanja (🤖, ono što daje tačne brojeve)
- [ ] **Fact-sheet po standardu** (`kb/<id>.yaml`): normalizovane vrednosti po pojmu sa citatom
      (vrednost, jedinica, uslov/projektna brzina, standard, član/tabela, strana)
- [ ] **Komparativne matrice po pojmu** (`kb/compare/<pojam>.md`): jedan red = jedan standard, kolone =
      parametri. Npr. tabela „max superelevacija e_max po klasi" ili „min dužina prepleta vs. protok/brzina".
- [ ] Eksplicitno beležiti **„nem"** (standard ne propisuje X) — to je ključno za gap-analizu srpskog

---

## FAZA 4 — Sam SKILL (🤖, koristiti `skill-creator`)
- [ ] `SKILL.md`:
  - [ ] **Opis/trigeri** (SR+EN): uporedna pitanja o geometrijskim elementima, granični elementi,
        vitoperenje, preplitanje, rampe, preglednost, poprečni profil, K-vrednosti… (slično `pravilnik-reference`,
        ali za *sve* standarde i *uporedno*)
  - [ ] **Workflow**: klasifikuj pitanje → mapiraj na pojam(ove) → povuci iz fact-sheet baze + full-text indeksa →
        sastavi **uporedni** odgovor sa citatima, jedinice u SI → eksplicitno naznači gde standard ćuti
  - [ ] **Format odgovora**: kratka uporedna tabela + narativ + citati (standard · član · strana) + caveat o izdanju
  - [ ] Priložene reference: komparativne matrice, glosar, „pojam→lokacija" indeks
- [ ] Odnos prema postojećim skill-ovima: komplementaran sa `pravilnik-reference` (SR) i `gcm-d-reference`
- [ ] Razrešiti veličinu: skill ne sme da gura 200 MB u kontekst — koristi indeks + skripte za pretragu

---

## FAZA 5 — Evaluacija (🤖)
- [ ] **Banka pitanja** (≥20), uključujući 2 kanonska primera, sa očekivanim izvorima/odgovorom
- [ ] Meri: da li nalazi pravi član u pravom standardu; tačnost vrednosti; pokrivenost više standarda; citati
- [ ] Iteriraj glosar/ontologiju gde retrieval promaši (npr. PL/SR inflekcija, sinonimi tipa *peralte/dévers/vitoperenje*)

---

## FAZA 6 — Analiza srpskog standarda + predlozi unapređenja (👤 cilj projekta) — OBAVEZNO
> Iskoristiti gotov skill da se srpski standard uporedi sa svetom.
- [ ] 🤖 Po svakom pojmu uporediti **SRB (Pravilnik 50/11)** sa korpusom → identifikovati:
  - [ ] **Najproblematičnije tačke** (vrednosti koje odstupaju/su manje bezbedne, zastarele metode)
  - [ ] **Šta NEDOSTAJE** u srpskom a postoji drugde (npr. eksplicitna metodologija prepleta, granični
        nagib vitoperenja na ulivnoj/izlivnoj traci, K-vrednosti, kriterijumi preglednosti…)
- [ ] 🤖 Za svaku tačku: **predlog unapređenja** sa referencom kako to rešavaju drugi standardi (citirano)
- [ ] 🤖 Izlaz: izveštaj `ANALIZA_SRB.md` (tabela: tema · šta kaže SRB · šta kažu drugi · problem · predlog · izvor)

---

## Održavanje
- [ ] Pratiti izdanja (npr. SWE VGU 2025 = PUBEN, AASHTO 8. izd. u izradi) i datume revizija
- [ ] Skripta za dodavanje novog standarda (download → validacija → ekstrakcija → fact-sheet → matrice)

---

## Odluke (potvrđeno 2026-06-14)
1. **Proširenje korpusa (Faza 0b): DA** — dodajemo raskrsnice/preplitanje + poprečni profil/vitoperenje.
   Besplatno: DMRB CD 122 (grade separated junctions), TII junction standardi. Login-gated (→needs_manual):
   Austroads AGRD Part 4 serija (intersections/interchanges) — kao i Part 3.
2. **Plaćeni: SVE** ostaju na listi za kupovinu (AASHTO Green Book uklj. pogl. 10 weaving + pogl. 3 superelevacija,
   TAC GDG, IRC serija, FGSV uklj. **RAA = FGSV 202** i RAS-Q, CROW; + mixed JPN/CHN, FRA ICTAAL/ARP). Ja NE kupujem.
3. **Redosled: SAMO korpus + nacrt skilla za sada** — kompletiramo korpus i pravimo `SKILL.md` nacrt (skeleton)
   + arhitekturu. Pun build baze znanja (Faze 1–3, 5) i **Faza 6 (analiza SRB)** dolaze kasnije, na poseban zahtev.
4. **Format izlaza Faze 6**: odlučiti kasnije (Markdown podrazumevano; mogu i Word/PDF).

## Struktura foldera (predlog)
```
standardi/
  road-geometric-standards/   # sirovi PDF + manifesti (postoji)
  corpus/
    text/<id>/pNNN.txt         # ekstrahovan tekst po strani
    ocr/                       # OCR rezultati
  kb/
    glossary.yaml              # višejezični glosar (pojam→termini)
    concept_index.yaml         # pojam→standard→član/strana
    <id>.yaml                  # fact-sheet po standardu
    compare/<pojam>.md         # komparativne matrice
  skill/                       # SKILL.md + reference + skripte za pretragu
  eval/questions.yaml          # banka pitanja
  ANALIZA_SRB.md               # finalni deliverable (Faza 6)
  TODO.md                      # ovaj fajl
```

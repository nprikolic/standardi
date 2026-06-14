# Faza 5 — Paralelni benchmark retrievala i odgovora (autonomno, preko noći)

> **Kako se koristi:** otvori SVEŽU sesiju u `D:\My Drive\Nauka\standardi` i prosledi ceo ovaj fajl kao zadatak
> (npr. „Izvrši eval/BENCHMARK_PROMPT.md"). Namenjeno za **autonoman, paralelan, nenadgledan** rad (overnight).
> Ako želiš maksimalnu paralelizaciju, dodaj reč **ultracode** ili eksplicitno traži *workflow / fan-out agente*.

## Cilj
Kvantitativno dokazati vrednost skilla: da li **concept + višejezični-glosar** retrieval pobeđuje baseline-ove
u nalaženju i CITIRANJU tačne vrednosti/klauzule kroz svetske standarde geometrijskog projektovanja — sa
naglaskom na **PRIMARNU temu**: *minimalni podužni nagib + minimalna rampa vitoperenja (min/max relativni
nagib na deonici vitoperenja) iz USLOVA ODVODNJAVANJA*. Izlaz: benchmark izveštaj + lista za dopunu glosara
(zatvara petlju ka Fazi 6).

## Režim rada
Autonomno i paralelno; **fan-out background agentima / Workflow-om, ~6–8 konkurentno**; idempotentno i resumable;
ne blokiraj korisnika; sve artefakte piši pod `eval/`. **Ne commit-uj pun copyrighted tekst** — citati ≤200 znakova.
Datum stampaj iz prosleđene vrednosti (u Workflow skriptama `Date.now()` ne radi).

## ⚠️ Integritet rezultata — ANTI-FABRIKACIJA (OBAVEZNO, ispred svega)
**Sukob interesa:** isti model gradi sistem, pitanja, izvršava i sudi — postoji jaka sklonost da se rezultati
ULEPŠAJU u korist „našeg" sistema (S3). Tvoj posao je da budeš **skeptičan prema sopstvenim rezultatima** i da
aktivno tražiš razloge zašto bi mogli biti PRECENJENI. Bolje konzervativan, proverljiv broj nego lep neproverljiv.
1. **Bez izmišljanja.** Nijedna vrednost/citat ne sme doći iz parametarskog znanja. Ground-truth i svaka „correct"
   ocena moraju biti **doslovno prisutni na citiranoj strani** (proveri u `corpus/text/...jsonl`). Ne može se
   potvrditi → „unverified"/odbaci; **nikad ne pretpostavljaj ni „zaokruži"**.
2. **Ground-truth se gradi PRE i NEZAVISNO od sistema, pa se ZAMRZNE.** Ne izvodi „tačan odgovor" iz onoga što S3
   vrati (to je cirkularno i napumpava S3). Ne menjaj pitanja ni ground-truth nakon gledanja rezultata.
3. **Slepo suđenje.** Sudija NE sme znati koji sistem je dao odgovor — **anonimizuj i promešaj** oznake (S0–S3c).
   Sudi isključivo {pitanje, ground-truth, kandidat}. Default ocena = „wrong/unverified" kad si nesiguran.
4. **Metrike = kod, ne procena LLM-a.** Recall@k/MRR/Precision računa skripta poredeći `doc_id`/strane sa
   ground-truth-om. **Zabranjeno samoocenjivanje skora** od strane agenta.
5. **Bez naknadnog štelovanja (no overfitting).** NE menjaj glosar/termine da S3 prođe bolje pa ponovo meriš na
   ISTIM pitanjima. Predlozi za glosar idu u `glossary_improvements.md` za BUDUĆI rad — ne primenjuju se i ne
   re-meri na istom setu.
6. **Bez survivorship bias-a.** Sva izgrađena pitanja se ocenjuju i prijavljuju; **ne bacaj „teška" pitanja** na
   kojima S3 gubi. Broj odbačenih (i zašto) ide u izveštaj.
7. **Kontrole/zamke.** Ubaci 3–5 pitanja čiji odgovor NE postoji u korpusu (ispravno = „nije nađeno") + „silent"
   pitanja. Svaki sistem koji ipak „odgovori" → halucinacija, računa se PROTIV njega.
8. **Crvena zastava = sumnja, ne slavlje.** Ako S3 pobeđuje ~100% ili deluje savršeno, to je verovatnije
   GREŠKA/bias/curenje ground-truth-a u termine nego istina — istraži i prijavi pre nego što objaviš brojeve.
9. **Auditabilnost.** Čuvaj sve sirove per-pitanje rezultate + verbatim citate; označi nasumičan uzorak (≥10%) za
   ručnu reviziju (čovek mora moći da proveri tvoje brojeve).

## Sredstva (sve lokalno u repo-u)
- Korpus: **83 docs / 12.036 strana**, višejezično. FTS5 indeks: `corpus/index.sqlite` (gitignored; ako fali,
  pokreni `python road-geometric-standards/_tools/phase1_preprocess.py`).
- Query alat: `road-geometric-standards/_tools/query.py` — `--concept <NAME>`, `--iso3`, `--lang`, `--grep`,
  slobodan tekst; bm25 rangiranje. (Ovo je osnova za sistem S3 dole.)
- Glosar pojmova: `skill/reference/glossary.json` (10 pojmova × ~14 jezika, uklj. ćirilica/CJK).
- Tekst po stranama: `corpus/text/<folder>/<pdf>.pages.jsonl` (za čitanje/citiranje strane).
- Inventar: `road-geometric-standards/MANIFEST.md`, `CONTENT_VERIFICATION.md`.
  **Preskoči 4 NEEDS_OCR dokumenta** (nisu pretraživi): BRA IPR-706, CHN JTG D20-full, CHN JTG B01, ZAF UTG7.
- Primarni pojam: `DRAINAGE_MIN_GRADE`; relevantni i `SUPERELEVATION`, `VERTICAL`.

## Deliverables (pod `eval/`)
1. `eval/questions.yaml` — ≥50 pitanja sa **potvrđenim ground-truth** odgovorima.
2. `eval/runs/<system>/<qid>.json` — sirov rezultat po (sistem, pitanje).
3. `eval/BENCHMARK_REPORT.md` — tabele metrika + raščlanjenja + analiza grešaka.
4. `eval/glossary_improvements.md` — termini/sinonimi za dodavanje u `glossary.json` (iz promašaja).
5. `eval/benchmark.csv` — sirovi skorovani podaci (NE `.sqlite` — gitignored).

---

## Faza A — Banka pitanja (paralelno, grounded)
Cilj **≥50 pitanja**. Sastav:
- **≥20 na PRIMARNU temu** (min. podužni nagib; min/max relativni nagib na rampi vitoperenja; dužina „nulte"
  zone / odvodnjavanje na vitoperenju) kroz **≥8 zemalja** uklj. SRB, DEU, USA, GBR, ESP, IRL, SWE, HRV, SVN.
- ostatak raspoređen po preostalim pojmovima (design speed, sight distance, horizontalni R/klotoida, vertikalne
  K-vrednosti, poprečni profil, e_max, weaving, merge/diverge, interchange) i po **jezicima**
  (en/de/es/it/fr/sv/pl/sr/hr/sl/ko/ja/zh).
- **~5 „silent/negativnih"** pitanja (gde standard NE propisuje X) — testira ponašanje „reci da nedostaje".

**Gradi pitanja IZ korpusa** da odgovor sigurno postoji: fan-out agenti za svaki kandidat lociraju autoritativni
pasus preko `query.py` + čitanja citirane strane u `corpus/text/...jsonl`, i beleže ground-truth
`{doc_id, page, value/clause, lang, quote≤200ch}`. **Zaseban verifikator-agent** potvrđuje svaki ground-truth sa
citirane strane (adversarijalno: odbaci ako vrednost nije **doslovno** na toj strani). Zadrži samo pitanja sa
**nezavisno potvrđenim** ground-truth-om. Ground-truth se gradi **iz izvora, PRE pokretanja sistema, i ZAMRZNE** —
NIKAD izveden iz onoga što S3 vrati (cirkularno bi napumpalo S3).
Šema po pitanju: `{qid, topic, concept, question_en, question_local?, lang, expected:[{doc_id,page,value,quote}], difficulty, is_silent}`.

## Faza B — Sistemi pod testom (svaki sistem na svakom pitanju, paralelno)
Za svako pitanje proizvedi (a) rangirane pasuse i (b) odgovor + citat, za svaki sistem. **k = 10.**
- **S0 raw-LLM** — odgovor iz parametarskog znanja, BEZ retrievala (meri halucinaciju/lažni citat).
- **S1 keyword-BM25** — FTS5 upit = sirov tekst pitanja → top-k pasusi → odgovor samo iz njih.
- **S2 generic-RAG** — top-k pasusi po pitanju, BEZ glosara/taksonomije → odgovor.
- **S3 SKILL (naš)** — mapiraj pitanje→pojam (taksonomija) → višejezični termini iz glosara → FTS5 → top-k →
  odgovor + citat. (Tj. `query.py --concept`.)
- **Ablacije:** **S3a** = naš ali samo engleski termini (bez višejezičnog); **S3b** = naš bez concept-mapiranja
  (slobodni termini); **S3c** = LIKE umesto FTS5.
Zabeleži povučene `doc_id`+`page` i odgovor sa citiranim `doc/page/value`.

## Faza C — Skorovanje (paralelno)
**Retrieval metrike (determinističke) vs ground-truth:** Recall@10, MRR, Precision@10 (pogodak = ground-truth
`doc_id` I `page` u opsegu ±1, unutar top-k). Po sistemu, po pojmu, po jeziku, i za **PRIMARNI podskup
(DRAINAGE_MIN_GRADE)**.
**Tačnost odgovora:** LLM-sudija (**panel od 3, većina**) poredi proizvedenu vrednost+citat sa ground-truth →
`{correct, partially, wrong, hallucinated_citation, missing}`. Za „silent" pitanja: tačno = „kaže da X nije
propisano". **Suđenje je SLEPO:** sudija ne zna koji sistem je dao odgovor (anonimizuj i promešaj S0–S3c), vidi
samo {pitanje, ground-truth, kandidat}. Sudija mora da **otvori citiranu stranu** (`corpus/text/...jsonl`) i
potvrdi da vrednost zaista tamo stoji pre ocene „correct"; adversarijalno (default „wrong/unverified" ako se citat
ne može potvrditi). Ako proizvedena vrednost nije na navedenoj strani → `hallucinated_citation` (PROTIV sistema).

## Faza D — Agregacija + izveštaj
`eval/BENCHMARK_REPORT.md`:
- **Glavna tabela:** sistemi × {Recall@10, MRR, Answer-correct %, Hallucinated-citation %}.
- **Raščlanjenje:** PRIMARNI podskup (drainage/min-grade) izdvojeno; po pojmu; po jeziku (istakni ne-engleske +
  ćirilica/CJK).
- **Ablacioni delte** (S3 vs S3a/S3b/S3c) → kvantifikuj vrednost *višejezičnog* glosara i *concept-mapiranja*.
- **Analiza grešaka:** pitanja gde S3 promaši; uzrok (rupa u terminu, inflekcija, NEEDS_OCR dokument, FTS CJK
  ograničenje).
`eval/glossary_improvements.md`: konkretni termini/sinonimi za `glossary.json` (iz promašaja) + eventualne
dopune taksonomije/pojmova.
**Threats to validity (OBAVEZNA sekcija u izveštaju):** sukob interesa (isti model gradi+izvršava+sudi), mali N,
subjektivnost sudije, gde je ground-truth slab/dvosmislen, FTS-CJK i NEEDS_OCR ograničenja. **Eksplicitno navedi
gde S3 GUBI i zašto.** Ako S3 dominira gotovo svuda → tretiraj kao crvenu zastavu (bias/bug/curenje), istraži i
napiši nalaz. Daj i **konzervativan** sud: da li je razlika S3 vs baseline stvarna i dovoljno velika, ili u okviru
šuma malog N. Priloži sirove per-pitanje rezultate + ≥10% nasumično označeno za ručnu reviziju.

## Ograničenja / kvalitet
- Samo zvanični korpus; ground-truth MORA biti potvrđen sa citirane strane (bez parametarskog nagađanja).
- Citati ≤200 znakova; UTF-8; CJK pouzdano preko `--grep` (FTS `unicode61` ima ograničenje za CJK *phrase* MATCH).
- 4 NEEDS_OCR dokumenta se ne koriste za ground-truth.
- Idempotentno, resumable, loguj napredak. Background agenti / Workflow; ~6–8 konkurentno.

## Kriterijum uspeha
≥50 pitanja sa potvrđenim ground-truth-om; svi sistemi prošli kroz sva pitanja; izveštaj pokazuje da **S3
(naročito višejezični + concept-mapiranje) pobeđuje baseline-ove** po Recall@10 / tačnosti odgovora, sa
izdvojenim **PRIMARNIM podskupom**; proizvedena lista za dopunu glosara (ulaz u Fazu 6).

---
*Napomena: ovaj benchmark je „high-leverage" stavka iz `PUBLICATION_ASSESSMENT.md` — meren benchmark + baseline +
ablacija je ono što AI/NLP deo rada diže ka ASCE J. Computing in Civil Eng / Automation in Construction.*

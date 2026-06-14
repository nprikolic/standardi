# Taksonomija pojmova (concept taxonomy)

Pitanje korisnika se mapira na jedan ili više **pojmova** ispod. Mašinski termini (po jeziku) su u
[glossary.json](glossary.json) i koristi ih `scripts/search.py`. Pojam je ključ za retrieval i za
komparativne matrice (Faza 3).

## A. Trasa (alignment)
- **DESIGN_SPEED** — projektna / računska / merodavna brzina; klase puta. *(en: design speed)*
- **HORIZONTAL** — situacioni plan: poluprečnik/radijus (R, R_min), klotoida/prelazna krivina (param. A),
  dužina kružnog luka, dužina međupravca. *(en: horizontal alignment, radius, clothoid)*
- **VERTICAL** — niveleta: max podužni nagib, vertikalne (konveksne/konkavne) krivine, K-vrednosti.
  *(en: vertical alignment, gradient, K-value)*
- **SIGHT_DISTANCE** — preglednost: zaustavna, preticajna. *(en: stopping/overtaking sight distance)*

## B. Poprečni profil i vitoperenje
- **CROSS_SECTION** — poprečni profil: širina trake/kolovoza, bankina, ivična traka, razdelni pojas.
  *(en: cross-section, lane width, carriageway)*
- **SUPERELEVATION** — vitoperenje / poprečni nagib: max e (e_max), **razvoj/rampa vitoperenja**
  (superelevation runoff), jednostrešni↔dvostrešni („krovasti") prelaz, granični nagib ivice kolovoza.
  *(en: superelevation, crossfall rotation, runoff; de: Querneigung, Verwindung, Anrampung)*

## C. Denivelisane raskrsnice (interchanges)
- **INTERCHANGE** — denivelisana raskrsnica / petlja / čvor; tipovi, razmak. *(de: planfreier Knotenpunkt)*
- **MERGE_DIVERGE** — ulivna/izlivna traka, traka za ubrzanje/usporenje, rampa, priključna traka,
  nos/klin (gore/taper). *(en: merge/diverge, accel/decel lane, ramp, taper, gore)*
- **WEAVING** — preplitanje: dužina prepleta, deonica preplitanja, min. dužina preplitanja.
  *(en: weaving length; de: Verflechtungsstrecke; es: trenzado; ko: 엇갈림)*

> Pitanja često spajaju pojmove. Primeri:
> - „min. dužina **prepleta** na **denivelisanim raskrsnicama**" → `WEAVING` (+ `INTERCHANGE`)
> - „max nagib **krovastog vitoperenja** pri odvajanju **ulivne/izlivne** trake" → `SUPERELEVATION` (+ `MERGE_DIVERGE`)

## Srpsko/hrvatsko/slovenački termini (najvažniji)
| Pojam | SR | HR | SL |
|---|---|---|---|
| DESIGN_SPEED | računska/projektna brzina | računska/projektna brzina | računska/projektna hitrost |
| SIGHT_DISTANCE | preglednost, zaustavna preglednost | preglednost | pregledna razdalja |
| HORIZONTAL | poluprečnik, klotoida, prelazna krivina | polumjer, prijelazna krivina | radij, prehodnica |
| VERTICAL | niveleta, podužni nagib, vertikalna krivina | niveleta, uzdužni nagib | niveleta, vzdolžni nagib |
| SUPERELEVATION | vitoperenje, poprečni nagib | vitoperenje, poprečni nagib | nagib vozišča, prečni nagib |
| CROSS_SECTION | poprečni profil, širina trake | poprečni presjek, širina traka | prečni profil, širina pasu |
| WEAVING | preplitanje, dužina preplitanja | preplitanje | prepletanje |
| MERGE_DIVERGE | ulivna/izlivna traka, traka za ubrzanje/usporenje | trak za ubrzavanje/usporavanje | pospeševalni/zaviralni pas |
| INTERCHANGE | denivelisana raskrsnica, petlja | denivelirani čvor | izvennivojsko križišče, razcep |

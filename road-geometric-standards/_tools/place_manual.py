#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write/update _result.json for the manually-downloaded standards, and references/README."""
import os, json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader

R = r"D:\My Drive\Nauka\standardi\road-geometric-standards"

def meta(path):
    data = open(path, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    try:
        pages = len(PdfReader(path).pages)
    except Exception as e:
        pages = 0
    return sha, len(data), pages

def write_json(folder, rec, primary_file):
    p = os.path.join(R, folder, primary_file)
    sha, b, pg = meta(p)
    rec["file"] = primary_file; rec["sha256"] = sha; rec["bytes"] = b; rec["pages"] = pg
    out = os.path.join(R, folder, "_result.json")
    json.dump(rec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"  {rec['iso3']:4} {primary_file}  ok pages={pg} sha={sha[:12]}")

# --- SRB ---
write_json("free/SRB_Pravilnik-50-11", {
 "iso3":"SRB","country":"Serbia",
 "standard":"Pravilnik o uslovima koje sa aspekta bezbednosti saobraćaja moraju da ispunjavaju putni objekti i drugi elementi javnog puta (Sl. glasnik RS 50/11)",
 "issuer":"Ministarstvo za infrastrukturu RS","status":"free","result":"retrieved",
 "source_url":"manual download (SSRN id4258153 — kopija Sl. glasnik RS 50/11)",
 "price":"","store_url":"",
 "notes":"Manuelno preuzeto. Pun tekst sa graničnim elementima/tabelama (~143 str.), ćirilica. Kopija sa SSRN; sadržaj = zvanični Pravilnik 50/11 — verifikovati protiv Sl. glasnika RS 50/11. REFERENTNI standard za Fazu 6 (analiza SRB)."
}, "SRB_Pravilnik-50-11_full.pdf")

# --- HRV ---
write_json("free/HRV_NN-110-2001", {
 "iso3":"HRV","country":"Croatia",
 "standard":"Pravilnik o osnovnim uvjetima kojima javne ceste izvan naselja i njihovi elementi moraju udovoljavati sa stajališta sigurnosti prometa (NN 110/2001)",
 "issuer":"Ministarstvo (RH) / Narodne novine","status":"free","result":"retrieved",
 "source_url":"Narodne novine NN 110/2001 (zakon.hr)","price":"","store_url":"",
 "notes":"Manuelno preuzeto. NN 110/2001, jezik hr. Proveriti pretraživost (p1 prazna) — moguće delom skenirano → NEEDS_OCR."
}, "HRV_NN-110-2001_Pravilnik.pdf")

# --- SVN (Slovenia; folder label SLO) ---
write_json("free/SLO_Pravilnik-projektiranje-cest", {
 "iso3":"SVN","country":"Slovenia",
 "standard":"Pravilnik o projektiranju cest (neuradno prečiščeno besedilo)",
 "issuer":"Ministrstvo za infrastrukturo (SI) / Uradni list RS","status":"free","result":"retrieved",
 "source_url":"manual download (NPB; pisrs.si)","price":"","store_url":"",
 "notes":"Manuelno preuzeto. Slovenački Pravilnik o projektiranju cest (NPB). Fajl je stigao kao 'PRAV5811_NPB3.pdf'; jezik sl."
}, "SLO_Pravilnik-o-projektiranju-cest_NPB.pdf")

# --- DEU update (now acquired) ---
deu = json.load(open(os.path.join(R,"paid/DEU_FGSV/_result.json"), encoding="utf-8-sig"))
deu["result"] = "retrieved"
deu["notes"] = ("ACQUIRED (manuelno, licencirana EN izdanja): RAA=FGSV202 (motorways, PRIMARY), "
  "RAL=FGSV201 (rural, 2012/tr2024), RASt=FGSV200 (urban, 2006/tr2012) u folderu. "
  "RStO=FGSV499 (pavement) premešten u references/ (van geometrijskog opsega). "
  "Plaćeno/zaštićeno autorskim pravom — ne redistribuira se (PDF-ovi su gitignored). " + deu.get("notes",""))
sha,b,pg = meta(os.path.join(R,"paid/DEU_FGSV/RAA_FGSV202_Motorways_EN_2008-tr2011.pdf"))
deu["file"]="RAA_FGSV202_Motorways_EN_2008-tr2011.pdf"; deu["sha256"]=sha; deu["bytes"]=b; deu["pages"]=pg
json.dump(deu, open(os.path.join(R,"paid/DEU_FGSV/_result.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"  DEU  updated -> retrieved, primary RAA pages={pg}")

# --- USA update (now acquired) ---
usa = json.load(open(os.path.join(R,"paid/USA_AASHTO-Green-Book/_result.json"), encoding="utf-8-sig"))
usa["result"] = "retrieved"
usa["notes"] = ("ACQUIRED (manuelno, licencirani PDF, 7th ed. 2018). Plaćeno/zaštićeno — ne redistribuira se "
  "(gitignored). " + usa.get("notes",""))
sha,b,pg = meta(os.path.join(R,"paid/USA_AASHTO-Green-Book/AASHTO_Green_Book_7th_2018.pdf"))
usa["file"]="AASHTO_Green_Book_7th_2018.pdf"; usa["sha256"]=sha; usa["bytes"]=b; usa["pages"]=pg
json.dump(usa, open(os.path.join(R,"paid/USA_AASHTO-Green-Book/_result.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"  USA  updated -> retrieved, Green Book pages={pg}")

# --- references README ---
ref = """# references/ — supplementary material (NIJE deo standardnog korpusa)

Ovi fajlovi nisu nacionalni standardi geometrijskog projektovanja, pa se NE računaju u MANIFEST/summary
i ne pretražuju se kao standardi. Čuvaju se kao pomoćna literatura.

| Fajl | Šta je | Zašto van korpusa |
|---|---|---|
| DEU_RStO12_Pavement-Structures_EN_tr2015.pdf | FGSV 499 — RStO 12, standardizacija **kolovoznih konstrukcija** (Translation 2015) | pavement/kolovoz, ne geometrija |
| Maletin_Planiranje-i-projektovanje-saobracajnica-u-gradovima.pdf | Udžbenik (Mihailo Maletin), urbane saobraćajnice | udžbenik, ne standard |

PDF-ovi su gitignored (autorska prava). Ako želiš da skill pretražuje i ove, reci pa ih uključim posebno.
"""
open(os.path.join(R,"references","README.md"),"w",encoding="utf-8").write(ref)
print("  references/README.md written")
print("DONE")

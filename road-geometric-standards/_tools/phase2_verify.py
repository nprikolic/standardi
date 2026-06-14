#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 2 content verification.

For every PDF under free/** and mixed/**: extract text per page (pdftotext -layout),
match the six geometric-design concept categories in the document's language set + English,
and write a per-file _content__<name>.json. Deterministic substring matching (case-insensitive
for Latin; CJK matched as-is). No LLM needed.

Verdict by category coverage (of 6):
  CONFIRMED   - >=4 categories AND at least one of {DESIGN_SPEED, SIGHT_DISTANCE}
  PARTIAL     - 2-3 categories (or >=4 but missing both speed & sight)
  NO_GEOMETRY - <=1 category
  NEEDS_OCR   - image-only scan (extracted text < 200 chars)
"""
import os, sys, json, subprocess, re

ROOT = r"D:\My Drive\Nauka\standardi\road-geometric-standards"

# ---- ISO3 -> language set (always includes 'en') ----
LANGS = {
    "GBR": ["en"], "IRL": ["en"], "AUS": ["en"], "NZL": ["en"], "MWI": ["en"],
    "AFG": ["en"], "MODEL": ["en"],
    "ESP": ["es", "en"], "MEX": ["es", "en"],
    "ITA": ["it", "en"], "SWE": ["sv", "en"], "POL": ["pl", "en"],
    "KOR": ["ko", "en"], "BRA": ["pt", "en"], "FRA": ["fr", "en"],
    "JPN": ["ja", "en"], "CHN": ["zh", "en"],
}

# ---- six categories x multilingual terms (lowercased for Latin; CJK literal) ----
CATS = {
 "DESIGN_SPEED": {
   "en": ["design speed"], "es": ["velocidad de proyecto", "velocidad de diseño"],
   "pt": ["velocidade de projeto", "velocidade diretriz"], "it": ["velocità di progetto"],
   "fr": ["vitesse de référence"], "sv": ["dimensionerande hastighet"],
   "pl": ["prędkość projektowa"], "ko": ["설계속도"], "ja": ["設計速度"], "zh": ["设计速度"],
 },
 "SIGHT_DISTANCE": {
   "en": ["sight distance", "stopping sight"],
   "es": ["distancia de visibilidad", "distancia de parada"],
   "pt": ["distância de visibilidade", "distância de parada"],
   "it": ["distanza di visibilità", "distanza di arresto"],
   "fr": ["distance de visibilité", "distance d'arrêt"],
   "sv": ["stoppsikt", "siktsträcka"],
   "pl": ["odległość widoczności", "widoczność na zatrzymanie"],
   "ko": ["시거", "정지시거"], "ja": ["視距"], "zh": ["视距"],
 },
 "HORIZONTAL": {
   "en": ["horizontal alignment", "curve radius", "transition curve", "clothoid", "spiral"],
   "es": ["alineación", "trazado en planta", "radio", "clotoide"],
   "pt": ["raio", "curva horizontal", "clotoide"],
   "it": ["raggio", "clotoide", "planimetrico"],
   "fr": ["rayon", "clothoïde", "raccordement", "tracé en plan"],
   "sv": ["radie", "klotoid", "horisontalkurva"],
   "pl": ["promień", "łuk poziomy", "krzywa przejściowa", "klotoida"],
   "ko": ["곡선반경", "평면선형", "완화곡선", "클로소이드"],
   "ja": ["曲線半径", "平面線形", "緩和曲線", "クロソイド"],
   "zh": ["曲线半径", "平面线形", "缓和曲线", "回旋线"],
 },
 "VERTICAL": {
   "en": ["vertical alignment", "gradient", "crest curve", "sag curve", "vertical curve"],
   "es": ["rasante", "acuerdo vertical", "pendiente longitudinal"],
   "pt": ["greide", "rampa", "curva vertical"],
   "it": ["livelletta", "pendenza", "raccordo verticale"],
   "fr": ["profil en long", "déclivité", "raccordement vertical"],
   "sv": ["vertikalkurva", "lutning"],
   "pl": ["niweleta", "pochylenie podłużne", "krzywa pionowa"],
   "ko": ["종단선형", "종단곡선", "종단경사"],
   "ja": ["縦断線形", "縦断曲線", "縦断勾配"],
   "zh": ["纵断面", "竖曲线", "纵坡"],
 },
 "SUPERELEVATION": {
   "en": ["superelevation", "cant"], "es": ["peralte"], "pt": ["superelevação"],
   "it": ["sopraelevazione", "pendenza trasversale"], "fr": ["dévers"],
   "sv": ["skevning"], "pl": ["przechyłka"], "ko": ["편경사"], "ja": ["片勾配"], "zh": ["超高"],
 },
 "CROSS_SECTION": {
   "en": ["cross section", "lane width", "carriageway"],
   "es": ["sección transversal", "ancho de carril"],
   "pt": ["seção transversal", "largura da faixa"],
   "it": ["sezione trasversale", "corsia"],
   "fr": ["profil en travers", "largeur de voie"],
   "sv": ["tvärsektion", "körfältsbredd"],
   "pl": ["przekrój poprzeczny", "szerokość pasa"],
   "ko": ["횡단면", "차로폭"], "ja": ["横断面", "車線幅"], "zh": ["横断面", "车道宽"],
 },
}

REFETCH = {
 "GBR": "have CD109; if weak, add related CDs (CD127 cross-sections, CD116 roundabouts)",
 "AUS": "fetch Austroads Guide to Road Design Part 3 (AGRD03, login-gated)",
 "IRL": "TII DN-GEO-03031 (current v12 held)",
 "POL": "WR-D-22-2 geometric part (held)",
 "KOR": "use the Commentary 해설 (held), not the bare rule",
 "ITA": "DM 6792/2001 annex with geometric tables (all_1 held)",
 "ESP": "Norma 3.1-IC full BOE text incl. annex (held)",
 "FRA": "full ICTAAL 2015 / ARP 2022 are paywalled (only corrigendum free)",
 "MEX": "Manual de Proyecto Geometrico 2018 (needs_manual, gov server down)",
 "JPN": "law text only; geometric values live in the paid JRA commentary",
 "CHN": "use the EN JTG D20-2017 (text); Chinese scan is image-only",
}

def pdftotext_pages(path):
    """Return list of per-page text strings (split on form feed)."""
    try:
        out = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", path, "-"],
                             capture_output=True, timeout=600)
    except Exception as e:
        return None, f"pdftotext failed: {e}"
    if out.returncode != 0:
        # retry without -layout
        try:
            out = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"],
                                 capture_output=True, timeout=600)
        except Exception as e:
            return None, f"pdftotext failed: {e}"
    txt = out.stdout.decode("utf-8", "replace")
    pages = txt.split("\f")
    return pages, ""

def match_file(path, iso3):
    langs = LANGS.get(iso3, ["en"])
    pages, err = pdftotext_pages(path)
    rec = {"file": os.path.basename(path), "iso3": iso3, "lang": "+".join(langs),
           "verdict": "", "categories": {}, "categories_hit": 0,
           "pages_total": 0, "notes": "", "refetch_hint": ""}
    if pages is None:
        rec["verdict"] = "NEEDS_OCR"; rec["notes"] = err
        rec["refetch_hint"] = REFETCH.get(iso3, "")
        return rec
    rec["pages_total"] = len([p for p in pages if p is not None])
    # lowercase per page for Latin matching; CJK unaffected by lower()
    low = [p.lower() for p in pages]
    total_chars = sum(len(p.strip()) for p in pages)
    if total_chars < 200:
        rec["verdict"] = "NEEDS_OCR"
        rec["notes"] = f"image-only / no extractable text ({total_chars} chars); tesseract unavailable"
        rec["refetch_hint"] = "OCR needed (no tesseract installed); seek a text-based official edition"
        for c in CATS:
            rec["categories"][c] = {"hit": False, "page": None, "count": 0}
        return rec
    hits = 0
    for cat, langmap in CATS.items():
        terms = []
        for lg in langs:
            terms += langmap.get(lg, [])
        first_page = None; count = 0
        for i, pg in enumerate(low):
            c = 0
            for t in terms:
                c += pg.count(t.lower())
            if c:
                count += c
                if first_page is None:
                    first_page = i + 1
        hit = count > 0
        if hit: hits += 1
        rec["categories"][cat] = {"hit": hit, "page": first_page, "count": count}
    rec["categories_hit"] = hits
    ds = rec["categories"]["DESIGN_SPEED"]["hit"]
    sd = rec["categories"]["SIGHT_DISTANCE"]["hit"]
    if hits >= 4 and (ds or sd):
        rec["verdict"] = "CONFIRMED"
    elif hits >= 4:
        rec["verdict"] = "PARTIAL"
        rec["notes"] = ">=4 categories but neither DESIGN_SPEED nor SIGHT_DISTANCE matched"
        rec["refetch_hint"] = REFETCH.get(iso3, "")
    elif hits >= 2:
        rec["verdict"] = "PARTIAL"
        rec["refetch_hint"] = REFETCH.get(iso3, "")
    else:
        rec["verdict"] = "NO_GEOMETRY"
        rec["refetch_hint"] = REFETCH.get(iso3, "")
    return rec

def iso3_for_folder(folder):
    rp = os.path.join(folder, "_result.json")
    if os.path.exists(rp):
        try:
            with open(rp, encoding="utf-8-sig") as f:
                return json.load(f).get("iso3", "") or "MODEL"
        except Exception:
            pass
    # model-standards subfolders
    return "MODEL"

def main():
    targets = []
    for sub in ("free", "mixed"):
        base = os.path.join(ROOT, sub)
        for dp, _, fs in os.walk(base):
            iso3 = iso3_for_folder(dp)
            for f in fs:
                if f.lower().endswith(".pdf"):
                    targets.append((os.path.join(dp, f), iso3))
    print(f"Verifying {len(targets)} PDFs...")
    for path, iso3 in sorted(targets):
        rec = match_file(path, iso3)
        outp = os.path.join(os.path.dirname(path),
                            "_content__" + os.path.basename(path) + ".json")
        with open(outp, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False)
        print(f"  [{rec['verdict']:11}] {rec['categories_hit']}/6  {os.path.relpath(path, ROOT)}")

if __name__ == "__main__":
    main()

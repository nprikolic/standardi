#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for the Phase-5 benchmark (deterministic, no LLM).

Provides: path resolution, page-text loading, query tokenisation, and the six
retrieval systems under test (S1, S2, S3, S3a, S3b, S3c). S0 has no retrieval.

All retrieval is pure SQLite/FTS5 over corpus/index.sqlite — fully reproducible.
"""
import os, sys, json, re, sqlite3, functools

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))            # .../eval/_tools
EVAL = os.path.dirname(HERE)                                  # .../eval
STANDARDI = os.path.dirname(EVAL)                             # .../standardi
INDEX_DB = os.path.join(STANDARDI, "corpus", "index.sqlite")
GLOSSARY = os.path.join(STANDARDI, "skill", "reference", "glossary.json")
TEXT_DIR = os.path.join(STANDARDI, "corpus", "text")

# --- multilingual stopwords (small; only to keep FTS MATCH queries sane) ------
STOP = set("""
a an the of to in on at for and or is are be by with from as into that this these those
what which how much many value values minimum maximum required require requires standard
koliki kolika koliko je su za na od do iz se sa po u i ili koji koja koje sto što vrednost
der die das und oder ist sind fur für von mit den dem ein eine im am des
el la los las de en y o para con que es son del un una por
le la les des et ou est pour avec dans que un une du
il lo la i gli le di e o per con che un uno una del della
vad vilken hur mycket ar och eller for med av en ett som
co jaki jaka jakie ile dla na od do lub i oraz jest jak wartosc
quanto qual quais para com que e ou um uma do da
""".split())

# Latin-script word characters incl. accented + Slavic + Turkish etc.
_WORD = re.compile(r"[0-9A-Za-zÀ-ɏЀ-ӿĀ-ſ]+", re.U)
_CJK = re.compile(r"[　-鿿가-힯豈-﫿]+")


@functools.lru_cache(maxsize=1)
def _conn():
    if not os.path.exists(INDEX_DB):
        sys.stderr.write(f"index not found: {INDEX_DB}\n")
        sys.exit(1)
    c = sqlite3.connect(INDEX_DB)
    return c


@functools.lru_cache(maxsize=1)
def has_fts():
    c = _conn()
    names = {r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    return "pages_fts" in names


@functools.lru_cache(maxsize=1)
def _glossary():
    with open(GLOSSARY, encoding="utf-8") as f:
        return json.load(f)["concepts"]


def concept_terms(concept, lang=None):
    g = _glossary()
    c = concept.upper()
    if c not in g:
        raise KeyError(f"unknown concept {c}")
    terms = []
    for lg, vals in g[c].items():
        if not isinstance(vals, list):
            continue
        if lang and lg != lang:
            continue
        terms.extend(vals)
    seen, out = set(), []
    for t in terms:
        t = t.strip()
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out


def tokenize(text):
    """Free-text -> list of distinct query tokens (stopwords dropped).
    Keeps Latin/Cyrillic words (len>=3) and any CJK run as a single token."""
    if not text:
        return []
    out, seen = [], set()
    for m in _WORD.findall(text):
        w = m.lower()
        if len(w) < 3 or w in STOP:
            continue
        if w not in seen:
            seen.add(w); out.append(w)
    for m in _CJK.findall(text):
        if m not in seen:
            seen.add(m); out.append(m)
    return out


# --- text loading -------------------------------------------------------------
@functools.lru_cache(maxsize=256)
def _pages_path(doc_id):
    c = _conn()
    row = c.execute("SELECT folder, pdf FROM docs WHERE doc_id=?", (doc_id,)).fetchone()
    if not row:
        return None
    folder, pdf = row
    stem = pdf[:-4] if pdf.lower().endswith(".pdf") else pdf
    return os.path.join(TEXT_DIR, folder, stem + ".pages.jsonl")


@functools.lru_cache(maxsize=4096)
def page_text(doc_id, page):
    """Return the verbatim text of one page, or '' if unavailable."""
    p = _pages_path(doc_id)
    if not p or not os.path.exists(p):
        return ""
    for line in open(p, encoding="utf-8"):
        o = json.loads(line)
        if o.get("page") == page:
            return o.get("text", "")
    return ""


def country_of(doc_id):
    c = _conn()
    row = c.execute("SELECT country FROM docs WHERE doc_id=?", (doc_id,)).fetchone()
    return (row[0] if row and row[0] else "")


# --- FTS / LIKE primitives ----------------------------------------------------
def _fts_match(terms):
    return " OR ".join('"' + t.replace('"', '""') + '"' for t in terms)


def _run_fts(match, iso3, lang, limit):
    c = _conn()
    where = ["pages_fts MATCH ?"]
    params = [match]
    if iso3:
        where.append("iso3 = ?"); params.append(iso3.upper())
    if lang:
        where.append("(lang = ? OR lang LIKE ? OR lang LIKE ? OR lang LIKE ?)")
        params += [lang, lang + ",%", "%," + lang + ",%", "%," + lang]
    sql = (f"SELECT doc_id, iso3, lang, page, bm25(pages_fts) AS rank "
           f"FROM pages_fts WHERE {' AND '.join(where)} ORDER BY rank LIMIT ?")
    params.append(limit)
    return c.execute(sql, params).fetchall()


def _run_like(terms, iso3, lang, limit):
    c = _conn()
    where = ["(" + " OR ".join("text LIKE ?" for _ in terms) + ")"]
    params = [f"%{t}%" for t in terms]
    if iso3:
        where.append("iso3 = ?"); params.append(iso3.upper())
    if lang:
        where.append("(lang = ? OR lang LIKE ? OR lang LIKE ? OR lang LIKE ?)")
        params += [lang, lang + ",%", "%," + lang + ",%", "%," + lang]
    # deterministic order: by doc_id, page (NO relevance ranking — the point of S3c)
    sql = (f"SELECT doc_id, iso3, lang, page, 0 AS rank "
           f"FROM pages_fts WHERE {' AND '.join(where)} ORDER BY doc_id, page LIMIT ?")
    params.append(limit)
    return c.execute(sql, params).fetchall()


def _fts_or_like(terms, limit, label):
    """Try FTS MATCH; on operational error (e.g. CJK phrase) fall back to LIKE.
    Returns (rows, mode_used)."""
    if not terms:
        return [], "empty"
    if has_fts():
        try:
            return _run_fts(_fts_match(terms), None, None, limit), "fts"
        except sqlite3.OperationalError:
            return _run_like(terms, None, None, limit), "like(fallback)"
    return _run_like(terms, None, None, limit), "like"


def _rows_to_hits(rows):
    out = []
    for i, (doc_id, iso3, lang, page, rank) in enumerate(rows, 1):
        out.append({"rank": i, "doc_id": doc_id, "iso3": iso3, "lang": lang,
                    "page": page, "score": round(float(rank), 3)})
    return out


# --- the six retrieval systems ------------------------------------------------
# Each returns dict: {system, query_terms, mode, retrieved:[hit,...]}
def retrieve(system, q, limit=10):
    """q = question dict with keys: concept, question_en, question_local, lang."""
    s = system.upper()
    qen = q.get("question_en", "") or ""
    qloc = q.get("question_local", "") or ""
    concept = q.get("concept")

    if s == "S1":              # naive English keyword BM25
        terms = tokenize(qen)
        rows, mode = _fts_or_like(terms, limit, s)
    elif s == "S2":            # generic RAG: native-language question, no glossary
        terms = tokenize((qloc + " " + qen) if qloc else qen)
        rows, mode = _fts_or_like(terms, limit, s)
    elif s == "S3":            # SKILL: concept -> multilingual glossary terms
        terms = concept_terms(concept)
        rows, mode = _fts_or_like(terms, limit, s)
    elif s == "S3A":           # ablation: concept, English glossary terms only
        terms = concept_terms(concept, lang="en")
        rows, mode = _fts_or_like(terms, limit, s)
    elif s == "S3B":           # ablation: no concept mapping -> free question terms
        terms = tokenize((qen + " " + qloc).strip())
        rows, mode = _fts_or_like(terms, limit, s)
    elif s == "S3C":           # ablation: concept multilingual terms, LIKE (no bm25)
        terms = concept_terms(concept)
        rows = _run_like(terms, None, None, limit)
        mode = "like"
    elif s == "S4":            # principled skill: question terms + glossary expansion
        qterms = tokenize((qen + " " + qloc).strip())
        cterms = concept_terms(concept) if concept else []
        seen, terms = set(), []
        for t in qterms + cterms:        # question terms first, then multilingual synonyms
            if t.lower() not in seen:
                seen.add(t.lower()); terms.append(t)
        rows, mode = _fts_or_like(terms, limit, s)
    elif s == "S1G":           # isolate glossary's cross-lang value: EN question + glossary
        qterms = tokenize(qen)
        cterms = concept_terms(concept) if concept else []
        seen, terms = set(), []
        for t in qterms + cterms:
            if t.lower() not in seen:
                seen.add(t.lower()); terms.append(t)
        rows, mode = _fts_or_like(terms, limit, s)
    else:
        raise ValueError(f"unknown retrieval system {system}")

    return {"system": s, "query_terms": terms, "mode": mode,
            "retrieved": _rows_to_hits(rows)}


RETRIEVAL_SYSTEMS = ["S1", "S2", "S3", "S3a", "S3b", "S3c", "S4", "S1g"]
ALL_SYSTEMS = ["S0"] + RETRIEVAL_SYSTEMS

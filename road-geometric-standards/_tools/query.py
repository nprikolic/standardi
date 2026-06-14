#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query helper over corpus/index.sqlite (built by phase1_preprocess.py).

Examples:
  python query.py --concept DRAINAGE_MIN_GRADE
  python query.py --concept SUPERELEVATION --iso3 DEU
  python query.py --concept DRAINAGE_MIN_GRADE --lang sr
  python query.py "minimum longitudinal gradient"
  python query.py --grep "подужни"          # literal substring (LIKE), bypasses FTS
  python query.py --list-concepts

Builds an FTS5 MATCH OR-query from the multilingual terms of the requested
concept (skill/reference/glossary.json). Prints doc_id / country / page + a
snippet, ranked by bm25, top ~20. Falls back to LIKE if the index has no FTS5.

NOTE: corpus/index.sqlite is gitignored (regenerable). If missing, run
road-geometric-standards/_tools/phase1_preprocess.py first.
"""
import os, sys, json, re, sqlite3, argparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))                 # .../road-geometric-standards/_tools
STANDARDI = os.path.dirname(os.path.dirname(HERE))                # .../standardi
INDEX_DB = os.path.join(STANDARDI, "corpus", "index.sqlite")
GLOSSARY = os.path.join(STANDARDI, "skill", "reference", "glossary.json")


def load_concepts():
    with open(GLOSSARY, encoding="utf-8") as f:
        return json.load(f)["concepts"]


def concept_terms(concept, lang=None):
    """Flat, de-duplicated list of terms for a concept (optionally one lang)."""
    g = load_concepts()
    c = concept.upper()
    if c not in g:
        sys.stderr.write(f"Unknown concept '{c}'. Available: {', '.join(g)}\n")
        sys.exit(2)
    terms = []
    for lg, vals in g[c].items():
        if not isinstance(vals, list):      # skip "_note" etc.
            continue
        if lang and lg != lang:
            continue
        terms.extend(vals)
    # de-dup preserving order
    seen, out = set(), []
    for t in terms:
        t = t.strip()
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out


def fts_phrase(term):
    """Quote a term as an FTS5 phrase; escape embedded double-quotes."""
    return '"' + term.replace('"', '""') + '"'


def build_match(terms):
    """OR-query of quoted phrases for FTS5 MATCH."""
    return " OR ".join(fts_phrase(t) for t in terms)


def has_fts(conn):
    try:
        row = conn.execute("SELECT value FROM meta WHERE key='fts5'").fetchone()
        if row is not None:
            return row[0] == "1"
    except sqlite3.OperationalError:
        pass
    # fall back to table introspection
    names = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    return "pages_fts" in names


def snippet_around(text, terms, width=140):
    """Plain snippet centred on the first matching term (case-insensitive)."""
    low = text.lower()
    pos = -1
    hit = ""
    for t in terms:
        k = low.find(t.lower())
        if k >= 0 and (pos < 0 or k < pos):
            pos, hit = k, t
    if pos < 0:
        s = re.sub(r"\s+", " ", text).strip()
        return s[:width]
    a = max(0, pos - width // 2)
    b = min(len(text), pos + len(hit) + width // 2)
    s = re.sub(r"\s+", " ", text[a:b]).strip()
    return ("…" if a > 0 else "") + s + ("…" if b < len(text) else "")


def run_fts(conn, match, iso3, lang, limit):
    where = ["pages_fts MATCH ?"]
    params = [match]
    if iso3:
        where.append("iso3 = ?")
        params.append(iso3.upper())
    if lang:
        where.append("(lang = ? OR lang LIKE ? OR lang LIKE ? OR lang LIKE ?)")
        params += [lang, lang + ",%", "%," + lang + ",%", "%," + lang]
    sql = (f"SELECT doc_id, iso3, lang, page, text, bm25(pages_fts) AS rank "
           f"FROM pages_fts WHERE {' AND '.join(where)} "
           f"ORDER BY rank LIMIT ?")
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def run_like(conn, terms, iso3, lang, limit, table="pages"):
    """Literal substring (LIKE) search. Works against either the plain `pages`
    table (no-FTS index) or the `pages_fts` virtual table (FTS index + --grep)."""
    where = ["(" + " OR ".join("text LIKE ?" for _ in terms) + ")"]
    params = [f"%{t}%" for t in terms]
    if iso3:
        where.append("iso3 = ?")
        params.append(iso3.upper())
    if lang:
        where.append("(lang = ? OR lang LIKE ? OR lang LIKE ? OR lang LIKE ?)")
        params += [lang, lang + ",%", "%," + lang + ",%", "%," + lang]
    sql = (f"SELECT doc_id, iso3, lang, page, text, 0 AS rank "
           f"FROM {table} WHERE {' AND '.join(where)} LIMIT ?")
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def country_of(conn, doc_id, cache):
    if doc_id not in cache:
        row = conn.execute("SELECT country FROM docs WHERE doc_id=?", (doc_id,)).fetchone()
        cache[doc_id] = (row[0] if row and row[0] else "")
    return cache[doc_id]


def main():
    ap = argparse.ArgumentParser(description="Query corpus/index.sqlite")
    ap.add_argument("query", nargs="?", help="free-text query (FTS MATCH)")
    ap.add_argument("--concept", help="glossary concept, e.g. DRAINAGE_MIN_GRADE")
    ap.add_argument("--grep", help="literal substring search (LIKE), bypasses FTS")
    ap.add_argument("--iso3", help="filter by ISO3, e.g. DEU")
    ap.add_argument("--lang", help="filter by language tag, e.g. de")
    ap.add_argument("--limit", type=int, default=20, help="max hits (default 20)")
    ap.add_argument("--list-concepts", action="store_true")
    a = ap.parse_args()

    if a.list_concepts:
        print("Concepts:", ", ".join(load_concepts().keys()))
        return

    if not os.path.exists(INDEX_DB):
        sys.stderr.write(f"index not found: {INDEX_DB}\nRun _tools/phase1_preprocess.py first.\n")
        sys.exit(1)

    conn = sqlite3.connect(INDEX_DB)
    fts = has_fts(conn)

    # Resolve terms / mode
    if a.concept:
        terms = concept_terms(a.concept, a.lang)
        label = f"concept {a.concept.upper()}" + (f" lang={a.lang}" if a.lang else "")
        use_like = a.grep is not None  # concept never uses grep
    elif a.grep:
        terms = [a.grep]
        label = f"grep '{a.grep}'"
        use_like = True
    elif a.query:
        terms = [a.query]
        label = f"text '{a.query}'"
        use_like = False
    else:
        ap.print_help()
        return

    if not terms:
        print("(no terms for this concept/lang)")
        return

    flt = []
    if a.iso3:
        flt.append(f"iso3={a.iso3.upper()}")
    if a.lang:
        flt.append(f"lang={a.lang}")
    print(f"# {label}  | index={'FTS5' if fts else 'LIKE'}"
          + (f"  | {' '.join(flt)}" if flt else "")
          + f"  | terms={len(terms)}  | top {a.limit}\n")

    if fts and not use_like:
        match = build_match(terms)
        try:
            results = run_fts(conn, match, a.iso3, a.lang, a.limit)
        except sqlite3.OperationalError as e:
            sys.stderr.write(f"FTS query error ({e}); falling back to LIKE.\n")
            results = run_like(conn, terms, a.iso3, a.lang, a.limit, table="pages_fts")
    else:
        # LIKE path: --grep on an FTS index queries pages_fts; otherwise the
        # plain `pages` table from a no-FTS build.
        like_table = "pages_fts" if fts else "pages"
        if not fts and conn.execute(
                "SELECT name FROM sqlite_master WHERE name='pages'").fetchone() is None:
            sys.stderr.write("No 'pages' table for LIKE search.\n")
            sys.exit(1)
        results = run_like(conn, terms, a.iso3, a.lang, a.limit, table=like_table)

    if not results:
        print("(no hits)")
        return

    ccache = {}
    for i, (doc_id, iso3, lang, page, text, rank) in enumerate(results, 1):
        country = country_of(conn, doc_id, ccache)
        snip = snippet_around(text, terms)
        rk = f"  bm25={rank:.2f}" if fts and not use_like else ""
        print(f"{i:>2}. [{iso3}] {country}  p.{page}  — {doc_id}{rk}")
        print(f"    …{snip}")
    print(f"\n# {len(results)} hit(s)")
    conn.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PHASE 1 PREPROCESSING — build the searchable text layer for the road
geometric-design standards corpus.

For every PDF under free/ mixed/ paid/ (one folder per item, each with a
_result.json):
  - extract text with `pdftotext -layout -enc UTF-8 <pdf> -`, split pages on \f
  - store ORIGINAL text (no lowercasing) to corpus/text/<folder>/<base>.pages.jsonl
  - build corpus/index.sqlite (docs + FTS5 pages_fts, LIKE fallback if no FTS5)
  - flag needs_ocr (>70% of pages <15 chars), cross-checked vs content_summary
  - write corpus/PREPROCESS_REPORT.md (COUNTS ONLY)

Idempotent: drops+recreates the index, overwrites jsonl on every run.
All generated text/index goes under corpus/ (gitignored). PDFs are never modified.

Usage:  python phase1_preprocess.py
"""
import os, sys, json, glob, shutil, subprocess, sqlite3, time

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))                 # .../road-geometric-standards/_tools
RGS = os.path.dirname(HERE)                                       # .../road-geometric-standards
STANDARDI = os.path.dirname(RGS)                                  # .../standardi
CORPUS = os.path.join(STANDARDI, "corpus")                        # .../standardi/corpus  (GITIGNORED)
TEXT_DIR = os.path.join(CORPUS, "text")
INDEX_DB = os.path.join(CORPUS, "index.sqlite")
REPORT_MD = os.path.join(CORPUS, "PREPROCESS_REPORT.md")
CONTENT_SUMMARY = os.path.join(RGS, "content_summary.json")

SUBSETS = ("free", "mixed", "paid")

# ---------------------------------------------------------------------------
# ISO3 -> language set (copied from _tools/phase2_verify.py; 'en' always added).
# MODEL / unknown -> ['en'].
# ---------------------------------------------------------------------------
LANGS = {
    "GBR": ["en"], "IRL": ["en"], "AUS": ["en"], "NZL": ["en"], "MWI": ["en"],
    "AFG": ["en"], "MODEL": ["en"], "CAN": ["en"], "IND": ["en"], "NLD": ["en"],
    "ZAF": ["en"], "USA": ["en"],
    "ESP": ["es", "en"], "MEX": ["es", "en"],
    "ITA": ["it", "en"], "SWE": ["sv", "en"], "POL": ["pl", "en"],
    "KOR": ["ko", "en"], "BRA": ["pt", "en"], "FRA": ["fr", "en"],
    "JPN": ["ja", "en"], "CHN": ["zh", "en"],
    "SRB": ["sr", "en"], "HRV": ["hr", "en"], "SVN": ["sl", "en"], "DEU": ["de", "en"],
}

def langs_for(iso3):
    return LANGS.get((iso3 or "").upper(), ["en"])

# ---------------------------------------------------------------------------
# Locate a Poppler (or compatible) pdftotext that supports -layout / -enc.
# On this Windows box the MiKTeX-bundled binary is Poppler 24.04; the mingw64
# one is an ancient xpdf 4.00. We prefer a binary that advertises Poppler.
# ---------------------------------------------------------------------------
def find_pdftotext():
    candidates = []
    env = os.environ.get("PDFTOTEXT")
    if env:
        candidates.append(env)
    # Known-good Poppler 24.04 on this machine
    candidates.append(
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdftotext.exe")
    )
    # Anything on PATH
    found = shutil.which("pdftotext")
    if found:
        candidates.append(found)
    # de-dup, keep order
    seen, ordered = set(), []
    for c in candidates:
        if c and c not in seen and os.path.exists(c):
            seen.add(c)
            ordered.append(c)
    # Prefer a binary whose -v mentions poppler; else first that runs.
    fallback = None
    for c in ordered:
        try:
            r = subprocess.run([c, "-v"], capture_output=True, timeout=30)
            ver = (r.stdout + r.stderr).decode("utf-8", "replace").lower()
            if fallback is None:
                fallback = c
            if "poppler" in ver:
                return c, ver.splitlines()[0].strip()
        except Exception:
            continue
    if fallback:
        return fallback, "(non-poppler / unverified)"
    raise RuntimeError("pdftotext not found on PATH or known locations")

PDFTOTEXT, PDFTOTEXT_VER = find_pdftotext()

# ---------------------------------------------------------------------------
# Corpus discovery
# ---------------------------------------------------------------------------
def read_result_json(folder):
    rp = os.path.join(folder, "_result.json")
    if os.path.exists(rp):
        try:
            return json.load(open(rp, encoding="utf-8-sig"))
        except Exception as e:
            sys.stderr.write(f"  ! bad _result.json in {folder}: {e}\n")
    return {}

def discover_docs():
    """Yield dicts: folder, folder_rel, subset, iso3, country, status, result, pdf."""
    docs = []
    for sub in SUBSETS:
        base = os.path.join(RGS, sub)
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            folder = os.path.join(base, entry)
            if not os.path.isdir(folder):
                continue
            meta = read_result_json(folder)
            iso3 = (meta.get("iso3") or "MODEL").upper()
            pdfs = sorted(p for p in glob.glob(os.path.join(folder, "*"))
                          if p.lower().endswith(".pdf"))
            for pdf in pdfs:
                docs.append({
                    "folder": folder,
                    "folder_rel": entry,
                    "subset": sub,
                    "iso3": iso3,
                    "country": meta.get("country") or "",
                    "status": meta.get("status") or sub,
                    "result": meta.get("result") or "",
                    "pdf": pdf,
                })
    return docs

# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------
def extract_pages(pdf):
    """Run pdftotext -layout -enc UTF-8; return (pages:list[str], err:str|None)."""
    try:
        r = subprocess.run(
            [PDFTOTEXT, "-layout", "-enc", "UTF-8", pdf, "-"],
            capture_output=True, timeout=900,
        )
    except Exception as e:
        return None, f"pdftotext exception: {e}"
    if r.returncode != 0:
        msg = r.stderr.decode("utf-8", "replace").strip().replace("\n", " ")
        # Poppler often returns text on stdout even with a nonzero code (warnings);
        # only treat as failure when there is no usable stdout.
        if not r.stdout:
            return None, f"pdftotext rc={r.returncode}: {msg[:200]}"
    txt = r.stdout.decode("utf-8", "replace")
    pages = txt.split("\f")
    # pdftotext appends a trailing \f after the last page -> drop empty tail
    if pages and pages[-1] == "":
        pages.pop()
    return pages, None

# ---------------------------------------------------------------------------
# SQLite index
# ---------------------------------------------------------------------------
def fts5_available(conn):
    try:
        conn.execute("CREATE VIRTUAL TABLE _fts_probe USING fts5(x)")
        conn.execute("DROP TABLE _fts_probe")
        return True
    except sqlite3.OperationalError:
        return False

def build_index_schema(conn, use_fts):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS docs")
    cur.execute("DROP TABLE IF EXISTS pages_fts")
    cur.execute("DROP TABLE IF EXISTS pages")
    cur.execute("DROP TABLE IF EXISTS meta")
    cur.execute("""
        CREATE TABLE docs(
            doc_id TEXT PRIMARY KEY,
            iso3    TEXT,
            country TEXT,
            lang    TEXT,
            folder  TEXT,
            pdf     TEXT,
            pages   INTEGER,
            status  TEXT,
            result  TEXT
        )""")
    if use_fts:
        cur.execute("""
            CREATE VIRTUAL TABLE pages_fts USING fts5(
                text,
                doc_id UNINDEXED,
                iso3   UNINDEXED,
                lang   UNINDEXED,
                page   UNINDEXED
            )""")
    else:
        cur.execute("""
            CREATE TABLE pages(
                text   TEXT,
                doc_id TEXT,
                iso3   TEXT,
                lang   TEXT,
                page   INTEGER
            )""")
        cur.execute("CREATE INDEX ix_pages_doc ON pages(doc_id)")
    cur.execute("CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    print(f"# phase1_preprocess — corpus={CORPUS}")
    print(f"# pdftotext: {PDFTOTEXT}  [{PDFTOTEXT_VER}]")

    os.makedirs(TEXT_DIR, exist_ok=True)

    # NEEDS_OCR cross-check list (by filename) from content_summary.json
    summary_ocr = set()
    try:
        cs = json.load(open(CONTENT_SUMMARY, encoding="utf-8-sig"))
        for e in cs.get("non_confirmed", []):
            if e.get("verdict") == "NEEDS_OCR" and e.get("file"):
                summary_ocr.add(e["file"])
    except Exception as e:
        sys.stderr.write(f"  ! could not read content_summary.json: {e}\n")

    docs = discover_docs()
    print(f"# discovered {len(docs)} PDF(s) under {'/'.join(SUBSETS)}\n")

    # Idempotent: rebuild index from scratch.
    if os.path.exists(INDEX_DB):
        os.remove(INDEX_DB)
    conn = sqlite3.connect(INDEX_DB)
    use_fts = fts5_available(conn)
    build_index_schema(conn, use_fts)
    print(f"# FTS5: {'YES' if use_fts else 'NO (fallback to pages + LIKE)'}\n")
    cur = conn.cursor()

    rows = []           # per-doc report rows
    failures = []       # (doc_id, err)
    needs_ocr_docs = [] # doc_ids
    total_pages = 0
    total_chars = 0
    index_rows = 0
    seen_ids = set()

    for d in docs:
        base = os.path.basename(d["pdf"])
        pdf_base_noext = os.path.splitext(base)[0]
        doc_id = f"{d['folder_rel']}::{pdf_base_noext}"
        # guard against duplicate doc_id (shouldn't happen, but stay safe)
        if doc_id in seen_ids:
            n = 2
            while f"{doc_id}#{n}" in seen_ids:
                n += 1
            doc_id = f"{doc_id}#{n}"
        seen_ids.add(doc_id)

        lang = ",".join(langs_for(d["iso3"]))

        pages, err = extract_pages(d["pdf"])
        if pages is None:
            print(f"  ! FAIL {doc_id}: {err}")
            failures.append((doc_id, err))
            # still record the doc with 0 pages so the corpus is complete
            cur.execute(
                "INSERT INTO docs VALUES (?,?,?,?,?,?,?,?,?)",
                (doc_id, d["iso3"], d["country"], lang, d["folder_rel"], base,
                 0, d["status"], d["result"]),
            )
            continue

        # Write per-PDF jsonl (overwrite).
        out_dir = os.path.join(TEXT_DIR, d["folder_rel"])
        os.makedirs(out_dir, exist_ok=True)
        out_jsonl = os.path.join(out_dir, pdf_base_noext + ".pages.jsonl")
        doc_chars = 0
        short_pages = 0
        npages = len(pages)
        with open(out_jsonl, "w", encoding="utf-8") as fh:
            for i, pg in enumerate(pages, start=1):
                chars = len(pg)
                doc_chars += chars
                if chars < 15:
                    short_pages += 1
                fh.write(json.dumps(
                    {"page": i, "chars": chars, "text": pg},
                    ensure_ascii=False) + "\n")
                # index row
                if use_fts:
                    cur.execute(
                        "INSERT INTO pages_fts(text, doc_id, iso3, lang, page) VALUES (?,?,?,?,?)",
                        (pg, doc_id, d["iso3"], lang, i))
                else:
                    cur.execute(
                        "INSERT INTO pages(text, doc_id, iso3, lang, page) VALUES (?,?,?,?,?)",
                        (pg, doc_id, d["iso3"], lang, i))
                index_rows += 1

        # needs_ocr: >70% of pages have <15 chars
        needs_ocr = (npages > 0 and (short_pages / npages) > 0.70)
        if needs_ocr:
            needs_ocr_docs.append(doc_id)

        cur.execute(
            "INSERT INTO docs VALUES (?,?,?,?,?,?,?,?,?)",
            (doc_id, d["iso3"], d["country"], lang, d["folder_rel"], base,
             npages, d["status"], d["result"]),
        )

        total_pages += npages
        total_chars += doc_chars
        rows.append({
            "doc_id": doc_id, "iso3": d["iso3"], "lang": lang,
            "pages": npages, "chars": doc_chars, "needs_ocr": needs_ocr,
            "pdf": base,
        })
        flag = "  [needs_ocr]" if needs_ocr else ""
        print(f"  ok {doc_id:<48} {d['iso3']:<4} p={npages:<4} chars={doc_chars:>9}{flag}")

    # store run metadata
    cur.execute("INSERT INTO meta VALUES ('fts5', ?)", ("1" if use_fts else "0",))
    cur.execute("INSERT INTO meta VALUES ('pdftotext', ?)", (PDFTOTEXT,))
    cur.execute("INSERT INTO meta VALUES ('built', ?)", (time.strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()

    # cross-check vs content_summary NEEDS_OCR
    ocr_basenames = {r["pdf"] for r in rows if r["needs_ocr"]}
    cross_match = sorted(summary_ocr & ocr_basenames)
    cross_only_summary = sorted(summary_ocr - {r["pdf"] for r in rows})
    cross_only_ours = sorted(ocr_basenames - summary_ocr)

    write_report(rows, failures, needs_ocr_docs, total_pages, total_chars,
                 index_rows, use_fts, summary_ocr, cross_match,
                 cross_only_summary, cross_only_ours)

    conn.close()
    dt = time.time() - t0
    print(f"\n# DONE  docs={len(rows)}  pages={total_pages}  chars={total_chars}  "
          f"index_rows={index_rows}  fts5={use_fts}  failures={len(failures)}  "
          f"needs_ocr={len(needs_ocr_docs)}  ({dt:.1f}s)")
    print(f"# index : {INDEX_DB}")
    print(f"# text  : {TEXT_DIR}")
    print(f"# report: {REPORT_MD}")


def write_report(rows, failures, needs_ocr_docs, total_pages, total_chars,
                 index_rows, use_fts, summary_ocr, cross_match,
                 cross_only_summary, cross_only_ours):
    lines = []
    lines.append("# Phase 1 Preprocessing Report")
    lines.append("")
    lines.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')} — COUNTS ONLY (no extracted text)._")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Documents (PDFs): **{len(rows)}**")
    lines.append(f"- Total pages: **{total_pages}**")
    lines.append(f"- Total characters: **{total_chars:,}**")
    lines.append(f"- Index rows (page records): **{index_rows}**")
    lines.append(f"- FTS5 enabled: **{'yes' if use_fts else 'no (LIKE fallback)'}**")
    lines.append(f"- Extraction failures: **{len(failures)}**")
    lines.append(f"- needs_ocr documents: **{len(needs_ocr_docs)}**")
    lines.append("")

    lines.append("## Per-document")
    lines.append("")
    lines.append("| iso3 | lang | pages | chars | needs_ocr | doc_id |")
    lines.append("|------|------|------:|------:|:---------:|--------|")
    for r in sorted(rows, key=lambda x: (x["iso3"], x["doc_id"])):
        lines.append(f"| {r['iso3']} | {r['lang']} | {r['pages']} | {r['chars']:,} | "
                     f"{'YES' if r['needs_ocr'] else ''} | {r['doc_id']} |")
    lines.append("")

    if failures:
        lines.append("## Extraction failures")
        lines.append("")
        for doc_id, err in failures:
            lines.append(f"- `{doc_id}` — {err}")
        lines.append("")

    lines.append("## needs_ocr documents")
    lines.append("")
    if needs_ocr_docs:
        for d in needs_ocr_docs:
            lines.append(f"- `{d}`")
    else:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Cross-check vs content_summary.json NEEDS_OCR")
    lines.append("")
    lines.append(f"- content_summary NEEDS_OCR files: {sorted(summary_ocr) if summary_ocr else '(none)'}")
    lines.append(f"- matched (both flag): {cross_match if cross_match else '(none)'}")
    lines.append(f"- flagged by summary but not by us: {cross_only_summary if cross_only_summary else '(none)'}")
    lines.append(f"- flagged by us but not by summary: {cross_only_ours if cross_only_ours else '(none)'}")
    lines.append("")

    lines.append("## OCR status")
    lines.append("")
    if shutil.which("tesseract"):
        lines.append("- tesseract: present (OCR may be run by a separate step).")
    else:
        lines.append("- tesseract: **NOT on PATH** — image-only PDFs are listed as **pending-OCR** "
                     "(no install performed).")
        if needs_ocr_docs:
            lines.append("- Pending-OCR documents:")
            for d in needs_ocr_docs:
                lines.append(f"  - `{d}`")
    lines.append("")

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()

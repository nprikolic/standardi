#!/usr/bin/env python3
"""Validate a downloaded standards PDF.

Usage: python validate_pdf.py <path-to-file>
Prints a JSON object to stdout:
  { "ok": bool, "is_pdf": bool, "bytes": int, "pages": int|null,
    "sha256": "", "reason": "" }

A file is considered a valid PDF download when:
  - first bytes are the %PDF magic header
  - size > 50 KB (51200 bytes)
  - page count is readable and >= 1
Anything else (HTML landing page, login wall, 0-byte file, truncated) -> ok=false.
"""
import sys, json, hashlib

def main(path):
    out = {"ok": False, "is_pdf": False, "bytes": 0, "pages": None,
           "sha256": "", "reason": ""}
    try:
        with open(path, "rb") as f:
            data = f.read()
    except Exception as e:
        out["reason"] = f"cannot read file: {e}"
        print(json.dumps(out)); return

    out["bytes"] = len(data)
    out["sha256"] = hashlib.sha256(data).hexdigest()

    head = data[:1024].lstrip()
    out["is_pdf"] = head[:5] == b"%PDF-"
    if not out["is_pdf"]:
        # surface what it actually looks like, to spot HTML/login walls
        sniff = head[:120].decode("latin-1", "replace").replace("\n", " ")
        out["reason"] = f"not a PDF (no %PDF header); starts: {sniff!r}"
        print(json.dumps(out)); return

    if out["bytes"] <= 51200:
        out["reason"] = f"too small ({out['bytes']} bytes <= 50 KB)"
        print(json.dumps(out)); return

    try:
        from pypdf import PdfReader
        r = PdfReader(path)
        out["pages"] = len(r.pages)
    except Exception as e:
        out["reason"] = f"PDF header present but unreadable: {e}"
        print(json.dumps(out)); return

    if not out["pages"] or out["pages"] < 1:
        out["reason"] = "no readable pages"
        print(json.dumps(out)); return

    out["ok"] = True
    out["reason"] = "valid pdf"
    print(json.dumps(out))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"ok": False, "reason": "usage: validate_pdf.py <file>"}))
        sys.exit(2)
    main(sys.argv[1])

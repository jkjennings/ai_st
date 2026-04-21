#!/usr/bin/env python3
"""
Generic PDF text extractor — no book registry, no game logic.
Outputs page_0001.txt ... page_NNNN.txt to output_dir.
Exits 0 with JSON summary: {"pages": N, "output_dir": "...", "skipped": N}

Usage:
    python3 extract_pdf_text.py <pdf_path> <output_dir> [--verbose]
"""
import sys
import json
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print(json.dumps({"error": "PyMuPDF not installed. Run: pip install pymupdf"}))
    sys.exit(1)

# Reuse column detection and text extraction from the existing extractor
sys.path.insert(0, str(Path(__file__).parent))
from extract_wod_pdfs import detect_columns, extract_page_text


def extract_pdf_generic(pdf_path: str, output_dir: str, verbose: bool = False) -> dict:
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    pages_written = 0
    skipped = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        two_col = detect_columns(page)
        text = extract_page_text(page, two_column=two_col)

        if not text.strip():
            skipped += 1
            continue

        out_file = output_dir / f"page_{page_num + 1:04d}.txt"
        out_file.write_text(text, encoding="utf-8")
        pages_written += 1

        if verbose:
            print(f"  page {page_num + 1:4d} → {out_file.name} ({'2col' if two_col else '1col'})")

    doc.close()

    return {"pages": pages_written, "output_dir": str(output_dir), "skipped": skipped}


def main():
    parser = argparse.ArgumentParser(description="Extract PDF pages to text files")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("output_dir", help="Directory to write page_NNNN.txt files")
    parser.add_argument("--verbose", action="store_true", help="Print per-page progress")
    args = parser.parse_args()

    if not Path(args.pdf_path).exists():
        print(json.dumps({"error": f"File not found: {args.pdf_path}"}))
        sys.exit(1)

    result = extract_pdf_generic(args.pdf_path, args.output_dir, verbose=args.verbose)
    print(json.dumps(result))


if __name__ == "__main__":
    main()

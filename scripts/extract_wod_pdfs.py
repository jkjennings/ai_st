#!/usr/bin/env python3
"""
WoD20 PDF Extractor — Extracts text from World of Darkness 20th Anniversary PDFs.

Usage:
  python3 extract_wod_pdfs.py <pdf_path_or_directory> [--game v20|w20|m20|c20|dav20|wr20]

Outputs raw text files to:
  raw_text/[game]/[book_slug]/page_NNNN.txt

Each page file also has metadata in a header comment.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Book registry: maps filename patterns to metadata
# ---------------------------------------------------------------------------
BOOK_REGISTRY = {
    # V20 — Vampire: The Masquerade
    "V20 Vampire the Masquerade - 20th Anniversary Edition": {
        "game": "v20", "code": "v20_core", "type": "core",
        "priority": 1,
        "key_sections": ["character creation", "clans", "disciplines",
                         "merits and flaws", "combat", "the kindred condition"],
    },
    "V20 Lore of the Clans": {
        "game": "v20", "code": "v20_lotc", "type": "supplement",
        "priority": 2,
        "key_sections": ["brujah", "gangrel", "malkavian", "nosferatu", "toreador",
                         "tremere", "ventrue", "assamite", "followers of set",
                         "giovanni", "lasombra", "ravnos", "tzimisce"],
    },
    "V20 Lore of the Bloodlines": {
        "game": "v20", "code": "v20_lotbl", "type": "supplement",
        "priority": 3,
        "key_sections": ["bloodlines"],
    },
    "V20 Companion": {
        "game": "v20", "code": "v20_companion", "type": "supplement",
        "priority": 4,
        "key_sections": ["merits", "flaws", "backgrounds", "disciplines"],
    },
    "V20 Rites of the Blood": {
        "game": "v20", "code": "v20_rotb", "type": "supplement",
        "priority": 5,
        "key_sections": ["thaumaturgy", "necromancy", "rituals", "paths"],
    },
    "V20 Ghouls and Revnants": {
        "game": "v20", "code": "v20_ghouls", "type": "supplement",
        "priority": 6,
        "key_sections": ["ghouls", "revenants", "disciplines"],
    },
    "V20 Anarchs Unbound 20th Anniversary": {
        "game": "v20", "code": "v20_anarchs", "type": "supplement",
        "priority": 7,
        "key_sections": ["anarchs", "disciplines", "merits", "backgrounds"],
    },
    "V20 Becketts Jyhad Diary": {
        "game": "v20", "code": "v20_bjd", "type": "sourcebook",
        "priority": 8,
        "key_sections": ["clans", "npcs", "setting"],
    },
    "V20 Children of the Revolution": {
        "game": "v20", "code": "v20_cotr", "type": "supplement",
        "priority": 9,
        "key_sections": ["characters", "disciplines"],
    },
    "V20 Dread Names Red List": {
        "game": "v20", "code": "v20_dnrl", "type": "supplement",
        "priority": 10,
        "key_sections": ["antagonists", "disciplines"],
    },
    "V20 Dust to Dust": {
        "game": "v20", "code": "v20_dtd", "type": "adventure",
        "priority": 11,
        "key_sections": ["setting", "npcs"],
    },
    "V20 Ready Made Characters": {
        "game": "v20", "code": "v20_rmc", "type": "supplement",
        "priority": 12,
        "key_sections": ["characters"],
    },
    "V20 The Black Hand A Guide to the TalMaheRa": {
        "game": "v20", "code": "v20_blackhand", "type": "supplement",
        "priority": 13,
        "key_sections": ["tal'mahe'ra", "disciplines", "merits", "backgrounds"],
    },
    "V20 The Hunters Hunted II": {
        "game": "v20", "code": "v20_hh2", "type": "supplement",
        "priority": 14,
        "key_sections": ["hunters", "merits", "flaws"],
    },
    # Dark Ages V20
    "DAV20 20th Anniversary Edition Vampire Dark Ages": {
        "game": "dav20", "code": "dav20_core", "type": "core",
        "priority": 1,
        "key_sections": ["character creation", "clans", "disciplines", "roads"],
    },
    "DAV20 Dark Ages Companion": {
        "game": "dav20", "code": "dav20_companion", "type": "supplement",
        "priority": 2,
        "key_sections": ["disciplines", "merits", "flaws"],
    },
    "DAV20 Dark Ages Darkening Sky": {
        "game": "dav20", "code": "dav20_sky", "type": "supplement",
        "priority": 3,
        "key_sections": [],
    },
    "DAV20 Dark Ages Tome of Secrets": {
        "game": "dav20", "code": "dav20_tos", "type": "supplement",
        "priority": 4,
        "key_sections": ["rituals", "disciplines"],
    },
    "DAV20 Legacy of Lies": {
        "game": "dav20", "code": "dav20_lol", "type": "adventure",
        "priority": 5,
        "key_sections": [],
    },
    # W20 — Werewolf: The Apocalypse
    "W20 - Werewolf the Apocalypse 20th Anniversary Edition": {
        "game": "w20", "code": "w20_core", "type": "core",
        "priority": 1,
        "key_sections": ["character creation", "tribes", "gifts", "rites",
                         "combat", "the garou condition"],
    },
    "W20 - Changing Breeds": {
        "game": "w20", "code": "w20_cb", "type": "supplement",
        "priority": 2,
        "key_sections": ["changing breeds", "gifts"],
    },
    "W20 - Book of the Wyrm": {
        "game": "w20", "code": "w20_botw", "type": "supplement",
        "priority": 3,
        "key_sections": ["fomori", "disciplines", "gifts"],
    },
    "W20 - Changing Ways": {
        "game": "w20", "code": "w20_cw", "type": "supplement",
        "priority": 4,
        "key_sections": ["gifts", "rites", "tribes"],
    },
    "W20 - Kinfolk": {
        "game": "w20", "code": "w20_kinfolk", "type": "supplement",
        "priority": 5,
        "key_sections": ["kinfolk", "merits", "flaws", "gifts"],
    },
    "W20 - Rage Across the World": {
        "game": "w20", "code": "w20_ratw2", "type": "supplement",
        "priority": 6,
        "key_sections": ["setting", "gifts", "rites"],
    },
    "W20 - Rage Across - The World (Vol I)": {
        "game": "w20", "code": "w20_ratw1", "type": "supplement",
        "priority": 7,
        "key_sections": ["setting", "gifts"],
    },
    "W20 - Shattered Dreams": {
        "game": "w20", "code": "w20_sd", "type": "supplement",
        "priority": 8,
        "key_sections": ["setting", "gifts", "antagonists"],
    },
    "W20 - Tribebook White Howlers": {
        "game": "w20", "code": "w20_wh", "type": "supplement",
        "priority": 9,
        "key_sections": ["white howlers", "gifts", "rites"],
    },
    "W20 - Umbra The Velvet Shadow": {
        "game": "w20", "code": "w20_umbra", "type": "supplement",
        "priority": 10,
        "key_sections": ["umbra", "spirits", "realms"],
    },
    "W20 - Wyld West Expansion Pack": {
        "game": "w20", "code": "w20_ww", "type": "supplement",
        "priority": 11,
        "key_sections": ["setting", "gifts"],
    },
    "W20 Pentex Employee Indoctrination Manual": {
        "game": "w20", "code": "w20_pentex", "type": "supplement",
        "priority": 12,
        "key_sections": ["pentex", "fomori", "setting"],
    },
    "W20 Skinner": {
        "game": "w20", "code": "w20_skinner", "type": "adventure",
        "priority": 13,
        "key_sections": [],
    },
    "W20_Apocalyptic_Record_(Final_Download)": {
        "game": "w20", "code": "w20_apoc", "type": "supplement",
        "priority": 14,
        "key_sections": ["setting", "metaplot"],
    },
    # M20 — Mage: The Ascension
    "M20 - Mage the Ascension 20th Anniversary Edition": {
        "game": "m20", "code": "m20_core", "type": "core",
        "priority": 1,
        "key_sections": ["character creation", "traditions", "spheres",
                         "magick", "paradox", "combat"],
    },
    "M20 Gods & Monsters": {
        "game": "m20", "code": "m20_gm", "type": "supplement",
        "priority": 2,
        "key_sections": ["antagonists", "spirits", "demons"],
    },
    "M20 The Book of Secrets": {
        "game": "m20", "code": "m20_bos", "type": "supplement",
        "priority": 3,
        "key_sections": ["merits", "flaws", "backgrounds", "spheres", "rotes"],
    },
    "M20_Faces_of_Magick_(Final_Download)": {
        "game": "m20", "code": "m20_fom", "type": "supplement",
        "priority": 4,
        "key_sections": ["characters", "traditions"],
    },
    "M20_Forbidden_and_Forgotten_Orders_(Download)": {
        "game": "m20", "code": "m20_ffo", "type": "supplement",
        "priority": 5,
        "key_sections": ["traditions", "conventions", "spheres"],
    },
    "M20_Sorcerer_(Download)": {
        "game": "m20", "code": "m20_sorc", "type": "supplement",
        "priority": 6,
        "key_sections": ["sorcerers", "psychics", "linear magic"],
    },
    "M20 - Lore_of_the_Traditions_(Download)": {
        "game": "m20", "code": "m20_lott", "type": "supplement",
        "priority": 7,
        "key_sections": ["traditions", "spheres", "rotes", "merits", "flaws"],
    },
    # C20 — Changeling: The Dreaming
    "C20 - Changeling The Dreaming 20th Anniversary Edition": {
        "game": "c20", "code": "c20_core", "type": "core",
        "priority": 1,
        "key_sections": ["character creation", "kiths", "arts", "realms"],
    },
    "C20 - Book of Freeholds": {
        "game": "c20", "code": "c20_bof", "type": "supplement",
        "priority": 2,
        "key_sections": ["freeholds", "trods", "setting"],
    },
    "C20 Players Guide": {
        "game": "c20", "code": "c20_pg", "type": "supplement",
        "priority": 3,
        "key_sections": ["kiths", "arts", "realms", "merits", "flaws"],
    },
    # WR20 — Wraith: The Oblivion
    "WR20 Wraith The Oblivion 20th Anniversary Edition": {
        "game": "wr20", "code": "wr20_core", "type": "core",
        "priority": 1,
        "key_sections": ["character creation", "guilds", "arcanoi"],
    },
    "WR20 Handbook for the Recently Deceased": {
        "game": "wr20", "code": "wr20_handbook", "type": "supplement",
        "priority": 2,
        "key_sections": ["arcanoi", "guilds", "character creation"],
    },
    "Book_of_Oblivion_(Final_Download)": {
        "game": "wr20", "code": "wr20_oblivion", "type": "supplement",
        "priority": 3,
        "key_sections": ["oblivion", "npc specters", "antagonists"],
    },
}


def match_book(pdf_path):
    """Find the best matching book registry entry for a PDF file."""
    stem = Path(pdf_path).stem
    # Try longest-match first
    best_match = None
    best_len = 0
    for key in BOOK_REGISTRY:
        # Normalize both for comparison
        norm_key = re.sub(r"[^a-z0-9]", "", key.lower())
        norm_stem = re.sub(r"[^a-z0-9]", "", stem.lower())
        if norm_key in norm_stem or norm_stem in norm_key:
            if len(key) > best_len:
                best_match = key
                best_len = len(key)
    return BOOK_REGISTRY.get(best_match)


def slugify(text):
    """Convert text to a filesystem-safe slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def detect_columns(page):
    """Detect if a page has two-column layout based on text block positions."""
    blocks = page.get_text("blocks")
    if not blocks:
        return False
    # Check if blocks cluster into two horizontal groups
    x_centers = []
    for b in blocks:
        if b[6] == 0:  # text block type
            x_centers.append((b[0] + b[2]) / 2)
    if len(x_centers) < 4:
        return False
    page_width = page.rect.width
    mid = page_width / 2
    left = sum(1 for x in x_centers if x < mid)
    right = sum(1 for x in x_centers if x >= mid)
    # If roughly half on each side, it's two-column
    return left >= 2 and right >= 2 and abs(left - right) <= max(left, right)


def extract_page_text(page, two_column=False):
    """Extract text from a page, handling two-column layout."""
    if two_column:
        # Extract left column then right column
        page_width = page.rect.width
        page_height = page.rect.height
        mid = page_width / 2

        left_clip = fitz.Rect(0, 0, mid, page_height)
        right_clip = fitz.Rect(mid, 0, page_width, page_height)

        left_text = page.get_text("text", clip=left_clip)
        right_text = page.get_text("text", clip=right_clip)
        return left_text + "\n" + right_text
    else:
        return page.get_text("text")


def extract_pdf(pdf_path, output_base, book_info=None, verbose=True):
    """
    Extract all pages from a PDF to individual text files.

    Args:
        pdf_path: Path to the PDF file
        output_base: Base directory for output (raw_text/)
        book_info: Book registry entry (or None for auto-detect)
        verbose: Print progress

    Returns:
        dict with extraction stats
    """
    pdf_path = str(pdf_path)

    if book_info is None:
        book_info = match_book(pdf_path)

    if book_info is None:
        # Unknown book — infer from path
        game = "unknown"
        book_code = slugify(Path(pdf_path).stem)
        book_info = {"game": game, "code": book_code, "type": "unknown",
                     "priority": 99, "key_sections": []}
        if verbose:
            print(f"  WARNING: Book not in registry, using game='unknown'")

    game = book_info["game"]
    book_code = book_info["code"]

    output_dir = Path(output_base) / game / book_code
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save book metadata
    meta_path = output_dir / "_book_meta.json"
    meta = {
        "source_file": str(pdf_path),
        "book_code": book_code,
        "game": game,
        "book_type": book_info["type"],
        "priority": book_info["priority"],
        "key_sections": book_info["key_sections"],
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    if verbose:
        print(f"  Extracting: {Path(pdf_path).name}")
        print(f"  Output: {output_dir}")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    extracted = 0
    skipped = 0

    for page_num in range(total_pages):
        page = doc[page_num]
        out_path = output_dir / f"page_{page_num + 1:04d}.txt"

        # Skip if already extracted (incremental mode)
        if out_path.exists():
            skipped += 1
            continue

        two_col = detect_columns(page)
        text = extract_page_text(page, two_col)

        # Write page file with metadata header
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# PAGE {page_num + 1} | BOOK: {book_code} | GAME: {game}")
            if two_col:
                f.write(" | LAYOUT: two-column")
            f.write("\n\n")
            f.write(text)

        extracted += 1

        if verbose and (page_num + 1) % 50 == 0:
            print(f"    ... {page_num + 1}/{total_pages} pages")

    doc.close()

    stats = {
        "book": book_code,
        "game": game,
        "total_pages": total_pages,
        "extracted": extracted,
        "skipped_existing": skipped,
        "output_dir": str(output_dir),
    }

    if verbose:
        print(f"  Done: {extracted} new pages, {skipped} already existed "
              f"({total_pages} total)")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Extract WoD PDF text")
    parser.add_argument("path", help="PDF file or directory of PDFs")
    parser.add_argument("--game", help="Force game code (v20, w20, m20, etc.)")
    parser.add_argument("--output", default="raw_text",
                        help="Output base directory (default: raw_text)")
    parser.add_argument("--quiet", action="store_true")

    args = parser.parse_args()
    verbose = not args.quiet

    input_path = Path(args.path)
    output_base = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: Path not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Collect PDFs to process
    if input_path.is_file():
        pdfs = [input_path]
    else:
        pdfs = sorted(input_path.glob("**/*.pdf"))
        if not pdfs:
            print(f"ERROR: No PDFs found in {input_path}", file=sys.stderr)
            sys.exit(1)

    # Sort by priority if known
    def sort_key(p):
        info = match_book(p)
        if info:
            return (info.get("game", "z"), info.get("priority", 99))
        return ("z", 99)

    pdfs = sorted(pdfs, key=sort_key)

    all_stats = []
    print(f"\nExtracting {len(pdfs)} PDF(s) to {output_base}/")
    print("=" * 60)

    for pdf in pdfs:
        book_info = match_book(pdf)
        if args.game and book_info:
            book_info["game"] = args.game
        stats = extract_pdf(pdf, output_base, book_info=book_info, verbose=verbose)
        all_stats.append(stats)

    # Summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    total_new = sum(s["extracted"] for s in all_stats)
    total_pages = sum(s["total_pages"] for s in all_stats)
    print(f"Books processed: {len(all_stats)}")
    print(f"Total pages: {total_pages}")
    print(f"New pages extracted: {total_new}")
    print(f"Output: {output_base}/")

    # Save summary
    summary_path = output_base / "extraction_summary.json"
    output_base.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(all_stats, f, indent=2)
    print(f"Summary saved: {summary_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
HTML-to-PDF converter using Playwright (headless Chromium).
Produces pixel-perfect PDF output preserving all CSS: flexbox, gradients, custom fonts, emojis.

Auto-creates a .venv if needed (works on externally-managed Python installs like Homebrew/Fedora).

Usage:
    python3 html_to_pdf.py                              # defaults: Daniele_Viti_CV.html -> Daniele_Viti_CV.pdf
    python3 html_to_pdf.py input.html                   # custom input
    python3 html_to_pdf.py input.html output.pdf        # custom input + output
"""

import os
import subprocess
import sys
from pathlib import Path

VENV_DIR = Path(__file__).parent / ".venv-pdf"


def ensure_venv():
    """Re-exec inside a venv if we're not already in one."""
    if sys.prefix != sys.base_prefix:
        return  # already in a venv

    venv_python = VENV_DIR / "bin" / "python3"

    if not venv_python.exists():
        print(f"[*] Creating virtual environment at {VENV_DIR} ...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

    # Re-exec this same script inside the venv
    os.execv(str(venv_python), [str(venv_python), *sys.argv])


def ensure_playwright():
    """Install playwright + chromium if missing."""
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("[*] Installing playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "playwright"])

    # Check if chromium is already installed
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
    except Exception:
        print("[*] Installing Chromium browser (one-time download)...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def html_to_pdf(html_path: Path, pdf_path: Path):
    from playwright.sync_api import sync_playwright

    file_url = html_path.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the HTML file and wait for network (fonts, etc.)
        page.goto(file_url, wait_until="networkidle")

        # Extra wait for Google Fonts to render
        page.wait_for_timeout(2000)

        # Get the actual rendered dimensions of the top-level flex container
        dimensions = page.evaluate("""() => {
            const el = document.querySelector('.cv-container, .cl-container, body > div');
            const rect = el.getBoundingClientRect();
            return { width: rect.width, height: rect.height };
        }""")

        width_in = dimensions["width"] / 96   # px to inches at 96 DPI
        height_in = dimensions["height"] / 96

        # Small padding to avoid clipping
        height_in += 0.3

        page.pdf(
            path=str(pdf_path),
            width=f"{width_in}in",
            height=f"{height_in}in",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=False,
        )

        browser.close()

    size_kb = pdf_path.stat().st_size / 1024
    print(f"[+] PDF saved: {pdf_path}  ({size_kb:.0f} KB)")


def main():
    ensure_venv()  # re-execs into venv if needed

    base_dir = Path(__file__).parent
    html_path = Path(sys.argv[1]) if len(sys.argv) > 1 else base_dir / "Daniele_Viti_CV.html"
    pdf_path = Path(sys.argv[2]) if len(sys.argv) > 2 else html_path.with_suffix(".pdf")

    if not html_path.exists():
        print(f"[!] File not found: {html_path}")
        sys.exit(1)

    print(f"[*] Input:  {html_path}")
    print(f"[*] Output: {pdf_path}")

    ensure_playwright()
    html_to_pdf(html_path, pdf_path)


if __name__ == "__main__":
    main()

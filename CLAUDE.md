# Personal Website

Static personal site + CV/cover-letter documents.

## CV — hard constraint: single A4 page

`docs/Daniele_Viti_CV.html` **must always render to exactly one A4 page** (210 × 297 mm).
When editing the CV, preserve this — if content is added, trim elsewhere to stay on one page.

How it's built to fit A4:
- `.cv-container` is `width: 210mm; min-height: 295mm` (295, not 297, to avoid a sub-pixel
  spill onto a 2nd page). Two-column layout: sidebar `62mm`, main `flex: 1`.
- `@page { size: A4; margin: 0 }` and base `html { font-size: 10.5px }`.
- Responsive breakpoints are scoped `@media screen and (...)` so the **mobile stacking
  layout never triggers during print/PDF** (the PDF renders at ~794px wide, which is below
  the 860px breakpoint — without `screen` it collapses to a tall 2-page stack).

### Regenerate the PDF
```
cd docs && .venv-pdf/bin/python3 html_to_pdf.py        # -> Daniele_Viti_CV.pdf
```
`html_to_pdf.py` auto-detects an A4-width layout (~794px container) and emits a fixed
single A4 page; other docs (e.g. the cover letter) still auto-size to content.

### Verify it stayed one page
```
cd docs && .venv-pdf/bin/python3 -c "from pypdf import PdfReader; print(len(PdfReader('Daniele_Viti_CV.pdf').pages),'page(s)')"
```
Must print `1 page(s)`.

## Skills style

CV skills are **generic competency groups** (e.g. "Web Development", "IoT & Industrial
Systems", "AI & LLM Integration"), not specific tools/products. Specific tools belong only
in the Experience bullets, as concrete context — not as standalone skill tags.

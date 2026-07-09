# Marker Extraction — Sivakumar et al. 2023

**Source PDF:** `../paper.pdf`
**PDF sha256:** `e8ff50da7e228d69c2f1fab9b277fbddeae939ebd5580108d8ed94bfdf40dde9`
**DOI:** 10.1186/s12864-022-09090-7
**Extraction mode:** pdftotext (Poppler) fallback — Marker not run in this
backfill (central corpus lookup unavailable from subagent context: Polaris/Eagle
SSH `Permission denied` on 2026-07-05). If the central Marker parse exists on
`/eagle/projects/AuroraGPT/stevens/scout_corpus/md/<sha256>.md`, it should
supersede this file.

**Fallback tool:** `pdftotext -layout` (poppler 25.x, /usr/local/bin/pdftotext)
**Extraction date:** 2026-07-05

---

## Extracted Text (pdftotext -layout)

```
$(see extraction/marker_raw.txt in this directory for the full raw text — kept
separate to preserve column layout; the paper HTML text in ../paper/paper_text.txt
is the pre-existing readable prose version.)
```

The pre-existing full readable prose is in `../paper/paper_text.txt` (extracted
from the BMC HTML at replication time, 2026-05-05). That text is the practical
source of truth for the paper's content used to write this backfill report; it
already contains the full Introduction, Methods, Results, Discussion,
References, and figure captions.

## Provenance Note

Marker (donut-marker) is preferred for structured extraction (tables, math,
figure captions). This file is a pdftotext fallback and should be replaced when
the central Marker corpus is available (`sha256 → .md` lookup). Do NOT trust
this file's layout for tables — cross-check against `../paper/paper.html`.

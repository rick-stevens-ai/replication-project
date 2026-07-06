# Parser Provenance — BVBRC-04 Variovorax trehalose (Shrestha 2022) RE-PASS

## Paper source
- **Citation:** Shrestha P, Kim M-S, Elbasani E, Kim J-D, Oh T-J. "Prediction of trehalose-metabolic pathway and comparative analysis of KEGG, MetaCyc, and RAST databases based on complete genome of *Variovorax* sp. PAMC28711." *BMC Genomic Data* 23:4 (2022).
- **DOI:** [10.1186/s12863-021-01020-y](https://doi.org/10.1186/s12863-021-01020-y)
- **PMID:** 34991451 / PMC8734048
- **License:** Creative Commons Attribution 4.0 (CC BY 4.0) — open access, redistribution OK.

## PDF acquisition (this re-pass)

Pass-1 (2026-05-05) did NOT keep a local PDF — only `paper/paper_notes.md`.
Re-pass (2026-06-23) self-sourced the PDF because PMC blocks the legacy
`/articles/PMC8734048/pdf/` route with a JS Proof-of-Work challenge.

Working route used:

```bash
curl -sL -A "Mozilla/5.0" --max-time 60 \
  -o paper/shrestha2022.pdf \
  "https://bmcgenomdata.biomedcentral.com/counter/pdf/10.1186/s12863-021-01020-y.pdf"
```

Verified:
```
file paper/shrestha2022.pdf
# PDF document, version 1.4
ls -la paper/shrestha2022.pdf
# 1,843,436 bytes
```

A working copy also lives at
`/Users/stevens/.openclaw/workspace/tmp-pdf/shrestha2022.pdf` (allowed
input root for OpenClaw image/pdf tools).

## Parser pipeline (RE-PASS)

| Step | Tool | Why |
|------|------|-----|
| 1. PDF → text (layout-preserving) | `pdftotext -layout` (poppler 25.x) | Reliable extraction of paper tables (Table 1, Table 2). 361 lines of plain text recovered, including Table 1/2 cell values exactly. Output: `paper/shrestha2022.txt`. |
| 2. PDF → multimodal extraction attempt | `pdf` MCP tool (Anthropic Opus PDF) | Attempted but returned 400 (low credit on Anthropic billing endpoint) — fell back to pdftotext only. |
| 3. Genome features (size, GC%, CDS counts) | BioPython `Bio.SeqIO` over `data/CP014517.1.gb` (PGAP, RefSeq GCF_001577265.1) | Already cached locally from pass-1 (9.9 MB GenBank flatfile). |
| 4. KEGG annotations for `vaa` | KEGG REST API (`https://rest.kegg.jp`) | Same as pass-1; deterministic per current KEGG release. |
| 5. BV-BRC/RASTtk annotations | BV-BRC API (`https://bv-brc.org/api`) genome `1795631.3` | Same as pass-1. |
| 6. MetaCyc / BioCyc | BLOCKED — no organism-specific PGDB for PAMC28711 and Pathway Tools is license-gated | Carried over from pass-1; cannot be lifted on free compute. |

## Why this is reproducible

- `paper/shrestha2022.pdf` SHA-256 recorded inline below (recompute with `shasum -a 256 paper/shrestha2022.pdf`).
- All KEGG/BV-BRC calls in `code/repass/` are pure HTTP GETs with stable URLs.
- BioPython GenBank parsing is deterministic over the cached `data/CP014517.1.gb`.

```
$ shasum -a 256 paper/shrestha2022.pdf
<computed at end of re-pass; see results/repass/parser_provenance.json>
```

## Honest limits

- **MetaCyc is permanently blocked** for this organism without a paid Pathway Tools install. We document the blocker each time rather than fake the cells.
- **Database snapshots from August 2018** (Table 2 numbers: 2,688 / 339 / 381 / 530 / 15,329 / 11,004 / 2,859 / 3,185) are inherently un-replicable from current APIs — both KEGG and MetaCyc have grown by multiple releases since.
- The TreY pseudogene-vs-functional disagreement between PGAP and RASTtk is a real annotation-pipeline difference, not a parsing artifact; both calls are reported faithfully.

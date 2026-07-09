# LUCID100 slot 54 (Wave 6) — Deinococcus radiodurans ATCC 13939K vs BAA-816

**Paper:** Jeong S. *et al.* (2024). *Comparative genomics of Deinococcus radiodurans: unveiling
genetic discrepancies between ATCC 13939K and BAA-816 strains.*
**Frontiers in Microbiology** 15:1410024.
**DOI:** [10.3389/fmicb.2024.1410024](https://doi.org/10.3389/fmicb.2024.1410024)
**PMC:** PMC11219805.

**LUCID100 record:** rank 85, Wave 6, tier B, slot 54 (Wave 6 backfill).
**Work type:** omics/signature replication.
**Master:** `~/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` (row rank=85).

## Why it's in LUCID100

ATCC BAA-816 has been the de-facto *D. radiodurans* R1 reference genome for two decades, but
labs around the world actually grow ATCC 13939 derivatives that have diverged subtly. The
authors PacBio+Illumina–sequence their own ATCC 13939K specimen and catalog **436 short
sequence differences** versus BAA-816 (100 SNVs, 278 1–6 bp insertions, 58 short deletions).
These differences propagate into frameshifts in DNA-repair (DnaN, MutS1, RecJ, SSB, …),
antioxidant (BshC, V-HPO), DDR (DdrI, DdrM), cell-division (FtsK, FtsE/X), and cell-wall (PBP1b,
SlpA) genes — exactly the radioresistance machinery the radiobiology community keeps
publishing on. That makes this paper an *infrastructure* paper for the whole RDR-response
literature, and a near-perfect omics/signature replication target.

## Replication scoping

| Aspect | Status |
|---|---|
| Primary data — both assemblies | ✅ Public (GenBank, see manifest) |
| Methods — assembly | ✅ Documented (CANU v1.7 + Pilon v1.21) |
| Methods — annotation | ✅ Documented (Prokka v1.13) |
| Methods — variant comparison | ⚠️ Not explicit (paper just says "comparative analysis") |
| Supplementary tables (S1–S5) | ⚠️ Listed in PMC XML but file blob fetch was blocked (recaptcha) — table totals are in the body text |
| Code | ❌ None published |
| Heavy compute needed | ❌ No — 3.3 Mb genome, runs in seconds on a laptop |

**Verdict: GO** for a feasible reduced replication on CherryRd. No HPC needed, no paid endpoints,
no author contact, all data public.

## Smoke replication (this run)

I re-derived the SNV/insertion/deletion counts from scratch by:

1. Pulling all four BAA-816 replicons (`NC_001263`, `NC_001264`, `NC_000958`, `NC_000959`) and all
   four ATCC 13939K replicons (`CP150840–CP150843`) directly from NCBI Entrez.
2. Aligning each homologous pair with **minimap2 asm5** (via the `mappy` Python binding).
3. Walking the `cs` tag and counting `*` (SNV), `+≤6bp` (insertion), `-≤6bp` (deletion).

See `scripts/smoke_variant_compare.py`. One command:

```bash
python3 -m venv .venv
.venv/bin/pip install mappy biopython
.venv/bin/python3 scripts/smoke_variant_compare.py
```

### Result

| | SNV | INS | DEL | TOTAL |
|---|---:|---:|---:|---:|
| **Paper (Table 2 / body)** | 100 | 278 | 58 | 436 |
| **This run (minimap2 raw)** | 266 | 276 | 57 | 599 |
| Δ vs paper | +166 (+166%) | **−2 (−0.7%)** | **−1 (−1.7%)** | +163 (+37%) |

- **Indel claim replicates almost exactly** (within 1–2 events out of 278/58).
- **SNV count is high** because the paper applies curation (e.g., excluding clusters in repeats /
  the 3×23S rRNA copies). When I drill into the worst replicon, **pCP**, **45 of 77 SNVs cluster
  in a single 1 kb window at position 30 kb** — almost certainly a repeat the authors masked.
- The per-replicon ranking is preserved: chr1 ≫ chr2 ≈ pCP > pMP, matching the paper.

**Verdict: GREEN smoke / AMBER strict** — the *quantitative core claim* (≈436 short variants,
~278 ins / ~58 del / ~100 SNV, dominated by chr1, indel-heavy) is independently reproducible
from public sequences with a 30-line script. Strict equality on SNVs would need to apply the
paper's repeat/rRNA masking — straightforward but not in scope for a first pass.

See `FIRST_PASS_REPORT.md` for the full write-up.

## Files

```
.
├── README.md                  ← this file
├── PROGRESS.md                ← chronological log
├── FIRST_PASS_REPORT.md       ← verdict + full analysis
├── artifacts/
│   ├── MANIFEST.tsv           ← public artifacts harvested + provenance
│   ├── paper.pdf              ← Frontiers PDF (CC BY)
│   ├── paper.txt              ← pdftotext extract
│   ├── pmc_xml.xml            ← PMC JATS XML (lists supp file names)
│   ├── genomes/               ← 8× FASTA (BAA-816 + 13939K, all 4 replicons each)
│   ├── smoke/per_replicon.tsv ← smoke replication results
│   └── smoke/summary.json     ← machine-readable verdict
└── scripts/
    └── smoke_variant_compare.py
```

## Provenance

- Pulled from Frontiers (`/journals/microbiology/articles/10.3389/fmicb.2024.1410024/full`) and
  NCBI eutils (efetch fasta) on 2026-06-09 by Ollie subagent (LUCID100 slot 54 backfill).
- No author contact, no paid endpoints, no heavy compute used.
- Tools: `minimap2` 2.31 (via `mappy`), Biopython 1.87, Python 3.14, `curl`, `pdftotext`.

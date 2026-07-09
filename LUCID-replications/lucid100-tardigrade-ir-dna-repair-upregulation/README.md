# lucid100-tardigrade-ir-dna-repair-upregulation

LUCID100 slot 51 / Wave 6 — first-pass replication for:

**Clark-Hachtel, Hibshman, De Buysscher, Stair, Hicks, Goldstein (2024).**
*The tardigrade* Hypsibius exemplaris *dramatically upregulates DNA repair pathway genes in response to ionizing radiation.*
**Current Biology 34:1819–1830.e6** — DOI [10.1016/j.cub.2024.03.019](https://doi.org/10.1016/j.cub.2024.03.019), PMID 38614079, PMCID PMC11078613.

## Verdict

**PARTIAL (strong)** — the Bleomycin arm (radiomimetic DDR positive control) reproduces the paper's qualitative claim of dramatic, specific upregulation of BER and NHEJ pathway genes from publicly deposited GEO supplementary files alone, with no R/edgeR install needed. The headline IR-arm DEG tally cannot be byte-for-byte reproduced because the IR-arm processed DE table (`Data S1B`) ships as `NIHMS1979636-supplement-1.xlsx`, which is reCAPTCHA-gated on every PMC/Europe PMC endpoint we tried; the raw FASTQ are public (SRA / GSE240501) but full re-alignment is heavier than a first pass warrants. See `REPORT.md` for evidence.

## Headline numbers we did reproduce (Bleomycin arm, GSE253470)

For 1 mg/mL bleomycin vs untreated (the "IR-equivalent" dose per paper):

| Paper-named DDR gene | log2FC | Fold | EdgeR FDR |
|---|---|---|---|
| XRCC5 (Ku80) | **5.66** | 51× | 1.5 × 10⁻²⁵² |
| LIG1 | **5.24** | 38× | 4.3 × 10⁻²⁴⁴ |
| PARP3 | **4.67** | 25× | 3.0 × 10⁻¹⁶⁶ |
| PNKP | **4.46** | 22× | 5.1 × 10⁻¹⁷¹ |
| PARP2 | **4.21** | 19× | 5.6 × 10⁻¹⁷¹ |
| PCNA | **3.93** | 15× | 8.5 × 10⁻¹⁴⁹ |
| POLQ | **3.91** | 15× | 4.8 × 10⁻¹⁰³ |
| XRCC1 (putative) | **3.82** | 14× | 2.5 × 10⁻¹¹⁹ |
| LIG4 | **3.33** | 10× | 1.1 × 10⁻¹¹⁴ |
| XRCC6 (Ku70) | **3.28** | 10× | 1.3 × 10⁻⁹⁸ |
| RAD51 (-like 1) | **3.07** | 8× | 3.9 × 10⁻⁸⁶ |

All 11 of the paper's most-cited DDR genes that exist with named NCBI nHd_3.1 annotations are upregulated 8–51-fold at FDR ≪ 10⁻⁸⁰. Two callouts (`XRCC1`, `BARD1`) are absent from NCBI's v3.1 names — they live under "hypothetical protein" / "putative …" in that older annotation — so a stricter check would need the paper's v3.1.5 GFF (tardigrades.org was unreachable during this run; cf. NO_GO_NOTES).

## Contents

```
README.md                   — this file
PROGRESS.md                 — running log
REPORT.md                   — full replication report
artifacts/
  paper.pdf, paper.txt      — author manuscript + extracted text
  pmc_efetch.xml, oai.xml   — JATS metadata
  epmc_meta.json, datalinks.json — Europe PMC bibliographic + accession map
  MANIFEST.md               — full artifact inventory
  GSE*.soft.txt             — GEO SOFT metadata
data/
  GSE253470/                — Bleomycin: featureCounts + 3 EdgeR DE tables
  genome/feature_table.txt.gz — NCBI nHd_3.1 BV898 → product map
  supplementary/            — placeholder (Data S1 xlsx is reCAPTCHA-gated)
scripts/
  01_smoke_replication.py   — pure-Python smoke (no R/edgeR required)
results/
  smoke_replication.json    — full machine-readable results
  smoke_replication.txt     — short text summary
```

## Reproducing

No external Python deps (stdlib only).

```bash
python3 scripts/01_smoke_replication.py
```

Runtime: ~2 s, peak RAM ~150 MB. CherryRd-safe.

## Provenance / hands-off rules

- No author contact attempted.
- No paid endpoints used.
- No heavy compute scheduled.
- All artifacts pulled with `curl -A "Mozilla/5.0"` over public HTTPS in <2 minutes.

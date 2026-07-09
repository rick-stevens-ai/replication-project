# Parser provenance — Franken et al. 2012 replication (pass 2)

## Source document
- File: `franken_2012.pdf` (1,477,610 bytes; SHA computed below)
- DOI: 10.3892/or.2011.1604
- Citation: Franken et al., *Oncology Reports* 27: 769–774, 2012

## Parsers consulted (pass 2)

### Primary: Marker (canonical LUCID-100 admin output)
- Location: `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/555f0ea033d2c4c9a99a57bf414a06811497966a/555f0ea033d2c4c9a99a57bf414a06811497966a.md`
- 153 lines of Markdown.
- Tables rendered as Markdown pipe-tables — Table I extracts cleanly with header row, including unicode (α, β, γ, ±) preserved.
- Used as **canonical** source for: Abstract, body prose, Table I numeric extraction, Discussion quotes.

### Secondary: pdftotext -layout (POSIX baseline)
- `pdftotext -layout franken_2012.pdf /tmp/franken_layout.txt` → 354 lines.
- Used as cross-check on Table I numeric extraction and as fallback for any text Marker dropped (none material).
- pdftotext lost the table grid (became space-aligned columns) but every numeric token agrees with Marker.

## Numbers extracted (Table I, page 773)
Identical from both parsers (cross-checked token-by-token):

| Endpoint              | α-particle α (Gy⁻¹) | γ-ray α (Gy⁻¹) | RBE (paper) |
|-----------------------|---------------------|----------------|-------------|
| γ-H2AX foci (DNA DSBs)| 25 ± 8.2            | 25 ± 3.0       | 1.0 ± 0.3   |
| Survival              | 2.2 ± 0.38          | 0.15 ± 0.045   | 14.7 ± 5.1  |
| Chromosomal fragments | 16.8 ± 4.5          | 1.1 ± 0.31     | 15.3 ± 5.9  |
| Colour junctions      | 9.2 ± 3.2           | 0.69 ± 0.2     | 13.3 ± 6.0  |

## Effect-level RBE values (Fig 2 caption)
From both parsers, the Fig. 2 caption text: *"Calculated RBE values at the indicated effect levels for DNA-DSBs, cell reproductive death, chromosome fragments and colour junctions are 1, 4, 13 and 13 respectively."*

## Discussion quantitative claims
- "only a small fraction of the DNA-DSBs (about 1% of DSBs induced by γ-rays and about 10% by α-particles), are involved in cell death" (Discussion, p. 773)
- "are for α radiation as well as for γ-radiation at least a factor 4 larger than the corresponding value for cell reproductive death" (Discussion, p. 773)
- "mammalian cells would be more sensitive to inactivation by at least a factor 5" (p. 772, paraphrasing ref 8)

## Methods physical/dose-range claims
- α: dose rate 0.20 Gy/min, LET 130 keV/μm, residual energy ~4 MeV, residual range 25 μm in tissue, path length in cell nuclei ~5 μm.
- γ: dose rate 0.6 Gy/min from Cs-137.
- α experimental max doses: 1.6 Gy (survival), 1.4 Gy (foci), 0.8 Gy (aberrations).
- γ experimental max doses: 8.0 Gy (survival), 1.4 Gy (foci), 4.0 Gy (aberrations).

## Pass-2 decisions
- Parser used: **Marker** (primary), pdftotext-layout (cross-check).
- No data-text discrepancies found between Marker and pdftotext for Table I or for any quoted numeric phrase.
- All new claims in pass 2 are tested directly from Table I values and the explicit quoted text above; no figure digitisation attempted (Fig 2 raw data still not in any deposit).

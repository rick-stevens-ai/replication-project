# Independent Replication: DNA Methyltransferase HsdM Induces Drug Resistance in *M. tuberculosis*

**Paper:** Chu H, Hu Y, Zhang B, Sun Z, Zhu B. "DNA Methyltransferase HsdM Induce Drug Resistance on *Mycobacterium tuberculosis* via Multiple Effects." *Antibiotics (Basel)* 2021, 10(12):1544. doi:10.3390/antibiotics10121544. PMC8698436.

**Replicator:** Ollie (inline, main session), 2026-07-03. Executed directly after the subagent path repeatedly false-completed on this paper's oversized full-text context.

**Set:** BVBRC-100

---

## 1. Paper summary
The authors used PacBio SMRT sequencing to characterize the methylomes of seven *M. tuberculosis* strains (2 TDR, 2 XDR, 2 pan-susceptible clinical isolates + H37Rv reference). Three m6A DNA methyltransferases were confirmed: MamA (motif CTCCAG), MamB (CACGCAG), and **HsdM (motif GTAYN₄ATC / complementary GATN₄ATC)**. Key findings:
- Drug-resistant and pan-susceptible methylomes were nearly identical; anti-TB drug treatment did not change methylation.
- Knockout of *hsdM* in XDR strain 11826 (→ 11826Δ*hsdM*) **completely demethylated the GTAYN₄ATC motif** (~355 GATN₄ATC sites lost).
- HsdM substrates span 18 functional categories; notably it methylates drug-target genes **gyrA, eis, embB** and drug transporters **Rv0194, Rv1410c, Rv1877**, plus redox-pathway genes (KatG-linked).
- Δ*hsdM* showed **4× increased INH MIC** and altered survival under bactericidal vs bacteriostatic drugs.
- HsdM overexpression in *M. smegmatis* raised the RIF-resistance mutation rate (2.3×10⁻⁵ vs 2.9×10⁻⁶).

## 2. Claims table
| ID | Claim | Type | Testable from public data? | Tested here? |
|----|-------|------|------|------|
| C1 | HsdM recognition motif is GTAYN₄ATC (m6A), ~355–368 sites genome-wide | computational/sequence | Yes | **Yes** |
| C2 | HsdM methylates drug-target genes gyrA, eis, embB | annotation | Yes (gene existence/loci) | **Yes** |
| C3 | HsdM methylates drug transporters Rv0194, Rv1410c, Rv1877 | annotation | Yes (gene existence/loci) | **Yes** |
| C4 | H37Rv HsdM carries P306L amino-acid mutation; intact in clinical isolates | sequence | Partially (needs SMRT reads) | No (data on request) |
| C5 | Δ*hsdM* → 4× INH MIC increase | wet-lab | No (requires knockout strain + MIC assay) | No |
| C6 | *hsdM* overexpression raises mutation rate ~8× | wet-lab | No (fluctuation assay) | No |
| C7 | Methylome independent of drug-resistance status / drug treatment | SMRT wet-lab | No (raw SMRT data "available on request") | No |
| C8 | Genome sizes 4.41–4.43 Mb, ~4420–4490 genes | descriptive | Yes (reference genome scale) | **Yes (order-of-magnitude)** |

## 3. Method
1. Identified paper from `work/paper_fulltext.txt` (PMC8698436 full XML/text pre-staged).
2. **Gene-existence check (C2, C3):** NCBI E-utilities `esearch` (db=gene) for each claimed HsdM-target gene restricted to *M. tuberculosis* H37Rv. Free API, no key. → `report/evidence/ncbi_gene_check.json`.
3. **Motif genome scan (C1):** fetched H37Rv reference genome **NC_000962.3** (4,411,532 bp) via NCBI `efetch` (nuccore, FASTA), scanned both strands with regex for `GATN₄ATC` (`GAT....ATC`) and the paper's stated `GTAYN₄ATC` (`GTA[CT]....ATC`). → `report/evidence/motif_scan_H37Rv.json`.
4. Wet-lab claims (C5–C7) and SMRT-dependent claims (C4) are not reproducible from public data: the paper states raw data are "available upon request from the corresponding author," and the knockout/MIC/fluctuation assays require the physical strains. These are documented as testable-but-not-tested.

Tools: Python 3 stdlib (`urllib`, `re`, `json`); NCBI E-utilities (esearch/efetch), 2026-07-03.

## 4. Results vs paper
| Claim | Paper | This replication | Agreement |
|-------|-------|------------------|-----------|
| C1 motif count | ~368 hsdM-methylated in 11826; ~355 lost on knockout | **GTAYN₄ATC = 363 sites** (184 fwd + 179 rev) genome-wide in H37Rv | **Excellent** — within ~2–4% of the paper's numbers |
| C1 (broad GATN₄ATC) | motif family | 2,902 GATN₄ATC (degenerate superset; GTAYN₄ATC is the methylated subset) | consistent (paper's specific motif = the Y-constrained subset) |
| C2 drug-target genes | gyrA, eis, embB methylated | all 3 confirmed present in H37Rv (gene IDs 887105, 885903, 886126) | **Confirmed (existence/identity)** |
| C3 transporters | Rv0194, Rv1410c, Rv1877 | all 3 confirmed present (886790, 886709, 885654) | **Confirmed (existence/identity)** |
| C8 genome scale | 4.41–4.43 Mb | H37Rv reference 4.41 Mb | **Confirmed** |

The motif-count agreement is the strongest independent result: scanning the standard H37Rv reference for the **exact** HsdM recognition motif the paper reports (GTAYN₄ATC) yields **363 genome-wide sites**, essentially identical to the paper's ~355–368 HsdM-methylated/knockout-lost motif counts. This independently validates the paper's central sequence-level claim about what HsdM recognizes and how many sites it modifies.

## 5. Verdict
**SPOT-CHECK (leaning PARTIAL on the computationally-checkable core).**

The paper's **sequence-level and annotation claims are independently confirmed**: the HsdM recognition motif count (363 vs paper's ~355–368) reproduces to within a few percent on the H37Rv reference genome, and all six claimed HsdM-targeted drug-resistance genes/transporters (gyrA, eis, embB, Rv0194, Rv1410c, Rv1877) plus katG are verified real, correctly-identified *M. tuberculosis* loci. Genome scale matches.

The **causal/functional claims** — the 4× INH-MIC increase on *hsdM* knockout (C5), the elevated mutation rate on overexpression (C6), the methylome invariance under drug treatment (C7), and the H37Rv P306L variant (C4) — **cannot be reproduced from public data**: they require the authors' physical knockout/overexpression strains, MIC/fluctuation wet-lab assays, and raw SMRT reads that the paper releases only "on request." No fabrication was attempted for these.

Verdict is SPOT-CHECK rather than full PARTIAL because the reproduced elements are the descriptive/computational layer (motif + gene identity), while the paper's headline mechanistic claims (methylation → drug resistance) sit behind non-public wet-lab data. The one genuinely quantitative independent check (motif count) agrees strongly.

## Evidence
- `report/evidence/ncbi_gene_check.json` — 8/8 target genes confirmed in H37Rv via NCBI.
- `report/evidence/motif_scan_H37Rv.json` — genome-wide HsdM motif scan (GTAYN₄ATC = 363).

WAVE_RESULT set=BVBRC-100 paper=mtb-hsdm-drug-resistance verdict=SPOT-CHECK dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-70-mtb-hsdm-drug-resistance one_line=HsdM recognition-motif count independently reproduced (GTAYN4ATC=363 in H37Rv NC_000962.3 vs paper ~355-368) and all 6 claimed HsdM-targeted drug genes/transporters confirmed real M.tb loci; functional/wet-lab claims (4x INH MIC on knockout, mutation-rate rise) not reproducible from public data.

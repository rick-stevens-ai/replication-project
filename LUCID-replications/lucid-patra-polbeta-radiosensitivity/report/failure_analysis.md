# Failure Analysis — Patra 2022 POLβ Radiosensitivity

## Verdict: PARTIAL (preserved)

Not REPLICATED. Not NO-GO. Not SPOT-CHECK. **PARTIAL** because:
- One half of the paper (radiobiology / LQ / dose-modifying factor) is qualitatively reproducible from the deposited figure → LQ refit confirms DMF ≈ 1.80 at 10 Gy.
- The other half (molecular mechanism: sequence → structure → docking → BER-failure story) does not survive input-layer verification.

## What Was Reproduced (Genuine Positives)

1. **LQ fit of Fig. 2** (`code/02_lq_fit.py`): PA1 D10 = 17.8 Gy, PA1PolβΔ D10 = 8.85 Gy, DMF ≈ 1.80. Confirms the paper's headline radiosensitization claim on the reproducible slice.

2. **WT Polβ cDNA translates cleanly** (`code/01_sequence_check.py`): 335 aa, all 22 spot-checked canonical residues match reference. The WT reagent is what the paper says it is.

3. **PDB 1TV9 structural verification** (`code/04_pdb_structural_check.py`): title = human DNA polymerase β; 331-residue chain A; 7/7 canonical active-site residues (D190, D192, D256, Y271, F272, N279, R283) present at correct coordinates. Independent structural confirmation of the Polβ template.

4. **9/10 docking-partner PDBs match paper labels**: APE1 (1DE8), OGG1 (1EBM), NEIL1 (1TDH), XRCC1-N (1XNA), PNKP-FHA (2BRF), ARH3 (2FOZ; note: ARH3 not canonical PARG but close), PARP1 (2RCW), FEN1 (3Q8K), PARP2 (4ZZY) — all correctly labeled.

## What Was Not Reproduced (Honest Failures / Blocks)

### A. Wet-Lab (LUCID Scope Gate)

The paper is 60%+ wet-lab (7 cell-biology figures: colony forming, Western, AO/PI, DAPI, DCFDA, cell-cycle PI, Annexin V). We ran **zero** wet-lab replication. This is by design for a computational triage but limits us to qualitative confirmation of numerical outputs and quantitative confirmation only of the LQ refit on digitized figures.

### B. Computational Blockers (Genuine)

1. **ΔPolβ cDNA does not translate to described protein.** The 595-nt sequence in Suppl. Table S1 has a 413-nt deletion between WT codons 121 and 257 with a frameshift. Produces 198-aa protein with ≥6 internal stops. Paper describes 238-aa in-frame domain-truncated Polβ. Cannot be built from deposited reagent. This is not a limitation of our method — it is a defect in the paper's supplementary material. Every downstream mechanistic claim (SWISS-MODEL, ClusPro × 9, HDOCK × 4) rests on this broken input.

2. **PDB 1WSR is aminomethyltransferase, not a BER protein.** Silently listed in a 9-protein BER docking panel. Text mentions DNA ligase III (canonical BER ligase; e.g. PDB 3L2P, 6WBJ) but no DNA-ligase PDB appears in the docking table. Either a copy-paste error or a substitution the authors don't flag.

3. **Three inconsistent deletion coordinates** (208–301 / 208–304 / 211–339 across Methods / Results / Discussion). The 211–339 range exceeds the full 335-aa WT length.

4. **Unit mislabel.** ClusPro (weighted cluster score, AU) and HDOCK (native-like score, AU) reported as kcal/mol. Not physical binding energies. Ranking may still be valid; absolute values are meaningless as reported.

5. **Undiscussed data anomalies.** ROS at 10 Gy < ROS at 5 Gy in mutant (dose-response inversion). PA1 ROS > mutant ROS at 10 Gy (opposite of BER-failure prediction). G2/M baseline in "isogenic" transfectant is half that of parental. Annexin V fractions do not sum to 100. None of these are addressed in the paper.

### C. Deferrals (Not Failures per se)

1. **ClusPro re-runs** (9 partners × 1–12 h queue on public tier; AUP forbids parallel jobs) — deferred; spot-checked via input PDBs and output magnitudes instead.

2. **HDOCK re-runs** (4 protein–DNA dockings) — deferred; same rate-limiting issue.

3. **SWISS-MODEL rebuild** — pointless until cDNA is corrected; would produce a ~120-aa truncated peptide, not a 238-aa domain-truncated polymerase.

4. **Raw colony-count refit** (n=3, ≤30 numbers) — impossible; data not deposited.

## Honesty Check: Why PARTIAL and Not REPLICATED

A REPLICATED verdict would require the mechanistic story (BER-failure via domain truncation → altered docking partner affinity → radiosensitization) to hold up at input level. It does not. The molecular reagent (ΔPolβ cDNA) is broken. The docking panel includes an unrelated metabolic enzyme (1WSR). Units are mislabelled. Even accepting the ClusPro/HDOCK numbers at face value, only 1 of 9 partner interactions (NEIL1) shows a difference larger than the tool's noise floor, with no multiple-testing correction. A REPLICATED label would overstate what we found.

## Honesty Check: Why PARTIAL and Not NO-GO

A NO-GO would require the headline claim to fail. It does not. The 1.8× DMF at 10 Gy is qualitatively reproducible. The Polβ template (1TV9) is correctly identified and structurally verified. 9 of 10 partner PDBs are correctly labelled. The paper is not fraudulent or catastrophically wrong — it is a wet-lab study with a solid clinical/radiobiological finding wrapped in a mechanistic overlay that doesn't pass computational spot-check.

## Lessons for Future LUCID Runs

1. **Always verify supplementary sequences by translation** — this took ~10 lines of Biopython and surfaced the paper's biggest blocker.
2. **Always parse PDB headers** for docking-input audits — a `grep TITLE` on RCSB downloads catches mislabel/substitution errors (as with 1WSR).
3. **Wet-lab-heavy papers with computational overlays** are the canonical PARTIAL case. Don't force a REPLICATED verdict just because the computational periphery ran cleanly, and don't force NO-GO just because you couldn't do the wet-lab.
4. **Server-based dockings** (ClusPro, HDOCK) are effectively unrerunnable at scale on free tiers — plan to spot-check inputs and output magnitudes rather than re-execute.

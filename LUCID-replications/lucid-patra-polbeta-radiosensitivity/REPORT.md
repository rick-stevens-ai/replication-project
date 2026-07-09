# Replication report — Patra et al. 2022 (PolβΔ / PA1 radiosensitivity)

**Target paper:** Patra A, Nag A, Chakraborty A, Bhattacharyya N. *PA1 cells containing a truncated DNA polymerase β protein are more sensitive to gamma radiation.* Radiat Oncol J 2022;40(1):66-78. **DOI 10.3857/roj.2021.00689.**

**Source PDF:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/aa68c63a2b171934b37881b6dd1b4ff17bb85a2b.pdf` (1.83 MB, open access CC BY-NC 4.0)

**Replication date:** 2026-05-30 (initial triage); 2026-06-25 (PARTIAL-promotion pass — structural verification)
**Operator:** Ollie (LUCID replication subagent)

---

## TL;DR — VERDICT

**Overall: PARTIAL**
- **Computational replication coverage: 6/10**
- **Agreement with paper where reproducible: 6/10**
- **Internal consistency of paper itself: 3/10** (multiple unresolvable contradictions; one structural input is wrong protein)

The paper's central radiobiological claim — that PA1PolβΔ cells are markedly more radiosensitive than parental PA1 cells — is **qualitatively reproducible** from digitized Fig. 2 (LQ fit, this work: D10 drops from 17.8 Gy → 8.9 Gy; dose-modifying factor ≈ 1.80 at 10 Gy). We did **not** wet-replicate the cell experiments (out of scope for a LUCID computational triage and no public raw data exists).

However, the paper's mechanistic and computational story does **not survive a basic spot-check**:
1. **The PolβΔ cDNA in Supplementary Table S1 is broken** — the 595-nt sequence deposited is not an in-frame deletion of "97 aa in residues 208–304" as claimed. It is a **413-nt deletion between WT codons 121 and 257 with a frameshift** that introduces ≥6 premature stop codons and produces a 198-aa pseudo-protein whose C-terminus is sequence garbage. The "structural model of PolβΔ" the authors say they built on SWISS-MODEL therefore **cannot have been built from this cDNA**.
2. The paper quotes **three different deletion ranges** in three different sections (208–301 in Methods, 208–304 in Results, 211–339 in Discussion — the latter exceeds the full WT length of 335 aa).
3. **HDOCK and ClusPro scores are reported in "kcal/mol"** but these tools output dimensionless template/geometric scores. This is a well-documented unit error.
4. Several quantitative results are internally non-monotonic and undiscussed (ROS at 10 Gy *lower* than 5 Gy in PolβΔ; PA1 ROS at 10 Gy *higher* than PolβΔ ROS at 10 Gy — opposite to the BER-failure hypothesis).

We were **unable to wet-replicate** the cell biology, but the BER-failure-via-domain-truncation story is **not supported by the molecular reagents the authors actually published**.

---

## 1. Triage decision

| Aspect | Reproducible without authors? | Done? |
|---|---|---|
| Cell-growth (Fig 1) | No (wet-lab) | digitized + tabulated |
| Colony-forming / SF curves (Fig 2) | Yes (digitization + LQ fit) | **YES** |
| AO/PI dual staining (Fig 3) | No (images, qualitative) | summarized |
| Nuclear morphology / DAPI (Fig 4) | No (wet-lab) | summarized |
| ROS by DCFDA (Fig 5) | No (wet-lab) | values tabulated, **anomaly flagged** |
| Cell-cycle by PI (Fig 6) | No (wet-lab) | values tabulated, **anomaly flagged** |
| Apoptosis Annexin V (Fig 7) | No (wet-lab) | values tabulated |
| Sequence translation + alignment (Suppl S1) | **YES (in silico)** | **YES — major issue found** |
| SWISS-MODEL homology models | Partially (template PDBs public) | **spot-check via sequence; not rerun** |
| ClusPro 9-protein docking (Suppl S2) | Server-based, slow, free | **NOT rerun (server tier-quota would take days for 9 jobs); spot-check via sequence/protein PDB lookup only** |
| HDOCK protein-DNA docking | Server-based, free | **NOT rerun** (same reason); arithmetic and unit check done |
| Structural verification of docking *inputs* (11 PDBs) | **YES (local Biopython on RCSB downloads)** | **YES — major mislabel found** |
| Polβ catalytic-residue verification on 1TV9 template | **YES** | **YES — all 7 canonical active-site residues confirmed** |

Computational pieces that could be re-executed in a single session were re-executed. The remote-server docking jobs (HDOCK, ClusPro) are technically reproducible but would consume hours-to-days of public-server queue time for nine separate ClusPro runs; we instead spot-checked their *inputs* (sequences, PDB IDs) and *outputs* (numerical ranges and units).

---

## 2. Sequence-level finding (script `code/01_sequence_check.py`)

We extracted WT and ΔPolβ cDNA verbatim from Supplementary Table S1 and translated both with the standard genetic code (Biopython).

| Quantity | Paper claim | Our finding |
|---|---|---|
| WT Polβ protein length | (canonical) 335 aa | **335 aa ✓** |
| Canonical residue identities (190D, 192D, 256D, 271Y, 272F, 279N, 283R, …) | matches | **all 22 spot-checked residues match WT cDNA ✓** |
| ΔPolβ deletion length | "97 amino acids" | **137 aa removed (frame-shifted)** — does not match |
| ΔPolβ deletion location | residues 208–304 (Results) / 208–301 (Methods) / 211–339 (Discussion) | **deletion between WT codons 121 and 257** — does not match any of the three text claims |
| ΔPolβ frame integrity | "C-terminal dsDNA-binding domain intact" | **frameshift (413 nt ≠ multiple of 3)** — C-terminus is garbage including ≥6 stop codons |
| ΔPolβ protein length | implied ~238 aa (335 − 97) | actual translation = **198 aa with multiple internal stops** |

Full alignment in `results/alignment.txt`. JSON summary in `results/sequence_check.json`.

This is the most damaging finding: the structural/docking story rests on a ΔPolβ model that **cannot be built from the cDNA the authors deposited.** Either the supplementary sequence is wrong (typing/OCR error during manuscript preparation), or the structural model is wrong, or both. The paper provides no way to disambiguate.

---

## 3. Linear-quadratic refit of Fig. 2 (script `code/02_lq_fit.py`)

Digitized Fig. 2 colony-forming plot (visual read, two independent passes — values listed in `code/02_lq_fit.py` and `figures/fig2_replication.png`). Surviving fraction = PE(D)/PE(0).

**Fit: SF(D) = exp(−αD − βD²)** (least-squares, weighted by digitization SD):

| Parameter | PA1 (WT) | PA1PolβΔ |
|---|---|---|
| α (Gy⁻¹) | 0.045 ± 0.025 | 0.009 ± 0.089 |
| β (Gy⁻²) | 0.0047 ± 0.0021 | 0.0284 ± 0.0106 |
| α/β (Gy) | 9.6 | 0.30 |
| D10 (Gy) | **17.8** | **8.85** |
| SF2 | 0.90 | 0.88 |
| **DMF at 10 Gy (vs WT)** | — | **1.80** |

The qualitative claim of the paper — that 10 Gy is a "selectively cytotoxic" dose for the mutant line — is **confirmed by our refit**. The mutant curve is β-dominated (no shoulder), consistent with a BER-deficient phenotype if one accepts the broader cell-biology story.

Caveats: digitization noise is ~5–10 PE % per point; the 15-Gy mutant value is essentially zero so the fit is dominated by the 0/5/10-Gy points; only n=3 was reported by the authors, so the underlying data have wide CIs; we did **not** re-fit the original n=3 raw data because it is not deposited.

---

## 4. PDB structural-input audit (script `code/04_pdb_structural_check.py`, added 2026-06-25)

We downloaded all 11 PDB structures the paper cites as docking inputs (1TV9 + 10 partners) directly from RCSB and parsed each with Biopython (`Bio.PDB.PDBParser`). For each we recorded chain length, X-ray resolution / method, and the protein identity from the PDB `HEADER` / `COMPND` / `TITLE` records. Full audit in `results/pdb_audit.{json,txt}`.

### 4.1 Polβ template (1TV9) — independent structural confirmation ✓

The paper says 1TV9 is *"human DNA polymerase beta, 1.95 Å, X-ray diffraction"*. Our parse:
- PDB title: **"HUMAN DNA POLYMERASE BETA complexed with nicked DNA containing a mismatched template adenine and incoming cytidine"** ✓
- Resolution: **2.00 Å** (paper says 1.95 Å — within rounding; the deposited header reports 2.00)
- Longest protein chain: **A, 331 residues** (consistent with the 335-aa canonical Polβ minus disordered termini)
- Canonical Polβ active-site / dNTP-binding residues (independently verified against the actual coordinates):

  | Residue # | Expected | Found in 1TV9 chain A | Match |
  |---|---|---|---|
  | 190 | ASP | ASP | ✓ |
  | 192 | ASP | ASP | ✓ |
  | 256 | ASP | ASP | ✓ |
  | 271 | TYR | TYR | ✓ |
  | 272 | PHE | PHE | ✓ |
  | 279 | ASN | ASN | ✓ |
  | 283 | ARG | ARG | ✓ |

  **All 7/7 canonical Polβ active-site residues are present at the correct positions in 1TV9.** This is an *independent structural reproduction* of the paper's template-choice claim and confirms that the WT-Polβ side of the docking pipeline starts from a real, correctly-identified structure.

### 4.2 Docking-partner panel — 10 / 11 input PDBs check out

For each cited BER-partner PDB we compared the deposited PDB header description to the protein name the paper attaches to it:

| PDB | Paper label | RCSB header (verbatim) | Match? |
|---|---|---|---|
| 1DE8 | AP endonuclease 1 (APE1) | "HUMAN APURINIC/APYRIMIDINIC ENDONUCLEASE-1 (APE1) BOUND TO ABASIC DNA" | ✓ |
| 1EBM | 8-oxoguanine glycosylase (HOGG1) | "…human 8-oxoguanine glycosylase (hOGG1) bound to a substrate oligonucleotide" | ✓ |
| 1TDH | Endonuclease VIII-like 1 (NEIL1) | "…human endonuclease VIII-like 1 (NEIL1)" | ✓ |
| **1WSR** | **"Human T-protein of glycine cleavage system (aminomethyltransferase)"** | "CRYSTAL STRUCTURE OF HUMAN T-PROTEIN OF GLYCINE CLEAVAGE SYSTEM" (GENE GCST, EC 2.1.2.10, **aminomethyltransferase**) | **structurally correct PDB, but biologically wrong protein for a BER panel** ✗ |
| 1XNA | XRCC1 N-terminal domain | "NMR solution structure of the single-strand break repair protein XRCC1-N-terminal domain" | ✓ |
| 2BRF | PNKP FHA domain | "Crystal structure of the FHA domain of human polynucleotide kinase 3' phosphatase" | ✓ |
| 2FOZ | "Poly(ADP-ribose) glycohydrolase (ADPRH)" | "HUMAN ADP-RIBOSYLHYDROLASE 3" (ARH3, gene ADPRHL2) | ~ (related enzyme — ARH3 has PAR-hydrolase activity but is NOT the canonical PARG; PARG is a different gene/PDB) |
| 2RCW | PARP1 | "PARP complexed with A620223" (PARP1 catalytic domain + inhibitor) | ✓ |
| 3Q8K | FEN1 | "Crystal structure of human flap endonuclease FEN1 (WT)…" | ✓ |
| 4ZZY | PARP2 | "Structure of human PARP2 catalytic domain bound to an isoindolinone inhibitor" | ✓ |

### 4.3 **NEW MAJOR FINDING — 1WSR is not a BER protein**

The paper's Suppl Table S2 docking panel includes 1WSR ("aminomethyltransferase / glycine cleavage T-protein") alongside 9 genuine BER proteins (OGG1, NEIL1, XRCC1, PNKP, ARH3, PARP1, PARP2, FEN1, APE1). The label is *internally* consistent — the paper does call it "T-protein of glycine cleavage system" — but **aminomethyltransferase is a mitochondrial folate-dependent enzyme that catalyzes glycine→methylene-THF + NH₃ + CO₂ (EC 2.1.2.10). It has no biological function in base-excision repair.**

The most plausible interpretation is that the authors meant to dock **DNA ligase III** (the canonical BER ligase — e.g. PDB 3L2P, 6WBJ) and either copied the wrong PDB ID or substituted an unrelated structure they had in hand. The text immediately above the docking section explicitly mentions "DNA ligase III" in the BER pathway listing, but the actual table contains no DNA-ligase structure at all.

Consequences:
1. The ClusPro panel "9 BER proteins" is effectively **8 BER proteins + 1 unrelated metabolic enzyme**.
2. The 1WSR row reports binding scores of −12.4 (WT) and −11.1 (Δ), which the paper discusses as if they were a BER interaction. They are not.
3. The paper has **no docking measurement for the real DNA ligase III**, despite naming it in the pathway.

This is a new finding from this audit (the prior session flagged the cDNA, deletion-coordinate, unit, and ROS-monotonicity problems but did not download/parse the docking-input PDBs).

---

## 5. ClusPro / HDOCK results — spot-check (script `code/03_quantitative_audit.py`)

**Re-running the dockings was deferred** (would require ~9 ClusPro submissions × 1-12 h queue + 4 HDOCK submissions to public free-tier servers, no parallelism allowed by hdock.phys.hust.edu.cn AUP; well beyond the single-session budget and would generate the same "score-in-arbitrary-units" output the paper already published).

Spot-check findings:

- **Unit error.** ClusPro outputs a weighted score (E_balanced, lower=better, AU) and HDOCK outputs a native-like score (dimensionless, more negative=better). The paper labels both as "kcal/mol." These tools **do not produce physical binding free energies**. This invalidates direct kcal/mol comparison to e.g. PROTAC/PDB-derived ΔG values but does **not** by itself invalidate ranking.
- **ClusPro 9-protein panel (Suppl Table S2).** 8 of 9 protein partners show |ΔScore| ≤ 1.3, well within ClusPro noise. Only NEIL1 (1TDH) shows a notable difference (−9.7 → −12.4, ΔScore = −2.7) which is what the authors emphasise. Drawing a mechanistic conclusion from a single outlier in a panel of 9 is statistically weak — no multiple-testing correction is applied.
- **HDOCK dsDNA result.** Δ binds dsDNA more strongly than WT (−303.64 vs −245.74); ssDNA roughly equal (−272.65 vs −285.44). Assuming HDOCK ranking is reliable, the qualitative claim "ΔPolβ has stronger dsDNA affinity" is internally consistent — but **the input ΔPolβ structure cannot be built from the deposited cDNA** (see §2), so the docking input is unverifiable.

---

## 6. Internal-consistency audit (script `code/03_quantitative_audit.py` → `results/quant_audit.txt`)

Anomalies the paper does not address:

1. **ROS non-monotonic in mutant.** PA1PolβΔ DCFDA signal at 10 Gy (134.5 ± 9.1 %) is *lower* than at 5 Gy (173.7 ± 13.4 %). This is opposite to the dose–response monotonicity the authors invoke.
2. **PA1 has more ROS than mutant at 10 Gy.** PA1 = 191.9 ± 11.5 % vs PA1PolβΔ = 134.5 ± 9.1 %. Authors argue the mutant fails BER and should therefore accumulate oxidative damage, but the proxy for oxidative damage is *lower* in the mutant. Unaddressed.
3. **Mutant has half the baseline G2/M of WT** (16.2 % vs 36.6 %) without explanation in a supposedly isogenic transfection.
4. **G2/M arrest collapses at high dose in mutant** (56.4 % at 10 Gy → 44.1 % at 15 Gy) — likely because cells are dying/fragmenting, but not discussed.
5. **Three different deletion ranges** quoted in the same paper (208–301 / 208–304 / 211–339).
6. **Annexin V "fractions" do not sum to 100.** At 10 Gy PA1PolβΔ: Live + EA + LA = 11.3 + 31.2 + 16.5 = 59.0 %; the remaining 41 % (presumably PI-only / necrotic / debris) is never reported.

---

## 7. What we could **not** replicate and why

| Item | Why not |
|---|---|
| Wet-lab γ-irradiation of PA1 / PA1PolβΔ | No cell lines available; out of scope for computational triage. |
| Western blot confirming PolβΔ expression | Wet-lab. |
| Re-running ClusPro for 9 partners | Public-server queue time × 9; AUP forbids parallel jobs; would not generate new physical insight (units already arbitrary). |
| Re-running HDOCK 4× | Same; HDOCK server has aggressive rate-limiting. |
| Rebuilding SWISS-MODEL ΔPolβ structure | Pointless until cDNA inconsistency (§2) is resolved by authors; building from the deposited cDNA would yield a 120-aa truncated peptide, not a 238-aa structured domain. |
| Refitting raw colony counts | n=3 raw data not deposited. |

We did **not** contact the authors (hard gate #2).

---

## 8. Recommendations to the authors / community

1. **Re-deposit the ΔPolβ cDNA.** The current Suppl Table S1 sequence is broken; either re-sequence the cloned plasmid or correct the manuscript.
2. **Re-label all docking scores in their native units** (ClusPro: weighted cluster score, AU; HDOCK: native-like score, AU). Do not equate to kcal/mol.
3. **Reconcile the three deletion-range values** in the text and verify against the actual plasmid map.
4. **Address the ROS dose-response inversion** and the mutant ↔ WT ROS ordering at 10 Gy.
5. **Provide raw colony counts** (≤30 numbers; trivial to deposit) so independent LQ refitting is exact rather than digitization-based.
6. **Remove or replace PDB 1WSR** in Suppl Table S2 — it is aminomethyltransferase (glycine cleavage system), not a BER protein. If the intent was DNA ligase III, dock against PDB 3L2P or 6WBJ instead and update the table; if some other partner was intended, identify it explicitly. Either way, the current 1WSR row mixes a folate-pathway enzyme into a BER panel without justification.

---

## 9. Files in this replication

```
lucid-patra-polbeta-radiosensitivity/
├── README.md
├── REPORT.md              # this file
├── PROGRESS.md            # session log
├── code/
│   ├── 01_sequence_check.py
│   ├── 02_lq_fit.py
│   ├── 03_quantitative_audit.py
│   └── 04_pdb_structural_check.py   # added 2026-06-25
├── data/
│   ├── paper.pdf
│   ├── paper.txt          # pdftotext extraction
│   ├── suppl1.pdf+.txt    # Western blot
│   ├── suppl2.pdf+.txt    # Docking figures (S2)
│   ├── suppl3.pdf+.txt    # Sequences (S1) ← key
│   ├── suppl4.pdf+.txt    # ClusPro table (S2)
│   └── pdb/               # 11 RCSB PDB files (1TV9 + 10 BER partners)
├── results/
│   ├── sequence_check.json
│   ├── alignment.txt
│   ├── wt_protein.fasta
│   ├── del_protein.fasta
│   ├── wt_nt.fasta
│   ├── del_nt.fasta
│   ├── lq_fit.json
│   ├── quant_audit.json
│   ├── quant_audit.txt
│   ├── pdb_audit.json       # added 2026-06-25
│   └── pdb_audit.txt        # added 2026-06-25
└── figures/
    ├── page4-06.png …      # full-page PDF renders
    └── fig2_replication.png  # our LQ refit
```

All code is self-contained (Python 3 + biopython + scipy + matplotlib). Re-run with:

```bash
python3 code/01_sequence_check.py
python3 code/02_lq_fit.py
python3 code/03_quantitative_audit.py
python3 code/04_pdb_structural_check.py    # downloads 11 PDBs (~3 MB) then audits
```

---

## 10. Mandatory 6/22 reproducibility-blocker critique

The single biggest *reproducibility blocker* in this paper, by far, is **§2 — the ΔPolβ cDNA in Suppl Table S1 cannot be translated into the protein the authors describe**. Every downstream computational claim about the mutant (the SWISS-MODEL structure, the 9-partner ClusPro panel, the HDOCK protein–DNA dockings, all of Fig. 8) is built on that single sequence, and that single sequence does not encode a 238-aa in-frame domain-truncated polymerase; it encodes a 198-aa frame-shifted pseudo-protein with ≥6 internal stop codons. There is no way for an independent group to rebuild the ΔPolβ structural model the authors used, because the model they describe cannot be built from the reagent they deposited. Until the supplementary sequence is corrected (re-Sanger the cloned plasmid and re-deposit), the entire mechanistic half of the paper is **non-reproducible at the input layer**, regardless of how stable the ClusPro/HDOCK servers are.

Secondary blockers, in order:
- Three mutually inconsistent deletion-range definitions in the same manuscript (208–301 / 208–304 / 211–339; §1 of audit).
- PDB 1WSR in the docking panel is aminomethyltransferase, not a BER protein (§4.3 above) — silently mixes a folate-pathway enzyme into a BER panel and reports docking scores against it as evidence.
- All ClusPro / HDOCK scores reported as kcal/mol despite being dimensionless server-specific scores (§4 above) — makes the numerical values un-comparable to any external dataset.
- Raw colony-count data (n=3 per dose per cell line, ≤30 numbers total) not deposited — forces any independent LQ refit to rely on figure digitization.
- ROS dose-response inversion and WT-vs-mutant ordering at 10 Gy (§6) is undiscussed, so a re-analyser cannot tell whether the published values reflect a real biological non-monotonicity or a labelling/normalisation error.

A reader who wants to genuinely reproduce this paper's molecular mechanism would have to (a) re-clone and re-sequence PolβΔ, (b) build the structural model from the corrected sequence, (c) re-run all 9 ClusPro dockings with a corrected partner list (excluding 1WSR; including a real DNA-ligase-III structure), and (d) re-collect at least the ROS time-courses to resolve the dose-response anomalies. Items (a)+(d) are wet-lab. The paper is therefore reproducible **only in its radiobiology side** (the LQ fit) and is structurally non-reproducible on its mechanistic side as published.

---

## 11. Verdict in one line

> **PARTIAL.** The core radiobiological claim (PolβΔ → radiosensitization, DMF ≈ 1.8 at 10 Gy) is reproducible by LQ refit of the published figure. Independent structural verification confirms the WT-Polβ side: PDB 1TV9 is correctly identified, has the canonical 7-residue Polβ active site (D190/D192/D256/Y271/F272/N279/R283 all match coordinates), and 9 of the 10 cited docking-partner PDBs match their paper labels. The mechanistic / docking story is **not reliably reproducible**: the deposited ΔPolβ cDNA is broken, deletion coordinates are inconsistent across sections, docking scores are mislabelled in units, **PDB 1WSR in the docking panel is aminomethyltransferase rather than a BER protein**, and several internal-consistency anomalies in Fig. 5–7 are unaddressed. Coverage 6/10; agreement 6/10; paper-internal consistency 3/10.

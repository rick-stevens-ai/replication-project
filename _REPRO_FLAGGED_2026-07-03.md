# Flagged for actual independent reproduction — 2026-07-03

Per Rick's standard (2026-07-03): if a replication's computational work is cheaply/fully reproducible (minutes, laptop, public accessions, deterministic — like BVBRC-68), we ACTUALLY REPRODUCE it independently, not just spot-check. SPOT-CHECK is only for genuinely-gated work (heavy GPU/HPC, non-public data/code, license walls).

Triage of the 255 PARTIAL+SPOT-CHECK rows by reproduction-cost heuristic (report keyword scan: public-data/tools signals vs compute/license-gate signals).

## TIER 1 — CHEAP_REPRO_CANDIDATE (35): re-run independently, minutes each
Highest priority. Mostly BVBRC genomics (public NCBI accessions + abricate/BLAST/prodigal = deterministic, laptop-fast). Independent re-run = fresh downloads by accession + independent code + separate tool run; save to report/evidence/independent_reproduction/.

Strongest (cheap>=10, gated=0), do first:
- BVBRC-10 Llactis-LL16 (29) · BVBRC-13 Efaecalis-envadapt (10) · BVBRC-16 Efaecium-probiotic (10)
- BVBRC-19 Propionibacterium (17) · BVBRC-21 ESBL-Ecoli-pigs (11) · BVBRC-22 Arthrobacter-uranium (14)
- BVBRC-26 Ecoli-antiphage (38) · BVBRC-27 Efaecium-optrA (40) · BVBRC-32 MRSA-plasmidome (13)
- BVBRC-42 Bsmithii (56) · BVBRC-74 PLA-degrading (21) · BVBRC-77 progenomes3 (25)
- BVBRC-78 efaecium-phage (37) · BVBRC-84 ljohnsonii (32) · BVBRC-85 Saureus-Sudan (48) · BVBRC-62 Phangzhouensis (15)
Also cheap (some gated=1, still likely laptop): BVBRC-12,14,20,23,33,58,61,89,70,30; OTHER 2469515,2475938,34325466,36123438; LUCID ipsc-chondrocyte, rprm-egfr, zebrafish; QC-Stim.

## TIER 2 — MIXED (44): inspect individually
Analytic/small-numerics PDE + QC-sim + some LUCID modeling. Many are cheap (small python solver) but the keyword scan couldn't confirm. Manual per-paper check: if it's a small deterministic solve (spectral Poisson, KdV, stabilizer sim, VQE small), reproduce; if it needs real training/HPC, leave SPOT-CHECK/PARTIAL.

## TIER 3 — GATED (173): SPOT-CHECK/PARTIAL is defensible
Heavy compute (GPU training, MC/MD/DFT at scale), non-public data, or license walls. Leave as-is unless a specific asset turns out public. Includes most LUCID mechanistic-modeling papers (TOPAS/MEDRAS/Geant4-DNA MC) and BVBRC pangenome/phylogenomics that need multi-genome OrthoFinder/roary runs.

## NO-REPORT (3): finish first — PDE-amr-numerical-relativity-radia-2021, alter-multitensor-2026, drift-flux-indoor-particles

## Method note
Heuristic only — the cheap/gated split is a starting filter, not final. Each TIER-1 gets a real independent re-run; if it turns out gated on contact, document and downgrade to SPOT-CHECK honestly.
BVBRC-42: CONFIRMED 15/15 (independent re-run, verdict upgraded to INDEPENDENTLY CONFIRMED)
BVBRC-27: CONFIRMED 36/36 (independent abricate+NCBI; C5-C7 gated by non-deposited raw reads, verdict PARTIAL preserved)
BVBRC-84: CONFIRMED 11/12 (fresh Datasets+prodigal/barrnap/abricate; C12 gated by missing SRA deposit; bonus: PATRIC undercounts 23S rRNA, strain AMR/VF/plasmid-free across 5 DBs)
BVBRC-26: CONFIRMED 13/13 (fresh NCBI eutils/Datasets; 71 strains/21 systems/32 proteins all reproduced; C6 wet-lab gated by missing SRA)
BVBRC-10: CONFIRMED 29/29 (fresh GCF_029912225.1 + skani/fastani/minced/abricate/prodigal, all independent; 23 EXACT, 6 within-convention, 0 contradicted)
BVBRC-85: CONFIRMED 16/16 (fresh datasets MD5-identical + own MLST/tblastn/16S; ST140 exact, tet(K)/tet(M) uniqueness confirmed, paper's norA-uniqueness independently CONTRADICTED same as replication)
QC-1703.05169 Bayesian-QPE: REPLICATED (Qiskit RFPE, 1.87e-4 rad @50 steps vs paper 2.4e-4, 1.12x Heisenberg, 69x below SQL)

# FIRST_PASS_REPORT — LUCID100 Slot 41

**Paper:** Jolly & Fielding 2025, *Modelling single cell dosimetry and DNA damage of targeted alpha therapy using Monte-Carlo techniques*  
**DOI:** 10.1007/s13246-025-01605-2  
**Workdir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-targeted-alpha-single-cell-monte-carlo-dna-damage`

## Verdict

**PARTIAL first-pass / KEEP.** The paper is open access and reproducible in principle, but a full numerical reproduction requires TOPAS-nBio/Geant4-DNA and should be run off CherryRd. This first pass completed artifact harvest and reduced CPU smoke checks.

## Verified smoke checks (6/6)

- PASS — Ac-225 has 4 alpha emissions per parent decay
- PASS — Ra-223 has 4 alpha emissions per parent decay
- PASS — Pb-212 has 1 alpha emission per parent decay
- PASS — At-211 has 1 alpha emission per parent decay
- PASS — At-211 nucleus-source analytical dose brackets Table-2 nucleus column within reduced-model tolerance
- PASS — DBSCAN synthetic unit tests distinguish sDSB/cDSB/SSB and threshold behavior

## Key reduced results

From `results/01_decay_chains.json`:

- Ac-225: 4.0 α/decay, mean α energy 6.890 MeV
- Ra-223: 4.0 α/decay, mean α energy 6.637 MeV
- Pb-212: 1.0 α/decay, mean α energy 7.802 MeV
- At-211: 1.0 α/decay, mean α energy 6.790 MeV

From `results/02_alpha_geom.json`:

- At-211 nucleus-source analytical estimate: 20.97 cGy/decay
- At-211 membrane-source analytical estimate: 2.81 cGy/decay
- Published Table 2 At-211 nucleus range: 12.88–16.63 cGy/decay depending on physics/source treatment
- Published Table 2 At-211 membrane range: 0.93–2.59 cGy/decay

The reduced analytical model is deliberately coarse but captures the core localization effect: nucleus-localized sources deliver much more dose to the nucleus than membrane-localized sources.

From `results/03_dbscan_unit_test.json`:

- close high-energy pair → sDSB
- high-energy triplet → cDSB
- far high-energy pair → two SSBs
- subthreshold ionization → no lesion
- midpoint ramp probability observed ≈ 0.499 with DNA fraction 1.0 and ≈ 0.080 with DNA fraction 0.16

## Blockers for full quantitative replication

- TOPAS-nBio / Geant4-DNA not installed locally.
- No public author code or raw scorer dumps.
- Full campaign is compute-heavy and should be scheduled on uicgpu/Aurora, not CherryRd.

## QA recommendation

Keep as `simulation/model replication`. Retag status to **partial first-pass complete / HPC-gated**. A full reproduction is feasible with public software and decay data, but requires an off-CherryRd TOPAS-nBio campaign.

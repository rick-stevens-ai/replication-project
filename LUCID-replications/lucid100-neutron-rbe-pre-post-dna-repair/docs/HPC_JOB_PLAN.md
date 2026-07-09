# HPC job plan — full pipeline re-run

DOI: 10.1088/1361-6560/ae36e1

Use this plan if a follow-up run wants exact reproduction of the paper's
Table-2 / Figure-3 / Figure-4 numerics rather than the reduced-analytic
smoke that this folder ships.

**Do NOT execute the heavy compute on CherryRd.** Suitable targets:

* **uicgpu** — 2 TB RAM, but TOPAS-nBio is CPU-bound so memory is overkill;
  fine for medium-scale runs and dev/iteration of the SDD clusterer at scale.
* **Aurora** (PBS, allocation `datascience`) — best for the per-energy
  embarrassingly-parallel array (18 neutron energies × 3 secondaries × 100
  reps + 950 photon reps). Wide CPU parallelism, low job latency.
* **CELS compute-11..15** — fine for the SDD clusterer post-processing of
  the Zenodo 690 MB Data.zip (pure Python, NumPy only).

## Software stack required

| Component       | Version (paper)        | Notes                                                |
| --------------- | ---------------------- | ---------------------------------------------------- |
| Geant4          | v10.04.p02             | with the DNA extension                               |
| Geant4-DNA      | matching v10.04.p02    | physics list `G4EmDNAPhysics_hybrid2and4`           |
| TOPAS           | v3.6.1                 | needs a TOPAS license token (free for research)      |
| TOPAS-nBio      | v1.0                   | bundles DaMaRiS                                      |
| Python          | ≥ 3.10, numpy ≥ 1.24   | for the clusterer                                    |

All TOPAS / Geant4 build inputs live in
`artifacts/code_SDD-Scorer/` (see ARTIFACT_MANIFEST.md). The author
ships the TOPAS extension as source — no precompiled binary.

## Pipeline (mirrors paper Sections 2.2-2.5)

1. **CHMC step** — already done by the authors (Lund 2020). The relative
   dose fractions `d_S(E)` for all 18 neutron energies in the outer 1.5 cm
   scoring volume are shipped in
   `artifacts/code_SDD-Scorer/payload/supportFiles/relative_doses/`.
   **No need to re-run CHMC**; just consume these files. If a re-run is
   wanted, source = Geant4 only, ICRU-4 30 cm sphere, mono-energetic
   neutron source, inversely isotropic distribution.

2. **TSMC / DNA damage step (heavy)** — per neutron energy E:
   * For S ∈ {electron, proton, alpha}, sample secondary spectrum from
     the CHMC output, set
     `s:So/Example/BeamEnergySpectrumType = "Continuous"` (paper's choice),
     target 1 Gy, run 100 repeats. Score in SDD format.
   * For 250 keV photons (electrons only), run 950 repeats.
   * Walltime budget: ~ 4–6 CPU-hours per repeat → ~ (18 × 3 × 100 + 950)
     ≈ 6 350 repeats → ~ 25–40 k CPU-h end-to-end.
   * Embarrassingly parallel; one TOPAS process per repeat per core.
   * Output: SDD files (the same format as `zenodo:17087505/Data.zip`).

3. **Pre-repair endpoint clustering (light)** — feed each SDD file into
   `payload/ComplexDSbCounter.py::clusterer(path, eps)` where `eps`
   is the list of Euclidean distances to evaluate (paper sweeps 11–300 nm).
   Aggregate yields, then apply Eq. 5 (sum over species weighted by
   `d_S / D_S`) and Eq. 6 (RBE = `Y_n(E)/Y_X`). The reduced-analytic
   smoke in this folder shows that once per-energy `Y_S` are available,
   reproducing Figures 3 and 6(b) is a few lines of NumPy.

4. **Post-repair (misrepair) endpoint (medium)** — pipe each SDD file
   through DaMaRiS NHEJ (default 24 h repair time, the cubic-nucleus
   circumscribed sphere, radius 6.755 µm) and count DSB ends that joined
   to ends from a different DSB site. Walltime budget: ~ 2–4 CPU-h per
   SDD file → ~ 25 k CPU-h additional.

## Cheap-pull intermediate option

If the goal is just to re-run **Steps 3 and 4** (clusterer + DaMaRiS) using
the authors' SDD outputs:

* Pull `zenodo:17087505/Data.zip` once on the HPC target (690 MB).
* Skip Step 2 entirely. Walltime ~ 25–30 k CPU-h for DaMaRiS only +
  minutes for the clusterer.

This is the **lowest-cost** path to a full numerical reproduction.

## Verification gates

* **Smoke parity** (CherryRd CPU) — Eq. 5/Eq. 6 maxima match paper within
  ~ 10 % using shipped `d_S(E)`. See `smoke/smoke_report.txt`.
* **Per-energy Y_S parity** (HPC) — once TSMC is rerun, the per-energy
  Y_n(E) should match the paper's Figure 3 curves (DSB sites, complex
  DSB, DSB clusters) within statistical error (~ few %).
* **Misrepair parity** (HPC) — Y_misrep(E) curve from DaMaRiS should
  peak at 0.5 MeV with RBE = 23(1) per Section 4.4.
* **Code parity** — the synthetic block-table test in
  `smoke/smoke_eq5_eq6_rbe.py` confirms `ComplexDSbCounter.py` is wireable;
  re-running it on a sample of `Data.zip` SDD files should reproduce
  the authors' published yields per energy.

## Out of scope

* Reimplementing the TOPAS extension itself (`scoring/`, `topas_mods/`)
  — the author code is MIT licensed; reuse, don't rewrite.
* Bench-marking against PARTRAC (Baiocco 2016) or PHITS (Mentana 2025)
  — those would be separate replications.

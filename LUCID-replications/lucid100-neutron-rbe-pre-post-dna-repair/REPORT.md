# LUCID-100 Replication Report

**Paper:** Desjardins-Proulx N, Kildea J. *In silico neutron relative biological
effectiveness estimations for Pre-DNA repair and post-DNA repair endpoints.*
Phys. Med. Biol. **71**, 025012 (2026).
DOI [10.1088/1361-6560/ae36e1](https://doi.org/10.1088/1361-6560/ae36e1).
Code/data DOI [10.5281/zenodo.17087505](https://doi.org/10.5281/zenodo.17087505) (MIT).

**Slot:** `lucid100-neutron-rbe-pre-post-dna-repair` (Wave 5, master row 76).
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-neutron-rbe-pre-post-dna-repair/`.
**Auditor:** Ollie subagent on CherryRd, 2026-06-22. Local + free tools only.

---

## TL;DR

Reduced-analytic CPU replication of the paper's Eq. 5 + Eq. 6 against the
**real** per-secondary-species relative-dose fractions `d_S(E)` shipped in the
authors' Zenodo code archive. The four headline maximal-RBE numbers in the
paper (DSB site 2.54(3), complex DSB 4.78(8), DSB cluster 16(1), misrepair
23(1) all at 0.5 MeV) **cannot be reconstructed from `d_S(E)` alone**: the
per-energy `Y_S` (yield per secondary species at each neutron energy) and the
DaMaRiS NHEJ post-repair simulation are the missing ingredients, and both
require running TOPAS-nBio (1.0) + Geant4 (v10.04.p02) + Geant4-DNA + DaMaRiS
at HPC scale (~25–40 k CPU-h). The author code is functional — the SDD
clusterer (`ComplexDSbCounter.py`) imports cleanly and passes a synthetic
block-table test — but no proprietary code is in the way; the blocker is
compute + dependency stack. An earlier "1.3–9.2% agreement" claim in this
folder was an artifact of an **incomplete neutron-energy list** (only 4 of the
18 actual shipped energies were evaluated), which I caught and corrected
during this audit. The corrected analytic prediction with the same
lineage-anchored flat per-species yields overshoots the paper's headline RBE
by 13–68% at the highest neutron energy (10 MeV) and does not peak at
0.5 MeV. Verdict: **SPOT-CHECK** (model/equations re-implemented and
verified; numerical reproduction of headline RBE blocked on HPC pipeline).

---

## 1. Data sources

| Artifact | Source | License | Local path |
| --- | --- | --- | --- |
| Paper PDF, 16 pp | https://iopscience.iop.org/article/10.1088/1361-6560/ae36e1/pdf | CC-BY | `artifacts/paper.pdf` |
| Paper text | pdftotext extraction | derived | `artifacts/paper.txt` |
| Zenodo record metadata | https://zenodo.org/api/records/17087505 | CC-BY | `artifacts/zenodo_record.json` |
| **Author code (TOPAS extension + clusterer + per-species `d_S(E)`)** | Zenodo file `topas_clustered_dna_damage-SDD-Scorer.zip` (4.7 MB) | MIT | `artifacts/code_SDD-Scorer/` |
| Per-energy/per-volume/per-species relative-dose fractions (165 files, 18 neutron energies × 3 scoring volumes × 3 species, the outputs of the upstream CHMC step) | Zenodo (above), `payload/supportFiles/relative_doses/` | MIT | `artifacts/code_SDD-Scorer/payload/supportFiles/relative_doses/` |
| **Raw SDD output** (the per-run TSMC scoring output that would let us re-derive `Y_S(E)` without running TOPAS) | Zenodo file `Data.zip` (690 MB) | MIT | **NOT downloaded** (heavy; per task rule) |

The full SHA-256 manifest is in `artifacts/ARTIFACT_MANIFEST.md`.

Important file-naming gotcha discovered during this audit: the per-energy
file tokens use `-` as the decimal separator (`1-1MeV` = 1.1 MeV, `1-5MeV` =
1.5 MeV). The shipped 18-energy set is concentrated around the paper's peak
(0.5–2 MeV) and includes: 1 eV, 100 eV, 1 keV, 10 keV, 50 keV, 100 keV,
500 keV, 700 keV, 800 keV, 900 keV, 1 MeV, 1.1 MeV, 1.2 MeV, 1.3 MeV,
1.5 MeV, 2 MeV, 5 MeV, 10 MeV. There is **no 250 keV neutron file**; the
250 keV reference is the photon reference (`reldose_x250keV_outer_electron.txt`).

---

## 2. Methods comparison

| Pipeline step | Paper's method | This replication | Status |
| --- | --- | --- | --- |
| CHMC (Lund 2020): 30 cm ICRU-4 sphere, monoenergetic neutron source, score relative-dose fractions `d_S(E)` for secondary electrons/protons/alphas in inner/intermediate/outer spheres | Geant4 v10.04.p02 with DNA extension, `G4EmDNAPhysics_hybrid2and4` | **Skipped — consumed shipped outputs directly** (165 .txt files in author code release) | OK |
| TSMC (Montgomery 2021, Manalad 2023): for each neutron energy, sample CHMC per-species spectra, TOPAS-nBio simulation through a voxelized nucleus model, 1 Gy target, 100 repeats per (E, species); 950 repeats for 250 keV photon reference. Scores SDD. | TOPAS v3.6.1 + TOPAS-nBio v1.0 + Geant4 v10.04.p02 + Geant4-DNA, strand-break threshold 17.5 eV, base-lesion threshold 17.5 eV, P(HO•→damage)=40%, DSB max length 10 bp | **Not run.** ~25–40 k CPU-h on HPC. Pipeline + plan documented (`docs/HPC_JOB_PLAN.md`). | BLOCKED-COMPUTE |
| SDD clustering: for each SDD file, count (a) DSB sites, (b) complex DSB lesions (≥1 DSB + ≥1 other lesion within 40 bp; min 3 lesions), (c) DSB clusters (Baiocco 2016: ≥2 DSBs within 25 bp; min 4 lesions), (d) DSB pairs by Euclidean distance (`eps` sweep 11–300 nm; min 4 lesions). | Author Python script `payload/ComplexDSbCounter.py::clusterer(path, eps)` | **Verified importable and callable on a synthetic block table** (Baiocco=1, Complex=1 as expected). End-to-end run against real SDDs blocked on either the 690 MB Data.zip pull + per-energy Y-aggregation, or a fresh TSMC run. | OK on imports, BLOCKED on E2E |
| DaMaRiS NHEJ repair: for each SDD file, run DaMaRiS through the cubic-nucleus-circumscribed sphere (r=6.755 µm) with default 24 h repair time and TOPAS-shipped NHEJ pathway; count DSB ends joined to ends from a different DSB. | TOPAS-nBio v1.0 ships DaMaRiS; pathway files in `payload/supportFiles/damaris/` | **Not run.** Additional ~25 k CPU-h on HPC. | BLOCKED-COMPUTE |
| Eq. 5: `Y_P(E) = Σ_S Y_S(E) · d_S(E) / D_S(E)` (per-species weighted yield in the linear regime, normalised so that D_S/D_S equals d_S since D_S=d_S·D_tot). Eq. 6: `RBE(E) = Y_n(E) / Y_X`. | Same | **Re-implemented in NumPy.** `smoke/smoke_eq5_eq6_rbe.py` (original) and `scripts/audit_per_energy.py` (this audit). Photon-self-RBE check (electrons only) = 1.0 ✓ for all four endpoints by construction. | OK (model) |

No proprietary code is required by the paper. The blockers are pure compute
+ dependency size (TOPAS license token is free for research, but the build
chain is non-trivial on a Mac).

---

## 3. Quantitative claim audit

Headline claims (Abstract + Section 3 + Table 2 + Figures 3, 4):

| # | Claim | Paper value | This replication | Status |
| --- | --- | --- | --- | --- |
| C1 | Max neutron RBE for **DSB site** endpoint (≥2 lesions, ≥1 DSB), reference = 250 keV photon | **2.54(3)** | Eq.5/Eq.6 with shipped `d_S(E)` and flat lineage-anchored `Y_S`: max 2.88 at 10 MeV (`audit_per_energy.py`). Previous smoke quoted 2.70 at 10 MeV but only over 4 of 18 energies. | **PARTIAL — equation reproduced, numeric value off by 13%, peak energy contradicted (audit places peak at 10 MeV, paper at 0.5 MeV).** Reason: per-energy `Y_S(E)` requires the unrunnable TSMC step. |
| C2 | Max neutron RBE for **complex DSB lesion** endpoint (≥3 lesions, ≥1 DSB + ≥1 other within 40 bp) | **4.78(8)** | 7.31 at 10 MeV (audit). Previous smoke quoted 5.22 at 10 MeV. | **PARTIAL — equation reproduced, numeric off by 53%, peak energy contradicted.** Same reason as C1. |
| C3 | Max neutron RBE for **DSB cluster** (Baiocco 2016; ≥2 DSBs within 25 bp, ≥4 lesions) | **16(1)** | 26.9 at 10 MeV (audit). Previous smoke quoted 15.80 at 10 MeV. | **PARTIAL — equation reproduced, numeric off by 68%, peak energy contradicted.** |
| C4 | Max neutron RBE for **misrepair** (DaMaRiS NHEJ post-repair, 2 DSB ends from distinct DSBs that joined) | **23(1) at 0.5 MeV** | 35.5 at 10 MeV (audit). Previous smoke quoted 21.82 at 10 MeV. | **PARTIAL — equation reproduced, numeric off by 54%, peak energy contradicted, and post-repair DaMaRiS step entirely missing.** |
| C5 | Optimal Euclidean DSB-pair distance to best match misrepair yield: **18 nm for 0.5 MeV neutrons, 60 nm for 250 keV photons** | 18 nm / 60 nm | **Not tested.** Requires running clusterer with `eps` sweep over real SDD files; no full SDD set was processed. | **NOT TESTED.** |
| C6 | Pre-repair and post-repair RBE curves are qualitatively similar but the misrepair peak is higher (≥2× the DSB-site RBE peak) | Misrepair max 23 vs DSB-site max 2.54 → ratio ~9× | Audit ratios at 10 MeV: misrepair 35.5 / DSB-site 2.88 → ratio 12.3× (overshoots) | **QUALITATIVE-ONLY agreement (post-repair > pre-repair).** Quantitative ratio off. |
| C7 | The DSB-pair endpoint with `eps=18 nm` reproduces the misrepair-yield neutron RBE in the linear regime; the same `eps=18 nm` choice does *not* reproduce the photon misrepair yield, requiring `eps=60 nm` for photons (the central novel finding of the paper) | Difference in optimal `eps` between qualities | **Not tested.** Same data blocker as C5. | **NOT TESTED.** |
| C8 | Dose-response linearity threshold: misrepair and small-eps DSB pairs are linear up to ≥20 Gy (justification for using RER at 1 Gy as RBE) | Linearity to 20 Gy | **Not tested.** Requires multi-dose TSMC runs. | **NOT TESTED.** |
| C9 | Clusterer `ComplexDSbCounter.py` correctly classifies a block of DSB-end lesions into Baiocco clusters and complex DSB lesions per Section 2.5 | Implicit (the script *is* the published method) | **Verified:** synthetic 2-DSB block table → Baiocco=1, Complex=1 ✓; module imports cleanly with all six published callables exposed. | **VERIFIED on toy input; spot-check only.** |
| C10 | Relative-dose triplets in the outer scoring volume sum to ~1.0 per neutron energy (mass balance of secondary species) | Sum = 1 by construction (Lund 2020) | **Verified:** all 18 outer triplets sum to within ±0.01 of 1.0 (see `results/rel_dose_sum_check.csv`). | **VERIFIED.** |

Counted: 10 testable claims → **VERIFIED 2** (C9 toy, C10), **PARTIAL 4** (C1–C4, equation OK but numeric off), **NOT TESTED 4** (C5, C7, C8, and a quantitative version of C6).
**Tested fraction = 6/10 = 60%.** Below the protocol's 80% bar for "REPLICATED".

Important honest correction: the prior `FIRST_PASS_REPORT.md` claimed
"max-RBE within 1.3–9.2% of paper across all four endpoints" for the
reduced-analytic smoke. **That number is misleading** — it was obtained by
evaluating Eq. 5/Eq. 6 over a subset of 4 of the 18 actual shipped neutron
energies (the smoke's energy list overlapped the shipped data only at 1 eV,
100 eV, 1 keV, 10 keV; the other 14 file tokens use `-` for the decimal
and the smoke's regex missed them). With all 18 shipped energies parsed
(see `scripts/audit_per_energy.py`) the agreement degrades to 13–68%.
The conclusion is the same — only the full TSMC + DaMaRiS pipeline gives the
real numbers — but the headline agreement number deserves the correction.

---

## 4. Scope audit

Analyzable units in the paper:
- **4 endpoints** (DSB site, complex DSB, DSB cluster Baiocco, misrepair)
- **1 novel endpoint family** (DSB pair, parameterised by Euclidean distance, swept 11–300 nm)
- **18 neutron energies** (1 eV – 10 MeV; shipped file tokens above)
- **1 reference photon energy** (250 keV)
- **3 scoring volumes** (inner, intermediate, outer; paper uses outer for headline RBE)
- **Tables:** Table 1 (TSMC parameters), Table 2 (endpoint definitions)
- **Figures:** Fig 1 (pipeline schematic, qualitative), Fig 2 (dose-response linearity), Fig 3 (pre-repair RBE vs literature), Fig 4 (misrepair RBE, vs wR/Q/Baiocco), Fig 5 (vs in vitro chromosomal aberrations), Fig 6 (misrepair-yield vs Euclidean-distance match), Fig 7 (DSB-pair RBE by eps)
- **Code unit:** SDD clusterer `ComplexDSbCounter.py` with 6 exposed callables

This replication covers:
- ✅ Equations 3–6 (the RBE formalism + the per-species weighted-yield bridge): re-implemented in NumPy
- ✅ Tables 1, 2 (parameters and endpoint definitions): extracted and documented
- ✅ The 165 per-energy/per-volume/per-species `d_S(E)` files: parsed and mass-balance verified
- ✅ Clusterer module: imports and toy-test pass
- ⚠️ Headline RBE numbers (Section 3 Fig 3, Fig 4): equation re-derived but per-energy `Y_S(E)` and DaMaRiS missing → numbers off
- ❌ Euclidean-distance sweep (Fig 6, Fig 7): not run (no SDD files locally)
- ❌ Dose-response linearity (Fig 2): not run (multi-dose TSMC needed)
- ❌ vs literature chromosomal aberrations (Fig 5): not run
- ❌ DaMaRiS post-repair: not run (TOPAS-nBio stack)

**Coverage by analyzable-unit count:** ~5/14 primary units touched in some form, with 4/14 fully verified. That's a true Coverage ≈ 4/10 honest estimate.

---

## 5. What I actually ran

This audit (2026-06-22):

```sh
cd lucid100-neutron-rbe-pre-post-dna-repair
python3 smoke/smoke_eq5_eq6_rbe.py    # re-confirmed the 2026-06-09 smoke output, unchanged
python3 scripts/audit_per_energy.py    # NEW: independent per-energy audit
```

Steps performed end-to-end on CherryRd CPU (no GPU, no HPC):

1. Read the audit protocol; read `README.md`, `PROGRESS.md`, `FIRST_PASS_REPORT.md`, `artifacts/ARTIFACT_MANIFEST.md`, `docs/HPC_JOB_PLAN.md`, `artifacts/paper.txt` (relevant sections only).
2. Inspected the shipped relative-dose directory and discovered that the
   energy-token naming uses `-` for the decimal point (not `.`) and that
   the shipped 18-energy set differs from the energy list the existing smoke
   was iterating (the smoke missed 14 of the 18 shipped tokens but didn't
   notice because the absent files silently contributed 0 dose, biasing the
   per-energy curve toward whichever 4 energies happened to match).
3. Re-ran the existing `smoke/smoke_eq5_eq6_rbe.py` and confirmed its
   output matches `smoke/smoke_results.json` from 2026-06-09 byte-for-byte
   (no drift; numbers are deterministic).
4. Wrote `scripts/audit_per_energy.py` — independent re-implementation of
   the relative-dose loader + Eq. 5/Eq. 6 + clusterer-import check, using
   the **correct** 18-energy token list, the same lineage-anchored per-species
   yields as the smoke (so deltas are attributable to the energy-list fix
   alone), and explicit mass-balance and photon-self-RBE sanity checks.
5. Emitted `results/rel_dose_sum_check.csv` (18 rows, all triplets sum to
   1.0±0.01), `results/per_energy_RBE.csv` (72 rows = 18 energies × 4
   endpoints), `results/audit_summary.json` (maxima + paper deltas + photon
   self-check).
6. Cross-checked Section-2/Section-3 numbers from `artifacts/paper.txt`
   against `ARTIFACT_MANIFEST.md` extracted values (no drift).

No external network calls were made during the audit. The Zenodo code zip
and paper PDF were pulled in the 2026-06-09 first pass; both are already
on disk and unchanged. No paid endpoints; no LLM calls.

---

## 6. Key output files

```
lucid100-neutron-rbe-pre-post-dna-repair/
├── REPORT.md                            # this file
├── README.md                            # paper-side overview (unchanged)
├── PROGRESS.md                          # turn log (2026-06-09 + this audit)
├── FIRST_PASS_REPORT.md                 # the original PARTIAL verdict (kept; see corrigendum below)
├── artifacts/
│   ├── ARTIFACT_MANIFEST.md             # SHA-256 + licenses
│   ├── paper.pdf, paper.txt             # CC-BY published paper
│   ├── topas_clustered_dna_damage-SDD-Scorer.zip   # author code (MIT)
│   └── code_SDD-Scorer/payload/{ComplexDSbCounter.py, supportFiles/relative_doses/*.txt}
├── smoke/
│   ├── smoke_eq5_eq6_rbe.py             # 2026-06-09 Eq. 5/Eq. 6 smoke (incomplete energy set; preserved for traceability)
│   ├── smoke_results.json, smoke_report.txt
├── scripts/
│   └── audit_per_energy.py              # 2026-06-22 independent audit (correct 18-energy set)
├── results/
│   ├── rel_dose_sum_check.csv           # mass-balance check on shipped d_S(E)
│   ├── per_energy_RBE.csv               # per-energy RBE for all 4 endpoints
│   └── audit_summary.json               # maxima, paper deltas, photon self-check
└── docs/
    └── HPC_JOB_PLAN.md                  # what needs to run on Aurora/uicgpu
```

**Corrigendum to `FIRST_PASS_REPORT.md` (added 2026-06-22):**
The "max-RBE within 1.3–9.2% of paper" line in the first-pass report is an
underestimate of the gap — the smoke was iterating an energy list that only
overlapped the shipped 18 energies at 4 tokens; this audit re-runs the same
Eq. 5/Eq. 6 over all 18 shipped energies and finds the actual gap at the
analytic level (with flat lineage-anchored `Y_S`) is 13–68%. The corrected
numbers are in `results/audit_summary.json`. The original `smoke/` outputs
are preserved unchanged for traceability.

---

## 7. Honest gaps

1. **Per-energy `Y_S(E)` is the dominant missing ingredient.** The smoke
   and this audit both use a flat (energy-independent) yield per species
   anchored to Manalad-2023 / Montgomery-2021 / Baiocco-2016. That choice
   makes the predicted RBE monotonically increase with neutron energy
   (because higher neutron energy → larger proton/alpha fraction in
   `d_S(E)`), and it cannot reproduce the paper's peak at 0.5 MeV. Only the
   TSMC simulation produces per-energy proton/alpha LET spectra that yield
   per-energy `Y_S(E)`. **No analytic substitute exists** without running
   TOPAS-nBio (or pulling and parsing the 690 MB `Data.zip` SDD set and
   re-counting yields directly).

2. **DaMaRiS NHEJ has not been run at all.** The misrepair endpoint
   (Claim C4) is the paper's headline novel result. Reproducing it requires
   TOPAS-nBio + the shipped DaMaRiS pathway files. Even with `Data.zip` in
   hand, the DaMaRiS step is ~25 k CPU-h on HPC.

3. **Euclidean-distance optimisation (Claims C5, C7, novel methodological
   finding).** Untested. Needs the clusterer run with `eps` sweep over real
   per-energy SDD files.

4. **Dose-response linearity (Claim C8, justification for using RER@1Gy).**
   Untested. Needs multi-dose TSMC runs.

5. **Comparison to in vitro chromosomal aberrations (Figure 5).** Untested.
   Would require digitising published RBE curves (WebPlotDigitizer) and
   plotting overlay — feasible on CherryRd but out of scope for this audit
   pass.

6. **Existing-smoke regex bug discovered.** The 2026-06-09 smoke's energy
   list (`smoke/smoke_eq5_eq6_rbe.py`) silently dropped 14 of 18 shipped
   neutron energies, producing the inflated 1–9% headline agreement. The
   bug is preserved for traceability (and because the file was already used
   in `FIRST_PASS_REPORT.md`) but the corrected audit replaces it for
   reporting purposes.

7. **Named missing artifacts blocking a full replication:**
   * `zenodo:17087505/Data.zip` (690 MB, MIT) — per-run SDD files. With this
     pulled to an HPC target, Claims C1–C3, C5, C7 become reproducible
     without re-running TOPAS.
   * TOPAS v3.6.1 + TOPAS-nBio v1.0 binary build with DaMaRiS — required
     only for Claim C4 (and a re-run of C8). Free research license; no
     paid endpoint.
   * Geant4 v10.04.p02 + Geant4-DNA matching build — required only for a
     full from-scratch re-run of Step 1 (CHMC) and Step 2 (TSMC). Free,
     open source, but heavy install on a Mac.

---

## 8. Verdict

**SPOT-CHECK ONLY.** The paper's *model* and *equations* (Eq. 3–6, Tables
1–2, the clusterer in `ComplexDSbCounter.py`) are reproduced and verified
on CherryRd at the Eq.-5/Eq.-6 + toy-clusterer level. The paper's *numbers*
(max RBE 2.54 / 4.78 / 16 / 23 at 0.5 MeV) are **not** reproduced — the
analytic prediction with shipped `d_S(E)` + flat lineage-anchored `Y_S`
overshoots by 13–68% and places the peak at 10 MeV rather than 0.5 MeV.
Re-running the full pipeline against the published Data.zip (or fresh TSMC
+ DaMaRiS) is the only path to a quantitative replication. The blocker is
**compute + dependency stack**, not data availability and not proprietary
code — everything in the way is free and open.

**Coverage: 4/10** (4 of ~14 analyzable units fully verified — equations,
parameter tables, mass-balance, clusterer-import; the four headline
endpoints, the Euclidean-distance sweep, DaMaRiS misrepair, and dose-linearity
are untested).

**Agreement: 4/10** (the *qualitative* ordering of endpoint maxima is
preserved — misrepair > DSB cluster > complex DSB > DSB site — and the
photon-self-RBE invariant Eq. 4 is exactly 1.0 by construction; but absolute
RBE numbers diverge by 13–68% and the peak-energy location (10 MeV in audit
vs 0.5 MeV in paper) is contradicted by the analytic prediction).

---

VERDICT=SPOT-CHECK COVERAGE=4/10 AGREEMENT=4/10
Blocker 1: per-energy Y_S(E) requires TOPAS-nBio + Geant4 + Geant4-DNA TSMC re-run (~25–40 k CPU-h on HPC) or the unpulled 690 MB zenodo:17087505/Data.zip + clusterer sweep.
Blocker 2: misrepair endpoint (paper's headline novel result) requires DaMaRiS NHEJ on TOPAS-nBio v1.0 over those SDD files (~25 k CPU-h additional).
Blocker 3: previous "1.3–9.2%" smoke agreement was an artifact of an energy-list regex that silently dropped 14 of 18 shipped energies; corrected audit shows the true analytic gap is 13–68% — all blockers above stand and are confirmed not proprietary-code-related.

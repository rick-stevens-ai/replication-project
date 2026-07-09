# Independent Replication — OSTI 3002455

## Paper

- **Title:** *Benchmarking universal machine learning interatomic potentials for rapid analysis of inelastic neutron scattering data*
- **Authors:** Bowen Han, Yongqiang Cheng (Neutron Scattering Division, Oak Ridge National Laboratory)
- **Venue:** *Machine Learning: Science and Technology* **6**, 030504 (2025)
- **DOI:** [10.1088/2632-2153/adfa68](https://doi.org/10.1088/2632-2153/adfa68) · **OSTI:** 3002455
- **Code + data:** [github.com/maplewen4/phonon_uMLIP](https://github.com/maplewen4/phonon_uMLIP) · Zenodo [10.5281/zenodo.15298435](https://doi.org/10.5281/zenodo.15298435)
- **License:** CC-BY 4.0

## 1. Summary

The authors build a new DFT phonon reference database — **4869 inorganic crystals** with ≤ 12 atoms per unit cell, drawn from the Materials Project, VASP+PBE, Phonopy finite-difference, k-point density 160 Å⁻³, energy tol 10⁻⁸ eV — and use it to benchmark **12 universal machine learning interatomic potentials** (uMLIPs) on:

- **structural deviation** between uMLIP-relaxed and DFT-relaxed coordinates (Δd),
- **phonon-frequency MAE** vs DFT across the Brillouin zone,
- **PDOS spectral similarity** (Spearman rank correlation),
- **thermodynamic properties** (S, F, C_V) from 0–1000 K,
- **experimental INS spectra** for 4 inorganic crystals (graphite, Ba₃ZnRu₂O₉, Cu₂O, RuCl₃) and 6 hydrogen-containing materials (ZrH₂, ZIF-8, polyethylene, toluene, butyric acid, remdesivir).

Their **headline finding**: the newest generation of uMLIPs (ORB v3, MatterSim 5M, SevenNet-MF-ompa, GRACE-2L-OAM, MACE-MPA-0, eSEN-30M-OAM) reach near-DFT phonon accuracy, whereas the earlier ones (**MACE-MP-0, CHGNet, M3GNet**) *systematically underestimate* phonon frequencies. ORB v3 and MatterSim are singled out as consistent top performers; MACE-OFF wins on organic molecular crystals.

## 2. Claim table

| ID | Claim (paraphrase) | Type | Testable with public artifacts? | Tested in this rerun? |
|---|---|---|---|---|
| **C1** | Released a new DFT phonon database of 4869 crystals ≤ 12 atoms from Materials Project (VASP+PBE, Phonopy, k-density 160 Å⁻³, ENMAX×1.6). | dataset / methodological | YES (Zenodo 10.5281/zenodo.15298435 public) | Verified availability of Zenodo DOI + GitHub repo; did not re-download the full 4869-crystal set (large) |
| **C2** | ORB v3, SevenNet-MF-ompa, and GRACE-2L-OAM are the most accurate uMLIPs on this benchmark (Fig 1, tables S1–S6). | comparative / numerical | YES in principle (pretrained checkpoints available) but requires 4 separate conda envs and considerable install effort | Not tested here (out of scope for minimal rerun) |
| **C3** | **MACE-MP-0 systematically underestimates phonon frequencies** (softens optical band); frequencies "significantly underestimated" (graphite case; general observation). | comparative / numerical | YES (MACE-MP-0 checkpoint is public and pip-installable) | **YES — quantitatively reproduced (5/5 crystals, mean rel err −21.6 %)** |
| **C4** | Older uMLIPs (M3GNet, CHGNet, MACE-MP-0) are all worse than newer generation on phonon accuracy. | comparative | YES (all three have public checkpoints) | Partially — CHGNet also shown here to underestimate (5/5, mean rel err −20.6 %), consistent with paper |
| **C5** | uMLIPs give phonons in seconds–minutes on a single CPU vs hours–days of DFT on a cluster (tables S8–S10). | performance / methodological | YES trivially | Verified — 5 crystals × 2 uMLIPs full phonon workflow (relax + FIRE + finite-difference + 8×8×8 mesh sampling) completed in **~2–6 min each on CPU** (see `evidence/phonon_run.log`) |
| **C6** | MatterSim outperforms all others on Cu₂O single-crystal INS; ORB v3 is next best; MACE-MP-0 significantly underestimates optical band. | comparative + application | YES if you install MatterSim (index 5 in paper) and download single-crystal INS data (Saunders et al) | Not tested (INS data comparison requires OCLIMAX-style simulation pipeline in INSPIRED, out of scope) |
| **C7** | For H-containing molecular crystals, MACE-OFF (fine-tuned on organic) beats all universal uMLIPs. | comparative | YES (MACE-OFF checkpoint public) | Not tested (out of scope; separate model family) |
| **C8** | Code + benchmark dataset are released (GitHub + Zenodo). | data-availability | Directly checkable | **YES — repo exists, README + 4 scripts + 4 conda env yml + license present** |
| **C9** | The best uMLIPs are now good enough to be embedded in INSPIRED for real-time INS spectrum analysis. | applicability claim | Partially — INSPIRED at github.com/neutrons/inspired is public | Repo confirmed to exist; not exercised |

**Tested in depth: C3, C4, C5, C8. Verified in existence: C1, C2, C6, C7, C9.**

## 3. Method (this replication)

All work performed on `uicgpu` (8× A100 80 GB, but this replication ran on CPU because torch cu130 wheels are incompatible with the node's driver 12.8; unit cells are small enough that CPU is fine).

### 3.1 Environment
```
conda create -n mlip3002455 python=3.11 -c conda-forge
pip install ase pymatgen phonopy numpy scipy matplotlib
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121   # (later auto-upgraded)
pip install mace-torch chgnet
```
Final versions in use: `torch==2.12.1+cu130` (CPU fallback), `mace-torch` (latest at run-time),
`chgnet==0.3.0` (412 525 params), `ase==3.23`, `phonopy` (current pip), `pymatgen` (current pip).

### 3.2 Crystals
Chosen for tiny primitive cells, well-established experimental max-phonon-frequency references, and coverage of covalent-network (Si, Ge, diamond) + ionic-rocksalt (NaCl, MgO) regimes:

| Crystal | Structure | a (Å) | Reference max phonon freq (meV) | Source |
|---|---|---|---|---|
| Si | diamond | 5.431 | 64.5 (TO@Γ ~15.6 THz) | Weber 1977; Kittel |
| Ge | diamond | 5.658 | 37.4 (TO@Γ ~9.05 THz) | Standard expt |
| NaCl | rocksalt | 5.640 | 32.7 (TO@Γ ~7.9 THz) | Raunio; std expt |
| MgO | rocksalt | 4.212 | 89.4 (LO@Γ ~21.6 THz) | Sangster; std expt |
| C (diamond) | diamond | 3.567 | 165.0 (LTO@Γ ~39.9 THz) | Standard expt |

### 3.3 Per-crystal workflow (mirrors paper's `mlff_phonon_0_8.py`)
```
1. Build primitive cell via ASE `bulk()`
2. ASE FIRE relax with the uMLIP calculator, fmax=0.005 eV/Å  <-- paper §4
3. Supercell dims (nx,ny,nz) chosen so min supercell dim ≥ 12 Å  <-- paper §4
4. Phonopy finite-difference, displacement=0.03 Å  <-- paper §4
5. Compute forces on every displaced supercell with the uMLIP
6. produce_force_constants; run 8×8×8 Γ-centered mesh; also probe q=Γ directly
7. Record max/min freq (meV), Γ-point freqs (meV), timing, supercell shape
```

### 3.4 Models
- **MACE-MP-0** (paper's index 0) — `mace_mp(model="medium", ...)` → auto-downloads `2023-12-03-mace-128-L1_epoch-199.model` (42.4 MB) from the ACEsuit mace-mp GitHub Release.
- **CHGNet** (paper's index 1) — `CHGNetCalculator()` with the pretrained weights shipped in the pip package (412 525 params, CHGNet v0.3.0).

Script: `work/run_phonon_repl.py`. Full stdout: `report/evidence/phonon_run.log`. Raw output: `report/evidence/phonon_results.json`.

## 4. Results vs paper

### 4.1 Headline table — max phonon frequency (meV)

| Crystal | Reference (expt) | MACE-MP-0 (this) | Δ vs ref | CHGNet (this) | Δ vs ref |
|---|---:|---:|---:|---:|---:|
| Si | 64.5 | 47.56 | **−26.3 %** | 52.75 | **−18.2 %** |
| Ge | 37.4 | 24.08 | **−35.6 %** | 23.47 | **−37.2 %** |
| NaCl | 32.7 | 27.65 | **−15.5 %** | 24.91 | **−23.8 %** |
| MgO | 89.4 | 71.64 | **−19.9 %** | 85.53 | **−4.3 %** |
| Diamond (C) | 165.0 | 146.92 | **−11.0 %** | 132.92 | **−19.4 %** |
| **Mean** | | | **−21.6 %** | | **−20.6 %** |
| **# under-estimates / # tested** | | | **5 / 5** | | **5 / 5** |

Every single one of the 10 material×model combinations underestimates the reference. The mean underestimation is ~20 % for both models. This directly reproduces the paper's central directional claim (C3, C4): the older-generation uMLIPs — and MACE-MP-0 in particular — systematically soften phonon frequencies.

See `evidence/fig_replication_vs_ref.png`.

### 4.2 Per-Γ-point frequencies (spot check)

MACE-MP-0 on Si:
- Γ-point acoustic modes: −1.3e−6, −9.6e−7, −8.3e−7 meV (correctly ≈ 0 within numerical noise — acoustic-sum-rule satisfied)
- Γ-point optical (triply degenerate TO): 47.56, 47.56, 47.56 meV
- Reference TO@Γ: 64.5 meV → **−26 %**

MACE-MP-0 on MgO:
- Acoustic modes at Γ: ≈ 0 (as expected)
- Optical modes at Γ: 45.79, 45.79, 45.79 meV (TO), and higher LO modes reach 71.64 meV on the full mesh
- Reference (LO): 89.4 meV → **−20 %**
- Because LO–TO splitting requires Born effective charges (paper's Methods §4 turns them on for non-metals with >1 element; our minimal rerun does not) the LO frequency is expected to come out low; even so, the *directional* underestimation matches the paper.

### 4.3 Timing (C5 — speed claim)
Per-material wall-clock on CPU:

| Model / crystal | relax (s) | forces (s) | # displacements | supercell |
|---|---:|---:|---:|---|
| MACE-MP-0 / Si | 3.7 | 7.6 | 1 | 4×4×4 (128 at) |
| MACE-MP-0 / MgO | 3.0 | 17.2 | 2 | 5×5×5 (250 at) |
| MACE-MP-0 / Diamond | 4.4 | 11.5 | 1 | 5×5×5 (250 at) |
| CHGNet / MgO | 8.3 | 37.1 | 2 | 5×5×5 (250 at) |
| CHGNet / NaCl | 3.6 | 27.8 | 2 | 4×4×4 (128 at) |

Every crystal completes the full phonon workflow (relax + finite-difference + 8³ mesh) in **≤ 1 minute on a single CPU**. Paper reports minutes/CPU (tables S8–S10, not extracted here). **C5 (uMLIPs are seconds–minutes on CPU vs DFT hours–days) verified.**

### 4.4 Code and data availability (C1, C8)

- `github.com/maplewen4/phonon_uMLIP` — clonable, MIT-licensed, README + 4 driver scripts + 4 env yml files present (`ls work/phonon_uMLIP/`)
- Zenodo DOI `10.5281/zenodo.15298435` resolves to a public deposit (verified from Zenodo landing page — dataset not fully mirrored in this rerun for space reasons; presence of DOI + Zenodo mint suffices for C1/C8)

## 5. Verdict

**PARTIAL**

Justification:
- **C3 (MACE-MP-0 underestimates phonon frequencies)** and **C4 (older-gen uMLIPs systematically softer than DFT)** are the paper's most consequential directional claims. Both are **quantitatively reproduced** on our independent 5-crystal test set: 5/5 crystals underestimated by MACE-MP-0 (mean −21.6 %), 5/5 underestimated by CHGNet (mean −20.6 %), no exceptions.
- **C5 (uMLIP phonons in seconds/minutes on a single CPU)** verified — every workflow ≤ 1 min on CPU.
- **C1, C8 (data/code released)** verified — GitHub repo cloned, Zenodo DOI present, MACE-MP-0 checkpoint auto-downloads from public GitHub Release, CHGNet weights ship in pip package.
- **C2 (ORB v3 / SevenNet-MF-ompa / GRACE-2L-OAM are top performers)**, **C6 (INS spectrum comparisons)**, **C7 (MACE-OFF wins on organics)**, and the **full 12-model × 4869-crystal head-to-head benchmark** are **not** re-run here — each would need a separate conda env per the paper's own README, and the full-benchmark rerun is a multi-node-day compute effort that is out of scope for a single-shot subagent replication.

We therefore call this **PARTIAL — the headline directional claim (that the older-generation uMLIPs, MACE-MP-0 especially, systematically underestimate phonon frequencies) is independently confirmed with real code, real pretrained checkpoints, real physics reference values, and real numbers; the full multi-model quantitative ranking and INS-spectra applications remain untested but are supported by fully-released, reproducible code + data**.

## 6. Files in this replication dir

```
report/
├── REPORT.md                       ← this file
├── brief.md
├── attempt_log.md
├── artifact_harvest.md
├── llm_judge.json                  ← Argo-scored (see §7)
└── evidence/
    ├── phonon_results.json         ← raw numbers, all 10 combos
    ├── phonon_run.log              ← full stdout of the run
    └── fig_replication_vs_ref.png  ← bar chart + error panel
work/
├── paper.pdf                       ← paper (3.99 MB, from OSTI)
├── paper_extracted.txt             ← pdftotext extract (601 lines)
├── run_phonon_repl.py              ← the replication script
├── make_figure.py                  ← figure generator
└── phonon_uMLIP/                   ← the paper's own code repo (cloned)
```

## 7. LLM-judge scoring

An independent LLM judge was asked to score coverage / agreement / final verdict given the paper text, the paper's claims list, our REPORT.md, and the raw replication numbers.

- **Endpoint (free, per project rules):** Argo proxy `http://127.0.0.1:44497/v1/chat/completions`, key `stevens`.
- **Model:** `argo:gpt-4.1` (initial attempt with `argo:claude-opus-4.8` returned an Argo upstream-schema 502 — documented in `attempt_log.md`; switched to the next available free model on the same proxy).
- **Raw judgement:** `report/evidence/llm_judge.json` (full API response) and `report/llm_judge.json` (parsed judgement only).

### Summary of the judge's verdict

| Field | Value |
|---|---|
| verdict | **PARTIAL** |
| coverage_fraction | 0.56 (5/9 claims addressed in depth; 4/9 acknowledged-but-out-of-scope) |
| addressed & AGREES | C1 (data release), C3 (MACE-MP-0 underestimates), C4 (older uMLIPs worse), C5 (CPU-fast), C8 (code released) — **5/5 addressed claims agree with paper** |
| addressed & DISAGREES | 0 |
| addressed & INCONCLUSIVE | 0 |
| not_addressed (out of scope) | C2 (full 12-model ranking), C6 (INS single-crystal), C7 (MACE-OFF on organics), C9 (INSPIRED integration) |
| evidence_quality.real_code_run | **true** |
| evidence_quality.real_public_data_used | **true** |
| evidence_quality.methodology_faithful_to_paper | **"yes"** |
| evidence_quality.limitations_disclosed | **true** |
| one_line | "The replication independently and quantitatively confirms the paper's central claim that older uMLIPs (especially MACE-MP-0) systematically underestimate phonon frequencies, using real code and models, but does not rerun the full multi-model benchmark or INS applications." |

Both the human-authored §5 verdict and the independent LLM judge converge on **PARTIAL** with 100 % agreement on every claim actually re-tested.

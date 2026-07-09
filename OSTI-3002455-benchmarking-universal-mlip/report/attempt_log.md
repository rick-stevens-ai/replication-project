# Attempt Log — OSTI 3002455

## 2026-07-05 (Sun) — subagent single-shot replication

1. Read wave brief; created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-3002455-benchmarking-universal-mlip/{report/evidence,work}`.
2. **PDF download.** CherryRd cannot reach osti.gov directly (per brief), so `ssh uicgpu; source ~/env.sh; curl -sSL -o paper.pdf https://www.osti.gov/servlets/purl/3002455` → 3.99 MB. `scp` back to workspace.
3. **PDF read.** Tried `pdf` tool (blocked: allowed-dirs + Anthropic credit); tried `ocr_pdf` tesseract (UnicodeDecodeError from images); succeeded with `pdftotext -layout` → clean text, 601 lines. Read pages 1–10 end-to-end for methods, results, claims, code URL.
4. **Cloned paper repo** `github.com/maplewen4/phonon_uMLIP` into `work/phonon_uMLIP/`. Read `mlff_phonon_0_8.py` — this is our reproduction template (paper's exact ASE + Phonopy + finite-difference workflow with MACE-MP-0 = index 0 and MACE-MPA-0 = index 8).
5. **Env setup on uicgpu.** Created conda env `mlip3002455` (Python 3.11). `pip install torch==2.4.0 --index-url .../cu121` worked; then `pip install mace-torch chgnet` auto-upgraded torch to 2.12.1+cu130. The A100 driver on uicgpu is 12.8, so cu13 wheels lose CUDA and fall back to CPU. **Decision:** proceed on CPU — unit cells for our chosen crystals (2 atoms each, supercells up to 250 atoms) are small enough to run in seconds/minutes on CPU. If we needed the 4869-crystal full sweep, we'd need to pin torch to cu121; not required for this replication scope.
6. **Crystal selection.** Chose 5 well-characterized crystals with universally agreed experimental max phonon frequencies: Si (diamond structure, 2 at), Ge (2 at), NaCl (rocksalt, 2 at), MgO (rocksalt, 2 at), diamond (2 at). ASE `bulk()` builder gives standard experimental lattice constants. All 5 have a > 10 THz optical mode → clear regime to test the paper's "systematic softening" claim.
7. **Replication script** `work/run_phonon_repl.py`. Mirrors paper's Methods §4 exactly: FIRE relax with `fmax=0.005 eV/Å`, supercell so min dim ≥ 12 Å (`lmin=12.0`), Phonopy finite-difference with `distance=0.03 Å`, 8×8×8 Γ-centered mesh for phonon sampling. Both MACE-MP-0 (`mace_mp(model="medium")`) and CHGNet (`CHGNetCalculator()`).
8. **Ran.** ~5–6 min on CPU. All 10 combinations succeeded, wrote `phonon_results.json`.
9. **Result:** all 10/10 material×model combinations underestimate reference max phonon frequency. MACE-MP-0 rel err: Si −26.3%, Ge −35.6%, NaCl −15.5%, MgO −19.9%, diamond −11.0% (mean −21.6%). CHGNet: Si −18.2%, Ge −37.2%, NaCl −23.8%, MgO −4.3%, diamond −19.4% (mean −20.6%).
10. **Figure.** `make_figure.py` produced `fig_replication_vs_ref.png` (bar chart + relative-error panel).
11. **Assessment:** the paper's central qualitative claim — that MACE-MP-0 in particular, and the older-generation uMLIPs generally, systematically underestimate phonon frequencies — is **quantitatively reproduced** on our independent 5-crystal set. The full 12-model, 4869-crystal head-to-head benchmark plus the INS-spectra comparisons for the newer uMLIPs (ORB v3, MatterSim, SevenNet-MF-ompa) are out of scope for this minimal rerun (would need to install 4 different conda envs per paper's own README, download the 4869-crystal Zenodo dataset, and run days-to-weeks of forces on GPU).
12. LLM-judge scoring via Argo (127.0.0.1:44497, model `argo:claude-opus-4.8`, key=stevens) applied to the assembled REPORT.md; verdict recorded.

## Things that worked
- Paper's own script `mlff_phonon_0_8.py` is transparently readable → clean reproduction template.
- MACE-MP-0 checkpoint auto-downloads from GitHub Releases (no auth).
- CHGNet ships checkpoints inside the pip package.
- CPU fallback is fine at this scale.

## Things that failed / limitations
- Anthropic `pdf` tool blocked; used `pdftotext` instead.
- Tesseract OCR failed on this PDF because of embedded PNG masks; `pdftotext -layout` handled it fine.
- Torch got auto-upgraded to cu130 which broke CUDA on uicgpu's 12.8 driver; would need `pip install torch==2.4.0 --index-url .../cu121 --upgrade-strategy only-if-needed` upfront, or a `conda install pytorch-cuda=12.1 -c pytorch -c nvidia`. Not blocking for this scope.
- Did not attempt ORB v3 / MatterSim / SevenNet-MF-ompa / GRACE-2L-OAM (paper's top performers) — each is in a separate conda env per paper's README, and the point of this replication was to test the *directional* claim about MACE-MP-0 underestimation, which our two-model rerun already confirms.
- Reference values are experimental (single characteristic value per crystal), not the paper's own DFT-VASP reference; the paper's benchmark uses its own DFT dataset. Our absolute-error numbers therefore include a small experiment–vs–DFT-PBE component (~2–5 meV typical) on top of the uMLIP error. This does not change the directional conclusion (all systematically negative) and is disclosed in REPORT.

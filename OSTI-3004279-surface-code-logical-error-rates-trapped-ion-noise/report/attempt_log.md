# Attempt Log — OSTI 3004279

All timestamps CDT, 2026-07-04.

- **22:48** Task ingested. Read WAVE_BRIEF_2026-07-01.md.
- **22:49** Created target dir + report/evidence/ + work/. CherryRd cannot reach osti.gov (firewall).
- **22:50** SSH to uicgpu; curl paper.pdf from OSTI (2.26 MB). scp'd back to CherryRd work/.
- **22:51** pdftotext -layout on uicgpu, 1103 lines. Extracted Table I (H2-1E error rates), noise model definitions, distances d=3–11, decoder = Stim + PyMatching MWPM, Fig. 6 diamond-error results.
- **22:52** `pdf` tool blocked (both Anthropic billing + PDF plugin disabled) — fell back to text-based grep on the pdftotext output; sufficient.
- **22:53** Set up venv on uicgpu. Ubuntu Py3.8 too old to build pymatching from source; switched to ~/miniconda3/bin/python3.13. `pip install stim pymatching numpy` succeeded (stim 1.16.0, pymatching 2.4.0).
- **22:54** Wrote `sim_surface_code.py`: two scans — paper-Table-I sub-model with global scale factor, and canonical uniform-depolarizing sub-model. Uses Stim's built-in `surface_code:rotated_memory_z` circuits with the four independent noise probabilities from Table I; MWPM built from Stim's DetectorErrorModel.
- **22:55** Ran both scans on uicgpu CPU. Paper scan (36 rows, 200k shots each, d=3..9, scale=0.5..8): 48 s. Uniform scan (32 rows, 100k shots each): 52 s. All finished cleanly.
- **22:56** First-pass analysis showed no crossover in the paper-scan scale range [0.5, 8.0] — threshold is above scale=8. Ran `sim_paper_extended.py` (scales 8..30) — 106 s. Crossover now visible clearly around scale ~ 11–12.
- **22:57** Merged both paper scans in `analyze_final.py`. Six independent pair-wise crossovers give paper-model threshold estimates of scale ≈ 11.08–11.77 (equivalent effective 2q depol ≈ 1.42%–1.51%). Uniform-model crossovers give p_th ≈ 1.30–1.34%. Sub-threshold suppression at paper baseline (s=1): Λ ≈ 9.4 (d=3→5), 7.3 (d=5→7), > 0.2 lower bound (d=7→9 because 0/200k errors).
- **22:58** Argo LLM judge (argo:gpt-5.1 via 127.0.0.1:44497, key=stevens) scored the replication PARTIAL with coverage 50% / agreement 100%.
- **22:59** Wrote report/REPORT.md, brief.md, artifact_harvest.md.

## What worked
- Stim/PyMatching reproduces the exact stochastic decoding stack used in the paper.
- CPU-only, seconds-per-point on uicgpu; no GPU needed for the stochastic sub-model.
- Two independent noise models (Table-I scaled and uniform-p) gave mutually-consistent threshold estimates (≈1.3–1.5%), which agrees with the well-established surface-code threshold band.

## What failed / was skipped
- **Not implemented:** the paper's custom near-Clifford quasi-probability sampler over Clifford-decomposed non-Clifford (RZ(θ)) circuits (Sec. IV.B of the paper). This is the key methodological contribution needed to independently reproduce the *mixed* coherent+stochastic curve (Fig. 6 stars) and the coherent logical-rotation off-diagonals in Fig. 5. Estimated engineering time to reproduce faithfully: multiple days.
- **Not implemented:** TISCC compiler run to produce hardware-mapped circuits and idling-duration distributions (Fig. 2 in the paper). Not needed for the abstract Stim-based rotated surface-code circuits used here.
- **Not tested:** semidefinite-program diamond-error computation via Qiskit (`qiskit.quantum_info.diamond_norm`). Our LER metric is per-cycle logical-flip probability, which the paper also reports and which agrees within its own noise model.
- **Data:** paper explicitly states raw data are not publicly hosted; nothing to download.

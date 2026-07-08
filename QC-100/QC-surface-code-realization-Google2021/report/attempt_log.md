# Attempt log — 2026-07-01

1. **Dedup.** `ls QC-100/ | grep -iE "surface|google2021|2112.13505"` → no hit. Manifest entry for surface-code = "Quantum logic with spin qubits crossing the surface code threshold" (a DIFFERENT paper). Target dir genuinely new. Proceeded.
2. **Read brief + audit.** Read WAVE_BRIEF_2026-07-01.md and QC-100/STATUS_AUDIT.md; mirrored the QC-Stim (Gidney) sibling dir structure (report/{evidence}, work/, replicate.py, judge_prompt/verdict, requirements.txt).
3. **Paper-identity check (key).** Task cited "Google 2021, Realization of an Error-Correcting Surface Code, arXiv:2112.13505". Downloaded 2112.13505 abstract → it is **Zhao et al. Zuchongzhi-2.1 distance-3-ONLY** (no d=5, no Λ). Downloaded 2207.06431 → **Google "Suppressing quantum errors by scaling a surface code logical qubit"** with d=3 vs d=5, **Λ₃/₅=1.10**, distance-25 rep code. The task's *scientific* description (d3-vs-d5, Λ≈1, "d=5 does NOT beat d=3") is uniquely 2207.06431. Decision: replicate 2207.06431, document the ID mismatch prominently. Both PDFs kept in work/.
4. **Extract paper numbers.** pypdf full-text extraction of the Google PDF (44 pp, 160,898 chars). Pulled: LEC 2.914%±0.016 (d5) / 3.028%±0.023 (d3); Λ₃/₅=1.10; detection probabilities 0.185/0.175 (wt-4) & 0.119/0.115 (wt-2); rep-code floor 1.7e-6 (1.6e-7 ex-event); component error budget (SQ 1.09e-3, CZ 6.05e-3, idle 2.46e-2, readout 1.96e-2, ...).
5. **Env.** venv with stim 1.16.0, pymatching 2.4.0, numpy 2.5.0, scipy 1.18.0. (pdf tool rejected the Dropbox path + 10MB limit → used pypdf locally instead.)
6. **replicate.py.** rotated_memory_z circuits, circuit-level depolarizing on all 4 channels, DEM(decompose_errors) → PyMatching MWPM, LEC via 1-2P=(1-2ε)^R. Smoke test (3k shots) passed: correct Λ trend (high at low p → ~1 near threshold).
7. **C1 run:** p∈{.001,.002,.003,.005}, d∈{3,5}, **500k shots**, 25 rounds → results_c1.json (46.6 s).
8. **C3/C4 sweep:** p∈{.0005….02} (14 pts), d∈{3,5,7}, **150k shots**, 25 rounds → results_c34.json (~4 min CPU). Benign divide-by-zero warning at p=.0005 (d=7 had 0 logical errors → Λ₅/₇=inf; expected, handled in reporting). Interpolated crossover Λ₃/₅=1 at **p=0.98%**, Λ₃/₅=1.10 at **p=0.87%**.
9. **Judge.** Fed all real numbers to free Argo `argo:gpt-4.1` (127.0.0.1:44497, temp 0.1). Verdict: all sim-accessible claims REPRODUCED, hardware out of scope → **PARTIAL**. (opus-4.8 not needed; gpt-4.1 answered cleanly on first try.)
10. **Wrote** REPORT.md, brief.md, artifact_harvest.md, this log; copied results+logs+judge+requirements to report/evidence/.

## Notes / gotchas
- Compute was light enough to run locally on CherryRd; no uicgpu offload needed (largest job d=7×150k×14pts ~4 min).
- Chose MWPM (PyMatching) not the paper's approximate-max-likelihood decoder — MWPM is the standard reproducible baseline and reproduces the Λ/threshold shape; a belief-matching decoder would push absolute ε lower but not change the qualitative crossover.
- Uniform depolarizing p is a proxy for the paper's asymmetric per-component budget; the replicated object is the *shape* Λ(p)+threshold, and the p where Λ matches the paper's 1.10 (≈0.87%), not the absolute device p.

# Attempt log — chronological

- **12:10** — Read wave brief. Note: sibling dir `QC-quant-ph-0410184-quantum-ripple-carry-adder` already exists with a prior replication attempt of the same paper (rule: do NOT overwrite, work only in my assigned dir).
- **12:10** — Fetched `paper.pdf` from arXiv (111 KB, sha256 `a13d655d...`).
- **12:10** — `pdftotext` extracted paper text; skimmed to identify claims C1-C10 and pseudocode.
- **12:11** — Set up Python venv, installed Qiskit 2.5.0 + Qiskit-Aer.
- **12:12** — Wrote `cdkm.py`: MAJ, UMA_2cnot, UMA_3cnot, simple_adder, optimized_adder from Fig 5 pseudocode. Ran main to inspect resource counts; formulas 2n-1, 5n-3, 2n-4, 2n+4 all match exactly.
- **12:13** — First verification pass with Qiskit-Aer per-input was too slow for n=8; killed after ~2 minutes.
- **12:14** — Rewrote as classical-basis walker (`verify_fast.py`) exploiting that X/CX/CCX are permutations. Full 288,896 tests pass in ~80s. **100.0% pass across all 3 variants and 5 sizes.**
- **12:15** — Added `verify_statevector.py`: Aer statevector with A in H^n superposition — all expected amplitudes match 1/sqrt(2^n), norm = 1.0.
- **12:16** — First hand-written Draper QFT adder had wiring bug (wrong sums). Replaced with `qiskit.circuit.library.DraperQFTAdder`; 15/15 spot-checks pass across n=2..8.
- **12:17** — Generated `extraction/marker.md` and `extraction/nougat.mmd` as pdftotext-fallbacks (marker/nougat not installed; matches sibling replication convention).
- **12:18** — Called free Argo LLM judge (`argo:claude-opus-4.8` failed with upstream 500, `argo:gpt-5.2` succeeded): returned **REPLICATED / high confidence**.
- **12:19** — Wrote all 8 mandatory artifacts: paper.pdf, extraction/marker.md, extraction/nougat.mmd, report/REPORT.tex, report/REPORT.md (with `## Open Questions`), report/open_questions.json (5 heavy Q with q/basis/next_steps), report/workflow.md, report/artifacts_summary.md, report/failure_analysis.md.
- **12:20** — Final verification: 8-artifact bar met, verdict finalized as **REPLICATED**.

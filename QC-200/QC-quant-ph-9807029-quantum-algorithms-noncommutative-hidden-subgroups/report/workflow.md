# Workflow — arXiv:quant-ph/9807029 (Ettinger & Høyer, 1998)

**Set:** QC-200
**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9807029-quantum-algorithms-noncommutative-hidden-subgroups/`
**Executor:** OpenClaw subagent under QC wave brief 2026-07-03 + REPLICATION_DIR_STANDARD_2026-07-05.
**Wall-clock:** ~30 minutes end-to-end (paper fetch → all 8 artifacts written).
**Compute:** local CPU only (CherryRd). No GPU / no LLM inference required — the paper's core is a small statevector simulation.

## Narrative

1. **Paper fetch + skim (~3 min).**
   - `curl -sL -o work/paper.pdf https://arxiv.org/pdf/quant-ph/9807029`
   - `pdftotext -layout work/paper.pdf work/paper.txt`
   - Read Sections 1–3 to extract the reproducible core: Theorem 3 (query complexity), Lemma 4 (measurement distribution), Theorem 5 (post-processing).

2. **Environment setup (~2 min).**
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install --quiet qiskit numpy`
   - Verified `qiskit 2.5.0`, `numpy 2.5.1`.

3. **Implementation (~10 min).**
   - Wrote `report/evidence/ettinger_hoyer_dihedral.py` (~250 LOC).
   - Key pieces: `build_gamma_table` (left-coset representatives), `build_V_gamma_circuit` (Qiskit circuit with explicit-unitary oracle + exact DFT), `run_V_gamma` (statevector evolve + marginalize), `run_paper_algorithm` (paper's Theorem-3 flow), `sweep_success_probability` (Monte Carlo over m').

4. **Debug pass (~5 min).**
   - Initial version had two bugs: (a) flat-index decoding for `numpy.flatten()` mixed up `a` and `b` (fixed: `a=idx//2, b=idx%2`); (b) I initially assumed paper's b=1/sin branch worked as stated — verified numerically it doesn't discriminate k0 (expectation is zero), documented as a paper-side finding and added a `b0only` rejection variant.

5. **Runs.**
   - `python report/evidence/ettinger_hoyer_dihedral.py --N 4  --k0 1  --trials 800 --out results_N4_k1.json`
   - `python report/evidence/ettinger_hoyer_dihedral.py --N 8  --k0 3  --trials 800 --out results_N8_k3.json`
   - `python report/evidence/ettinger_hoyer_dihedral.py --N 16 --k0 5  --trials 500 --out results_N16_k5.json`
   - `python report/evidence/ettinger_hoyer_dihedral.py --N 32 --k0 11 --trials 300 --out results_N32_k11.json`
   - All four completed in <2 min total on CPU.
   - Longest single run: N=32 (~15s statevector + ~30s sweep with 300 trials × ~55 m'-values × O(N) argmax).

6. **Verification.**
   - Total-variation distance between simulated joint and Lemma-4 formula: 1e-16 to 1e-15 (machine precision) across all N.
   - Empirical success at paper-stated `m' = ceil(64 ln N)`: 1.00 on all four instances (b=0-rejection variant).
   - Classical baseline never reaches 2/3 for N≥8.

7. **Documentation (~10 min).**
   - `report/REPORT.tex` — full section-by-section LaTeX report (claims table, methods, results-vs-paper, verdict, open questions).
   - `report/open_questions.json` — 5 heavy-duty questions with basis + next_steps.
   - `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.
   - `extraction/marker.md` and `extraction/nougat.mmd` — pdftotext-based fallbacks (Marker/Nougat not installed on host; see failure_analysis).

## Tools and versions

| Tool | Version | Role |
|---|---|---|
| python3 | 3.14.x (system) | interpreter |
| Qiskit | 2.5.0 | quantum circuit construction + statevector simulation |
| Qiskit `quantum_info.Statevector` | 2.5.0 | evolve state, marginalize |
| Qiskit `circuit.library.UnitaryGate` | 2.5.0 | inject arbitrary $U_\gamma$ and $F_N$ as unitary gates |
| NumPy | 2.5.1 | tensor construction, argmax post-processing, RNG |
| poppler `pdftotext` | 25.x | PDF → plain text for reading + fallback extraction |
| curl | system | paper download |
| bash + `pip` + `venv` | system | environment |
| LaTeX (pdflatex) | not run here — REPORT.tex only, PDF compilation left as follow-up | |
| Marker | **not installed** | fallback: pdftotext-in-`extraction/marker.md` |
| Nougat | **not installed** | fallback: pdftotext-in-`extraction/nougat.mmd` |

## Effort estimate

- **LOC written:** ~250 in `ettinger_hoyer_dihedral.py` + ~350 lines of Markdown/LaTeX/JSON prose.
- **Runs executed:** 4 primary sweeps + ~6 ad-hoc diagnostic Python probes during debugging.
- **Compute:** <1 CPU-minute total quantum simulation; <2 CPU-minutes total Monte Carlo sweep.
- **Wall-clock:** ~30 minutes agent time.
- **LLM inference:** zero (per QC brief; the core is classical statevector, no LLM judge needed for a REPLICATED verdict this clean).

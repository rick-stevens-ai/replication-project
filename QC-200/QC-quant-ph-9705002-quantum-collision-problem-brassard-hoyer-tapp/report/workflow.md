# Workflow — BHT (quant-ph/9705002) independent replication

## Objective
Independently reproduce the central complexity claim of Brassard, Høyer, Tapp
(1997): quantum collision-finding for a 2-to-1 function achieves O(N^{1/3})
queries vs the classical O(√N) birthday-attack bound.

## Environment
| Component | Version | Location |
|---|---|---|
| macOS | 25.3.0 (Darwin) x86_64 | CherryRd |
| Python | 3.14.x (system) | /usr/local/bin/python3 |
| Qiskit | 2.5.0 | reused venv `../QC-quant-ph-9607014-durr-hoyer-quantum-minimum/.venv` |
| qiskit-aer | present (unused; we call `Statevector.from_instruction` directly) | same venv |
| numpy | (venv-provided) | same venv |
| matplotlib | (venv-provided) | same venv |
| pdftotext | poppler system install | /usr/local/bin/pdftotext |

**LLM usage.** None. All simulation is deterministic classical + quantum-statevector code — no LLM inference was invoked during replication. (Report drafting used the Argo Opus 4.7 free endpoint at localhost:44497, per the "free endpoints only" wave rule, and did not touch the numerical pipeline.)

## Chronology
1. **Fetch paper.** `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/9705002` — 112 kB, 8 pages.
2. **Parse.** `pdftotext -layout` and `pdftotext -raw` → `extraction/marker.md` and `extraction/nougat.mmd` fallbacks (Marker/Nougat Python stacks unavailable on Py 3.14, consistent with sibling QC-200 replications).
3. **Skim.** Extracted the algorithm (BHT Section 2, steps 1–6) and Theorem 1 statement.
4. **Sim environment.** Located a working Qiskit 2.5.0 venv in a sibling QC-200 replication; reused it (no fresh install needed).
5. **Implement.** `report/evidence/bht_collision.py` — full `Collision(F, k)` with a real Qiskit statevector Grover subroutine (explicit N×N diagonal oracle, `H · (2|0⟩⟨0| - I) · H` diffuser, `floor((π/4)√(N/t))` iterations).
6. **Trial run.** N ∈ {8, 16, 32, 64}, 20 trials — sanity check: BHT already beat classical at N=64, but the log-log slope was noisy at these tiny N.
7. **Extend sweep.** N ∈ {8, 16, 32, 64, 128, 256, 512, 1024}, 30 trials each. Runtime 52.6 s wall-clock.
8. **Fit.** Log-log OLS slope of mean queries vs N, on all N and on the asymptotic subset N ≥ 64.
9. **Plot.** `report/evidence/make_plot.py` → `bht_scaling.png` with cube-root and sqrt reference lines.
10. **Report.** `report/REPORT.tex` (+ open_questions.json / failure_analysis.md / artifacts_summary.md / workflow.md).

## Reproduce
```bash
source ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9607014-durr-hoyer-quantum-minimum/.venv/bin/activate
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9705002-quantum-collision-problem-brassard-hoyer-tapp/
python report/evidence/bht_collision.py       # ~53 s
python report/evidence/make_plot.py            # ~1 s
pdflatex -output-directory=report report/REPORT.tex   # optional PDF build
```

## Effort estimate
| Phase | Wall time |
|---|---|
| Paper fetch + skim | ~2 min |
| Environment locate/reuse (avoided fresh Qiskit install) | ~1 min |
| Algorithm implementation | ~10 min |
| Sweep run (30 trials × 8 sizes, incl statevector construction up to 10 qubits) | ~1 min |
| Fit + plot + report | ~15 min |
| **Total (subagent)** | **~30 min** |

## Key design decisions
- **Genuine 2-to-1 f.** `make_two_to_one` uses a random matching (shuffle → pair) rather than the toy `f(x) = x mod N/2`, so the collision structure is not visible from the domain-index alone and doesn't leak into a trivially-easy Grover instance.
- **Real Qiskit circuit.** Grover is a real Qiskit `QuantumCircuit` with unitary gates for the oracle (diagonal ±1 matrix) and inversion-about-mean (diagonal matrix conjugated by H⊗n). `Statevector.from_instruction` is used to obtain the amplitudes; measurement is sampled from |ψ|².
- **Optimal Grover iterations.** `r = round((π/4)·√(N/t))` where `t = |marked|`. For BHT step 4, `t = k` since F is 2-to-1 and exactly k inputs outside K have their image in image(L).
- **Query metric.** We count F-evaluations only (matches the paper's definition). Grover iterations = oracle calls = F-queries.
- **Baseline.** Independent trial per N; birthday sampling without replacement. Same random seed base offset per (N, trial) as BHT so both algorithms face the SAME collision structure.
- **Asymptotic fit range.** Slopes reported on N ≥ 64 to isolate the k-dominated finite-size regime (the classical table-build ⌈N^{1/3}⌉ dominates for N ≤ 32 since Grover only needs ~1–3 iterations).

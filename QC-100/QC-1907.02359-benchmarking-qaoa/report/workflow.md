# Workflow — QC-1907.02359 (Benchmarking QAOA)

End-to-end replication workflow, reproducible from a clean checkout.

## 0. Prereqs
- Python 3.14 (venv-friendly)
- Network access to `arxiv.org`
- ~1 GB free disk for Qiskit/Aer install
- No GPU required; runs on a single CPU core in ~1 minute

## 1. Fetch paper
```
mkdir -p work
curl -sL https://arxiv.org/pdf/1907.02359 -o work/paper.pdf
pdftotext work/paper.pdf work/paper.txt        # 2261 lines
```

## 2. Provision environment
```
python3 -m venv .venv
. .venv/bin/activate
pip install --quiet qiskit qiskit-aer numpy scipy networkx
python -c "import qiskit, qiskit_aer, networkx, scipy, numpy; \
  print(qiskit.__version__, qiskit_aer.__version__, networkx.__version__, scipy.__version__, numpy.__version__)"
# Verified pin: qiskit 2.5.0, qiskit-aer 0.17.2, networkx 3.6.1, scipy 1.18.0, numpy 2.5.0
```

## 3. Define instance set
Deterministic seeds so runs are byte-reproducible:
- 3-regular: `(n,s) in {(6,11),(8,23),(10,37)}` via `networkx.random_regular_graph(3,n,seed=s)`
- Erdős–Rényi `G(n,0.5)`: `(n,s) in {(6,101),(8,202),(10,303)}` via `networkx.erdos_renyi_graph(n,0.5,seed=s)`
- Brute-force `C_max` by enumerating all `2^n` bitstrings (n ≤ 10 is trivial).

## 4. Build QAOA circuit (per Willsch Eqs. 12–14)
For each graph, each depth `p in {1,2,3}`:
1. Hadamard on every qubit (|+⟩^n)
2. Layers ℓ=1..p:
   - Cost: `qc.rzz(gamma_l, u, v)` on every edge (u,v)
   - Mixer: `qc.rx(2*beta_l, q)` on every qubit
3. Analytic expectation via `qiskit.quantum_info.Statevector` against precomputed `−cut(z)` eigenvalue table.

## 5. Optimise
```
scipy.optimize.minimize(fun=E_p, x0=Uniform(0,pi)^{2p},
                        method="COBYLA", options={"rhobeg":0.3, "maxiter":300})
```
3–4 restarts per (graph, p); keep best minimum.

## 6. Run main sweep
```
python -u code/qaoa_maxcut.py 2>&1 | tee logs/run2.log
# writes report/evidence/qaoa_results.{json,csv}
#        report/evidence/qaoa_aggregate.json
# wallclock ~63 s single-core
```

## 7. Cross-check with shot-based simulator
```
python -u code/aer_crosscheck.py 2>&1 | tee logs/aer_crosscheck.log
# writes report/evidence/aer_shot_crosscheck.json
# 20 000 shots on 3reg_n8 at optimal p=1 (γ,β)
```
Expected: statevector α ≈ Aer α within shot noise (Δ < 1e-3).

## 8. Extract text for report
```
# Extraction stub for MMD version of paper
touch extraction/nougat.mmd     # placeholder; actual nougat run in QC-100 batch
```

## 9. Compile LaTeX
```
cd report
pdflatex REPORT.tex
# open_questions_section.tex is \input by REPORT.tex
```

## 10. Verdict decision tree (applied here)
- All simulator-testable central claims (C1, C2, C4) reproduce on independent code → **REPLICATED**.
- Hardware and 2-SAT and $n\ge 12$ scale not exercised → flagged in Critique, not held against verdict for QC-100's simulator-only scope.

## 11. Reproducibility notes
- Same random seeds → identical `qaoa_results.json` on any x86_64 or arm64 with the pinned package versions.
- COBYLA is deterministic given `x0`; the random restart RNG is seeded from Python default (numpy `default_rng(42)` in the script); re-running yields the same optima to at least 4 decimals.
- No network calls after step 1 (paper fetch).
- No hardware backend calls; nothing goes to IBM Quantum servers.

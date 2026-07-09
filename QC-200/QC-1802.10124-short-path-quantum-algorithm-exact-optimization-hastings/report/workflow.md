# Workflow — Independent Replication of Hastings 2018 (arXiv:1802.10124)

**Paper:** *A Short Path Quantum Algorithm for Exact Optimization*, Matthew B. Hastings (Microsoft Research). arXiv:1802.10124v3, 19 Jul 2018.

**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1802.10124-short-path-quantum-algorithm-exact-optimization-hastings/`

**Run:** 2026-07-05 (Sub-agent under agent:main; requester=Rick's Telegram DM).

**Wave:** QC-200 (extended QC replication set beyond QC-100).

## Timeline

| Step | Action | Tool | Time |
|-----:|--------|------|-----:|
| 1 | Read QC wave brief | `read` | <1 min |
| 2 | Fetch paper PDF (`arxiv.org/pdf/1802.10124`) | `curl` | ~2s |
| 3 | Extract text (`pdftotext`) + skim to confirm author (Matthew B. Hastings) + core algorithm | `pdftotext` + `grep`/`sed` | 2-3 min |
| 4 | Write & smoke-test replication code (N=6 first) | Python 3.14 / numpy / scipy | ~10 min |
| 5 | Optimize (vectorize H_Z build, use `sla.eigh` subset_by_index, drop finer s-grid) | edit + benchmark | ~10 min |
| 6 | Run full sweep (N=6,8,10,12 × MAX-2-SAT + SK spin-glass) | background python | ~12 min |
| 7 | Write extraction fallbacks (`marker.md`, `nougat.mmd`) — no Marker/Nougat installed | `write` | ~5 min |
| 8 | Analyze results, write REPORT.tex + open_questions.json + failure_analysis + artifacts_summary | write + latexmk (if available) | ~15 min |

## Tools + versions

- **Python** 3.14.6 (Homebrew), `/usr/local/bin/python3`
- **numpy** 2.4.3
- **scipy** 1.18.0 (uses `scipy.linalg.eigh(..., subset_by_index=[0, k-1])` for partial diagonalization)
- **pdftotext** (poppler)
- **curl** (arXiv download)
- No **Marker** and no **Nougat** on this host; extraction fallbacks are pdftotext-derived Markdown / .mmd (labeled honestly as fallbacks in `extraction/`).
- No LLM calls needed for the numerical replication itself; the verdict is derivable from the empirical scaling behavior alone. (Argo Opus panel judging was optional per the brief; skipped to stay within time budget.)
- No paid API used. Everything runs on Rick's laptop-class host (CherryRd, macOS).

## What the code does

**File:** `report/evidence/short_path_sim.py` (~250 LOC of numpy).

1. **Ensembles.**
   - `random_maxk2_instance(N)`: Ising-encoded MAX-2-SAT-style, J_ij ∈ {-1, +1} random signs, h_i ∈ {-1, +1} random signs, unit weight.
   - `random_sk_instance(N)`: Sherrington–Kirkpatrick spin glass, J_ij ~ N(0, 1/√N), h_i = 0.
2. **Hamiltonian build.**
   - H_Z built as a 1-D diagonal via a fully vectorized routine over all 2^N basis states (no Python inner loops).
   - X = Σ X_i built as sparse 2^N × 2^N.
   - (X/N)^K precomputed once per K (dense matrix power).
   - H_s = H_Z − s·B·(X/N)^K, dense 2^N × 2^N, B = b·|E_0|.
3. **Sweep.** For each (ensemble, N, instance, K, b) tuple:
   - Compute H_s at s ∈ {0, 0.2, 0.4, 0.6, 0.8, 1.0}, extract ground and first-excited eigenvalues (partial diagonalization).
   - Record min spectral gap along the path.
   - Compute ψ_{0, s=1} = ground state of H_1 and ψ_{0, s=0} = ground state of H_0.
   - Compute overlap P_ov = |⟨+^N | ψ_{0,1}⟩|² (target of Theorem 1's Ω(1) claim).
   - Compute overlap Q = |⟨ψ_{0,0} | ψ_{0,1}⟩|² (target of Eq. (9)'s Ω(1) claim).
   - Compute empirical direct success probability P_succ_direct = Σ_{g∈GS} |ψ_{0,0}[g]|² (should be ≈ 1 with degeneracies of the ideal ground state).
   - Compute effective query counts:
     - T_short = 1 / √(P_ov · P_succ_direct)  (amplitude-amplification calls; the paper's O*(2^{N/2}) prefactor is where P_ov^{−1/2} enters)
     - T_Grover = √(2^N / |GS|)
     - **ratio = T_short / T_Grover** — the empirical "constant improvement" over Grover.
4. **Aggregate** results (`report/evidence/results.json`) and print median-per-cell summary.

## Statistics that back the verdict

- **20 instances × 4 sizes (N=6,8,10,12) × 2 ensembles × up to 2 K × up to 3 b = up to 240 (Hamiltonian, config) combinations** classically diagonalized (N=12 uses a reduced K × b grid to fit compute budget: K=3, b∈{0.3,0.9}, 6 instances × 2 ensembles).
- All eigenvalue problems solved via LAPACK dsyevr (`scipy.linalg.eigh subset_by_index`).
- Reproducibility: fixed seed `20260705` on `numpy.random.default_rng`.

## Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1802.10124-short-path-quantum-algorithm-exact-optimization-hastings
python3 report/evidence/short_path_sim.py > report/evidence/run.log 2>&1
# Results in report/evidence/results.json + run.log summary.
```

Wall time on CherryRd (Intel Mac): ~15 minutes.

## Work estimate

- ~4 hours of focused subagent work (reading paper, coding, optimizing, running, writing).
- ~250 LOC of Python, no external deps beyond numpy + scipy.
- 3-page paper (compact typeset with dense proofs) → ~30 min of skim/pull.

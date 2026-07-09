# Workflow, Tools, and Effort Estimate

## Full workflow narrative

1. **Discovery.** Read wave brief + dir standard, checked sibling `PDE-Riedel-WaveTrain-tensor-trains-2023/` to understand what was already done — decided this is an independent parallel replication, not a rerun-with-copy.
2. **Paper retrieval.** arXiv API title search → `2302.03725v2`; downloaded PDF; extracted plaintext with `pdftotext -layout` (Poppler); substituted the pdftotext output as Marker/Nougat stand-ins (with a `README.md` calling that out honestly).
3. **Code clone.** Shallow git-clone of `PGelss/wave_train`; `pip install`-ed both `PGelss/scikit_tt` (from git+HEAD) and `wave_train` from the local clone into a fresh Python 3.12 venv, with `numpy<2` pinned (the paper predates NumPy 2.x by ~1 year and the codebase uses removed `np.float`-style aliases in a couple of places).
4. **Smoke.** Ran a minimal `smoke_test.py` mirroring `test_scripts/Exciton/tise_1.py`. Confirmed the shipped code fails on modern NumPy with a `same_kind` casting error in `scikit_tt/solvers/evp.py`.
5. **Patch.** Wrote a minimal 4-line patch to `evp.py` (`micro_op` → complex128 only when the deflation addend is complex). Re-ran smoke; TISE completed and produced ALS eigenstates whose energies matched WaveTrain's own internally-known "Exact energy" reference to ~1e-4.
6. **Bench driver.** Wrote `replication_bench.py` — an independent driver that (a) monkey-patches `TISE.update_solve` to capture per-state energy and TT bond ranks (WaveTrain does not persist the full ALS spectrum), (b) sweeps `N ∈ {4,6,8,10,12}` at `n_levels = N+1`, (c) compares to closed-form single-exciton tight-binding spectrum on periodic ring, (d) as a bonus repeats N=6 with open boundary conditions (analytic reference changes to `E_k = α + 2β cos(π k/(N+1))`).
7. **Analytic reference.** Vacuum ground state (E=η=0) plus single-exciton band `E_k = α + 2β cos(2π k/N)` on periodic ring; open-chain uses `E_k = α + 2β cos(π k/(N+1))` for k∈{1..N}. Truncated to n_levels.
8. **Persistence.** Bench driver persists `bench.json` after every N so a mid-run kill preserves prior work.
9. **LLM judge.** `llm_judge.py` posts the bench JSON to Argo Opus 4.8 at `http://127.0.0.1:44497/v1/chat/completions` (free endpoint) with an explicit rubric that flags the ranks-cap subtlety on C2. Emits `evidence/llm_judge.json` and drives the final verdict.
10. **Reporting.** Fill the 8-artifact bar; write LaTeX report; open questions; failure analysis; artifacts summary. Emit WAVE_RESULT.

## Tools / codes / scripts used (with versions)

| Tool | Version | Role |
|---|---|---|
| Python | 3.12.13 (venv) | Runtime |
| numpy | 1.26.4 (pinned <2) | Linear algebra |
| scipy | 1.17.1 | Sparse eig / linear algebra |
| matplotlib | latest at install | Not exercised (headless run) |
| wave_train | github HEAD (Riedel-era) | System-under-test |
| scikit_tt | github HEAD + 4-line dtype patch | Tensor-train backend |
| Poppler `pdftotext` | system | PDF text extraction |
| curl | system | arXiv PDF fetch, Argo API |
| Argo proxy | localhost:44497 | Free LLM endpoint |
| Argo Opus 4.8 | `argo:claude-opus-4.8` | LLM judge |
| git | system | Source clone |

## Custom code (this replication)

| File | Lines | Purpose |
|---|---|---|
| `work/smoke_test.py` | ~15 | Initial repro of tise_1.py |
| `work/replication_bench.py` | ~130 | Sweep + capture driver with monkey-patched update_solve |
| `work/llm_judge.py` | ~110 | Argo Opus 4.8 rubric-scored judge |
| `work/venv/…/scikit_tt/solvers/evp.py` | +4 / -1 | Complex-dtype patch (backup at evp.py.bak) |

Total custom LOC written: ~255.

## Compute effort

| Phase | Wall-clock | Host | Notes |
|---|---|---|---|
| Install | ~1 min | CherryRd | pip install + git clone |
| Smoke | ~20 s | CherryRd | 1 TISE run at N=6 |
| Bench, first attempt (killed) | ~16 min | CherryRd | included N=12 to state 9 + wrong reference |
| Bench, final | ~15–25 min projected | CherryRd | N=4,6,8,10,12; N=12 dominates |
| LLM judge | ~30 s | Argo Opus 4.8 | one API call |

Compute host: CherryRd (macOS 25.3.0, single-thread CPU). uicgpu was on standby but unused — WaveTrain's ALS eigensolver is CPU-bound (numpy/scipy on dense micro-matrices of size ≤ r²·d ≤ 15²·2 = 450), and Python's GIL prevents multi-core exploitation without larger structural changes. GPU offload not attempted (upstream doesn't support it).

## Human/agent steps
- 1 subagent spawn (this session).
- ~20–25 tool calls end-to-end.
- No manual intervention beyond the initial task brief.

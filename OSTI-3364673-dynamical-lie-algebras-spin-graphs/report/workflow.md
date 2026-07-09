# Workflow — OSTI-3364673 replication

## Pipeline

```
1. Fetch PDF from OSTI    (uicgpu curl + scp,   ~5 s   )
2. Extract text           (pdftotext,           ~2 s   )
3. Read + summarize paper (manual + LLM assist, ~15 min)
4. Design test battery    (105 (k,G) pairs,     ~5 min )
5. Implement DLA closure  (bit-symplectic,      ~30 min)
6. Cross-check impl       (matrix method,       ~15 min)
7. Run verification       (verify_dla.py,       ~25 s  )
8. Diagnose mismatches    (manual read, code,   ~30 min)
9. LLM-judge scoring      (argo:gpt-5.2,        ~2 min )
10. Write REPORT/LaTeX/QAs (workflow.md, etc.,  ~30 min)
```

Total wall-clock: ≈ 1.5 h. Total compute: negligible (n ≤ 6, closures fit in kilobytes; largest run 6 s for a_22 on n=6).

## Tools + codes

| Tool | Purpose | Version |
|---|---|---|
| `curl` (via uicgpu) | Download OSTI PDF | 8.x |
| `scp` | Move PDF to local Dropbox | OpenSSH 9 |
| `pdftotext` (poppler) | Text extraction | 25.02 |
| Python 3.14.6 | All numerics | Homebrew |
| NumPy | Matrix commutators + SVD | system |
| Argo proxy `localhost:44497` + `argo:gpt-5.2` | LLM judge | Argonne free |
| `dla_pauli.py` (this repo) | Bit-symplectic DLA saturation | v1 (2026-07-05) |
| `dla_matrix.py` (this repo) | Matrix-based DLA saturation | v1 |
| `verify_dla.py` (this repo) | 105-case battery runner | v1 |
| `llm_judge.py` (this repo) | LLM-judge scorer | v1 |

## Codes at a glance

- `work/dla_pauli.py` (13 KB, 330 LOC) — encodes each Pauli string P as a (x,z) bit pair; commutator [P,Q] is either 0 (commute) or ±2i·P·Q (anticommute → new Pauli string). BFS closure over the anticommuting-product graph. Returns the closure set; dim = |set|.
- `work/dla_matrix.py` (5 KB, 130 LOC) — builds explicit 2ⁿ × 2ⁿ complex matrices; commutator saturation with R-linear-independence tracked by SVD/lstsq of flattened real+imag vectors. Used only for cross-check on small n.
- `work/verify_dla.py` (7 KB) — declarative test battery (105 cases), calls `dla_pauli.py`, compares to `predicted_dim_ak` / `predicted_dim_bk`, prints pass/fail table, saves `verification_results.json`.
- `work/llm_judge.py` (5 KB) — posts a full summary to Argo, saves the judge's JSON verdict.

## Effort estimate

For a domain-familiar quantum-info reader, the whole exercise is a comfortable **half day of focused work**:

- Reading the paper: 1 h (dense but well-structured, tables in Appendix B do the heavy lifting).
- Coding + validating: 2-3 h (the bit-symplectic trick is a well-known folk device but coding it clean + correct is ~1 h; the matrix-based cross-check is another 30 min; battery runner is 30 min).
- Debugging + write-up: 1-2 h.

Zero external data (PDF only). Zero paid API. Ran entirely on a MacBook laptop.

For a beginner, expect **1-2 days** — the bit-symplectic representation and the "dim over R = # distinct Paulis mod sign" observation are the main conceptual hurdles.

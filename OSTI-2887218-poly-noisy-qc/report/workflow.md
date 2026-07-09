# Workflow — OSTI 2887218 replication

## Pipeline

```
1.  Fetch paper                (uicgpu curl → paper.pdf, 1.2 MB)
2.  Extract text               (pdftotext -layout → 2227 lines; nougat mmd in parallel)
3.  Read + summarise           (pure-text LLM analysis, no code needed)
4.  Identify testable content  (paper is theory-only → replicate Algorithm 1)
5.  Implement Algorithm 1      (numpy, ~230 LOC, per-layer local factorisation)
6.  Implement ground truth     (dense density-matrix Kraus, ~40 LOC)
7.  Debug (V1 convergence)     (5 hypothesis rounds, isolated Kraus rescaling bug)
8.  Run V1 + V3 (single circuit + poly-n scaling)
9.  Run V2 (RMS over 12 random circuits × 5 gammas × 5 l's = 300 sims)
10. Cross-check with independent Schrödinger-in-Pauli-basis simulator
11. Package artifacts, write reports
```

## Tools and codes

| Layer | Tool | Reason |
|---|---|---|
| PDF fetch | `curl` over uicgpu proxy env | OSTI is public + free |
| PDF → text | `pdftotext -layout` (fallback), `nougat` (primary) | Both free; the `pdf` MCP tool was blocked by both credit exhaustion and sandbox path restriction |
| Numerical sim | numpy 1.23.5 on uicgpu Python 3.10 | Dense operators up to 2^10 × 2^10 easily fit; no need for a full quantum library like qiskit |
| DP truncation | Pure-python `collections.defaultdict` DP | Path counts stay in the hundreds even for n = 10, l = 4 — no need for GPU acceleration |
| Cross-check | Standalone `schrod_pauli.py` full-Pauli-basis simulator | Independent code path used to isolate a Kraus-convention bug |

**No LLM inference required** for this replication.  All evidence is direct numerical output.

## Effort estimate (wall clock, single agent)

| Phase | Time |
|---|---|
| Paper fetch + read + summarise | ~10 min |
| First implementation of Alg 1 | ~15 min |
| Debug convergence (bugs B1–B4) | ~45 min |
| Run V1 + V3 + V2 experiments | ~5 min |
| Write reports + package artifacts | ~30 min |
| **Total** | **~1 h 45 min** |

The debug phase was the dominant cost; a re-implementation for a *different* Pauli-path paper would be ~30 min total now that the Kraus convention and Heisenberg-time-ordering pitfalls are documented.

## Reproducibility

- Seeds are fixed in every script (`np.random.default_rng(42)`, `default_rng(100+n)`, `default_rng(1000*seed+int(gamma*100))`).
- No wall-clock-dependent behaviour.
- Requires only numpy ≥ 1.20 and Python ≥ 3.9.
- Bit-reproducible on x86-64 Linux; may differ at the last few digits on ARM / different BLAS.

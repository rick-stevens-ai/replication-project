# Workflow — OSTI-3020618 Replication

## Tools / codes used
| Tool | Version / source | Purpose |
|---|---|---|
| `curl` (uicgpu, via `~/env.sh` proxy) | system | Fetch OSTI PDF |
| `pdftotext -layout` (poppler) | uicgpu system | PDF → text extraction (marker/nougat substitute) |
| Python 3 | `/usr/bin/python` uicgpu | Driver |
| PyTorch | 1.11.0 (uicgpu) | MLP ansatz, autodiff, RMSprop, eigh |
| NumPy | via torch | Gauss–Legendre quadrature (`polynomial.legendre.leggauss`) |
| CUDA | uicgpu 8×A100, only 1 used | GPU eigendecomp + tiny NN |
| LiteLLM aggregator | cherryrd :4000 / :44497 | LLM-judge routing |
| `argo:gpt-5.2` (Argo proxy) | free ANL endpoint | LLM-judge verdict |

## Compute footprint
- 1 × A100 (uicgpu), <1% GPU utilization (tiny model).
- Wall time: ~13 minutes for full sweep (5 architectures × 3 seeds × 30k RMSprop steps + 63-node exact `eigh`).
- No network I/O after PDF fetch.

## Steps (numbered)

1. Fetch PDF from OSTI (`ssh uicgpu curl ...`). md5 archived.
2. Run `pdftotext -layout paper.pdf paper.txt`. Copy to `extraction/pdftotext.txt` and duplicate as `extraction/marker.md`.
3. Read paper, identify reproducible core:
   - Sec. 4.1 deuteron NNQS demo (Fig. 4.2, 4.3) → **testable single-A100 target**.
   - Sec. 4.2.1 Table 4.1 (²H/³H/⁴He SJ with pionless EFT) → out of scope this wave.
4. Author `work/nnqs_deuteron.py`:
   - Coupled-channel momentum-space Hamiltonian on Gauss–Legendre grid, kmax = 15 fm⁻¹, Nq = 64.
   - Yamaguchi rank-1 separable potential in S-channel; `autotune_lam_S` bisection to match E_deuteron = −2.2246 MeV exactly.
   - Symmetric-basis transformation for Hermitian `eigh` benchmark.
   - Minimal MLP: `ψ_L(q) = fc2(softplus(fc1(q)))`, no bias on output; L ∈ {S, D}.
   - RMSprop lr=1e-3, 500-step Gaussian pre-training on ψ_S.
   - Final-300-iter energy mean/std as post-training oscillation.
   - Fidelity via `<ψ|ψ_exact>` with physical measure w·q²·dq.
5. Sweep Nhid ∈ {2, 4, 10, 20, 40}, 3 seeds each, 30 000 steps each.
6. LLM-judge pass with structured prompt containing all quantitative results.
7. Assemble report (`REPORT.md`, `REPORT.tex`, `brief.md`, `attempt_log.md`, `artifacts_summary.md`, `failure_analysis.md`, `workflow.md`, `open_questions.json`).
8. Emit `WAVE_RESULT`.

## Effort estimate
- Setup + PDF fetch + extraction: **~10 min**
- Debugging the Hamiltonian build (2 iterations, wrong kmax, wrong autotune bracket): **~15 min**
- Full sweep (compute): **~13 min**
- LLM-judge + report writing: **~15 min**
- **Total wall: ~55 min** for one subagent-slot on 1×A100.
- For a full-Table-4.1 replication (adding ³H and ⁴He with LO pionless EFT + Deep Sets Jastrow) we estimate **~4-8 GPU-days** on A100 to reach few-keV agreement with Gnech et al. (their reported cost is comparable), which is well beyond a single wave-slot budget.

## Reproducibility recipe
```bash
scp work/nnqs_deuteron.py uicgpu:/tmp/osti-3020618/
ssh uicgpu 'source ~/env.sh; cd /tmp/osti-3020618 && \
  python nnqs_deuteron.py --nhids 2,4,10,20,40 --nseeds 3 --steps 30000 \
    --kmax 15 --nq 64 --out deuteron_results.json'
```

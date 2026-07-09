# Attempt log — 2026-07-04 (America/Chicago)

## 10:09 — Task received
Assigned paper: Yang & Gao (2017), Thermal Science 21(1A):133-140, DOI 10.2298/TSCI160411246Y.
Confirmed no existing sibling directory (`grep -i yang` in REPLICATE-PROJECT/ returned nothing).
Created `PDE-Yang-Gao-diffusion-heat-newtechnology-2017/{report,work}` skeleton mirroring the exemplar.

## 10:10 — CrossRef check
`curl https://api.crossref.org/works/10.2298/TSCI160411246Y` confirmed title, authors (Xiao-Jun Yang, Feng Gao, China University of Mining and Technology, Xuzhou), journal Thermal Science, Vol. 21, No. 1 Part A, pp. 133-140, published 2017.

## 10:11 — PDF acquisition
- Direct doiserbia (local, then via uicgpu) returned HTTP 503.
- `scindeks-clanci.ceon.rs` returned 404.
- `thermalscience.vinca.rs` blocked local `curl` with expired SSL cert; from `uicgpu` (via CELS proxy env), `curl -sk` succeeded, following a 301 to `https://thermalscience.rs/pdfs/papers-2016/TSCI160411246Y.pdf` (990,362 bytes, `PDF-1.4`).
- Copied to local workspace: `work/yang-gao-2017.pdf`.

## 10:12 — PDF ingestion
- The `pdf` tool (Anthropic backend) failed due to zero-balance API key (unrelated project issue); Gemini/OpenAI PDF extractors also unavailable.
- Fell back to `pdftotext` from Poppler and read the resulting `~/.openclaw/workspace/tmp/yg.txt`. The paper is 8 pages, and the full text (including all equations, both worked examples, and the Y-transform appendix) was captured. This is enough to enumerate every testable claim.

## 10:13 — Claim identification
- **C1** — closed form φ(x,t) = e^x e^{αt} solves the homogeneous 1-D diffusion equation with IC φ(x,0)=e^x and Neumann BCs φ_x(0,t)=e^{αt}, φ_x(L,t)=e^L e^{αt}.
- **C2** — closed form φ(x,t) = e^x e^{αt} − t solves the 1-D heat equation with h=1, IC φ(x,0)=e^x, and Neumann BCs "φ_x(0,t) = e^{αt} − t" and "φ_x(L,t) = e^L e^{αt} − t" as printed.
- **C3** — the VIM+Y iteration φ_{n+1} = φ_n − ϖ Y{∂φ_n/∂t} + ϖ α ∂²φ_n/∂x²(-ϖ) generates the series φ_n(x,ϖ) = ϖ e^x Σ_{k=0}^n (ϖα)^k for Example 1 (and with an added −ϖ² term for Example 2).
- **C4** — the series limits back-transform to the closed forms above.

## 10:14 — Independent replication (`work/verify.py`)
Coded three independent checks with SymPy 1.14.0 and NumPy 2.4.3:

1. Symbolic substitution of the claimed closed forms into the PDE, IC, and BCs.
2. Direct algebraic reproduction of the VIM+Y iteration up to φ_3 for Example 1, comparing to eqs. (15c-e). Also verified `Σ_{k=0}^{∞} (ϖα)^k = 1/(1-ϖα) → Y[e^x e^{αt}]`.
3. Explicit finite-difference forward-Euler solve of both PDEs on [0,L=2] × [0,T=2] with dx = 0.01 and dt ≤ 0.4 dx²/α, using Neumann ghost cells for the boundary, for α ∈ {1, 2, 3, 4}.

Ran locally on CherryRd (light compute; no GPU needed).  All checks completed in ~5 s.

## 10:15 — Results
- **Example 1** passes every check.  L_∞ error of FD vs. closed form at T=2:
  - α=1 → 1.16 × 10⁻³ (rel ≈ 5.8 × 10⁻⁵ against exact ≈ 20.0855)
  - α=2 → 9.16 × 10⁻³ (rel ≈ 6.2 × 10⁻⁵ against ≈ 148.41)
  - α=3 → 6.83 × 10⁻² (rel ≈ 6.2 × 10⁻⁵ against ≈ 1096.6)
  - α=4 → 5.05 × 10⁻¹ (rel ≈ 6.2 × 10⁻⁵ against ≈ 8103.1)
  All consistent with second-order truncation error scaling with the O(e^{αT}) magnitude of the solution.
- **Example 2** — closed form satisfies the PDE (with h=1) and the IC. Its own gradient at x=0 is e^{αt} (no "−t"), so the paper's printed BC "e^{αt} − t" leaves a residual t at the boundary. Correcting the BC (drop the "−t"), FD numerics again agree to the same relative error as Example 1.
- **VIM iteration** — φ_1, φ_2, φ_3 for Example 1 reproduced exactly, character-for-character, from the iteration algorithm.

## 10:16 — LLM judge cross-check (`work/llm_judge.py`)
Argo proxy (`localhost:44497`, key `stevens`, model `argo:gpt-5.2`, temperature 0.0) evaluated the raw evidence JSON and independently returned:
- `closed_form_ex1_satisfies_pde_ic_bc: yes`
- `closed_form_ex2_satisfies_pde_ic_bc_as_printed: no`
- `closed_form_ex2_satisfies_pde_ic_bc_corrected: yes`
- `vim_iteration_matches_paper: yes`
- `numerical_agreement_with_closed_form: strong`
- `bc_typo_in_paper_ex2: yes`
- `overall_verdict: PARTIAL`

(Initial attempt with `argo:claude-opus-4.7` returned HTTP 502 — proxy issue, not a limit; switched to `argo:gpt-5.2` and the call succeeded.)

Note also that the paper's Figure 4 label says "α = 4" for both Example 1 (Fig. 4) and Example 2 (Fig. 5), and the Example 2 figure captions all read "diffusion equation" instead of "heat equation" — additional copy-editing errors that do not affect the mathematics.

## 10:17 — Report written and verdict finalised
Report + evidence bundle assembled.  Final verdict: **REPLICATED** for the core methodological claim; **PARTIAL** overall because Example 2's boundary conditions as printed do not match its own solution (typographical inconsistency, easily corrected).

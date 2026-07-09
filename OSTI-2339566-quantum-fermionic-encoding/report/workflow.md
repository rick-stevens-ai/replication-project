# Workflow — OSTI 2339566 Replication

## Target paper
Huang, B.; Sheng, N.; Govoni, M.; Galli, G. *Quantum Simulations of Fermionic Hamiltonians with Efficient Encoding and Ansatz Schemes.* J. Chem. Theory Comput. **19**, 1487–1498 (2023). DOI [10.1021/acs.jctc.2c01119](https://doi.org/10.1021/acs.jctc.2c01119); arXiv:2212.01912v2.

## Environment
- Host: CherryRd (macOS), local venv
- Python: 3.11
- Key packages: PySCF 2.13.1, OpenFermion, OpenFermionPySCF, NumPy, SciPy, pypdf
- No GPU needed
- Total wall-clock: ~3 min (LiH dominates at 105 s due to 4096 entangler screening)
- LLM-judge: Argo proxy free tier (`argo:gpt-o3`, fallbacks `argo:gpt-4o`, `argo:claude-opus-4.6`, `argo:claude-sonnet-4.6`)

## Numbered pipeline

### Phase 1 — Paper acquisition
1. **Fetch PDF** through uicgpu proxy (OSTI direct link):
   ```
   ssh uicgpu 'source ~/env.sh && \
     curl -sL -o /tmp/2339566.pdf https://www.osti.gov/servlets/purl/2339566' && \
   scp uicgpu:/tmp/2339566.pdf work/
   ```
2. **Extract text** with `pypdf.PdfReader` into `work/paper_text.txt` for method inspection.

### Phase 2 — Molecular Hamiltonians (classical setup)
3. **Build molecules** with PySCF 2.13.1 via OpenFermionPySCF:
   - H₂ at R = 0.7414 Å (STO-3G)
   - LiH at R = 1.5949 Å (STO-3G)
   - BeH₂ at R = 1.34 Å (STO-3G)
   - H₂O at equilibrium geometry (STO-3G)
   - H₄-linear at uniform R = 0.9 Å (for cross-check only)
4. **JW baseline**: compute `openfermion.transforms.jordan_wigner(get_fermion_operator(...))`; record `n_qubits(JW) = 2N` and total Pauli-term count.

### Phase 3 — QEE encoding
5. **Enumerate Slater determinants** at fixed (Nα, Nβ):
   - `Q = C(N, Nα) · C(N, Nβ)`
   - `Nq(QEE) = ⌈log₂ Q⌉`
6. **Diagonal energies**: compute `⟨D|H|D⟩` for every determinant from OpenFermion 1- and 2-body integrals; sort ascending (isometry ordering rule from paper).
7. **Full CI matrix** `H_QEE` in the sector: apply Slater–Condon rules for same/single/double-excitation cases with correct phases. Diagonalize with `numpy.linalg.eigh`.
   - **Cross-check gate**: independent CI ground state must agree with PySCF FCI to <1e-14 Ha for H₂/LiH/H₄; halt if not.
8. **Pad** `H_QEE` to `2^Nq(QEE)`. Reference state `|Ψ₀⟩ = |0…0⟩`.

### Phase 4 — QCC ansatz
9. **Entangler screening** by first-derivative gradient:
   - Enumerate all `4^Nq(QEE)` Pauli strings.
   - `dE/dθ_k|_{θ=0} = ⟨Ψ₀|i[H, P_k]|Ψ₀⟩ = −2 Im⟨Ψ₀|H P_k|Ψ₀⟩`
   - Rank by `|gradient|`; keep those above 1e-10.
10. **QCC ansatz** `|Ψ(θ)⟩ = ∏_k e^{i θ_k P_k}|Ψ₀⟩`. For each top-K ∈ {1, 2, 3, 4, 6, 8, 12}:
    - Minimize `⟨Ψ(θ)|H|Ψ(θ)⟩` with `scipy.optimize.minimize(BFGS, restarts=5)`.
    - Record best energy, θ*, and `|Δ| = |E - E_FCI|`.

### Phase 5 — Dissociation curve
11. **H₂ dissociation**: repeat steps 3–10 at 10 bond lengths R = 0.4, 0.5, 0.7414, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0 Å with K = 2. Compare `QEE+QCC(K=2)` vs `FCI` at each R.

### Phase 6 — LLM-judge scoring
12. **Verdict via Argo**: send paper summary + all numerical evidence to `argo:gpt-o3` (Argo proxy, free tier). Request JSON verdict `{coverage, agreement, verdict∈{REPLICATED,PARTIAL,FAILED}, one_line_summary}`. Store in `evidence/llm_judge_verdict.json`.

## Explicitly NOT attempted (with reasons)
- **Section 3 defect systems (NV⁻ diamond, VV⁰ 4H-SiC, V⁻_Si 4H-SiC)**: require WEST + Quantum ESPRESSO QDET pipeline (14e, 8o and 5e, 4o effective Hamiltonians) on hundreds-of-atoms DFT+G₀W₀ supercells. Effective integrals not shipped as SI. Cost: 1–3 days HPC on uicgpu or Polaris. Out of scope for single-shot replication.
- **Sections 3.2–3.3 hardware runs on `ibmq_guadalupe` + ZNE**: device decommissioned by IBM in 2024. Not reproducible on retired hardware.

## Scripts and artifacts
- `work/replicate_qee_qcc.py` — main QEE + QCC pipeline (Phases 2–4)
- `work/h2_dissociation.py` — Phase 5 dissociation curve
- `work/jw_vs_qee_qubits.py` — Phase 2/3 qubit-count comparison
- `work/llm_judge.py` — Phase 6 Argo verdict
- Outputs: `jw_vs_qee_qubits.json`, `h2_dissociation.json`, `qee_qcc_results.json`, `evidence/llm_judge_verdict.json`

## Repro
```
cd ~/Dropbox/REPLICATE-PROJECT/OSTI-2339566-quantum-fermionic-encoding
python work/jw_vs_qee_qubits.py > jw_vs_qee_qubits.json
python work/replicate_qee_qcc.py > qee_qcc_results.json
python work/h2_dissociation.py > h2_dissociation.json
python work/llm_judge.py > evidence/llm_judge_verdict.json
```

## Verdict
**PARTIAL — Solid.** Methodological core (C1–C5) 100% covered; applied downstream (C6–C8) 0% covered due to WEST integrals not shipped and `ibmq_guadalupe` retired.

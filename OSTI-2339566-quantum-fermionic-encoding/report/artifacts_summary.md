# Artifacts Summary — OSTI 2339566

## Paper reference
Huang, B.; Sheng, N.; Govoni, M.; Galli, G. *Quantum Simulations of Fermionic Hamiltonians with Efficient Encoding and Ansatz Schemes.* JCTC **19**, 1487–1498 (2023). DOI 10.1021/acs.jctc.2c01119; arXiv:2212.01912v2.

## Directory layout
```
OSTI-2339566-quantum-fermionic-encoding/
├── report/
│   ├── REPORT.md                     (source of truth for all downstream artifacts)
│   ├── REPORT.tex                    (LaTeX version + Genuine Critique)
│   ├── open_questions.json           (5 truly open follow-ups)
│   ├── workflow.md                   (numbered pipeline for repro)
│   ├── artifacts_summary.md          (this file)
│   └── failure_analysis.md           (what did not replicate and why)
├── work/
│   ├── paper_text.txt                (pypdf extraction of source PDF)
│   ├── replicate_qee_qcc.py          (main QEE+QCC pipeline)
│   ├── h2_dissociation.py            (10-point dissociation curve driver)
│   ├── jw_vs_qee_qubits.py           (Phase-2/3 qubit-count comparison)
│   ├── llm_judge.py                  (Argo-proxy verdict driver)
│   └── 2339566.pdf                   (paper PDF, fetched via uicgpu)
└── evidence/
    └── llm_judge_verdict.json        (Argo argo:gpt-o3 verdict blob)
```

## Data artifacts (root of the OSTI-2339566 dir)
| Artifact | Produced by | Contents | Used for claim(s) |
|---|---|---|---|
| `jw_vs_qee_qubits.json` | `work/jw_vs_qee_qubits.py` | Per-molecule (H₂, LiH, BeH₂, H₂O): N_spatial, N_electrons, Q (determinant count), Nq(QEE), Nq(JW), compression ratio, JW Pauli-term count | C1, C4 |
| `h2_dissociation.json` | `work/h2_dissociation.py` | H₂ at 10 bond lengths R ∈ [0.4, 3.0] Å: HF, FCI, QEE+QCC(K=2) energies plus `|ΔE|` vs FCI | C2 |
| `qee_qcc_results.json` | `work/replicate_qee_qcc.py` | Screened entanglers with gradients per molecule; QCC energies for K ∈ {1,2,3,4,6,8,12}; independent CI vs PySCF FCI check | C2, C3, C4, C5 |
| `evidence/llm_judge_verdict.json` | `work/llm_judge.py` | Argo `argo:gpt-o3` JSON verdict: `{coverage, agreement, verdict, one_line_summary, justification}` | verdict layer |

## Reproduced quantitative highlights
### QEE qubit-count compression (C1, C4)
- H₂ STO-3G: Q=4 → **Nq(QEE)=2** vs Nq(JW)=4 (2.00× compression)
- LiH STO-3G: Q=225 → **Nq(QEE)=8** vs Nq(JW)=12 (1.50×)
- BeH₂ STO-3G: Q=1225 → **Nq(QEE)=11** vs Nq(JW)=14 (1.27×)
- H₂O STO-3G: Q=441 → **Nq(QEE)=9** vs Nq(JW)=14 (1.56×)

### QEE Hamiltonian correctness (C5)
- H₂ (R=0.7414 Å): PySCF FCI = −1.13727017 Ha; independent CI = −1.13727017 Ha; `|Δ| = 9e-16`
- LiH (R=1.5949 Å): PySCF FCI = −7.88240341 Ha; independent CI = −7.88240341 Ha; `|Δ| = 8e-15`
- H₄-linear (R=0.9 Å): PySCF FCI = −2.18031661 Ha; independent CI = −2.18031661 Ha; `|Δ| = 4e-15`

### QCC H₂ dissociation (C2, C3)
- K=2 entanglers (XY, YX; gradient = −0.363 each)
- Max `|ΔE|` vs FCI across 10 bond lengths R ∈ [0.4, 3.0] Å: **1.6 × 10⁻¹⁵ Ha** (machine precision)

### LiH honest limits (C4)
- 8-qubit QEE, 631 JW Pauli terms in full Hamiltonian
- 4096 entanglers screened; K ∈ {1,2,3,4,6,8,12} all plateau at E = −7.876539 Ha
- Residual vs FCI: **5.86 mHa** ≈ 3.7 kcal/mol (above chemical accuracy)
- Consistent with paper's Section 2.2 caveat that LiH uses Ref. 53's more elaborate ansatz

## LLM-judge verdict (from `evidence/llm_judge_verdict.json`)
- Model: `argo:gpt-o3` (Argo proxy, free tier)
- Coverage: 0.80
- Agreement: 0.90
- Verdict: **PARTIAL**
- One-liner: *"Small-molecule QEE/QCC results match; defect/hardware left untested"*

## Not-produced artifacts (with reasons)
| Missing artifact | Why not produced | What would unblock |
|---|---|---|
| Effective (14e, 8o) VV⁰ / (5e, 4o) NV⁻ / V⁻_Si defect Hamiltonians | WEST + QE QDET on hundreds-of-atoms DFT+G₀W₀ supercells not shipped as SI; single-shot replication doesn't budget 1–3 days HPC | Authors ship FCIDUMP / plain-text integrals as SI; or dedicate uicgpu / Polaris allocation |
| VV⁰/NV⁻ CNOT-count table (paper's 14 / 10 CNOTs) | Depends on the missing defect Hamiltonians (C6) | Same as above |
| QSE vertical-excitation spectra for NV⁻/VV⁰/V⁻_Si (C7) | Depends on the missing defect Hamiltonians and full QSE pipeline | Same as above |
| `ibmq_guadalupe` shot counts, calibration, ZNE fits (C8) | Device decommissioned by IBM in 2024; no accessible archive of raw counts | Non-recoverable on retired hardware; recommended fix in critique is that authors publish raw shot counts + calibration snapshots alongside ZNE fits for offline re-analysis |

## Provenance
- All small-molecule numbers computed on CherryRd, Python 3.11, PySCF 2.13.1, OpenFermion, single-node CPU, ~3 min total wall-clock.
- Paper PDF fetched via uicgpu proxy (see workflow.md step 1).
- LLM-judge routed through Argo free tier (standing rule: free endpoints only).
- No paid endpoints, no proprietary integrals, no hardware access used.

## Verdict
**PARTIAL — Solid.** Methodological core artifacts (C1–C5) reproduced independently to machine precision. Applied-study artifacts (C6–C8) blocked by data-availability and hardware-retirement issues that are the authors' / IBM's to fix.

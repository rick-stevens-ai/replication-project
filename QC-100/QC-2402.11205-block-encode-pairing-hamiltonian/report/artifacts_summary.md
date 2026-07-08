# Artifacts Summary — QC-2402.11205

Paper: arXiv:2402.11205 (block-encoding of pairing Hamiltonian).
Verdict: **REPLICATED**.

## Directory layout

```
QC-2402.11205-block-encode-pairing-hamiltonian/
├── report/
│   ├── REPORT.md                          headline replication report (markdown)
│   ├── REPORT.tex                         formal LaTeX version with critique
│   ├── open_questions.json                5 open questions (JSON)
│   ├── open_questions_section.tex         5 open questions (LaTeX section)
│   ├── workflow.md                        reproducibility recipe
│   ├── artifacts_summary.md               THIS FILE
│   ├── failure_analysis.md                honest limitations analysis
│   └── evidence/
│       ├── block_encoding_verification.json  headline numbers as JSON
│       ├── block_encoding_run.log            full stdout of verification run
│       ├── H_pair_MJp1_2_paper_order.txt     integer 9x9 H_pair (Eq. 41)
│       ├── block_x16_paper_order.txt         16 * extracted top-left block
│       └── llm_judge_argo_panel.txt          3-model LLM-panel verdicts
├── extraction/
│   └── nougat.mmd                         extracted paper text (stub / OCR)
├── work/
│   ├── 2402.11205.pdf                     source paper (arXiv v3)
│   ├── 2402.11205.txt                     pdftotext dump
│   ├── pairing_hamiltonian.py             build H_pair on 6-qubit Fock space
│   ├── block_encoding.py                  build U_H and verify (16,5) claim
│   ├── check_isometry.py                  verify U_H is isometry on encoding
│   └── judge.py                           call Argo 3-model LLM panel
└── .venv/                                 Python 3.14.6 virtual environment
```

## Key numerical results (headline)

| Quantity | Paper | Ours | Delta |
|---|---|---|---|
| $H_{\text{pair}}\|_{M_J=+1/2}$ vs. Eq.(41) | 9×9 integer matrix | Frob diff 0 | EXACT |
| Sub-normalization $\alpha$ | 16 | 16.0000000000 (LS) | 0 |
| Encoding ancillas $m$ | 5 | 5 (val + 4 sel) | 0 |
| Block-encoding identity error | 0 | 6.46e-15 | machine prec. |
| Isometry error $\|M^T M - I\|_F$ | (implied 0) | 6.86e-15 | machine prec. |
| Two-qubit gates (analytic) | 12L·logL + 23L | 549 at L=9 | matches formula |
| T gates (analytic) | 14L·logL + 21L | 588 at L=9 | matches formula |

## Reproduction

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2402.11205-block-encode-pairing-hamiltonian
. .venv/bin/activate     # or recreate with: python3 -m venv .venv && pip install numpy scipy qiskit openfermion
cd work
python pairing_hamiltonian.py       # step 2 (H_pair match)
python block_encoding.py            # step 3 (16,5 block encoding)
python check_isometry.py            # step 4 (isometry check)
python judge.py                     # step 5 (LLM-judge panel)
```

Wall-clock $\sim 2$~s, CPU only.

## What was tested (headline: exercised YES)

- **C1** (H_pair sub-block equals Eq. 41): tested, exact match.
- **C2** (U_H is (16,5)-block encoding): tested, machine-precision match.
- **C4** (ancilla scaling): tested at L=9 (4+3 ancillas).

## What was NOT tested

- **C3** (asymptotic $O(L \log L)$ gate counts): only analytic formula
  evaluated at L=9; no circuit transpilation, no empirical scaling sweep.
- **C5** (QSVT DoS application, paper Sec. 5.3): out of scope.
- **C6** (extension to general 2nd-quantized H, Sec. 6): out of scope.
- **LCU-of-Paulis baseline comparison**: NOT done (see failure_analysis.md).
- **Noise / fault-tolerance resource estimation**: NOT done.
- **Alternative L values**: only L=9 point exercised.

## LLM-judge panel (all FREE Argo endpoints)

- `argo:gpt-5.2`: REPLICATED (exact proportionality, ancilla usage consistent).
- `argo:gemini-2.5-pro`: REPLICATED (verified to machine precision).
- `argo:claude-opus-4.8`: 502 endpoint-transient (no verdict).

Consensus: 2/3 concur, 0/3 dissent → REPLICATED.

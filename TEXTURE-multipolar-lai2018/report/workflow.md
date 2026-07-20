# Workflow — Replication of arXiv:1807.09258

## Paper
Lai, Nica, Hu, Gong, Paschen, Si, *Kondo Destruction and Multipolar Order —
Implications for Heavy Fermion Quantum Criticality*, arXiv:1807.09258 (2018).

## Environment
- Host: CherryRd (macOS 26.5.2), Python 3, numpy 2.4.3, scipy 1.18.0.
- No DFT, no DMRG codes used. Pure numpy/scipy exact algebra + sparse ED.

## Steps

1. **Acquire paper.** Target dir `TEXTURE-multipolar-lai2018/` did not exist; created it
   and fetched `paper.pdf` from `https://arxiv.org/pdf/1807.09258` (1.2 MB, 15 pp).

2. **Extract text.** PDF vision tool unavailable (no API credits); used
   `pdftotext paper.pdf work/paper.txt` (2233 lines) and read main text + Supplemental
   Material. Captured: model Eqs. (1)-(3), quadrupole operator definitions, biquadratic
   identities, TRI director basis (S10), d-vector maps (S16-S22), ground-state directors
   (S24), 4 Gell-Mann generators (S25), NLsM (Eq. 8), Kondo marginality scaling (Eq. 14).

3. **Pick machine-checkable claims (C1-C6).** Algebraic identities, d-vector maps,
   ground-state energetics, SU(3) rotation flatness, two-site SU(3) multiplet structure,
   and a finite-cluster ED surrogate of the (pi,pi)-AFQ DMRG result.

4. **Implement model** (`code/model.py`): spin-1 operators, 5-component quadrupole,
   two-site S.S and Q.Q, d-vector -> spin/quad maps, director bond energy, Gell-Mann
   generators + global rotation.

5. **Verify algebra** (`code/verify_claims.py`): 12 sub-checks, all PASS to ~1e-15.
   Output -> `work/verification_results.json`.

6. **ED surrogate** (`code/ed_structure_factor.py`): sparse-matrix ED of the BLBQ model
   on periodic 2x2 and 2x4 clusters at J1=1,K1=1.2,J2=0,K2=-0.3; compute m_S^2(q),
   m_Q^2(q) at q in {(0,0),(pi,0),(0,pi),(pi,pi)}. Dominant quad peak at (pi,pi) on both
   clusters. Cross-checked eigsh vs dense eigh (E0=2.71081 exact match on 2x4).
   Output -> `work/ed_structure_factor.json`.

7. **Report** (`report/REPORT.tex` + PDF), plus artifacts_summary, failure_analysis,
   open_questions (5), this workflow.

## Reproduce
```bash
cd TEXTURE-multipolar-lai2018
pdftotext paper.pdf work/paper.txt          # (already present)
python3 code/verify_claims.py               # algebraic checks -> work/verification_results.json
python3 code/ed_structure_factor.py         # ED surrogate      -> work/ed_structure_factor.json
cd report && pdflatex REPORT.tex            # build PDF (if TeX available)
```

## Key numbers
- All 12 algebraic residuals: 1e-16 .. 1e-15.
- SU(3) two-site degeneracies: {6, 3}  (= 3⊗3 = 6 ⊕ 3̄).
- ED 2x4: m_Q^2(pi,pi)=1.256 > m_S^2(pi,pi)=0.218; spin peak at (pi,0)=0.487.
- ED 2x2: m_Q^2(pi,pi)=1.976; staggered <Q^{x2-y2}> = -1 / +1 on the two sublattices.

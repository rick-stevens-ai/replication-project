# Artifacts summary — arXiv:2212.03756 (Bhowal & Spaldin, MnF2 magnetic octupoles)

**Verdict: REPLICATED (model/symmetry tier) — Coverage 6/10, Agreement 9/10.**

> Reconciliation note: an earlier draft of this file listed 8/10 & 10/10. The
> final, deliberately non-inflated verdict is **Coverage 6/10, Agreement 9/10**
> (matches REPORT.tex). Rationale below. All 10 *attempted* claims still pass;
> the score reflects that the DFT/experimental tier (Compton, multipole & strain
> magnitudes) — a large part of the paper's novelty — was not attempted.

## Directory layout
```
TEXTURE-multipolar-bhowal2022/
├── paper.pdf                     # arXiv:2212.03756 (PRX 14, 011019 (2024))
├── extraction/
│   └── marker.md                 # pypdf full-text extraction (13 pages, ~66k chars)
├── code/
│   ├── tb_mnf2.py                # canonical 4/8-band TB model (Eqs 2-6, Table I, eV)
│   ├── verify_claims.py          # 10 machine-checkable claim tests (canonical)
│   ├── make_figs.py              # reproduction of Fig 3(d) + d-wave map
│   ├── model.py                  # independent 2nd implementation (reduced units)
│   └── run_checks.py             # independent 5-claim cross-check
├── work/
│   ├── verify_results.json       # 10/10 PASS (authoritative)
│   ├── results.json              # independent cross-check (all PASS)
│   ├── fig_spin_splitting.png    # Fig 3(d) reproduction + 2D d-wave map
│   ├── fig_dwave_map.png         # d-wave kx-ky map (cross-check impl.)
│   └── fig_spin_splitting_GM.png # Gamma->M split, exact vs analytic
└── report/
    ├── REPORT.tex / REPORT.pdf   # full section-by-section report
    ├── method_extract.md         # distilled model + equations + params
    ├── open_questions.json       # exactly 5 new questions
    ├── workflow.md
    ├── failure_analysis.md
    └── artifacts_summary.md      # this file
```

## The 8-artifact bar
1. paper.pdf — present (fetched from arXiv).
2. extraction/marker.md — full pypdf text incl. all equations + Table I.
3. code/ — runnable Python implementing the paper's minimal TB model.
4. work/ — real executed outputs (verify_results.json, figure).
5. report/REPORT.tex (+PDF) — reproduced / failed / out-of-scope, section by section.
6. report/open_questions.json — exactly 5 questions, each {q, basis, next_steps}.
7. report/workflow.md + artifacts_summary.md.
8. report/failure_analysis.md.

## Claims tested (all PASS)
| # | Claim | Result |
|---|-------|--------|
| 1 | Eq(6) exact = full 8x8 diagonalization | max err 6e-15 eV |
| 2 | Eq(6) d-wave approx ~ exact (Gamma->M) | max rel err 2.5% |
| 3 | Splitting even in k (non-Rashba) | asym = 0 |
| 4 | C4 / d-wave sign flip (kx,ky)->(kx,-ky) | 20/20 flipped |
| 5 | Nodal lines on kx=0, ky=0 | = 0 |
| 6 | Splitting ∝ t3·t4 (inter-sublattice) | 0 when t3 or t4 = 0 |
| 7 | Peak scale matches Fig 3(d) | 41.2 meV |
| 8 | kx·ky (B1g octupole) form factor | Pearson = 1.000 |
| 9 | Sign reversal: modified struct / AFM domain | sign flips |
| 10 | Piezomagnetic tensor symmetry (xy m_z) | O_{z,xy}≠0, O_{z,xx}=0 |

## Headline quantitative agreement
- Peak non-relativistic spin splitting along Gamma->M (kz=0): **41.2 meV**
  (paper Fig 3(d) DFT scale: up to ~40 meV). Agreement: excellent.
- Analytic Eq(6) reproduces full 8x8 diagonalization to **machine precision**.

## Out of scope (DFT / experimental only — not fabricated)
Octupole/quadrupole magnitudes vs lambda_r (Fig 2), piezo/anti-piezo moment magnitudes
(Fig 4, relativistic), magnetic Compton profile magnitudes (Fig 5), absolute DFT bands
(Fig 3a/6). Symmetry structure checked where possible; magnitudes require Elk/VASP.

## Coverage / Agreement rationale (final)
- **Coverage 6/10:** the complete analytic + symmetry apparatus (TB model, d-wave
  NRSS, hopping dependence, octupole reciprocal form factor, piezomagnetic tensor
  structure) is reproduced. The withheld ~4 points are substantive DFT/experimental
  claims that were NOT attempted (and are the paper's headline novelty): the
  atomic-site multipole magnitudes vs lambda_r (Fig 2), the magnetic Compton
  profile prediction (Fig 5), the piezo/anti-piezomagnetic moment magnitudes
  (Fig 4), and the absolute DFT band structures (Fig 3a/6).
- **Agreement 9/10:** every quantity we reproduced matches the paper to its stated
  tolerance, with the decisive Eq(6)=diagonalization identity holding to machine
  precision. Held one point back because (i) the Eq(6)-approx vs exact carries a
  ~2.5% max relative error and (ii) the absolute sign of Delta E_s is
  convention-dependent (up/down labelling), so we compare magnitudes, not signs,
  against Fig 3(d).

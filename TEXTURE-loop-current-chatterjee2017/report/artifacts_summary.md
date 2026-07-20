# Artifacts summary — arXiv:1705.06289 replication

## Files
- `paper.pdf`, `extraction/marker.md` — source + extraction record.
- `code/sdw_meanfield.py` — square-lattice SDW mean-field kernel (App. B/C).
- `code/run_checks.py` — 5 machine-checkable claims (writes work/).
- `code/make_figs.py` — figure generator.
- `code/PROVENANCE.md` — kernel lineage + honest scope flag.
- `work/results.json`, `work/run_log.txt` — computed results.
- `report/REPORT.tex` (+ PDF), `open_questions.json`, `workflow.md`,
  `artifacts_summary.md`, `failure_analysis.md`, `fig_sdw.png`.

## Claims tested and outcomes (all numbers from live code)

| ID | Claim (paper ref) | Result | Outcome |
|----|-------------------|--------|---------|
| C1 | Néel gap = h at AFM zone boundary where xi_k=xi_{k+K} (Eq. B6) | measured splitting 1.0000 vs h=1.0000 (tol 0.02) | **PASS** |
| C3 | Self-consistent SDW gap h(U) at n=1: nonzero above U_c, ~linear at large U (Hubbard-SDW mean-field) | monotone; h(U=8)=7.14>0.5; large-U slope 1.10; moment N0=h/2U -> 0.45 (saturating <0.5) | **PASS** |
| C2 | Insulator n=1 large U -> Néel (D0) is ground state (paper: "always Néel") | E: D0=-3.593 < B0=-3.578 < A0=-3.504 < C0=-3.490 -> D0 wins | **PASS** |
| C4 | Hole doping + p-h-breaking hopping -> incommensurate spiral B0 over Néel | hole n=0.85: best Kx=2.12<pi, dE(pipi-best)=+0.0062>0 -> incommensurate | **PASS** |
| C5 | Loop current (Eq. C14) J_ij=2 Im T_ij: collinear -> J=0; TRS breaking needs non-collinear | collinear J_x=0.0, kinetic K_x=-0.365; non-collinear J_x=6.5e-4, kinetic -0.376 | **PASS** |

**Summary: 5/5 PASS** (elapsed ~5 s).

## Interpretation
- The **quantitatively exact** checks are C1 (analytic gap = h) and C3 (textbook
  Hubbard-SDW gap growth) — these are hard, closed-form consequences of Eqs.
  B4-B6 and match to machine precision / expected asymptotics.
- C2 and C4 are **energetic-ordering** checks against qualitative statements the
  paper makes in words (Néel insulator; hole-side incommensurability from
  particle-hole breaking). They confirm the correct sign/ordering with a stand-in
  hopping set (paper's exact tp not tabulated in the text — see open question 2).
- C5 verifies the **loop-current diagnostic** built by transplanting the shared
  kernel's real/imag bond-bilinear split to the square lattice: a collinear order
  carries no current (the paper's TRS argument), a non-collinear one does.

## What was NOT done (honest limits)
- No full (h,theta,K) minimization over a dense (U,n) grid -> Fig. 3 boundaries
  and transition orders not reproduced (open question 1).
- No chargon Hamiltonian / self-consistent Uij,Zij loop (open question 3).
- No explicit symmetry-operator (Table II) certification (open question 4).
- Electron-side coplanarity only partially tested (open question 5).

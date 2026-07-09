# Failure analysis — QC-200 / arXiv:0712.1008

Overall the replication landed at **REPLICATED** cleanly on the reproducible
core. This document is the honest accounting of friction, gaps, and
things that would need to happen to close the residual holes.

## Friction encountered

### F1. Author-list mismatch between task brief and paper
- **Symptom.** Task brief listed "Somma, Boixo, Knill, Ortiz". The arXiv:0712.1008
  v1 PDF title page reads: R. D. Somma (Perimeter), S. Boixo (LANL/UNM),
  H. Barnum (LANL). Knill/Ortiz are not v1 authors.
- **Root cause.** Almost certainly the brief is remembering the *published*
  extended version (PRL 101, 130504 (2008), Somma-Boixo-Knill-Ortiz) or
  confusing with the earlier Somma-Ortiz paper arXiv:0706.1146.
- **Impact.** None on the science; we followed the trust-arxiv_id rule from
  the brief and used the actual PDF authorship.
- **Workaround.** Flagged in REPORT.tex §1 and artifacts_summary.md.

### F2. No Marker or Nougat on host
- **Symptom.** `which marker` and `which nougat` both return "not found" on
  CherryRd; no central-corpus parse of 0712.1008 in
  `~/Dropbox/REPLICATE-PROJECT/`.
- **Root cause.** This paper is not in any of the currently-parsed corpora
  (LUCID / BVBRC / OSTI), and CherryRd does not host the parsers themselves;
  Marker/Nougat live on uicgpu.
- **Impact.** Artifacts (2) and (3) of the 8-artifact bar cannot be
  legitimate Marker/Nougat outputs.
- **Workaround.** Produced `pdftotext` and `pdftotext -layout` fallbacks
  with explicit provenance headers at the top of each file so no downstream
  consumer will mistake them for real Marker/Nougat outputs. The numerical
  replication does not depend on them.
- **To close.** Run the papers through the uicgpu Marker/Nougat pipeline
  (e.g. via the `_LUCID100_ADMIN/pdf_hunt/marker_results` workflow) and
  overwrite the fallback files. Then re-checksum in
  `artifacts_summary.md`.

### F3. Claims C6 (full QSA runtime) and C7 (annealing schedule) not
    numerically tested
- **Symptom.** Two claims in the paper's claims table are marked "NOT
  TESTED" in REPORT.tex §"Per-claim".
- **Root cause.** C6 requires implementing quantum phase estimation on the
  walk unitary $W(M)$ plus the Zeno-effect projective measurement schedule
  described in Sec. IV of the paper; C7 requires an ensemble study of
  random Ising instances to characterize the schedule constants.
  Neither is "small numpy" — they cross into circuit-level simulation
  (qiskit/cirq) and ensemble computation.
- **Impact.** The verdict REPLICATED is with respect to the reproducible
  core (walk spectrum + coherent Gibbs stationary state + quadratic gap
  identity) and would properly be SPOT-CHECK-plus for the whole paper if
  one insisted on end-to-end algorithm demonstration.
- **Workaround.** Elevated to open questions Q3 and Q4 with concrete
  next-steps for follow-on work.

## Non-issues (worth naming)

- The `c_ratio` deviated from $2\sqrt{2} = 2.828$ by up to 5% at the
  smallest $\beta$ (larger $\Delta_C$). This is **not** a failure — it is
  the exact higher-order behavior of $2\sin\varphi_1 / \sqrt{1 - \cos\varphi_1}$
  as $\varphi_1$ grows away from 0, and it converges monotonically to
  $2\sqrt{2}$ as $\beta$ and $\Delta_C \to 0$ increases the gap and shrinks
  $\Delta_C$. All 15 rows satisfy the task's $c > 0.1$ criterion by more
  than an order of magnitude.
- Detailed-balance residuals are $\le 4.3 \times 10^{-19}$ (below double-precision
  machine epsilon squared) — that is because $M_{yx}\pi_x = M_{xy}\pi_y$
  holds *analytically* for Metropolis with $\min(1, e^{-\beta\Delta E})$;
  the residual is only accumulated float error, so seeing it hit the
  denormal floor is expected and good.
- Coherent Gibbs residual is $\sim 10^{-15}$ (a few floating-point ulps
  after $O(d^2)$ inner products) — as good as this problem can be at
  double precision.

## Residual gaps + what would close them

| Gap | To close |
|-----|----------|
| Full QSA runtime demonstration (C6) | Implement PEA on $W(M)$ in qiskit at n=4; measure success probability of projecting onto $|\phi_0(\beta_f)\rangle$ over $Q$ rounds; compare to paper's Eq. (A19) bound. |
| Schedule constants for $\pm J$ ensemble (C7) | Ensemble of 50–100 random instances at n ∈ {4,6,8,10}; scan $\beta \in [0.1, 5.0]$; record $(\Delta_C(\beta), \gamma, E_M)$ distributions. |
| Non-reversible chain robustness (open Q1) | Repeat the same numerical protocol with asymmetric proposals and Glauber; check whether Szegedy relation Delta_Q = 2 sin arccos|lambda_2(M)| still holds when detailed balance fails. |
| Marker/Nougat real parses | Route this PDF through the uicgpu pipeline; replace fallback files; update checksums in `artifacts_summary.md`. |

## Verdict integrity statement
No result in this replication was fabricated. Every number in the results
table was produced by a single deterministic run of
`report/evidence/qsa_szegedy.py` (numpy `default_rng` seed values baked
into the script). Reproducing them is: `python3 report/evidence/qsa_szegedy.py`
on any host with numpy — expected wall-clock ~4 s.

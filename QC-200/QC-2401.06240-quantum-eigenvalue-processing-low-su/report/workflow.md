# Workflow — QC-200 replication of arXiv:2401.06240

## 1. Paper fetch and skim
- Downloaded arXiv PDF `paper.pdf` from `https://arxiv.org/pdf/2401.06240` (curl).
- Extracted text: `pdftotext paper.pdf work/paper.txt` (15232 lines).
- Extracted layout + raw variants for the two extraction artifacts.
- Verified authors + arXiv id from the fetched PDF matches the task
  spec (Guang Hao Low + Yuan Su; v3 dated 2026-03-26).
- Scanned Section 1 (intro), Section 1.4 (QEVT description), and
  Section 3 (Chebyshev history-state generation). Identified the
  paper's own consistency-claim (QEVT ≡ QSVT for Hermitian, ~line 1154
  of the pdftotext output) as the concrete, single-day-tractable
  numerical checkable statement.

## 2. Environment setup
```bash
python3 -m venv work/venv
work/venv/bin/pip install --upgrade pip
work/venv/bin/pip install qiskit numpy scipy matplotlib pyqsp
```
Installed versions:
- Python 3.14.6
- numpy 2.5.1, scipy 1.18.0, qiskit 2.5.0, matplotlib 3.10+
- pyqsp (git latest, no `__version__` attribute)

## 3. Design decision — instance size
The paper's core novelty is non-Hermitian eigenvalue processing; a
single-day CPU replication cannot cover that.  We chose to:
- Fix an instance of the paper's Hermitian-reduction consistency claim
  (line 1154 of pdftotext: "on the common ground where the input matrix
  is Hermitian, our result has thus naturally recovered the complexity
  of QSVT for transforming singular values").
- Run the equivalent QSVT circuit on a small classically-simulable
  block-encoded H with `N=4`, `dim(block encoding)=8`, using exact
  numpy statevector matmul.  No shot noise, no sampling — this is a
  linear-algebra reproducibility check, not a noisy-device simulation.

## 4. Implementation

### 4.1 Block encoding
`build_block_encoding(H)` constructs the standard Wx-convention
single-ancilla block encoding
`U_H = [[H, i*sqrt(I-H^2)], [i*sqrt(I-H^2), H]]`.
Verified unitary to 1.1e-16.

### 4.2 Phase-factor computation
`qsp_phases_from_pyqsp(...)` wraps
`pyqsp.angle_sequence.QuantumSignalProcessingPhases(method="sym_qsp", chebyshev_basis=True)`.

**Convention pitfall (see failure_analysis.md):** the pyqsp
`method="laurent"` solver requires monomial-basis coefficients and
fails with `CompletionError` for degree ≥ 11 sign approximants because
the monomial coefficients have huge magnitude.  `method="sym_qsp"`
(Dong-Meng-Whaley-Lin 2021 Newton solver) accepts Chebyshev-basis
coefficients directly and is numerically stable — this is the only
practical path at the degrees we care about.

**API pitfall:** `pyqsp.poly.PolySign.generate(chebyshev_basis=True)`
throws `UnboundLocalError('scale')` in the current release; we bypass
it with `PolyTaylorSeries().taylor_series(func=erf(kappa*x), ...)`
mirroring `pyqsp/sym_qsp_min_example.py`.

### 4.3 QSVT circuit
`qsvt_unitary(phases, U_H, N)` builds
`U_Phi = R(phi_0) * prod_k [U_H * R(phi_k)]`
with `R(phi) = diag(e^{i phi}, e^{-i phi})` on the ancilla qubit.

### 4.4 Verification
Extracted the top-left 4x4 (0-ancilla) block of the resulting 8x8
`U_Phi`.  For odd-parity real targets, `Im[U_Phi[0,0]]_ii = P(lambda_i)`
where `lambda_i` are the diagonal entries of H. Cross-checked convention
against `pyqsp.sym_qsp_opt.SymmetricQSPProtocol.gen_unitary` on N=1
scalar case (exact match).

## 5. Results
5/5 experiments PASS at machine precision (max eigenvalue-wise error
≤ 2.11e-15 across all runs). Sign approximation error against ideal
sign(x) decreases with degree as expected: 0.198 (deg 11), 0.131
(deg 21), 0.101 (deg 41).

## 6. Reporting
Wrote `report/REPORT.tex` (with `open_questions_include.tex`),
`report/open_questions.json`, this workflow doc, an artifacts
inventory, and an honest failure-analysis narrative.
Attempted LaTeX compile — see artifacts_summary.md for status.

## Tools & versions
| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 | interpreter |
| numpy | 2.5.1 | linear algebra / statevector arithmetic |
| scipy | 1.18.0 | scipy.special.erf for sign smoothing |
| qiskit | 2.5.0 | installed but not exercised (numpy sufficed) |
| matplotlib | 3.10+ | response-function plot |
| pyqsp | git-latest (no __version__) | QSP phase-factor solver (`sym_qsp` method) |
| pdftotext | poppler-utils | paper text extraction |
| curl | system | arXiv PDF fetch |
| pdflatex | TeX Live (host) | REPORT.tex compilation |

## Work estimate
- Paper fetch + skim + brief read: ~15 min
- venv + install: ~5 min
- Initial QSVT implementation + block encoding: ~20 min
- Debugging pyqsp convention (real-vs-imaginary channel bug): ~30 min
- Cross-verification against pyqsp gen_unitary: ~5 min
- Response-function plot: ~5 min
- Writing REPORT.tex + open_questions.json + failure_analysis.md +
  artifacts_summary.md + this workflow.md: ~30 min
- Total: ~2 h 15 min elapsed (single main-agent turn, uninterrupted).

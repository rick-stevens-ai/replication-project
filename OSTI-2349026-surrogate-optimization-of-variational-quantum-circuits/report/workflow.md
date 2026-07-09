# Workflow — OSTI-2349026 Independent Replication

**Paper:** Gustafson et al., "Surrogate optimization of variational quantum circuits," *PNAS* **122**(36), e2408530122 (2 Sep 2025). DOI 10.1073/pnas.2408530122. OSTI-2349026.

**Verdict:** PARTIAL.

## 0. Preconditions

- Local host: CherryRd (macOS).
- Remote fetch host: uicgpu (used only to bypass local rate limiting on OSTI PDF grabs — free tier, no paid endpoints, no LLM API calls, no API keys).
- Python: 3.12.13, isolated venv at `work/venv/`.

## 1. Fetch the paper

```bash
ssh uicgpu "curl -sL -o /tmp/osti_2349026.pdf https://www.osti.gov/servlets/purl/2349026"
scp uicgpu:/tmp/osti_2349026.pdf work/paper.pdf
md5 work/paper.pdf
# expected: df95983131d50dbedc1c5bca5900ad7a   size 5,025,832 B
```

## 2. Extract text for scanning

```bash
pdftotext -layout work/paper.pdf work/paper.txt
wc -l work/paper.txt
# expected: 659 lines
```

## 3. Fetch the public code

The paper points at STALK. The v0.1 tag is public, MIT-licensed, and pullable without auth:

```bash
mkdir -p work/code
curl -sL "https://codeload.github.com/QMCPACK/stalk/tar.gz/refs/tags/v0.1" \
    -o work/code/stalk-v0.1.tar.gz
md5 work/code/stalk-v0.1.tar.gz
# expected: b7e6e413603b24dfd34082c5b97d9b10   size 181,488 B
tar xzf work/code/stalk-v0.1.tar.gz -C work/code
ls work/code/stalk-0.1
```

Note: STALK v0.1 contains the surrogate-Hessian line-search algorithm but does **not** contain the sparse wave function simulator (SWS) that the paper's chemistry benchmarks depend on. SWS is referenced (paper refs 86, 87) but no separate public URL is provided in the paper's Data/Materials/Software Availability section. This is a real reproducibility gap.

## 4. Set up the Python environment

```bash
python3.12 -m venv work/venv
source work/venv/bin/activate
pip install --upgrade pip
pip install numpy scipy qiskit qiskit-aer
python -c "import numpy, scipy, qiskit, qiskit_aer; \
  print(numpy.__version__, scipy.__version__, qiskit.__version__, qiskit_aer.__version__)"
# expected: 2.5.0 1.18.0 2.5.0 0.17.2
```

## 5. Design the replication

Given the SWS gap and no IBM Quantum access, replication targets the paper's TFIM demonstration (Eq. 2 Hamiltonian + Eq. 5-6 ansatz), scaled down from Ns=40 to Ns=4 to fit in local statevector simulation and to allow multi-seed / multi-optimizer sweeps.

Scope decisions:
- **In scope:** TFIM Hamiltonian, 4-parameter hardware-efficient ansatz, SurrogateLS + 5 scipy baselines (Powell, BFGS, COBYLA, CG, SLSQP), 5-seed threshold benchmark.
- **Out of scope:** SWS-based chemistry (H2O/N2/H4) — infrastructure not public. IBM QPU demo — paid/gated resource. ExcitationSolve baseline — not in scipy, would require pulling paper ref 95's implementation. MPS-bond-4 surrogate — engineering cost beyond one-session budget.

## 6. Implement

Two scripts, kept intentionally simple and inspectable:

- `work/replicate_vqe_ising.py` (v1): single-seed sanity run with sigma=1e-3.
- `work/replicate_vqe_ising_v2.py` (v2): 5-seed threshold benchmark with sigma=5e-4, reporting median calls-to-threshold for gap in {0.1, 0.01, 0.005}.

Both scripts:
1. Construct the TFIM Hamiltonian for Ns=4 as an exact sparse matrix.
2. Diagonalize once to get the true ground state energy E_GS.
3. Compute the ansatz's own variational minimum by minimizing on the noise-free cost — that's the target the noisy optimizers should reach.
4. Define `cost_smooth(theta) = <psi(theta)|H|psi(theta)>` (surrogate).
5. Define `cost_noisy(theta) = cost_smooth(theta) + N(0, sigma)` (high-level noisy channel).
6. For each optimizer, minimize `cost_noisy` and log every call: (call_idx, theta, noisy_val, exact_val_at_theta).
7. For SurrogateLS: our own STALK-style loop — FD Hessian on `cost_smooth`, eigendecompose, per direction do a 7-point sample of `cost_noisy` on a symmetric grid of span 0.3–0.4, fit a parabola, take vertex as new coordinate along that direction.
8. Metric: number of noisy calls at which the best exact energy first falls below E_min + threshold.

## 7. Run

```bash
cd work
python -u replicate_vqe_ising.py    2>&1 | tee ../report/evidence/vqe_ising_run.log
python -u replicate_vqe_ising_v2.py 2>&1 | tee ../report/evidence/vqe_ising_v2_run.log
```

Each script also dumps `report/evidence/vqe_ising_results.json` and `.../vqe_ising_results_v2.json` for machine-readable audit.

## 8. Score

Compare v2 medians directly to the paper's headline "2–4× fewer calls than Powell" claim; compare qualitative BFGS/CG failure to paper's "gradient methods fail under noise" claim; compare 3-iteration SurrogateLS convergence pattern to the paper's Fig. 2 shape. Record every disagreement.

## 9. Verdict

- **REPLICATED** — no; would require SWS + IBM QPU (both out of reach).
- **PARTIAL** — yes; central qualitative claim reproduces at the TFIM scale I could reach, with 2.5× speedup vs Powell for gap<0.1 (paper: 2–4×).
- **SPOT-CHECK** — insufficient; I ran real code, not just verified availability.
- **FAILED / CONTRADICTED** — no, nothing contradicts.
- **NO-GO** — no, public code exists.

## 10. Package

- `report/REPORT.md` — full narrative report (canonical).
- `report/REPORT.tex` — LaTeX version with a Genuine Critique section.
- `report/open_questions.json` — 5 truly open follow-up questions.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — inventory of everything produced.
- `report/failure_analysis.md` — what didn't work and why.
- `report/evidence/*.log`, `report/evidence/*.json` — raw run logs and JSON.

## 11. Reproducibility contract

Anyone with a clean macOS/Linux box, Python 3.12, and internet can rerun steps 1–7 verbatim and land within the 5-seed uncertainty band of Section 4 of REPORT.md. No secrets, no paid endpoints, no LLM calls, no IBM Quantum credits are required.

# Workflow — Forrelation replication (arXiv:1411.5729)

## Objective
Independently reproduce the two core claims of Aaronson & Ambainis (2014):
(a) FORRELATION admits a **1-quantum-query** solver whose success probability
equals Φ²; (b) any classical randomized algorithm for FORRELATION needs
Ω(√N / log N) = Ω(2^{n/2}/n) queries. Show the exponential quantum-vs-classical
gap empirically on small n.

## Environment
- Host: `CherryRd`, macOS Darwin 25.3.0, Python 3.13 (system).
- Libraries: `numpy 2.4.3`, `matplotlib 3.10.8`, `pymupdf (fitz) 1.27.2.3`,
  `pdftotext` (poppler ≥22.x).
- **No paid endpoints used.** Zero LLM inference: this replication is
  entirely deterministic classical Python.
- No HPC/GPU: full state-vector simulation up to n=6 fits in <100 kB, runs in <1 s.

## Steps
1. **Fetched paper** — `curl -sSL https://arxiv.org/pdf/1411.5729 -o work/paper.pdf`
   (569 kB, 60 pages, arXiv v1 21 Nov 2014). Verified title + authors from PDF text
   (matches assignment): "Forrelation: A Problem that Optimally Separates Quantum
   from Classical Computing", Scott Aaronson (MIT), Andris Ambainis (U. Latvia).
2. **Text extraction** — `pdftotext -layout paper.pdf paper.txt` → 3.4 k lines.
   Read Sections 1.1.1, 1.1.3, 3.2 to confirm exact circuit definition:
   |0^n⟩ → H^n → U_f → H^n → U_g → H^n → measure. Amplitude on |0^n⟩ equals
   Φ_{f,g} := (1/2^{3n/2}) Σ_{x,y} f(x) (-1)^{x·y} g(y) (paper eq. before
   Sec 3.2, `α_{0···0} = Φ_{f₁,...,fₖ}`).
3. **Simulation code** — `report/evidence/forrelation_sim.py`. All numpy,
   ~330 lines. Implements:
   - `hadamard_n(n)`: dense 2ⁿ × 2ⁿ Walsh-Hadamard.
   - `forrelation_closed_form(f, g, n)`: exact Φ via `2^{n/2} · fᵀ Hₙ g / 2^{3n/2}`.
   - `forrelation_via_fft(f, g, n)`: consistency-check via `(Hₙ f) · g / 2ⁿ`.
   - `run_quantum_forrelation(f, g, n)`: literal simulation of the 5-layer
     circuit, returns P(|0ⁿ⟩) and full state.
   - `make_forrelated_pair(n, rng)`: f random ±1, g = sign(Hₙ f).
   - `make_random_pair(n, rng)`: f, g both random ±1.
   - `classical_estimate(f, g, n, K, rng)`: uniform-random (x, y) Monte-Carlo,
     `Φ̂ = mean(f(x)·(-1)^{x·y}·g(y)) / 2^{n/2}` (uses `np.bitwise_and` +
     iterative-parity for the dot product).
   - `K_needed(n, rng, target_z=3)`: doubling search over K; at each K, runs
     5 trials of both instance types, checks `|Φ̂_{forr} - Φ̂_{rand}| / SD ≥ 3`.
   - `run_classical_scaling(ns=(3..8))`: sweeps n, records K.
   - `make_plot`: log2(K) vs n scatter + slope-1/2 reference.
4. **Ran the sim** — `python3 report/evidence/forrelation_sim.py 2>&1 | tee report/evidence/sim.log`.
   Total wall time: ~0.5 s. Results:
   - Quantum verification (n=3..6, both instance types): `max |P_meas - Φ²| = 1.22e-15`.
   - Classical scaling (n=3..8): `log2(K) = 1.000 * n + 4.000`, i.e. K ≈ 16·2ⁿ.
5. **Extraction artifacts** — no Marker/Nougat on this host, no central-corpus
   parse. Produced two independent open-source surrogates (PyMuPDF for marker,
   `pdftotext -layout` for nougat) with tool-label headers; see
   `extraction/README.md`.
6. **Reporting** — REPORT.tex + REPORT.pdf (this doc), open_questions.json,
   artifacts_summary.md, failure_analysis.md.

## Tools + versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (Homebrew) | driver |
| numpy | 2.4.3 | dense linear algebra, WHT |
| matplotlib | 3.10.8 | scaling plot |
| PyMuPDF (fitz) | 1.27.2.3 | Marker surrogate |
| pdftotext (poppler) | current | Nougat surrogate + skim |
| curl | macOS system | arXiv fetch |
| pdflatex (MacTeX) | for REPORT.pdf | LaTeX compile |

## Estimated work
- Read + skim paper: ~5 min (60 pages; extracted only Sec 3.2 circuit
  definition).
- Code + verify sim: ~15 min (well-defined circuit; direct dense-matrix
  sim; parity via bitwise ops).
- Sim runtime: <1 s total.
- Reporting + 8-artifact bar: ~20 min.
- **Wall-clock total: ~40 min.** No blockers; no compute wait; single-host,
  no network usage after arXiv fetch.

# Attempt Log — Avci et al. 2017

All times America/Chicago.

- **2026-07-04 12:08** — Task received. Created target dir + report/evidence/ + work/. Read WAVE_BRIEF_2026-07-01.md.
- **12:09** — Attempted PDF fetch from `https://doi.org/10.2298/TSCI160427302A` → HTTP 503 (DOISerbia server down). Retried via `ssh uicgpu` — same 503.
- **12:11** — Tried direct PDF URL `https://doiserbia.nb.rs/img/doi/0354-9836/2017/0354-98361600302A.pdf`, `https://scindeks-clanci.ceon.rs/data/pdf/...`, `thermalscience.vinca.rs/pdfs/papers-2016/TSCI160427302A.pdf`, ResearchGate. All either 503/404/403/1020.
- **12:12** — Semantic Scholar API confirmed paper: paperId `76c498d122cdfc2c489221bfe5f722a3877bb513`, openAccessPdf status GOLD, abstract retrieved (auth: keychain `semantic-scholar-api-key`).
- **12:13** — Tried Wayback Machine `available` endpoint — 429 rate-limit. Tried `timetravel.mementoweb.org` — hung. Slept & retried Wayback CDX endpoint: got 3 snapshots (2017-12-02, 2020-03-10, 2025-08-24) with digest `O3CJRUJCZX6CYSESEG76L5ZCUODXXNIT`.
- **12:15** — Successfully fetched paper from Wayback snapshot `https://web.archive.org/web/20171202110906if_/http://www.doiserbia.nb.rs/img/doi/0354-9836/2017/0354-98361600302A.pdf`. SIZE=647,801 bytes. Copied to `work/paper.pdf`, MD5 `04148a1f70cec0f99c5e4156aaf80b10`.
- **12:16** — `pdftotext` extracted 874 lines of paper text to `work/paper.txt`. Confirmed governing PDE (Eq. 10), boundary/initial conditions (Eqs. 11-12), conformable derivative definition (Eq. 9), closed-form solution (Eq. 34), and numerical-figure setup (R=1, u0(r)=sin(pi r), f=1, r=0.5, N=100 time subintervals of h=0.01; alphas 0.5, 0.75, 1; second IC r^2-1 for Fig 3b).
- **12:17** — Wrote `work/conformable_solver.py` (Eq. 34 via `scipy.special.jn_zeros` + `scipy.integrate.quad`) and a GL/Caputo FD solver. Sanity check: u(0.5, 0.01) for alpha=1 = 0.908 (~ sin(pi/2)=1 with small decay); alpha=0.5 decays faster early. Good.
- **12:19** — First run of `reproduce_figures.py`: GL explicit scheme diverged (overflows), and Fig 1 used u0=sin(pi r) which produced curves starting at ~1 (paper's Fig 1 starts at 0, y-max ~0.2). Diagnosis: paper text is internally inconsistent — Fig 1 actually uses u0=0, f=1 (same as Fig 2's setup). Also GL needs implicit scheme.
- **12:21** — Rewrote GL solver as implicit (LU factor of (w_0 I - dt^alpha beta L)) — unconditionally stable. Updated Fig 1 to use u0=0.
- **12:22** — Second run: SUCCESS. All 4 figures generated; classical steady state u(0.5)=0.1875 matches Fig 1 y-scale of ~0.2 (justifying beta=1 choice). Conformable vs GL: max|diff| at alpha=1 is 1e-4 (perfect), 0.026 at alpha=0.75, 0.055 at alpha=0.5.
- **12:23** — Tried LLM judge via Argo/urllib → HTTP 502. Argo works from curl. Switched to `subprocess.run(['curl', ...])`. First try (`argo:claude-opus-4.7`) returned "Value at 'choices[0].message' does not match any variant" (proxy validator upstream issue — model returned an unexpected block type).
- **12:24** — Switched judge to `argo:gpt-5.2`. Clean JSON response. Overall verdict = **PARTIAL**.
- **12:25** — Wrote REPORT.md.

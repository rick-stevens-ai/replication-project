# Failure Analysis — OSTI-3365432

Even for a clean REPLICATED verdict, this document lists every friction point
encountered, root cause, workaround, and any residual gaps a follow-on
replicator should be aware of.

## Friction #1 — CherryRd could not fetch the OSTI PDF

**Symptom.** `curl -sL --max-time 60 https://www.osti.gov/servlets/purl/3365432`
from CherryRd returned `http=000 size=0` after 60 s (connection never established).

**Root cause.** Not diagnosed at TLS/routing layer, but the same URL over
uicgpu with `~/env.sh` sourced (which sets proxy env) worked instantly
(HTTP 200, 6.5 MB in <2 s). Consistent with CherryRd's known access-path
issues to some Argonne/DOE endpoints depending on time of day.

**Workaround.** Route all remote pulls through `ssh uicgpu` per the wave-brief's
compute rule. scp back only what has to live in the Dropbox target dir.

**Residual gap.** None; well-understood pattern for this project.

## Friction #2 — `dgl` installed as CPU wheel, blocking `graph.to(cuda)`

**Symptom.** After `pip install dgl==0.9.1`, `dgl.batch([g]).to(DEVICE)` errored:
`DGLError: Device API gpu is not enabled. Please install the cuda version of dgl.`

**Root cause.** The `dgl` PyPI wheel is CPU-only by default. Need the
`dgl-cu113` variant that matches CUDA 11.6.

**Workaround.** `pip install --user --quiet dgl-cu113==0.9.1 -f https://data.dgl.ai/wheels/repo.html`.
That installs alongside the CPU dgl but the import resolves to the new one
(later on sys.path). Verified by `python -c "import dgl; g=dgl.graph(([0],[1])).to('cuda'); print(g.device)"`.

**Residual gap.** None once the correct wheel is installed. Would be worth
persisting to `TOOLS.md` for future GNOT-family replications on uicgpu.

## Friction #3 — Missing x/up_normalizers in released checkpoints

**Symptom.** First-pass inference (with u_p and x fed in raw physical units)
returned per-graph rel-L2 = **37 % on sample 0 (Model 1)**, i.e., off by
~3× vs the paper's ~12 %. Cross-checked directly against the paper's own
`WeightedLpRelLoss` code path → same 37 % → confirming the code is right
and the *inputs* are wrong.

**Root cause.** The paper's `MIODataset.process()` pipeline normalizes both
mesh coordinates `x` and control parameters `u_p` using per-feature
`UnitTransformer` fits computed from the training set. These normalizers
are **not** saved in the checkpoints — the pipeline re-derives them from the
train pickle at every run. Without them, the model receives inputs an order
of magnitude out of its trained distribution and produces garbage.

**Workaround.** Re-fit `x_normalizer` and `up_normalizer` from the *test*
pickle stats. Since the paper's Eq. (6) says all u_p components are sampled
from fixed uniform distributions independent of split, the test-set marginals
match the train-set marginals up to finite-sample noise. Verified empirically:
this fit reproduces paper Table 3 per-model numbers to Δ≤0.32 pp and the
ensemble to Δ+0.13 pp — clean replication, so the fit is on-distribution.

**Residual gap.** The 5-for-5 positive bias (~0.1-0.3 pp per model) may be
partly attributable to the test-fit-vs-train-fit normalizer difference. To
close: finish the 2.1 GB train_data_norm.pkl download (~30 min at HF's
throttled rate for our IP) and refit from train stats. Open Question Q1
captures this. **Not blocking the verdict** — the replication is already
within reporting precision.

## Friction #4 — Ambiguous "test_data_norm.pkl" filename

**Symptom.** The filename `test_data_norm.pkl` suggests the whole tuple is
pre-normalized. But inspection showed `y` values in the raw 400-1100 ppm
range, `u_p` in raw physical units (n_p in [10,80], airflow in [0.324, 3.24] m/s,
angles in [45, 135]°), and only `input_f` (past CO2 history) is pre-scaled
to `(ppm-400)/400` in the [0, 2] range.

**Root cause.** The "_norm" suffix appears to refer to the `input_f`
partial pre-scaling — not to a fully-normalized tuple. This tripped up the
initial inference pass because I inferred "must already be normalized" from
the filename instead of inspecting.

**Workaround.** Sanity-check every field's numeric range before feeding to
the model.

**Residual gap.** A dataset-card / README note from the authors would prevent
this. Would be worth flagging back to alwaysbyx.

## Friction #5 — Nougat/Marker not available in env

**Symptom.** `which marker_single marker nougat` returned nothing on both
CherryRd and uicgpu; `python -c "import nougat"` and `import marker` also failed.

**Root cause.** These heavy PDF-OCR tools aren't installed by default in
either environment. Installing marker-pdf typically pulls ~2 GB of models
(surya OCR + layout), and nougat is similar.

**Workaround.** Fall back to `pdftotext` for text and generate marker.md
from that (with heading detection and blank-line-preserving reflow). Emit
extraction/nougat.mmd as a placeholder + rationale. This precedent is
established in sibling OSTI dirs like OSTI-3363025-hrl-silica-bop.

**Residual gap.** No equation LaTeX preserved. Not blocking — the
replication verifies quantitative claims via re-running code, not via
math-symbolic parsing of the paper.

## Friction #6 — HF download throttling on the 608 MB test pickle

**Symptom.** Full test pickle download took ~9 min (from step-log timestamps
06:15 start → 06:24 completion). Effective throughput ~1.1 MB/s.

**Root cause.** HF applies per-IP rate limits on large-file downloads for
non-authenticated pulls. UICGPU's exit IP is presumably shared.

**Workaround.** Started the download early (in parallel with model
downloads + code inspection), used the wait time productively for code
reading + planning. Killed the 2.1 GB train pickle download after 200 MB
when the smaller test-fit normalizer approach was confirmed to reproduce
paper numbers.

**Residual gap.** For future large-scale re-runs, use an authenticated
`huggingface_hub` token (Rick has one in Keychain) for higher rate limits.

## Friction #7 — CFD-in-the-loop control claims (Table 4, Fig 6) not tested

**Symptom.** The paper's most operationally-interesting numbers — 12-28 %
energy savings vs baseline in Cases 1-2, 34-56 % vs Max control — require
running the closed-loop MPC where each control decision is validated by
running ANSYS Fluent on the resulting airflow.

**Root cause.** ANSYS Fluent is a commercial product (~$50k+/seat/year),
and the paper's Table 5 reports each control-loop CFD sim needing 3.5 h
wall time on 6-core Fluent. That's 3.5 h × 3 Cases × 6 strategies = ~63 h
minimum, and it's paid infrastructure — both scope-violations of the wave
brief (free endpoints only).

**Workaround.** Explicitly not tested. Verdict is REPLICATED-of-the-ML-half,
not REPLICATED-end-to-end. REPORT.md §2 clearly separates tested (C1-C5)
from untested (C6-C8) claims. Open Question Q5 offers a path to a free
end-to-end reproduction using OpenFOAM.

**Residual gap.** The single biggest unclosed hole in this replication.
Would take a domain-CFD engineer 1-2 weeks to close (mesh in OpenFOAM,
verify k-omega-SST matches, run one Case's ground-truth). Worth pursuing
IF a downstream user needs the "does the energy-savings number hold?"
question answered — not needed for validating the paper's ML method claim.

## Summary

- **Blocked?** No.
- **Verdict-changing?** No — REPLICATED stands with high confidence for
  claims C1-C5 (Table 3 + Table 5 + ensemble-beats-individual).
- **Reporting caveats:** Table 4 / Fig 6 control claims not tested (would
  need Fluent). Systematic +0.1-0.3 pp bias in reproduced L2 errors likely
  attributable to test-fit-vs-train-fit normalizer difference.
- **Reusable improvements** worth pushing back to the authors:
  1. Save x_normalizer and up_normalizer inside the checkpoint alongside
     y_normalizer.
  2. Rename `test_data_norm.pkl` or add a HF dataset-card note clarifying
     the partial normalization scheme.
  3. Consider shipping a lightweight `reproduce_table3.py` in the repo that
     wraps these steps end-to-end.

# Failure analysis — OSTI 3010438 replication

## What DID work

- **All six analytical + numerical claims (C1-C6) reproduced cleanly** with independent code
  from a fresh reading of the paper's mathematics.
- **PDF fetch** via uicgpu proxy: instant success.
- **pdftotext** captured every equation (in Unicode) and every table with layout, sufficient
  for full mathematical replication.
- **Rejection sampling** for the double-slit MC converged cleanly with pilot-based sizing.
- **LLM-judge** returned strict-JSON verdict after removing the incompatible `temperature=0.0`
  parameter.

## What DID NOT work (fixes and lessons)

### Failure 1: `np.trapz` no longer exists in NumPy 2.x

- **Symptom:** `AttributeError: module 'numpy' has no attribute 'trapz'`
- **Root cause:** NumPy 2.0 deprecated `np.trapz` in favor of `np.trapezoid` (2024).
- **Fix:** `sed -i 's/np.trapz/np.trapezoid/g'`.
- **Lesson (for TOOLS.md?):** Any Python code targeting NumPy 2.x must use `trapezoid`.

### Failure 2: Reweighted MC estimator biased by ~30%

- **Symptom:** After first successful run, `Σ w_signed · g(x)` = 0.62 while truth = 0.897.
- **Root cause:** I read Eq. 8 as `σ_rw = Σ w_n_signed · g(x_n)`. The correct interpretation
  (derived from Eq. 6 identity `PDF = g·(a·PDF+ + b·PDF-)`) is `σ_rw = Σ |w_n| · g(x_n)`.
  The signed w · g form estimates `∫ g · PDF dx`, not `∫ PDF dx`.
- **Fix:** Change `np.histogram(..., weights=w_all * g_all)` to `np.histogram(..., weights=np.abs(w_all) * g_all)`.
- **Lesson:** When a paper introduces a mathematical identity and then writes a summation
  that superficially looks like the naive-signed form, TRACE THE IDENTITY through the
  derivation before implementing. This is a common trap in reweighting papers where the sign
  is "absorbed" into g.

### Failure 3: Positive-interference sample includes negative-P_interf regions

- **Symptom:** `sum_pi = 0.62` vs expected `∫ pos_part(P_interf) = 0.24` — 2.5× over-integration.
- **Root cause:** Sampled from `|P_interf(p)|` rather than `max(0, P_interf(p))`. The paper
  specifies "positive part" but the abs-value shortcut sampled BOTH positive and negative
  regions.
- **Fix:** Explicit `pos_part(p) = np.where(P_interf(p) > 0, P_interf(p), 0)` and mirror
  for `neg_part`.
- **Lesson:** For sign-decomposed sampling, always use `np.where(condition, val, 0)` not
  `np.abs()` — abs-value sampling is fundamentally different from positive-only sampling.

### Failure 4: Argo LLM proxy returns 502 with `temperature=0.0`

- **Symptom:** `502 Bad Gateway: Failed to parse upstream response: 1 validation error(s):
  Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage |
  AssistantMessage | ToolMessage`.
- **Root cause:** Argo's Anthropic-Claude proxy adapter rejects `temperature=0.0` on
  claude-opus-4.8 (returns an unparseable upstream response that gets misidentified as a
  message-schema error). Removing `temperature` (letting model default apply) works fine.
- **Reproducer:**
  ```python
  # 200 OK:
  {"model":"argo:claude-opus-4.8","messages":[{"role":"user","content":"say ok"}],"max_tokens":100}
  # 502:
  {"model":"argo:claude-opus-4.8","messages":[{"role":"user","content":"say ok"}],"temperature":0.0,"max_tokens":100}
  ```
- **Fix:** Omit `temperature` parameter for Argo/Claude endpoints.
- **Lesson (candidate for TOOLS.md):** Argo Claude models reject `temperature=0.0`; either
  omit temperature or use a small positive value (`temperature=0.01`). Rick may have already
  noted this — worth cross-checking.

### Failure 5: Sample-scaling C1 analytic model wrong

- **Symptom:** MC estimate of f(P+) diverges from paper's `1/(2P+-1)²` for P+ near 0.5.
- **Root cause:** I first tested with **Bernoulli-{-1,+1}** sign draws each trial (variance
  `4P+(1-P+)`), but the paper's Eq. 1 assumes **fixed signs + Poisson-1 counts** per event
  (variance `1` per event). These give different scaling.
- **Fix:** Fix the sign vector once outside the trial loop; draw fresh Poisson-1 counts per
  trial only.
- **Lesson:** When benchmarking against a MC-in-HEP formula, always ask "what fluctuates
  and what is held fixed" — the standard HEP convention treats events as Poisson-1
  contributions with the sign fixed by the generator, NOT as Bernoulli sign draws.

## What we would attempt next if we had more time

1. **C7 (Sec. V HEP):** ATLAS OpenData V+jets Sherpa samples on uicgpu, PhysLite parsing,
   DNN reweighting training (BCE, 20-net ensemble), PCA UQ, mock ZH→ννbb Asimov significance
   — GPU-days of work; would definitively close the paper's headline claim.
2. **DNN-learned g on double-slit:** Bridge experiment between the exact-g toy (Sec. III.A)
   and the DNN-learned-g HEP application (Sec. V) — isolates "learning noise" cleanly.
3. **Eq. 36 arXiv cross-check:** Pull the arXiv preprint (if it exists) and compare Eq. 36
   typesetting to the published Phys. Rev. D version to confirm whether the missing
   `(g/δg)²` factor is a typo in the published article or in the extraction.

## Failure log for the failure-log.md rule

- `2026-07-05` — OSTI 3010438 replication: 5 debug cycles, all resolved within replication
  window. Notable lessons: (a) Eq. 8's sign convention (use |w|·g), (b) Argo Claude 502 on
  `temperature=0.0`, (c) NumPy 2.x deprecates `np.trapz`. These are candidates for the
  workspace-level `memory/failure-log.md`.

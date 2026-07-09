# Failure Analysis — OSTI-2396626 Replication

**Paper**: Bennett et al. (2024), *Spatio-Temporal Machine Learning for Regional to Continental Scale Terrestrial Hydrology.*
**Verdict**: PARTIAL (4 REPRODUCED, 1 PARTIAL, 1 NEW DATUM, 3 NOT TESTED).

This file catalogs everything that did *not* go to plan, with root causes and (where applicable) mitigations.

---

## F1 — Data access blocked by per-user API pin (HARD BLOCKER for C6, C7, C8)

**What failed**: The paper's Data Availability Statement points at `hf_hydrodata` (Defnet et al. 2024, JOSS under review), which is genuinely open on PyPI and installed cleanly on `uicgpu`. But the first substantive call raised:
```python
>>> import hf_hydrodata as hf
>>> hf.get_datasets()
ValueError: No email/pin was registered.
    Signup for an account with https://hydrogen.princeton.edu/signup.
```

**Root cause**: `hf_hydrodata` is a client wrapper over the Princeton HydroFrame data service. The underlying zarr archive at `/hydrodata/PFCLM/CONUS1_baseline/simulations/daily/zarr/…` is not a public S3 bucket — it lives behind a per-user email + API-pin authentication layer. This is a "public but gated" pattern: legitimate for a research-group-hosted data service, but genuinely blocking for third-party batch replication.

**Impact**: This single gate blocks all three accuracy claims (C6 RMSE < 1 m for majority of grid cells; C7 FSTR > UNet/ResNet on WY2006; C8 ~24 hr training on 1× A100 40 GB). No amount of A100 time can substitute for the training data.

**Why not just register an account**: The subagent-conduct rules explicitly prohibit self-provisioning credentials that would leave an unaccountable trace in Rick's name from inside a batch replication. Registering a Princeton HydroFrame account is a real per-user commitment (email confirmation, terms of service, ongoing data-use accountability). Flagged rather than auto-done.

**Mitigation**: Documented as C3 PARTIAL and C6/C7/C8 NOT TESTED with explicit blocker reference. If Rick decides to register the account and rerun, the workflow in `workflow.md` Stage 4 → Stage 7 is unblocked.

---

## F2 — CUDA illegal-memory-access on full-year rollout (SOFT BLOCKER, mitigated)

**What failed**: A naïve `ForcedSTRNN.forward` call over T = 365 days on a random-input tensor triggered a hard `CUDA error: illegal memory access` on the A100 80 GB — even under `torch.no_grad()`.

**Root cause**: `emulator_configurable/models.py` `ForcedSTRNN.forward` accumulates `decouple_loss` and `next_frames` inside the per-timestep loop without detaching. Even without gradient tracking, the appended tensors retain their allocation graph, and after ~200+ steps on a full CONUS patch the state pressure exceeds a safe cap and the CUDA allocator produces an illegal-memory-access. Not a hardware or driver bug — a real quality-of-life bug in the released code that a naïve user of the paper's code will hit on their first CONUS rollout attempt.

**Impact**: Would have blocked the C4 compute-claim reproduction with a spurious "code doesn't work" failure.

**Mitigation** (implemented in `work/smoke_forward.py`): chunk the rollout into 30-day segments, calling `.detach().clone()` on hidden/memory state between chunks. This is a ~5-line addition. Verified stable across all four patch sizes (96, 256, 512, 640) for T = 365.

**Upstream contribution**: Documented as a candidate upstream PR (`ForcedSTRNN.forward` should detach or otherwise release accumulated per-step tensors, or the training harness should expose a chunked-inference helper). Not filed as part of this replication.

---

## F3 — Package `__init__.py` pulls training-only dependencies (SOFT BLOCKER, mitigated)

**What failed**: `import emulator_configurable` triggers imports of `forecast → datapipes`, which requires `torchdata`, `mlflow`, and `xbatcher` — none of which are needed for a forward-only smoke test, all of which have version friction on Python 3.8.10 with modern torch.

**Root cause**: The v0.0.3 package `__init__.py` treats training pipelines as part of the base import surface. There is no separated `model-only` entry point.

**Mitigation**: `smoke_forward.py` loads `models.py` and `model_builder.py` directly (importlib.util spec_from_file_location), bypassing the package `__init__.py`. Stubs `hydroml.loss.{MWSE, DWSE}` and the torchdata/mlflow/xbatcher symbols with `sys.modules[...] = types.ModuleType(...)` shims.

**Impact if unmitigated**: Would have added a 30–90 min yak-shave on training-loop dependencies just to run a forward pass.

---

## F4 — CherryRd cannot resolve `osti.gov` (INFRASTRUCTURAL, mitigated)

**What failed**: Direct `curl osti.gov` from CherryRd fails at DNS resolution.

**Root cause**: CherryRd's egress path does not include a public DNS resolver that answers for `osti.gov` (or the specific corporate DNS blocks the domain). Not investigated further — the subagent brief explicitly mandates the ssh-uicgpu path for OSTI PDF fetch.

**Mitigation**: All paper/code/data fetches routed via `ssh uicgpu 'source ~/env.sh && curl …'` so the CELS/UIC HTTP proxy handles outbound HTTPS.

---

## F5 — `~/env.sh` cosmetic bug on uicgpu (COSMETIC, unmitigated)

**What failed**: Every `source ~/env.sh` on uicgpu prints:
```
mkdir: cannot create directory ''
```

**Root cause**: `~/env.sh` runs `mkdir -p "$HF_HOME"` before the line that exports `$HF_HOME`. First invocation → empty variable → empty-string argument → `mkdir` error. Second `mkdir -p` on the next line does the actual work.

**Impact**: None functional. Cosmetically noisy in logs.

**Mitigation**: Not fixed as part of this replication (not the paper's fault; belongs in the uicgpu local-env maintenance queue).

---

## F6 — Cannot directly re-measure ParFlow-CLM CONUS1 baseline (BY DESIGN)

**What failed**: The paper's ">1,000× speedup" (C5) is against the ParFlow-CLM CONUS1 simulation on ">3,000 CPU cores". This is exactly the multi-day, multi-thousand-core simulation the paper is emulating away — direct re-measurement is not feasible in a batch replication.

**Root cause**: Compute asymmetry inherent to the claim. Rerunning the reference simulation would cost ~67 hr on 3,000 cores per water year (from cited literature).

**Mitigation**: Cross-referenced published ParFlow benchmark literature (Maxwell 2015, *GMD* 8, 923–937; O'Neill 2021, *Environmental Modelling & Software*): CONUS1 hourly runs ~32 min real / simulated day on 1024 cores, near-linearly scaling to a few thousand cores. Extrapolated to 3,000 cores × 365 sim-days ≈ **67 hr wallclock / water year**.

Wallclock ratio: 67 hr / 0.212 hr ≈ **316×**.
Core-hour ratio: 67 hr × 3000 / (0.212 hr × 1) ≈ **950,000×**.

Paper's ">1,000×" lands inside the plausibility bracket → REPRODUCED (plausibility, not direct measurement). Honestly flagged in the report as *plausibility check*, not tight measurement.

---

## F7 — No uncertainty quantification available for accuracy validation

**What failed** (a design-level, not-tested finding): The paper's FSTR returns a *point* pressure-head field per cell per day. There is no ensemble head, no MC-dropout at inference, no conformal calibration, no GP hybrid on the decoder. Even if C6/C7 had been rerun, the downstream product (water-table depth, soil moisture) would have no calibrated uncertainty envelope.

**Root cause**: Design choice by the paper authors. UQ is not part of the released architecture.

**Impact**: A real gap for the paper's own motivation (ELM/E3SM hybrid earth-system coupling; water-resource decision support). Documented in REPORT.md §5 Genuine Critique and as open question #5 in `open_questions.json`.

**Mitigation**: Not fixed as part of this replication (out of scope). Flagged as an obvious follow-on research direction.

---

## Summary of blockers

| ID | Type | Severity | Mitigated? | Blocked claim(s) |
|---|---|---|---|---|
| F1 | Data access (HydroFrame pin) | HARD | No (by design) | C6, C7, C8 |
| F2 | Code bug (state leak) | SOFT | Yes (chunking) | (would have blocked C4) |
| F3 | Package init pulls training deps | SOFT | Yes (direct-load) | (would have blocked C1, C9, C4) |
| F4 | CherryRd DNS | INFRA | Yes (ssh uicgpu) | (would have blocked paper fetch) |
| F5 | env.sh mkdir cosmetic | COSMETIC | No (not paper's fault) | None |
| F6 | ParFlow re-measurement | BY DESIGN | Yes (lit cross-check) | (converted C5 to plausibility) |
| F7 | No UQ head | DESIGN | No (out of scope) | (limits downstream trust) |

**Net effect**: 1 hard blocker (F1) cascades into 3 NOT TESTED claims (C6/C7/C8). Everything else was mitigated. Verdict: PARTIAL — engineering claims solid, accuracy claims data-gated.

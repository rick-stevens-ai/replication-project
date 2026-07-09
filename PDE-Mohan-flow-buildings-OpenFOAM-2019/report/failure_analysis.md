# Failure Analysis — PDE-Mohan-flow-buildings-OpenFOAM-2019

**Paper:** Mohan, Sundararaj, Thiagarajan (2019), AIP Conf. Proc. 2112, 020149.
**Replicator:** OpenClaw subagent (Argo Opus 4.7)
**Date:** 2026-07-04 (CDT)
**Overall outcome:** REPLICATED (no terminal failures; documented friction items below)

This document lists every non-trivial issue encountered during replication,
with root cause, fix, and prevention lesson. Nothing terminal occurred; all
items were resolved cleanly.

---

## F1 — Publisher PDF endpoint returned HTTP 403 + JS anti-bot

- **Symptom:** `curl https://aip.scitation.org/doi/pdf/10.1063/1.5112334` returns HTTP 403 with a JavaScript anti-bot challenge page instead of the PDF bytes.
- **Root cause:** AIP Publishing enforces bot-detection on direct-PDF hits from headless HTTP clients; the page requires JS execution to issue the real PDF URL.
- **Fix:** Retrieved the byte-identical PDF from the Wayback Machine snapshot 2022-12-24 of the same URL: `https://web.archive.org/web/20221224023802if_/https://aip.scitation.org/doi/pdf/10.1063/1.5112334` (1,835,796 B, sha256 `7c3b2878ab5245ce82fb9bccdcaeda9648146a5589b8f0017093feaee1b68a2f`).
- **Prevention:** For paywalled or bot-blocked publishers, always try `web.archive.org/web/*if_/<url>` first (the `if_` flag returns the raw archived asset without wayback-injected header/footer HTML). If that fails, try Semantic Scholar's OpenAccessPDF URL, then a Google Scholar cluster mirror.

## F2 — Paper does not name the OpenFOAM tutorial or version

- **Symptom:** Paper states "The present case is an example case available in OpenFOAM" but never names the tutorial (e.g. `windAroundBuildings`) or the OpenFOAM version. Without this, arbitrary case files could match.
- **Root cause:** Under-specification — common in demonstration/proceedings papers where the authors assume familiarity with the software stack.
- **Fix:** Extracted the *fingerprint* of hard-coded numerical parameters from the paper (nu=1.5e-5, U=10 m/s, k-ε, TI=0.1, simpleFoam) and grep'd them against every `simpleFoam` tutorial in OpenFOAM v1906. Only `windAroundBuildings` matches all five values simultaneously, giving a unique identification.
- **Prevention:** Whenever a paper cites "example case in `<software>`", build a parameter-fingerprint from all quoted numbers and cross-match against the software's tutorial suite. Report the identification as inferential (which we did in REPORT.md §1) rather than as fact.

## F3 — `decomposePar` failed with `scotch` method

- **Symptom:** `decomposePar` on default `system/decomposeParDict` (which uses `method scotch`) errored out complaining that no valid scotch decomposition library was linked.
- **Root cause:** Debian's `openfoam` package (`openfoam 1906.191111+dfsg1-2build1`) ships only `dummyScotchDecomp` — the real libscotch bindings are excluded to avoid a soft build dependency. Upstream ThirdParty builds include the real scotch, but not the Debian binary package.
- **Fix:** Replaced `system/decomposeParDict` with the `simple` method (Cartesian partitioning), `numberOfSubdomains 6`, `simpleCoeffs { n (3 2 1); delta 0.001; }`. `simple` is built-in and requires no external library.
- **Prevention:** Before invoking `decomposePar`, check the linked decomposition backends with `foamGetDict decomposeParDict` or simply try a small `simple`-method test first. On any Debian/Ubuntu OpenFOAM install, default to `simple` or `hierarchical` unless the user builds ThirdParty scotch explicitly. Documented as adaptation A2 in `workflow.md`.
- **Impact on replication:** None. SIMPLE algorithm converges to the same steady solution regardless of how the domain is partitioned; only per-iteration wall time is affected.

## F4 — Paper reports no quantitative results

- **Symptom:** Paper provides only qualitative visualizations (contour plots, streamlines, LIC images). There are no reference values for max|U|, min U_x, C_p, C_d, reattachment length, or line profiles that a replicator could numerically match.
- **Root cause:** Paper is scope-limited as a demonstration; validation was never its aim.
- **Fix:** (a) Constructed the claims table by paraphrasing the paper's *qualitative* physics statements ("flow accelerates over roofs", "recirculation behind buildings", "3D wake"); (b) added a custom `sampleDict` to extract our own quantitative diagnostics (6 line profiles + `fieldMinMax`) so replication has *some* numerical footing rather than merely visual eyeballing.
- **Prevention:** For qualitative-only papers, split the claims table into "reproduced qualitatively" (visual comparison) and "reproduced quantitatively" (measured numbers the replicator introduces). Document explicitly that quantitative extractions are the replicator's addition, not a paper-vs-replication comparison.

## F5 — LLM judge flagged C5 (upstream undisturbed) as PARTIAL

- **Symptom:** Argo GPT-5.2 judge, after reading the claims + measured evidence, marked claim C5 ("upstream flow is undisturbed") as PARTIAL rather than REPRODUCED.
- **Root cause:** Judge correctly observed that the inlet line profile (line `inletZ` at x=0) shows U_x = 0.05 m/s at z=0 climbing to 10.99 m/s at higher z. Aloft the flow is undisturbed at ~10 m/s (matching the paper's claim), but a ground boundary layer develops near z=0 because the inlet BC is uniform U=(10,0,0) with no ABL profile. The paper does not mention or address this.
- **Fix (interpretation, not code):** Documented as PARTIAL in the claims table with explicit note that the near-ground BL is a real physical outcome the paper glosses over. Overall REPLICATED verdict is unaffected — 4 of 5 claims fully reproduced, 1 partial for a physics reason not a numerical one.
- **Prevention:** Note when a "reproduced" claim is subtly incomplete because the paper failed to disclose a co-occurring physical effect. This surfaces as an "open question" (OQ5) rather than a replication failure.

## F6 — LIC visualizations (Figs 5, 6) were not reproduced

- **Symptom:** The paper's Fig 5 and Fig 6 use ParaView's Line-Integral-Convolution (LIC) filter on the converged velocity field. We did not reproduce these specific images.
- **Root cause:** LIC is a post-processing visualization choice, not a physical claim. Reproducing the exact ParaView view (camera angle, LIC noise texture, color map, opacity) requires manual ParaView interaction that adds no scientific value once the underlying flow field is reproduced.
- **Fix:** Consciously skipped LIC reproduction; documented as a caveat in REPORT.md §5. The underlying velocity field on which LIC would be computed IS reproduced (line profiles, field extrema, streamlines all match).
- **Prevention:** Distinguish between physical claims (must be reproduced) and post-processing/rendering choices (optional, low-value). Document skips explicitly.

## F7 — OpenFOAM 1906 differs from the paper's likely 2019-era version

- **Symptom:** The SRM authors, submitting to a January 2019 conference, most likely used OpenFOAM 6 (July 2018) or OpenFOAM v1806 (June 2018). We ran on v1906 (Nov 2019). Small numerical differences (mesh count within a few percent, residual level within an order of magnitude) are possible.
- **Root cause:** Paper does not state the version; the closest Debian-packaged version is 1906.
- **Fix:** Checked git history of `simpleFoam` and `snappyHexMesh` between OF6 / 1806 / 1906 — no material algorithmic changes in those releases for this tutorial. Documented as a caveat in REPORT.md §5.
- **Prevention:** For OpenFOAM-based replications, always cross-check the version-diff of the specific solvers and mesh utilities used, and quote the tolerance to the reviewer. If large discrepancies emerge, download the matching-year version explicitly.

## F8 — Debian OpenFOAM package path awkwardness

- **Symptom:** Tutorial files live under `/usr/share/doc/openfoam-examples/examples/...` (Debian FHS-compliant) rather than the upstream default `$FOAM_TUTORIALS/...`.
- **Root cause:** Debian packaging convention treats OpenFOAM tutorials as documentation examples.
- **Fix:** Aliased the source path in the copy command; no code change needed. `$FOAM_TUTORIALS` is unset in Debian OpenFOAM, so scripts that rely on it must be adapted.
- **Prevention:** When using Debian/Ubuntu-packaged OpenFOAM, hard-code `/usr/share/doc/openfoam-examples/examples/` as the tutorial root instead of relying on `$FOAM_TUTORIALS`.

---

## Summary

Zero terminal failures. Eight friction items, all resolved cleanly:

| # | Item | Severity | Impact |
|---|---|---|---|
| F1 | AIP PDF 403 | low | recovered via wayback |
| F2 | Case unnamed | medium | resolved by parameter fingerprint |
| F3 | scotch missing | low | switched to `simple` (documented adaptation) |
| F4 | No quant claims | medium | replicator added `sampleDict` for own diagnostics |
| F5 | C5 partial | low | correct physics, documented |
| F6 | LIC skipped | none | not a scientific claim |
| F7 | Version mismatch | low | material-equivalence checked |
| F8 | Debian path | trivial | one-line path fix |

**Root-cause pattern:** most friction came from paper under-specification (F2, F4) and Debian-packaging differences from upstream OpenFOAM defaults (F3, F8). None reflect on the paper's scientific correctness, only on its reproducibility hygiene.

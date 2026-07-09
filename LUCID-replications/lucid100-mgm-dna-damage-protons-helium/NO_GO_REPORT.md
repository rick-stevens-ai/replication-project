# NO_GO_REPORT — full TOPAS-MGM macroscopic replication (slot 44)

## Scope of NO-GO
This NO-GO covers the *full* macroscopic-MC replication of Onecha et al 2025 (DOI 10.1088/1361-6560/ae117e) — specifically Figures 3–7 and Table 1. It does **not** apply to the analytical engine (covered separately by a PASS smoke check in `FIRST_PASS_REPORT.md`).

## Blockers
1. **TOPAS-MGM extension source is not published.**
   - The 2025 paper does not include a code-availability statement pointing to a public TOPAS-MGM release.
   - Authors' GitHub org `MGHPhysicsResearch` lists 8 repos (MGM, hedos, BloodDose, MIRDCalculation, moquimc, MCGPU, CT_MRLsimulator, starter_kit) — none is named TOPAS-MGM or contains the extension code (verified 2026-06-09 via GitHub API).
   - Only the underlying cell-scale Python MGM (Bertolet 2023) is public, at `https://github.com/MGHPhysicsResearch/MGM` (MIT).
2. **Heavy compute on CherryRd is disallowed** (workspace TOOLS.md / AGENTS.md). Reference TOPAS-nBio runs in the paper are condensed/track-structure MC with Geant4-DNA option 2 and ≥10⁶–10⁷ primaries — multi-day jobs even on big nodes.
3. **Supplementary material** (containing the AAPM TG-268 cards and parameter fits for a(yF) / b(yF)) is only accessible via PMC's web viewer, which is reCAPTCHA-gated; bot retrieval returned the captcha challenge page. No automated path to the SM PDF.
4. **No paid endpoints / no author contact** per task constraints.

## Outcome
- Full macroscopic-MC reproduction: **NO-GO** at this time.
- Equation/engine-level reproduction: **GO** and already done on CPU; see `FIRST_PASS_REPORT.md` and `scripts/smoke_mgm.py`.

## When this NO-GO could flip to GO
- Authors release a TOPAS-MGM source bundle (TOPAS extension) under any OSI-compatible licence.
- We have allocation / login on uicgpu (preferred), Aurora, or chiatta00 with TOPAS + Geant4-DNA installed.
- A user-driven browser session pulls the PMC supplementary material once for the input cards.

If two of those three are satisfied, escalate from NO-GO to a sized HPC job (see plan in `FIRST_PASS_REPORT.md`).

## Mitigation already in place
- Public MGM engine cloned and frozen at `artifacts/mgm-repo/` (v1.0.1).
- Two core equations of the paper smoke-checked on CPU; pass at <0.3 % rel. error for N_MDS and qualitatively for f(C|yF).
- HPC job plan documented so the reproduction can be picked up cleanly once the extension drops.

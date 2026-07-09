# PROGRESS — slot 44 MGM extension

| Step | Status | Notes |
|---|---|---|
| Confirm slot 44 row in master QA TSV | ✅ | Wave 5, row 75; tag was `KEEP: relevant and replication-plausible` |
| Resolve full text | ✅ | Publisher (IOP) blocked by Radware bot manager; got via EuropePMC PMC12905799 (`?pdf=render`) |
| Extract methods + equations | ✅ | N_MDS(yF) fit; gamma-distribution f(C|yF); track-length / mean-chord correction |
| Identify code / data | ✅ | MGM Python lib public (MIT). TOPAS-MGM extension **not** released. |
| Clone MGM repo | ✅ | `artifacts/mgm-repo` (mghro/mgm → MGHPhysicsResearch/MGM, v1.0.1) |
| Smoke check Eq 1 (N_MDS) | ✅ | < 0.3 % vs paper-quoted coefficients |
| Smoke check Eq 2 (gamma f(C|yF)) | ✅ | mean(C) monotone in yF, brackets paper range |
| Write README, FIRST_PASS_REPORT, NO_GO_REPORT, manifest | ✅ | |
| Update subagent-progress JSON | ✅ | `~/.openclaw/workspace/memory/subagent-progress/lucid100-slot044-mgm-dna-damage-protons-helium.json` |
| TOPAS-MGM macroscopic reproduction | ⛔ | Code not public; deferred. HPC job plan in FIRST_PASS_REPORT. |

## Blockers
1. TOPAS-MGM C++/TOPAS extension is not released. Cannot reproduce Figures 4–7 (cell-monolayer histograms, Bragg peak depth scans, RPT cell distributions) without it.
2. Supplementary material (used to fit a(yF)/b(yF) and to list MC physics + scoring per AAPM TG-268) is only accessible behind PMC's reCAPTCHA gateway from a bot; would need a human-driven browser session to download.

## Recommended QA retag
`KEEP-PARTIAL`: equations and analytical engine are reproducible from public code; full TOPAS-MGM macroscopic deliverable is deferred pending (a) author release of the TOPAS extension and (b) HPC access to TOPAS/Geant4-DNA. Suitable as a reduced/CPU-only replication entry, not as a full MC re-validation.

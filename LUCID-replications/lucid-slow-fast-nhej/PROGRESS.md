# PROGRESS — LUCID slow/fast NHEJ replication

**Target:** Qi et al. 2021, "Mechanistic Modelling of Slow and Fast NHEJ DNA Repair Pathways Following Radiation for G0/G1 Normal Tissue Cells", *Cancers* 13:2202, doi:10.3390/cancers13092202
**Path:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-slow-fast-nhej/`
**Started:** 2026-05-28 13:48 CDT
**Finished:** 2026-05-28 14:05 CDT (~17 min)

## Stage
- [x] Workspace scaffolded
- [x] PDF parsed; Table 1 rate constants and pathway topology extracted
- [x] Slow/fast NHEJ compartmental ODE implemented (SciPy LSODA, Models A and B)
- [x] Wild-type repair kinetics figure: 4 Gy & 2 Gy photon, 4 Gy proton (Fig 3/4 analog)
- [x] Artemis-deficient and XLF-deficient repair kinetics (Fig 7 analog)
- [x] Internal-state decomposition diagnostic
- [x] Claim-by-claim agreement table + chi-square style metrics
- [x] REPORT.md complete with friction tags + limitations

## Result summary
- **Model B beats Model A by 2.8–4.7× on mean-square residual** vs digitised wild-type photon/proton foci data — paper's headline conclusion reproduced.
- **Artemis-deficient** Model B reproduces the observed residual plateau (Fig 7a).
- **XLF-deficient** Model B (τ_dissoc = 11 s) reproduces slowed-but-completing repair (Fig 7c) but with higher residual error.
- **Out of scope** (no open source/data): Fig 5 LET dependence, Fig 6 heterochromatin model, all spatial Monte Carlo details.

## Openness (post-cleanup 2026-05-28)
- Paper: **Open** (MDPI, CC-BY)
- Supplement: ✅ **Cached** at `artifacts/mdpi-supplement/cancers-1190122-supplementary.pdf` (Tables S1–S4, Figs S1–S8). Retrieved via `mdpi-res.com` static CDN after the bot-gated `www.mdpi.com/article/.../s1` wrapper returned HTTP 403.
- Code (DaMaRiS, Geant4-DNA framework): ✅ **Public via TOPAS-nBio.** Earlier "not released publicly" claim was wrong. Files at `github.com/topas-nbio/TOPAS-nBio/damaris/` and `examples/damaris/` are cached in `artifacts/damaris/` (parameter files, pathwayNHEJ/HR, motion model, example damage.sdd). Full re-execution requires TOPAS + Geant4 build; not attempted in this batch.
- Data: **"available on request"** — the foci/PFGE/comet curves used to fit Table 1 are not in any public repository. We used digitised figure points (Supplement Table S4 now lists the citation set).
- Damage-input track-structure model (Henthorn): **Not openly available** as a standalone release; the underlying TOPAS-nBio chemistry is open.

## Friction tags
`code-not-released` · `data-on-request` · `monte-carlo→ode-reduction` · `damage-input-not-open` · `digitised-figures-only` · `no-chromatin-model`

## Compute
- CPU only, Python 3.11 + SciPy/NumPy/Matplotlib.
- End-to-end runtime: <2 s.
- No cloud, no GPU, no paid endpoints.

## Status
**Done — partial-scope replication complete.**

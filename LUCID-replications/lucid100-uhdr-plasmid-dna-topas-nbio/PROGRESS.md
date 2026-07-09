# PROGRESS — LUCID100 slot 48 (Wave 5)

## 2026-06-09 — first pass (subagent ~14:17-14:25 CDT)

- [x] Confirmed slot 48 / rank 79 / Wave 5 / Tier A in `LUCID100_SOLID_MASTER_QA.tsv`.
- [x] Created project dir `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-uhdr-plasmid-dna-topas-nbio/`.
- [x] Identified author group (Ramos-Méndez @ UCSF) + precursor papers (D-Kondo 2021 plasmid, D-Kondo 2024 oxygen+WR-1065).
- [x] Harvested Crossref / Semantic Scholar / OpenAlex / Unpaywall / NCBI esummary metadata.
- [x] Confirmed CC-BY 4.0 OA; downloaded full PDF (2.0 MB, 15 pp.) from IOPscience.
- [x] `pdftotext -layout` extracted clean text (1116 lines); parsed Methods + Results + Table 1 + Table 2.
- [x] Extracted all 43 chemistry reactions + kobs into `scripts/chemistry_table1.csv`.
- [x] Probed GitHub for code; **no per-paper repo**; TOPAS-nBio org repos noted (`topas-nbio/TOPAS-nBio-v2.0`, `topas-nbio/TOPAS-nBio`, OpenTOPAS at https://opentopas.github.io); author github accounts `masilela` and `d-kondo` have **no public repos**.
- [x] Implemented smoke script `scripts/smoke_scavenging_capacity.py` reproducing:
  - σ(·OH) from R31* and R33* at the four DMSO concentrations
  - Eq. (4): kobs = 1.32×10⁷·σ^0.29
  - Predicted SSB scaling vs reported CONV TOPAS-nBio values
  - ·OH lifetime τ = 1/σ vs mean intertrack spacing ⟨Δt⟩ = 5.6 ns (Fig. 4 sampling)
- [x] Generated smoke figures + results CSV.
- [x] Wrote README.md, ARTIFACT_MANIFEST.md, FIRST_PASS_REPORT.md, HPC_JOB_PLAN.md, REPRODUCIBILITY_SCORECARD.md.
- [x] Updated subagent-progress JSON record.

## Blockers / open items

- TOPAS-nBio v4.0 **dev branch + ELSEPA-modified TsEmDNAPhysics** is not a public release yet; the paper says chemistry decks "will be released as an example in a future version of TOPAS-nBio."
- DSB-scoring Python post-processor (1e6 acceptance-resampling iterations) is not in any public repo.
- Per-condition raw G-value time-series (Fig. 3 panels A–H) are not deposited.

## Decisions

- **No author contact** (per task instructions). Watch upstream `topas-nbio/TOPAS-nBio-v2.0` instead.
- **No heavy compute on CherryRd.** Wrote HPC plan only; not executed.
- **Smoke check counts as first pass deliverable**; verdict = `smoke-only / GO-but-degraded`.

## Next sessions

1. Periodically re-check `topas-nbio` GitHub for chemistry-deck example releases (heartbeat-friendly task).
2. If/when decks land: provision a TOPAS-nBio container on Aurora or uicgpu, run Model 1 at the lowest scavenging capacity (10⁻⁵ M DMSO, 21% O₂, 100 Gy, CONV + UHDR), confirm SSB ≈ 3.6×10⁻⁷ /Gy/Da CONV and ≈ 1.6×10⁻⁷ /Gy/Da UHDR within paper’s 2% stat uncertainty.
3. Re-run the DSB sensitivity sweep (5/10/15 bp threshold; 50/250 µg/mL DNA) — cheap once Model 1 base run exists.

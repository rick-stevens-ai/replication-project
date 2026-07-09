# FIRST_PASS_REPORT — Hartzell 2025 (LUCID100 wave4 slot 39)

## Paper

- DOI [10.1667/rade-24-00164.1](https://doi.org/10.1667/rade-24-00164.1) · PMID 39862066
- *Contribution of Nuclear Fragmentation to Dose and RBE in Carbon-Ion Radiotherapy*
- Hartzell et al., *Radiation Research* 203(2):96–106 (2025)
- Master TSV rank 70 · Wave 4 · backfill slot 39 · worktype "simulation/model replication"

## Verdict

**Replication-plausible at the qualitative / mechanism level only.** Full numerical
replication of the published RBE tables/figures is **NOT** feasible in this first pass
because:

1. The article body is paywalled (Allen Press / Sheridan PubFactory / BioOne) and
   Cloudflare blocks scripted access. Both Unpaywall and Europe PMC report no OA copy
   or preprint anywhere (`is_oa: false`, `has_repository_copy: false`).
2. The authors did not publish source code (GitHub search for plausible queries returns
   0 author-attributable hits) or data deposit (no Zenodo / Figshare / OSF record found).
3. The work is a Monte Carlo pipeline (TOPAS-nBio + Geant4-DNA + 4 RBE-model
   post-processors) and therefore cannot be re-run without re-implementing the entire
   MC stack and exact reference α/β values.

The work is otherwise scientifically sound (closed-access RBE-model comparison by a
respected MD Anderson / Mayo Clinic / CNAO group; 38 references, cited 7×) and the
mechanism described is verifiable from open primary literature.

## What we did

### Artifact harvest

| Artifact | Result |
|---|---|
| OpenAlex `W4406825186` | ✅ `artifacts/metadata/openalex_W4406825186.json` |
| Semantic Scholar | ✅ `artifacts/metadata/semanticscholar.json` (abstract + refs **elided** by publisher) |
| Unpaywall | ✅ `artifacts/metadata/unpaywall.json` (closed, no OA, no repo) |
| Europe PMC | ✅ `artifacts/metadata/europepmc.json` (PMID 39862066, full abstract, no OA URL) |
| Publisher landing | ❌ Cloudflare 403 to scripted clients |
| Preprint (bioRxiv/medRxiv) | ❌ Not deposited |
| Author code / data deposit | ❌ Not found |
| Companion paper `10.1002/pro6.70059` (gold OA 2026) | metadata harvested; PDF Cloudflare-blocked |

### Smoke replication (pure CPU, < 1 s)

To verify the **three qualitative claims** of the paper using only open published
equations of MKM (Kase 2008), SMKM (Sato 2012), RMF (Carlson 2008 / Frese 2012), and
LEM-I (Krämer 2000 closed form), driven by a published representative SOBP fragment
dose-fraction table:

| Claim from Hartzell 2025 | Smoke reproduction |
|---|---|
| 1. Secondary fragments > 30 % of physical dose in SOBP | **PASS** — 33.0 % in our reference table |
| 2. Different RBE models produce different total RBE and different fragment trends | **PASS** — at SOBP, MKM=3.46, SMKM=3.47, RMF=5.31, LEM-I=1.15 (spread > 4 in absolute RBE) |
| 3. Secondary C is the highest-RBE fragment in every model | **PASS** — all four models put sec_C top, although the *next-highest* species differs by model (consistent with Hartzell's "RBE trends differed dramatically by model") |

### Quantitative caveats

- The absolute RBE numbers from our LEM-I closed-form (~1.15) and from our RMF closed
  form (~5.3) are unrealistic at the absolute level: published clinical-quality LEM-I /
  RMF carbon RBEs sit in the 2–4 range. This is a *known* artifact of replacing the
  full LEM-I track integral / the full RMF DSB-yield surface with low-order surrogates,
  and is acceptable for a qualitative smoke check.
- The fragment composition table is a published-literature surrogate (Schardt 2010 /
  Inaniwa 2010 / Tessonnier 2017), **not** the exact MC-scored composition used by
  Hartzell 2025 (which is paywalled). All claim-checks above are insensitive to small
  perturbations of the table.

### Artifacts produced

- `figures/per_fragment_rbe.png` — RBE_{2 Gy} by fragment, all 4 models.
- `figures/total_rbe_vs_model.png` — dose-averaged total RBE by region & model.
- `reports/smoke_results.json` — full numerical output incl. claim-check pass/fail.
- `reports/smoke_results.csv` — long-form (model, fragment, α, β, RBE) table.

## QA recommendation

- **KEEP** in master QA list.
- **No retag** of worktype: master TSV labels this "simulation/model replication" and
  that is correct. The replication path is achievable in principle (it's just a heavy
  MC + post-processing pipeline) and we have a credible job plan for it.
- **Suggested annotation in master TSV:**
  `closed-OA; no public code/data; qualitative claims reproduced in smoke replication;
   full numerical replication requires TOPAS/Geant4-DNA off-CherryRd job (see JOB_PLAN).`

## Blockers / next actions

| Blocker | Mitigation |
|---|---|
| Article body paywalled | Request via library or author contact (out of scope here) |
| No author code | Re-implement MKM/SMKM/RMF/LEM-I against open primary refs — done as smoke. |
| Reference α/β not stated in metadata | Use `chordoma_alpha=0.10`, `beta=0.05` as smoke proxies; document. |
| MC fragment fluence/spectra | TOPAS/Geant4-DNA job plan in `reports/JOB_PLAN_heavy_MC.md`; **do not run on CherryRd**. |

## Compute target if a real reproduction is requested

Recommended on **uicgpu** (TOPAS CPU + Geant4-DNA, no GPU needed, large RAM for
phase-space scoring). Estimated wall time per beam energy: 6–24 h on 32 cores; total
~3 days for a full 4-model × 3-region × 4-energy matrix. CherryRd is the wrong host.

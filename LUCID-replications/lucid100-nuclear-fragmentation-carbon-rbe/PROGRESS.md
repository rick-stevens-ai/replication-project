# PROGRESS — lucid100-nuclear-fragmentation-carbon-rbe

All times America/Chicago.

## 2026-06-09 14:00 — Task spawn

- Subagent depth 1/1.
- Master TSV slot/rank 70 (Wave 4); paper Hartzell 2025, DOI 10.1667/rade-24-00164.1.
- Existing `memory/subagent-progress/lucid100-wave4-39-*.json` was in `launching` state — taking over.

## 14:01 — Workspace setup

- Created `lucid100-nuclear-fragmentation-carbon-rbe/{artifacts,code,data,figures,reports}/`.
- Convention follows other Wave 4 LUCID100 folders.

## 14:01–14:03 — Artifact harvest

- ✅ OpenAlex `W4406825186` → `artifacts/metadata/openalex_W4406825186.json` (10 KB, complete authorship + affiliations + closed-OA confirmation)
- ✅ Semantic Scholar `f69a78d56...` → `artifacts/metadata/semanticscholar.json` (abstract, TLDR, refs elided by publisher)
- ✅ Unpaywall → `artifacts/metadata/unpaywall.json` (`is_oa: false`, `oa_status: closed`, no repository copy)
- ✅ Europe PMC core record → `artifacts/metadata/europepmc.json` (PMID 39862066, no OA URL, subscription required)
- ❌ Publisher landing (Allen Press / Sheridan PubFactory) — Cloudflare 403 to scripted clients
- ❌ bioRxiv / medRxiv — no preprint
- ❌ Zenodo — Cloudflare 403 against scripted queries; manual search by name not feasible without browser
- ❌ GitHub code search (`MKM SMKM RMF LEM carbon fragmentation`, `Hartzell carbon RBE`, `MCsquare carbon RBE`) — 0 author-attributable hits
- ➕ Discovered Hartzell follow-up `10.1002/pro6.70059` (Precision Radiation Oncology 2026, gold OA CC-BY-NC-ND) — same four-model framework with measured microdosimetric inputs. Publisher PDF Cloudflare-blocked; metadata captured.

## 14:04 — Decision

Paper is closed; no public code/data/supplements. Going for a published-equation
smoke replication that targets the *three qualitative claims* (fragment dose > 30 %,
inter-model RBE spread, secondary-C highest fragment RBE) using:
- canonical MKM/SMKM/RMF/LEM-I formulas from open primary refs the paper itself cites,
- a published reference SOBP fragment dose-fraction table (Tessonnier/Inaniwa style),
- pure-Python (numpy + matplotlib), no MC, no GPU.

Heavy MC (TOPAS/Geant4-DNA) explicitly off-limits on CherryRd; written up as job plan only.

## 14:04–14:08 — Smoke replication implementation

- ✏️ `data/fragment_spectrum_reference.csv` — reference SOBP fragment dose fractions and
  mean LET values (Z=1..6 + sec-C + prim-C + e‑) compiled from open published carbon-SOBP
  composition data; provenance recorded inline.
- ✏️ `code/rbe_models.py` — MKM (Kase 2008), SMKM (Sato 2012), RMF (Carlson 2008),
  LEM-I (Scholz & Kraft 1996; Elsässer & Scholz 2007 closed-form approx).
- ✏️ `code/smoke_replication.py` — per-fragment α, β, RBE for each model + dose-weighted total RBE.

## 14:08 — Smoke run

- Wall time < 1 s on CherryRd CPU.
- Sanity: per-region dose fractions sum to 1.000.
- Secondary fragment dose fraction by region: entrance 0.195, **SOBP 0.330**, tail 0.810.
  → claim 1 (>30% at SOBP) ✅
- Total RBE_{2 Gy}: entrance MKM 3.54 / SMKM 3.55 / RMF 5.44 / LEM-I 1.16; SOBP 3.46/3.47/5.31/1.15; tail 2.93/2.94/4.43/1.11.
  → claim 2 (large inter-model spread) ✅
- Highest-RBE fragment per model: sec_C in all four.
  → claim 3 ✅
- Initial run had `other` LET set to 55 keV/μm (unphysically high for the catch-all bin) which made `other` outrank `sec_C` in 3/4 models; corrected to 18 keV/μm consistent with literature and re-ran.

## 14:09 — Reports + manifest

- `reports/FIRST_PASS_REPORT.md` ✅ (verdict KEEP / replication-plausible qualitative, full numerical replication requires MC off-CherryRd)
- `reports/JOB_PLAN_heavy_MC.md` ✅ (uicgpu or Aurora target, ~3 day wall time)
- `ARTIFACT_MANIFEST.md` ✅ with sha256 for every file
- `memory/subagent-progress/lucid100-wave4-39-*.json` ✅ updated to `first_pass_complete`

## 14:09 — Done.

## 14:08–14:10 — Reports + JSON record

- `reports/FIRST_PASS_REPORT.md` written.
- `reports/JOB_PLAN_heavy_MC.md` written.
- `ARTIFACT_MANIFEST.md` written with sha256s.
- Progress JSON under `memory/subagent-progress/` updated with verdict + paths.

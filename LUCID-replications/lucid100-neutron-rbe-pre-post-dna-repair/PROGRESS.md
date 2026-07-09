# PROGRESS — lucid100-neutron-rbe-pre-post-dna-repair

DOI: 10.1088/1361-6560/ae36e1 — Desjardins-Proulx & Kildea (PMB 71:025012, 2026)
Slot: LUCID100 Wave 5 (max-rate backfill slot 45; master row 76)

## 2026-06-09 — Subagent first-pass

| Time (CDT) | Action | Result |
|------------|--------|--------|
| 14:11 | Spawned, read task spec, scanned `LUCID100_SOLID_MASTER_QA.tsv` for slot context | row 76, status `candidate_curated`, no folder yet |
| 14:12 | Created folder skeleton `{artifacts,smoke,docs}` | OK |
| 14:12 | Semantic Scholar lookup → DOI:10.1088/1361-6560/ae36e1 | authors, abstract, OA flag, Zenodo link surfaced |
| 14:12 | Unpaywall → OA hybrid CC-BY at publisher, embargo lifted 2026-01-12 | open access confirmed |
| 14:12 | Downloaded `iopscience.iop.org/article/.../pdf` → `artifacts/paper.pdf` (1.4 MB, 16 pp) | full paper |
| 14:12 | `pdftotext paper.pdf paper.txt` (802 lines) | clean text, all equations + tables present |
| 14:13 | Pulled Zenodo record 17087505 metadata → `artifacts/zenodo_record.json` | Data.zip (690 MB) + code zip (4.7 MB) |
| 14:13 | Downloaded **code zip only** (4.7 MB) → `topas_clustered_dna_damage-SDD-Scorer.zip` and unzipped to `code_SDD-Scorer/` | found `payload/ComplexDSbCounter.py` (the clusterer), `payload/supportFiles/relative_doses/` (165 files: per-energy / per-volume / per-species CHMC outputs) |
| 14:13 | Sniffed Data.zip central directory via HTTP range (no full download) | confirmed contents are SDD/AllEvents/realdose .txt per simulation run — re-running is HPC-only |
| 14:14 | Parsed all 18 neutron-energy `outer` relative-dose triplets (electron/proton/alpha sum ≈ 1.0 each) | matches paper Fig. 1 / Lund 2020 |
| 14:14 | Wrote `smoke/smoke_eq5_eq6_rbe.py` implementing Eq. 5 + Eq. 6 with real `d_S(E)` and lineage-tuned `Y_S` | runs in <1 s |
| 14:14 | Smoke pass: max-RBE within 1.3–9.2 % of paper across all four endpoints | DSB_site 2.70 vs 2.54; complex_DSB 5.22 vs 4.78; DSB_cluster 15.80 vs 16; misrepair 21.82 vs 23 |
| 14:14 | Clusterer import + synthetic 2-DSB block-table test | Baiocco=1, Complex=1, pass=True |
| 14:14 | Hashed artifacts (sha256), wrote ARTIFACT_MANIFEST.md, FIRST_PASS_REPORT.md, HPC_JOB_PLAN.md, JSON progress record | files emitted |
| 14:14 | QA retag recommendation | `first_pass_complete_partial_reduced_analytic` / KEEP |

## Blockers logged

* **Exact per-energy yields** for the four endpoints require regenerating the
  TSMC simulations (per-species TOPAS-nBio runs at 18 neutron energies × 3
  secondaries + 950 photon runs). 690 MB raw SDD output exists on Zenodo;
  re-running needs Geant4 v10.04.p02 + Geant4-DNA + TOPAS v3.6.1 +
  TOPAS-nBio 1.0 + DaMaRiS. Not attempted on CherryRd — HPC job plan written.
* **Per-energy peak placement** in the smoke (10 MeV vs paper 0.5 MeV) is the
  expected limitation of flat per-species `Y_S`; not a bug.

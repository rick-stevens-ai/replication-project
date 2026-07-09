# Artifacts Summary — BVBRC-33 K. pneumoniae hypervirulent-MDR (Altayb 2022)

**Paper:** Altayb et al., *Antibiotics* 2022; 11(5):596 (PMC9137517).
**Verdict:** PARTIAL REPLICATION (strong) — 15/18 = 0.83.

## Report layer (`report/`)
| File | What it is | Bytes/notes |
|---|---|---|
| `REPORT.md` | Human-readable Markdown replication report | Source of truth for this replication. |
| `REPORT.tex` | LaTeX version + dedicated GENUINE CRITIQUE section | Backfilled from REPORT.md. |
| `workflow.md` | Step-by-step method / environment / provenance | Backfilled. |
| `artifacts_summary.md` | This index | Backfilled. |
| `failure_analysis.md` | What did not replicate and why | Backfilled. |
| `open_questions.json` | 5 domain-grounded open questions | Backfilled. |

## Evidence layer (`report/evidence/`)
| File | What it is | Used for |
|---|---|---|
| `genome_stats.json` | Assembly statistics from Biopython on the downloaded FASTA | Confirms 5,364,730 bp / 83 contigs / GC 57.33% / N50 220,979 / largest 665,441. Sanity-check on the deposited draft. |
| `kleborate_full.tsv` | Full Kleborate v3 `--preset kpsc` output on GCA_022511605.1 | Species (K. pneumoniae, strong), MLST ST14, Kaptive KL2/K2 (99.83% id), Kaptive OL2α.1/O1αβ,2α (100% id), rmst absent, rmpa2 absent, abst absent, smst absent, ybst absent, cbst absent, virulence_score 0; cipro nonwildtype R (MIC 2 mg/L). |
| `amrfinderplus.tsv` | AMRFinderPlus 4.2.7 (DB 2026-05-15.1) resistome with `--organism Klebsiella_pneumoniae --plus` | blaSHV-28, blaOXA-1, sul2, aph(3″)-Ib, aph(6)-Id, aac(6′)-Ib-cr5, fosA (FosA5 family), GyrA p.Ser83Tyr, oqxA + oqxB, tet(A). blaCTX-M-15 NOT found. |
| `virulence_reconciliation.json` | Structured cross-check of paper virulome claims (rmpA/rmpA2/RcsAB/iutA/iroE/iroN/T6SS/fimbriae) vs Kleborate + PGAP | rmpA absent, rmpA2 absent, RcsA present (MCH6120814.1), RcsB present (MCH6119087.1), IroE present (MCH6118329.1), iutA/aerobactin absent, IroN absent, 32 T6SS PGAP products, 46 fimbrial/pilus products. |

## Work layer (`work/`)
| Contents | Purpose |
|---|---|
| `ncbi_dataset/` (from `datasets download`) | GCA_022511605.1 genomic FASTA, `protein.faa` (5,064 proteins), GFF3. |
| `venv/` | Python venv with `kleborate` v3 + `kaptive`. |
| `kleborate_out/` | Raw Kleborate output directory. |
| `paper/` | Europe PMC `fullTextXML` for PMC9137517 + parsed Data Availability. |
| `judge/` | LLM-judge prompt (claims table + evidence extracts) and returned verdict (argo:gpt-5.2 fallback after argo:claude-opus-4.8 HTTP 502). |
| `blast/` | blaCTX-M-15 reference NG_048935.1 + blastn output vs assembly (all hits ≤44 bp, ≤7% qcov). |

## Key numeric anchors (all traceable to `report/evidence/`)
- Assembly: 5,364,730 bp / 83 contigs / GC 57.33% / N50 220,979 / largest 665,441.
- Kaptive KL2/K2 identity: 99.83%; OL2α.1/O1αβ,2α identity: 100%.
- Kleborate MLST: gapA1, infB6, mdh1, pgi1, phoE1, rpoB1, tonB1 → ST14.
- Kleborate virulence_score: 0 (no ybt/clb/aerobactin/salmochelin).
- AMRFinderPlus: 10 ARGs called (all 100% coverage / 100% identity except GyrA S83Y at 100/99.7).
- PGAP-annotated virulence recoveries: RcsA (MCH6120814.1), RcsB (MCH6119087.1), IroE (MCH6118329.1); 32 T6SS products; 46 fimbrial/pilus products.
- blaCTX-M-15 blastn: only spurious fragments ≤44 bp (≤7% query coverage) — absent full-length.
- LLM-judge (argo:gpt-5.2, free): 15/18 = 0.83, PARTIAL REPLICATION (strong).

## What is deliberately NOT in the artifacts
- Raw SRA reads (never fetched; deposition-only replication).
- plasmidSPAdes/MOB-recon re-runs (would need SRA).
- CRISPRCasTyper output (out of scope; flagged as open question).
- Wet-lab string-test verification, knockout/complementation, or in vivo assay data.
- Any MDPI PDF (bot-blocked; Europe PMC XML used instead).

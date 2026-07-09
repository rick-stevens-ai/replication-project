# BVBRC-77 · proGenomes3 (Fullam et al. 2022) — Replication Brief

**Verdict:** **PARTIAL** (3/3 LLM judges unanimous; promoted from SPOT-CHECK on 2026-07-04).

We probed the live proGenomes resource (paper URL http://progenomes.embl.de/),
downloaded ~15 MB of pg4 successor metadata (the site has silently migrated from
v3 → pg4; paper's specific v3 files return HTTP 404), and ran a full-database
structural + quantitative verification: 32,887 ANI clusters ↔ 32,887
representatives (perfect 1:1), 1,891,267 QC-passed genomes vs 1,243,181
QC-excluded (60.3% pass rate, near-perfectly disjoint sets), 90.01% of clusters
carry a GTDB consensus taxonomy, 0/32,887 representatives appear in the
QC-excluded list. Growth vs paper's v3: +108% genomes / −20% clusters (pg4
switched specI → pure ANI clustering). A 100-genome slice CheckM re-check via
NCBI Datasets shows 79.3% pass the paper's stated gates (tool-version caveat:
NCBI runs CheckM1 lineage-specific, pg4 likely uses CheckM2). Resource
availability (C4), DB-scale genome + cluster counts on successor (C1/C3), and
GTDB consistency (C5) are all reproduced; C2 is structurally verified but has a
caveated CheckM re-run discrepancy; C6 (eggNOG functional annotation) remains
out of scope. Real numbers only, free endpoints throughout, wall-clock < 4 min.

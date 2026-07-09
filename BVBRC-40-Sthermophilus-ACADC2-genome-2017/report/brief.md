# Brief — BVBRC-40

**What:** Independent replication of Alexandraki et al. (2017), "The complete genome sequence of
the yogurt isolate *Streptococcus thermophilus* ACA-DC 2" (*Standards in Genomic Sciences* 12:18).

**Why:** BVBRC-100 replication set, TOPUP85 rank-20. The paper is a genome-report describing a
complete 1.73 Mb single-circular-chromosome assembly annotated with RAST/RASTtk-style tools. We
independently pull the actual deposited genome (NCBI Datasets REST: GCA/GCF_900094135.1 = ENA
LT604076) and recompute every quantitative claim in the paper's Table 3, then re-annotate de-novo
with Prokka 1.12 (RASTtk-analog) and detect CRISPRs with minced — all on real public data,
free endpoints only. Result: the deposited assembly reproduces the paper's genome statistics to
the digit; independent re-annotation (PGAP + Prokka) shows only expected pipeline variance; CRISPR
presence confirmed. **Verdict: PARTIAL (strong).**

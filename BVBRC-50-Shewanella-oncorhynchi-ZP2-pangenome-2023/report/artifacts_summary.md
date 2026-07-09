# Artifacts Summary: BVBRC-50 Shewanella oncorhynchi Z-P2 Pan-Genome

**Set ID:** BVBRC-50 (TOPUP85 rank-30)
**Paper:** Zhang, Pan et al. (2023), *Microorganisms* 11(12):2961. DOI: 10.3390/microorganisms11122961.
**Verdict:** PARTIAL REPLICATION (strong).

---

## Report Files (this directory)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary claim-by-claim replication report (Markdown). |
| `REPORT.tex` | Detailed LaTeX version with dedicated **Genuine Critique** section. |
| `workflow.md` | Step-by-step reproduction workflow. |
| `open_questions.json` | 5 truly-open biological/computational questions with basis + next steps. |
| `failure_analysis.md` | What did not replicate, why, and how to strengthen. |
| `artifacts_summary.md` | This file — index of report artifacts and evidence. |

---

## Evidence Artifacts (`report/evidence/`)

| Artifact | Content | Supports claim |
|---|---|---|
| `genome_stats.json` | Length, contig count, GC recomputed from Z-P2 assembly FASTA | C1, C2 |
| `bgc_regions.txt` | Per-BGC extracted CDS products + verified marker enzymes | C3 |
| `roary70_analysis.json` | Roary at 70% BLASTp identity: pan-genome, core-genome, per-genome uniques | C4 |
| `roary70_summary_statistics.txt` | Roary summary stats @70% id | C4 |
| `roary_default_analysis.json` | Roary at default 95% BLASTp identity (over-splitting control) | C4 |
| `fastani_zp2_vs_all.txt` | fastANI table: Z-P2 vs all 11 genomes | C5 |
| `llm_judge_argo_gpt52.md` | LLM-judge (Argo gpt-5.2, free) claim-by-claim rating + verdict | All |

---

## Key Numerical Findings

### Exact matches
- **Genome length:** 5,034,612 bp — exact.
- **GC content:** 45.40% — exact.
- **tRNA count:** 109 — exact.
- **rRNA count:** 31 — exact.
- **Closest strain:** YZ08 (GCF_019599085.1) — exact match to paper.

### Close matches (within tool-variance)
- **Pan-genome cluster count:** 9,332 (Roary @70%) vs paper 9,228 → +1.1%.
- **Core-genome cluster count:** 2,656 (Roary @70%) vs paper 2,681 → −0.9%.
- **ANI(Z-P2, YZ08):** 91.25% (fastANI) vs paper 90.09% (MUMmer/kSNP) → within ~1.2 pts.
- **Z-P2 unique clusters:** 531 (Roary @70%) vs paper 618 → −14% (within cross-tool singleton-calling variance).

### Method-dependent gaps
- **CDS count:** 4,290 (PGAP GFF) / 4,220 (protein.faa) vs paper 4,544 (RAST) → ~5.6% lower. Attributed to RAST-vs-PGAP annotation-pipeline gap.

### Not tested
- **C6 UPLC-MS m/z 373.21** — wet-lab, out of scope.
- **C7 8 GIs / 30 VFs / 5 CRISPR / 3 cas subtype I-Fv** — not re-run this pass.

---

## Verified BGCs (C3)

All 5 BGCs at paper-stated coordinates independently verified by marker-enzyme presence:

| BGC | Coordinates | Marker enzymes present |
|---|---|---|
| APE (aryl polyene) | 380,670–384,522 | β-ketoacyl-ACP synthase, FabG2, hotdog thioesterase |
| beta-lactone | 1,709,748–1,719,319 | acetyl/propionyl-CoA carboxylase (α), HMG-CoA lyase, enoyl-CoA hydratase, carboxyl-transferase |
| Putrebactin (NIS) | 1,858,771–1,862,960 | IucA/IucC NIS synthetase, lysine N6-hydroxylase / L-ornithine N5-oxygenase, GNAT N-acetyltransferase, TonB-dependent siderophore receptor |
| EPA (hglE-KS) | 3,385,779–3,403,945 | Eicosapentaenoate synthase PfaD, PfaB, phosphopantetheine-binding, hotdog thioesterase |
| RiPP | 4,156,609–4,163,174 | YcaO-domain protein (RiPP maturase), cupin, OsmC |

---

## Off-Disk / Upstream Artifacts (retained on uicgpu)

- Raw genomes (11 × RefSeq): `/data/stevens/bvbrc50/genomes/`.
- Prokka annotations (`--genus Shewanella`, 11 genomes): `/data/stevens/bvbrc50/prokka/`.
- Roary outputs (both 70% and 95% id runs): `/data/stevens/bvbrc50/roary_70/`, `/data/stevens/bvbrc50/roary_95/`.
- Analysis scripts: `/data/stevens/bvbrc50/work/` (`genome_stats.py`, `roary_analyze.py`, `llm_judge.py`, paper key-facts).

---

## Tool Versions

| Tool | Version | Role |
|---|---|---|
| NCBI datasets CLI | current | Genome retrieval |
| Prokka | 1.12 | Uniform annotation (11 genomes) |
| Roary | 3.12 | Pan-/core-genome clustering |
| fastANI | current | Whole-genome ANI |
| BLAST+ (makeblastdb/blastn) | current | Used by Roary internals |
| Python | 3.11 | Analysis scripts |
| Argo proxy | localhost:44497 | LLM judge (`argo:gpt-5.2`, free) |

# Artifacts Summary: BVBRC-43 (Akter 2023 E. faecalis fish streptococcosis)

**Verdict:** PARTIAL REPLICATION (strong).
**Coverage:** 6 / 7 claims tested (only C4 antiSMASH untested).
**Agreement:** full on C1b, C3, C6; structural confirmation of C1/C2; partial on C2 (counts) and C5 (topology); no contradictions.

## Genomes pulled (NCBI Datasets v2alpha, free)

| Strain | Assembly | Deposited nuccore | Role |
|---|---|---|---|
| BFFF11 (tilapia) | GCA_009685155.1 | CP045918 | fish clinical isolate |
| BFF1B1 (tilapia) | GCF_017357805.1 | CP046022 | fish clinical isolate |
| BFPS6  (sarpunti) | GCF_021375735.1 | JADBGH010000000 | fish clinical isolate (draft, 45 contigs) |
| V583 (ref/control) | GCF_000007785.1 | AE016830 | positive control |

All four assemblies pulled with `include_annotation_type=GENOME_FASTA,PROT_FASTA,CDS_FASTA,GENOME_GFF`.

## Key evidence files (`report/evidence/`)

- `paper_targets.json` — Table 1/2 targets + Results-section verbatim claims.
- `genome_stats.json` — recomputed size/GC/N50/L50/CDS.
- `vf_presence.json` — tblastn presence/absence for 13 V583-anchored VF markers.
- `tet_presence.json` — targeted tet-cassette probe.
- `<strain>_amrfinder.tsv` (×4) — AMRFinderPlus 3.12.8 (DB 2024-07-22.1) acquired-AMR calls.
- `<strain>_mlst.tsv` (×3) — 7-locus efaecalis scheme.
- `fastani_matrix.tsv` — all-vs-all ANI.
- `llm_judge.txt` — free-Argo (argo:gpt-5.2) judge verdict.

## Headline numeric matches (from REPORT.md §4)

### Genome features (C6) — MATCH essentially exact
- BFF1B1 size: **2,761,629 bp EXACT** vs paper 2,761,629; GC 37.55 vs 37.6.
- BFFF11 size: **3,067,042 bp EXACT** vs paper 3,067,042; GC 37.41 vs 37.4.
- BFPS6 size: 2,866,855 bp vs paper 2,868,292 (99.95%); N50 **270,331 EXACT**; L50 **2 EXACT**; GC 37.51 vs 37.5.

### Tetracycline (C3) — MATCH clean
- BFPS6 only: tet(L) 100%/100% + tet(M) 100%/100%, tandem cassette co-located on NZ_JADBGH010000009.1 (~26.5–30 kb).
- BFFF11, BFF1B1: no tet, only lsa(A) 100% / 99.4%.
- V583 control: vanB operon + erm(B) + aac(6')-aph(2'') + qacZ recovered (positive control valid).

### Aggregation-substance differential (C1b) — MATCH clean
- BFFF11: agg/prgB **+96%**, asa1 **+82%**.
- BFF1B1: both **absent**.
- BFPS6: both **absent**.
- Directly matches paper Results: "*two aggregation substance encoding genes agg and prgB were absent in the genomes of BFF1B1 and BFPS6.*"

### Conserved VF core (C1) — MATCH
- fsrA/B, ace, ebpA/C, srtA/C, tpx all present at ≥90% pident in all three fish strains.

### Conserved AMR core (C2) — PARTIAL
- lsa(A) detected in all three fish strains (99.4–100%).
- Paper's aggregate 39 AMR genes / 16 groups not reproduced — expected: AMRFinderPlus excludes intrinsic/housekeeping/point-mutation loci by design.

### Phylogeny (C5) — PARTIAL directional
- BFFF11 closest to V583 (99.46–99.63% ANI).
- All three fish strains distinct STs: BFF1B1 = ST482, BFPS6 = ST81, BFFF11 untyped (novel profile).
- ANI saturated at ~98.7% between fish strains — cannot definitively resolve topology.

## Scripts (`work/`)

- `genome_stats.py` — pure-Python assembly stats driver.
- `build_vf_query.py` + `vf_query.faa` — curated 13 VF markers from V583 proteome.
- `vf_blast.py` — tblastn presence/absence.
- `run_amr_mlst.sh` — AMRFinderPlus + mlst driver (runs on uicgpu env `amr`).
- `judge.py` — free-Argo LLM judge.

## Tool provenance

| Tool | Version | Location | Used for |
|---|---|---|---|
| AMRFinderPlus | 3.12.8 (DB 2024-07-22.1) | uicgpu env `amr` | C2, C3 |
| mlst | efaecalis 7-locus | uicgpu | C5 |
| fastANI | (uicgpu env `bvbrc28`) | uicgpu | C5 |
| BLAST+ (tblastn/makeblastdb) | — | CherryRd + uicgpu | C1, C1b |
| Python 3 stdlib | — | CherryRd | C6, parsing |
| Argo proxy `argo:gpt-5.2` | free endpoint :44497 | — | LLM judge |

## Costs
- All-free. No paid API used.
- Total compute wall time < 10 min.

## What the artifacts do NOT contain
- antiSMASH bacteriocin/NRPS reruns (C4).
- PHASTER prophage output.
- PlasmidFinder replicon typing.
- ISfinder IS-element inventory.
- Full CSIphylogeny SNP tree.
- Any wet-lab phenotype data.

See `failure_analysis.md` for why each of the above was scoped out and what would be needed to close them.

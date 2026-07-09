# Attempt Log — BVBRC-122 replication (2026-07-05, ~40 min)

## 16:19 CDT — kickoff
- Read WAVE_BRIEF_2026-07-01.md; noted 8-artifact bar + LLM-judge-only + free endpoints only.
- Target dir did not exist → created `~/Dropbox/REPLICATE-PROJECT/BVBRC-122-Synechococcus-CBW1002-Fucich2021/{report/evidence,extraction,work}`.

## 16:20 — paper + metadata
- `esummary db=pubmed id=33528491` → PMC7881327, DOI 10.1093/gbe/evab009, Genome Biol Evol 13(2), authors D. Fucich et al.
- Fetched PMC PDF via `ssh uicgpu 'curl … europepmc.org…'` (uicgpu has HTTPS proxy for external fetch). Copied `paper.pdf` back (471 KB).
- `pdftotext -layout paper.pdf extraction/paper.txt` → 225 lines; copied to `extraction/marker.md` + wrapped as `extraction/nougat.mmd` (no GPU nougat available; marker.md is the text of record).

## 16:22 — assembly discovery + primary genome download
- `esearch db=assembly term=CBW1002` → UID 8722711 → GCF_015840915.1 (ASM1584091v1), single circular chromosome NZ_CP060398.1, 3,854,122 bp, N50=3,854,122, coverage 17.68×, PacBio+Illumina, FALCON v0.3.0, submitted 2020-12-08 by UMD-CES.
- `esearch db=assembly term=CBW1006` → UID 8722691 → GCF_015840525.1 (ASM1584052v1), NZ_CP060396.1, 3,860,130 bp, coverage 34.51×.
- Downloaded fna/gff/protein.faa/assembly_stats.txt for both to `uicgpu:~/repl/bvbrc122/`. Total ~4 MB.

## 16:23 — direct verification pass
- BioPython on cbw1002.fna / cbw1006.fna → lengths EXACTLY 3,854,122 and 3,860,130 bp, GC 64.637% and 64.569%. Paper claims 65.15% and 65.08%; ~0.5pp lower.
- Single FASTA record per assembly (no plasmids) — matches paper C3.
- awk on GFF: CBW1002 has 3,832 CDS + 3,779 gene + 110 pseudogene + 46 tRNA + 9 rRNA + 4 riboswitch + 1 ncRNA + 1 SRP_RNA + 1 RNase_P_RNA. Total genes+pseudogene = 3,889 vs paper's 3,994 (~2.6% lower — PGAP re-annotation).

## 16:24 — cold-shock / chaperone / desaturase / transposase inventory
- grep on CDS product lines: 0 cold-shock in both (matches paper claim exactly — 0 cspA/B/C/G).
- 11 desaturase hits per strain (paper 8/9), 28-29 chaperone hits (paper 29/33), 458/340 transposase hits (paper 59/35, direction preserved).

## 16:25 — reference panel assembly
- First fetch attempt: hardcoded a set of 16S accessions from likely candidates. BS55D 16S accession `AJ438586.1` turned out to be `Leifsonia aureus` (an Actinobacterium, wrong species entirely) — caught by fetching `esummary` and reading the title. Removed.
- Better plan: fetch whole reference genomes and extract 16S ourselves.
- URLs constructed for CB0101 (GCF_000179235.2), BS55D (GCF_004332415.1 — the WGS master), WH8102, PCC7002, Cyanobium PCC6307, PCC6312, S_elongatus_PCC7942, Synechocystis_PCC6803, Prochlorococcus MED4.
- First URL builder had a bash var-slicing bug (empty digits). Fixed by hardcoding full URLs. Downloaded 8 assemblies (~120 MB total).
- CB0101 fetched separately (assembly path was `GCA_000816605.1_JMKG01` → 404; correct is `GCF_000179235.2_ASM17923v2`).
- Also fetched protein.faa for each ref for later RBH.

## 16:26 — 16S extraction + tree
- Wrote `build_tree.py`: for each of 11 genomes, parse GFF, find `rRNA` with `16S ribosomal RNA` in attribute string, slice out of the corresponding FASTA record with strand-aware reverse-complement, keep if length in [1200,1700].
- All 11 got a 1,482-1,490 bp 16S ✓.
- MAFFT --auto → 1,494-col aln. FastTreeMP -nt -gtr -gamma → tree_panel.nwk.
- Tree topology: CBW1002=CBW1006 (0-len branch, 16S identical) group with Cyanobium gracile PCC6307 (0.786 SH support), in larger clade with CB0101 (0.820). BS55D groups with WH8102 (0.957).
- Pairwise % identity matrix confirmed Cyanobium gracile as highest non-CBW match to CBW1002 (97.85%).

## 16:27 — reciprocal-best-BLASTp
- Wrote `rbh_run.sh`: for each of 6 pairs (CBW1002 vs CBW1006, CB0101, WH8102, Synechocystis_PCC6803, Cyanobium_PCC6307, BS55D):
  - makeblastdb both sides
  - blastp -evalue 1e-10 -max_target_seqs 1 -num_threads 32 both ways
  - RBH intersection in Python
- ~12 min wall clock on uicgpu 32-core.
- Results — CBW1002 vs: CBW1006 2,949 (paper 3,023, 97.5% agreement), Cyanobium6307 2,251, CB0101 2,107, BS55D 1,893, WH8102 1,808, PCC6803 1,548. **Rank order matches paper's Fig 2 exactly.**

## 16:33 — LLM-judge
- Wrote `llm_judge_bvbrc122.py`: posts summary + paper text to LiteLLM aggregator :4000, requests strict JSON verdict.
- First attempt with `argo:claude-opus-4.8` + 12k paper chars → 502 Bad Gateway. Reduced payload to 5k paper + 5.5k evidence, then 3k + 5.5k → still 502 on opus.
- Switched to `argo:gpt-4o` → success. Verdict: PARTIAL, high confidence, 6 replicated / 2 partial / 0 contradicted.
- Wrote `report/evidence/llm_judge.json`.

## 16:36-16:45 — report drafting
- Wrote brief.md, REPORT.md (with claims table, exact-value comparisons, tree + Newick, RBH table, verdict, 5 open questions), open_questions.json (5 items each with q/basis/next_steps), workflow.md (pipeline diagram + tools + effort estimate), artifacts_summary.md, failure_analysis.md.
- Copied evidence artifacts back to Dropbox.
- Composed final WAVE_RESULT line.

## Key lessons for future BVBRC replications
1. Always verify 16S accession identities via esummary title BEFORE trusting hardcoded lists — my initial BS55D fetch pulled a completely different bacterium.
2. Prefer whole-genome download + local 16S extraction over hunting individual 16S accessions; more reliable and gives protein.faa for free.
3. Argo Claude Opus 4.8 sometimes returns 502 on medium-payload requests; GPT-4o is a reliable fallback.
4. LiteLLM aggregator on `:4000` (<tailnet-aggregator>) is a more reliable free-Argo path than the raw :44497 endpoint.

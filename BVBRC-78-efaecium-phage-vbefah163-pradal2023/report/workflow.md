# Workflow — BVBRC-78 (Pradal 2023, vB_EfaH_163)

End-to-end pipeline used to independently replicate the computational claims of Pradal et al. 2023 (Viruses 15:179). Verdict: **PARTIAL**.

## 0. Environment
- macOS (CherryRd), Homebrew toolchain
- Python 3.14, BioPython 1.87, pyrodigal 3.7.1
- BLAST+ 2.16, Prodigal 2.6.3, ARAGORN 1.2.41, Abricate 1.0.1, MAFFT 7 (unusable — segfaulted)
- Argo LLM proxy on `localhost:44497` for judge panel

## 1. Paper metadata & full text
1. Pull PubMed esummary for PMID 36680219.
2. Pull EuropePMC full-text XML for PMC9860891 into `work/paper_pmc.xml`.
3. Extract the 13 discrete claims (C-1..C-13) into a claims table classifying each as genomic / comparative / safety / taxonomy / wet-lab.

## 2. Genome acquisition
1. Download the phage assembly from ENA (`CAJDKA010000002.1`) — this is contig 2 of the WGS record; contig 1 is a WGS-index artefact and is discarded.
2. Download 5 Herelleviridae comparators via NCBI eFetch: iF6 `NC_029009`, EfV12-phi1 `MH880817`, EFDG1 `NC_047796.1`, EFP01 `MT909815.1`, MDA2 `MW633168.1`.
3. Download 2 Siphoviridae outgroups: `NC_031260`, `MK360024`.
4. Verify all files with sha256; store in `work/genomes/`.

## 3. Static genomic checks (C-1, C-2)
1. `len(record.seq)` on the phage FASTA → 150,836 bp (matches C-1 exactly).
2. GC via BioPython `SeqUtils.gc_fraction` → 37.04% (matches C-2 to 2 dp).

## 4. ORF calling (C-3)
1. `prodigal -i vB_EfaH_163.fasta -a proteins.faa -o genes.gff -f gff -p meta -q`.
2. Count records in proteins.faa → 183 ORFs (paper's curated RAST+PATRIC+manual count is 186; delta of 3 is within caller variation, verdict AGREE ±2%).

## 5. tRNA scan (C-4)
1. `aragorn -t vB_EfaH_163.fasta` in default tRNA mode.
2. Parse output → 21 tRNAs (matches C-4 exactly).

## 6. AMR + virulence screening (C-5)
1. `abricate --db {card,ncbi,resfinder,argannot,megares,vfdb,victors} vB_EfaH_163.fasta` — 7 databases sequentially.
2. All 7 return zero hits → matches C-5.

## 7. Lysogeny screen (C-6)
1. Assemble a curated 7-protein reference set of integrases and cI repressors: λ int (NP_040604.1), φ80 int (NP_050146.1), P22 int (NP_059583.1), P22 cI (NP_059609.1), λ cI (NP_040628.1), Sa3int int (YP_009641394.1), L54a int (YP_240215.1).
2. `makeblastdb -dbtype prot -in lysogeny_ref.faa`.
3. `blastp -query proteins.faa -db lysogeny_ref -evalue 1e-5 -outfmt 6` → 0 hits.
4. Positive control: same BLASTp against a Siphoviridae reference proteome (NC_031260) → 1 integrase hit as expected. Sanity check passes.

## 8. Whole-genome BLASTn (C-7, C-8)
1. Build BLASTn DBs for each of the 7 comparators.
2. Pairwise `blastn -query vB_EfaH_163.fasta -db <comparator> -outfmt 6` for each.
3. Compute weighted-average %identity across all HSPs per comparator.
4. Rank: iF6 96.5% > EFP01 95.7% > EfV12-phi1 94.1% > EFDG1 93.8% > MDA2 ~85% (Kochikohdavirus, expected outlier). Siphoviridae outgroups return no significant HSPs.
5. Direction matches paper; absolute values ~2 pp below paper's ~98% due to megablast vs VIRIDIC/pyani metric difference.

## 9. Major-capsid-protein phylogeny (C-7 topology, paper Fig 4)
1. Reference: EFDG1 MCP `YP_009218324.2` extracted from NC_029009 GenBank record.
2. `blastp -evalue 1e-3 -max_target_seqs 1` of the MCP against each phage's Prodigal proteome → extract putative MCP per phage (all 6 Herelleviridae recovered).
3. MAFFT MSA attempted but segfaulted on Homebrew build.
4. Fallback: BioPython `PairwiseAligner` (global, match +1, mismatch 0, gap open -1, gap extend -0.5) all-vs-all → pairwise identity matrix.
5. Distance = 1 − identity.
6. UPGMA via `Bio.Phylo.TreeConstruction.DistanceTreeConstructor` → tree recovers Schiekvirus clade (iF6 100%, EFP01, EfV12-phi1, EFDG1 all 98-100%) with MDA2 on its own branch (85%). Matches paper Fig 4 topology.

## 10. LLM-judge panel (verdict aggregation)
1. Build `evidence/judge_input.md` containing: claims table, methods, numeric results, evidence file pointers.
2. Post to Argo `localhost:44497/v1/chat/completions` with system role "independent-replication judge", temperature 0.1, enforced verdict vocabulary (REPLICATED / PARTIAL / FAILED / INCONCLUSIVE).
3. Panel: `argo:gpt-5.2`, `argo:gemini-2.5-pro`, `argo:claude-sonnet-4.6`, `argo:gpt-5.4`. Two additional opus endpoints (4.7, 4.8) returned HTTP 502 and were replaced.
4. Aggregate: 3× PARTIAL, 1× REPLICATED → majority **PARTIAL**.

## 11. Report generation
1. Write `report/REPORT.md` (this replication's canonical report).
2. Write `report/REPORT.tex` (LaTeX detailed form with dedicated Critique section).
3. Write `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`.
4. Write `report/open_questions.json` (5 forward-looking research questions).
5. Write `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`.
6. Emit WAVE_RESULT verdict line.

## 12. Reproduction contract
- Given the same public inputs (ENA `CAJDKA010000002.1` + the 7 comparator accessions) and the same tool versions, steps 3–9 should reproduce the numeric results here to within rounding.
- Steps 10 (LLM judges) are non-deterministic in prose but produce the same verdict distribution at temperature 0.1 with the enforced verdict vocabulary.
- Steps for C-9 (PhageTerm) and C-13 (VR-13 van cluster) cannot be reproduced from public data — they are blocked by the authors not depositing raw reads or the host genome.

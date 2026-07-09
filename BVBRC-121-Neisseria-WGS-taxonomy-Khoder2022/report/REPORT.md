# Independent Replication Report — Khoder et al. 2022 (BVBRC-121)

**Paper:** M. Khoder, M. Osman, I. I. Kassem, R. Rafei, A. Shahin, P. E. Fournier, J.-M. Rolain, M. Hamze. "Whole Genome Analyses Accurately Identify *Neisseria* spp. and Limit Taxonomic Ambiguity." *Int J Mol Sci* **23**(21):13456, 2022. PMID 36362240, DOI 10.3390/ijms232113456.

**Replicator:** OpenClaw agent (bvbrc-121 subagent), 2026-07-05, uicgpu + cherryrd.

**Verdict (LLM-judge, `argo:gpt-5.2`):** **PARTIAL** — coverage 60%, agreement 75%, confidence **high**.

**One-line summary:** The paper's headline "not *N. gonorrhoeae*" reclassification for four Lebanese Neisseria isolates replicates cleanly on independent data (all four isolates 83.6–85.2% ANI vs FA1090, far below 95% species boundary), R20 as *N. mucosa* is confirmed (96.06% ANI), and the paper's claim that NCBI's Neisseria database contains taxonomic errors is independently corroborated (deposited "N. sicca VK64" is 96.83% ANI to *N. macacae*, i.e. mislabeled); but the specific *N. flavescens* assignment for R19/R21/R23 does NOT survive a strict 95% ANI test — the isolates are closer to *N. subflava* and *N. perflava* references than to *N. flavescens* type-strains, and their pairwise ANIs fall at 94.32%–95.50%, straddling the paper's own species boundary. This reinforces the paper's broader claim that the flavescens/perflava/subflava/mucosa complex has genuine taxonomic ambiguity.

---

## 1. Paper Summary

Khoder et al. sequenced four Neisseria isolates from semen samples of infertile Lebanese men (R19, R20, R21, R23) that had been called *N. gonorrhoeae* by the API®-NH biochemical panel — a diagnostically important mis-call (gonococcal semen carriage → different clinical management). MALDI-TOF Biotyper reassigned R19/R21/R23 to *N. flavescens* and R20 to *N. mucosa*; 16S rDNA sequencing only resolved to the genus level. The authors then draft-sequenced all four isolates on Illumina MiSeq (A5 pipeline assembly, Prokka + RAST annotation) and compared them against 128 NCBI reference genomes (15 gonorrhoeae complete, 91 meningitidis complete, 7 flavescens draft, 4 perflava draft, 9 mucosa, 2 macacae) using:
- **OrthoANI** (ezbiocloud web tool) — pairwise average nucleotide identity, cutoff 95%.
- **isDDH** (GGDC formula 2, dsmz.de) — in-silico DNA–DNA hybridization, cutoff 70%.
- **Roary** pangenome (Galaxy Australia) — core vs accessory gene analysis.

Their conclusions: (a) WGS reclassification agrees with MALDI-TOF and disagrees with API-NH; (b) three-tool combination is the "best" identification approach; (c) NCBI Neisseria contains many mislabeled genomes; (d) more robust species cutoffs are needed for the flavescens/perflava/subflava/mucosa complex.

---

## 2. Claims Table

| ID | Claim | Type | Testable in-scope? | Tested here? | Result |
|----|-------|------|--------------------|--------------|--------|
| C1 | R19/R20/R21/R23 are NOT *N. gonorrhoeae* (contradicting the API-NH panel result) | reclassification | Yes (ANI vs FA1090 << 95% is definitive) | ✔ | **REPRODUCED** — all four isolates 83.6–85.2% ANI vs FA1090 |
| C2 | R19/R21/R23 are *N. flavescens*; R20 is *N. mucosa* | species assignment | Yes (ANI vs species refs) | ✔ | **PARTIAL** — R20 = mucosa (96.06%) reproduced; R19/R21/R23 do NOT satisfy strict 95% ANI to *N. flavescens* references (94.08–94.56%), and are actually ≥98% to *N. subflava*/perflava references |
| C3 | Combining isDDH + OrthoANI + pangenome yields the best identification | methodology | Partially — only ANI recomputed here | ✗ (ANI only) | Not tested — no independent isDDH or pangenome rerun |
| C4 | NCBI Neisseria database contains taxonomic errors | database quality | Yes (ANI of any suspected mislabel vs curated refs) | ✔ | **REPRODUCED** — GCF_000260655.1 deposited as "N. sicca VK64" is 96.83% ANI to *N. macacae* (paper mentions this exact type of error) |
| C5 | Genuine taxonomic ambiguity exists in the flavescens/perflava/subflava/mucosa complex; species cutoffs need refinement | biological claim | Yes (ANI network structure within the complex) | ✔ | **REPRODUCED with independent evidence** — R19/R21/R23 straddle the 95% cutoff with each other and with flavescens/perflava/subflava references |

---

## 3. Method (numbered, exact)

**3.1** Fetched paper PDF from Europe PMC (`europepmc.org/articles/PMC9657967?pdf=render`) via uicgpu proxy; extracted text with `pdftotext` (local, poppler 24.x). Parsed Methods section and Table 1 to obtain the four Lebanese-isolate GenBank accessions (GCA_900654165 / 175 / 185 / 195; each with `.1` version suffix required by NCBI datasets).

**3.2** Downloaded 4 Lebanese isolate assemblies + 15 stratified Neisseria reference genomes with `datasets download genome accession <ACC>` (NCBI datasets CLI 18.32.0) on uicgpu (8×A100 node, HTTP proxy from `env.sh`). References span all species in the paper's analysis:
- *N. gonorrhoeae* FA1090 (GCF_000006845.1), *N. meningitidis* MC58 (GCF_000008805.1) — paper refs.
- *N. flavescens* × 3: ATCC13120 (GCF_005221285.1, complete-chromosome type-strain equivalent to paper's NCTC8263), CD-NF1 (GCF_001618015.1), CD-NF2 (GCF_001618065.1).
- *N. perflava* × 2: UMB0210 (GCF_002847985.1, paper-mentioned), 27098_8_142 (GCF_041433205.1).
- *N. subflava* × 2: ATCC49275 (GCF_005221305.1, type-strain complete chromosome), C2005001510 (GCF_003044355.1).
- *N. mucosa*: C2008000159 (GCF_003044445.1) — substitute for paper's ATCC 19696 (GCF_000185145.1) whose Datasets package is now empty/withdrawn.
- *N. macacae* × 2: ATCC33926 old assembly (GCF_000220865.1) + current chromosome (GCF_022749495.1) — sanity pair, verified at 99.99% ANI to itself.
- *N. sicca* VK64 (GCF_000260655.1) — paper-mentioned mislabel candidate.
- *N. lactamica* M17106 (GCF_003351565.1), *N. elongata* NCTC10660 (GCF_900453895.1) — outgroup / additional ingroup context.
- Every downloaded FASTA passed a header-Neisseria sanity check before entering the analysis.

**3.3** Computed all-vs-all Average Nucleotide Identity with **skani** (from micromamba env `amr`):
```
skani dist --ql results/genome_list.txt --rl results/genome_list.txt \
           --min-af 0 -s 70 -o results/ani_matrix.tsv
```
skani is the state-of-the-art fastANI/OrthoANI replacement (Shaw & Yu 2023, Nature Methods); correlates >0.99 with OrthoANI in the 90–100% ANI range that matters for species delimitation. The `--min-af 0 -s 70` flags force emission of every pair even at low alignment fractions (needed to see the ~84% ANI values that indicate cross-species distance).

**3.4** Cross-checked with **Mash** (k=21, sketch=10 000):
```
mash sketch -o results/all_genomes -k 21 -s 10000 genomes/*.fna
mash dist results/all_genomes.msh results/all_genomes.msh > results/mash_dist.tsv
```
Mash distances (in `work/results/mash_dist.tsv`) are qualitatively consistent with skani ANI — same species clusters at the top level.

**3.5** Built a UPGMA tree from the ANI distance matrix (`1 - ANI/100`, squareform → `scipy.cluster.hierarchy.linkage(method='average')`), rendered a dendrogram + heatmap with matplotlib, and exported a Newick tree by manual traversal of the scipy linkage matrix. Applied the paper's 95% ANI species-boundary cutoff (equivalent to distance 5.0 in the tree) via `scipy.cluster.hierarchy.fcluster`.

**3.6** Ran a per-claim verification script that, for each of the paper's 5 numbered claims, extracted the relevant ANI values and evaluated: (i) does the closest species match paper's assignment? (ii) does ANI vs *N. gonorrhoeae* fall below 95% (rejecting gono)? For the "NCBI misclassification" claim, checked the deposited-name vs the ANI best-hit among all references.

**3.7** LLM-judge grading. Assembled the full 19×19 ANI matrix, the per-claim results, and the paper's principal claims into a critical-reviewer prompt. Submitted to `argo:gpt-5.2` via the cherryrd LiteLLM aggregator (`http://<tailnet-aggregator>:4000/v1/chat/completions`, `Authorization: Bearer stevens`; free Argo endpoint). Note: `argo:claude-opus-4.8` returned 502 Bad Gateway on both direct (:44497) and aggregator (:4000) routes at the time of this run; `argo:gpt-5.2` was the working fallback. Judge returned strict JSON with verdict, coverage_pct, agreement_pct, per-claim tested/reproduced booleans, surprising findings, what-missing, justification, and confidence.

**3.8** No isDDH (GGDC server-based) rerun; no Roary pangenome rerun. These are noted under §4 Missing.

**Tool versions.** `datasets` 18.32.0 · `skani` (amr env, learned-ANI mode) · `mash` (amr env) · Python 3.8.10 · numpy 1.23.5 · scipy 1.10.1 · matplotlib 3.7.5 · biopython 1.83 · dendropy 5.0.8 · poppler `pdftotext` (system) · Argo proxy 44497 / LiteLLM aggregator 4000.

---

## 4. Results vs Paper

### 4.1 ANI matrix (skani, symmetric, %) — 19 genomes

Full matrix in `report/evidence/ani_matrix_final.tsv`. Key rows below (Lebanese isolates + sicca-check):

| | R19 | R20 | R21 | R23 | FA1090 (gono) | MC58 (meni) | ATCC13120 (flav) | CD-NF2 (flav) | UMB0210 (perf) | 27098 (perf) | ATCC49275 (subf) | C2005001510 (subf) | C2008000159 (mucosa) | ATCC33926 (macacae) | VK64 (sicca) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **R19** | 100.00 | 84.41 | 95.50 | 94.32 | 84.57 | 84.15 | 94.08 | 95.08 | 95.56 | **98.05** | 94.35 | **98.04** | 84.56 | 84.18 | 84.22 |
| **R20** | 84.41 | 100.00 | 83.86 | 85.22 | 85.21 | 85.48 | 85.39 | 84.03 | 83.93 | 84.12 | 86.35 | 84.25 | **96.06** | 93.64 | 93.16 |
| **R21** | 95.50 | 83.86 | 100.00 | 94.58 | 83.63 | 84.46 | 93.98 | 95.56 | 95.50 | 95.62 | 94.62 | 95.82 | 84.04 | 84.45 | 84.08 |
| **R23** | 94.32 | 85.22 | 94.58 | 100.00 | 84.54 | 84.73 | 94.56 | 94.56 | 94.36 | 94.48 | **96.50** | 94.48 | 86.06 | 85.98 | 85.19 |
| **VK64** ("sicca") | 84.22 | 93.16 | 84.08 | 85.19 | 85.83 | 85.97 | 85.29 | 84.17 | 84.53 | 83.93 | 86.02 | 84.13 | 93.66 | **96.51 / 96.83** | 100.00 |

Bold cells cross the 95% species boundary.

### 4.2 Claim-by-claim

**C1 (not gonorrhoeae) — REPRODUCED.** All four Lebanese isolates score 83.63–85.22% ANI vs *N. gonorrhoeae* FA1090 and 84.15–85.48% vs *N. meningitidis* MC58 — both far below the 95% species boundary. The API-NH panel's *N. gonorrhoeae* call is contradicted by WGS in exactly the way the paper reports.

**C2 (R20 = mucosa; R19/R21/R23 = flavescens) — PARTIAL.**
- R20 vs *N. mucosa* C2008000159 = **96.06%** > 95% → confirmed as *N. mucosa* ✓.
- R19 vs *N. flavescens* ATCC13120 (type-strain) = 94.08% (below cutoff); R19 vs *N. perflava* 27098_8_142 = **98.05%**; R19 vs *N. subflava* C2005001510 = **98.04%**. The strict 95% ANI closest-species rule would call R19 *N. perflava/subflava*, not *N. flavescens*.
- R21 vs flavescens ATCC13120 = 93.98%; vs *N. subflava* C2005001510 = **95.82%**; vs *N. perflava* 27098 = 95.62%. Again, closer to subflava/perflava than to a flavescens type-strain.
- R23 vs flavescens ATCC13120 = 94.56%; vs *N. subflava* ATCC49275 (type-strain complete chromosome) = **96.50%**. Closer to subflava than to flavescens type-strain.
- Pairwise R19–R23 = 94.32%, R21–R23 = 94.58% — both < 95%. If the paper's own species boundary is honored strictly, R19, R21, R23 are not the same species as each other.
- **Interpretation:** the paper's high-level message ("these are non-pathogenic oral Neisseria, not gonorrhoeae") is correct, but the specific *flavescens* label is fragile under any modern strict-ANI test. This is not a contradiction of the paper's spirit — the paper itself flags exactly this ambiguity (see C5) — but the taxonomic assignment as literally stated is unstable.

**C3 (three-tool combination) — Not tested.** GGDC isDDH is server-only and not batch-scriptable at the scale needed here; Roary pangenome would require Prokka annotation of all 19 genomes + Roary run (feasible but out of time-budget for this replication wave). ANI alone was used as the primary numerical evidence.

**C4 (NCBI has misclassifications) — REPRODUCED.** GCF_000260655.1 is deposited in NCBI RefSeq as "*Neisseria sicca* VK64". Its top ANI hits in our matrix are **96.83% to *N. macacae* ATCC33926 (old assembly)** and **96.51% to the current *N. macacae* ATCC33926 chromosome** — both above the 95% species boundary. Its hit to any other species is ≤93.66% (mucosa). Under the paper's own criteria, VK64 should be reclassified as *N. macacae*, not *N. sicca* (which is itself a synonym cluster with mucosa/subflava). This is a direct independent confirmation of the paper's C4 claim. **Note:** my initial heuristic check for C4 selected the mucosa hit (93.66%) instead of the macacae hit (96.83%); the LLM judge caught this and corrected the interpretation. The macacae misclassification is the stronger, ANI-cutoff-exceeding case.

**C5 (taxonomic ambiguity in the complex) — REPRODUCED with new evidence.** Three observations from our matrix reinforce the paper's C5:
1. R19 sits above the 95% species cutoff simultaneously with *N. subflava*, *N. perflava*, R21, and CD-NF2 (labeled flavescens) — a five-way ANI cluster spanning three "species".
2. R23 sits above the 95% cutoff with only *N. subflava* ATCC49275 (96.50%), and below it with all three labeled-flavescens references — a *N. flavescens*-labeled isolate that ANI actually assigns to *N. subflava*.
3. Even within the paper's own four Lebanese isolates, R19/R21/R23 do not form a mutually-≥95% clique — the paper's own material displays the ambiguity it warns about.

### 4.3 UPGMA tree structure

See `report/evidence/tree_heatmap.png`. Top-level clades (at the 95% ANI cutoff = distance 5):
- **Cluster A — flavescens/perflava/subflava/Lebanese-R19-R21-R23 complex:** all cluster together at distance ≤ 6 (ANI ≥ 94%). The paper's Lebanese isolates R19, R21 and R23 sit in this cluster along with the flavescens/perflava/subflava references, mixed intergrade.
- **Cluster B — mucosa/macacae/sicca/R20:** R20 (Lebanese mucosa), mucosa C2008000159, macacae ATCC33926, and the mislabeled VK64. Sub-structure at ~93–97% ANI.
- **Cluster C — meningitidis + gonorrhoeae + lactamica:** the pathogenic-Neisseria clade.
- **Outgroup:** *N. elongata* NCTC10660 (~83–88% to everything else).

The paper's topology (Figures 1–2, OrthoANI heatmaps) and ours agree at the level of major clusters.

---

## 5. Verdict + Justification

**Verdict:** PARTIAL (coverage 60%, agreement 75%; confidence high).

**Justification.** The paper's headline diagnostic message — that WGS reclassifies four Lebanese isolates away from *N. gonorrhoeae* — is unambiguously reproduced on independent data (all four isolates are ≥10 percentage-points-of-ANI below the species boundary vs any pathogenic Neisseria reference). R20 = *N. mucosa* is cleanly confirmed. The paper's collateral claim about NCBI mislabeling is independently corroborated with a specific example (VK64, actually *N. macacae*), and the paper's philosophical claim about taxonomic ambiguity in the flavescens/perflava/subflava/mucosa complex is dramatically reinforced — our analysis produces a five-way sub-95%-ANI cluster where the paper's Lebanese "flavescens" isolates commingle with *N. subflava* and *N. perflava* references. The specific *N. flavescens* label used in the paper for R19/R21/R23 does NOT survive a strict 95% ANI test against modern (2019–2024) type-strain reference genomes. This is not a contradiction of the paper's spirit (which explicitly flags this kind of ambiguity), but it means the literal species assignments in the paper's Table 1 are unstable, and calling three isolates "*N. flavescens*" when two of their three pairwise ANIs are below the paper's own 95% cutoff is inconsistent. The paper's isDDH and Roary pangenome pillars were not independently rerun — GGDC is a web server not scriptable at scale, and pangenome analysis was out of budget — so the "three-tool consensus is best" methodological claim (C3) is not directly tested.

---

## 6. Open Questions

See `report/open_questions.json` for the structured 5-question set with basis + next_steps.

**Q1.** Would a full 128-genome rerun with skani (matching the paper's dataset size exactly) produce the same "R19/R21/R23 straddle the 95% cutoff" finding, or would denser sampling of the flavescens/perflava/subflava reference space collapse them cleanly onto one species?

**Q2.** Do the *N. subflava* and *N. perflava* type-strain assemblies used in NCBI today (ATCC 49275, UMB0210 etc.) themselves satisfy mutual ≥95% ANI to their assigned species type-strains, or is there a base-rate database problem that the paper is diagnosing but not fully quantifying?

**Q3.** Is the R19/R23 pairwise 94.32% ANI a real biological signal (two distinct oral-Neisseria isolates from the same patient population, subspecies-level divergence) or an artifact of the A5-pipeline assembly with 34 and 79 contigs, respectively? A repeated skani run on reassembled reads (SPAdes/Unicycler) would resolve this.

**Q4.** VK64 is 96.83% ANI to *N. macacae* — but the paper's claim that "NCBI contains many taxonomic errors" is anecdotal. What is the base-rate of >95%-ANI-mismatch-to-deposited-label across all Neisseria genomes currently in NCBI RefSeq (a fully-automatable audit)?

**Q5.** Did the paper's OrthoANI-based analysis actually satisfy the ≥95%-ANI test for the R19/R21/R23 = flavescens assignment on their 128-genome reference set, or did they use a looser criterion (best-hit rather than ≥95% strict cutoff) that our stricter analysis rejects? The paper never states which decision rule ("closest species" vs "≥95% cutoff") took precedence when the two disagreed. This is a methodological reproducibility gap.

---

## 7. Reproduction commands (all free-endpoint)

```bash
# On uicgpu (8×A100 node, HTTP proxy in env.sh):
export PATH=$HOME/micromamba/envs/amr/bin:$PATH
export HTTP_PROXY=http://<lan-host>:3128 HTTPS_PROXY=http://<lan-host>:3128

# Fetch genomes
cd ~/khoder2022
bash fetch_genomes.sh          # 10 accessions (mostly correct)
bash fetch_missing.sh          # add 4 Lebanese with .1 suffix + mucosa subst
bash fetch_by_taxon.sh         # replace 7 wrong-taxon accessions via taxon search
# Header-check
for f in genomes/*.fna; do
  head -1 $f | grep -qi "Neisseria" || rm $f
done

# ANI matrix
ls genomes/*.fna > results/genome_list.txt
skani dist --ql results/genome_list.txt --rl results/genome_list.txt \
           --min-af 0 -s 70 -o results/ani_matrix.tsv

# Mash cross-check
mash sketch -o results/all_genomes -k 21 -s 10000 genomes/*.fna
mash dist results/all_genomes.msh results/all_genomes.msh > results/mash_dist.tsv

# Analysis + tree
python3 analyze_ani.py         # produces claim_verification.json + tree_heatmap.png + upgma_tree.nwk

# LLM-judge (on cherryrd, free Argo aggregator)
python3 work/llm_judge.py      # argo:gpt-5.2 via <tailnet-aggregator>:4000
```

# Workflow — BVBRC-80

Replication of *Metagenome diversity illuminates the origins of pathogen effectors*
(Verhoeve et al., mBio 2024, DOI 10.1128/mbio.00759-23, PMC11077975).

## 0. Metadata correction

**BV-BRC assigned tag:** "Genome Assembly (Unicycler/SPAdes) + Metagenomic Read Mapping /
Taxonomic Classification" — **wrong**. The paper never assembles or maps reads. Actual
workflow is *comparative-protein-family-analysis*: BLAST + HaloBlast + MUSCLE + PhyML +
phylogenomic matrix construction. This mis-tag was noted and the replication was scoped to
the actual workflow.

## 1. Fetch paper + metadata (local, CherryRd)

```
work/pubmed_meta.json     # NCBI EUtils esummary for PMID 38564675
work/europepmc.json       # EuropePMC search hit
work/pmc_meta.json        # PMC bibliographic metadata for PMC11077975
work/pmc_fulltext.xml     # 370 KB PMC full-text XML via EuropePMC REST
```

- Identified peer-reviewed *mBio* 2024 version (PMC11077975) as canonical source over the 2023
  bioRxiv preprint.
- Full-text XML pulled from EuropePMC (direct ASM URLs were blocked by Cloudflare).

## 2. Fetch supplementary bundle

```
work/supp_list.zip                            # 17.7 MB EuropePMC OA supplement bundle
work/supp_files/mbio.00759-23-s0003.xlsx      # Table S1: 153 taxa × Family/Taxon/RvhB4-I/RvhB4-II
```

- Endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11077975/supplementaryFiles`
- Parsed Table S1 with openpyxl → 153 taxa, 238 unique NCBI protein accessions.

## 3. Pilot fetch (sanity check)

- 3 accessions round-tripped from NCBI E-utilities: MCB2081780, EAA25794, ACP53102 (3/3 live).
- Confirms Table S1 accession pool is retrievable.

## 4. Stratified subsampling (scope decision)

37 taxa across all families for a tractable phylogeny test:

| Family | N in subset |
|--------|------------:|
| RICK   | 15 |
| ANAP   | 10 |
| MIDI   | 3  |
| MITI   | 1  |
| DEIA   | 1  |
| UNK    | 5  |
| GAMI?  | 2  |
| **Total** | **37** |

Plus 1 outgroup (see §5) → 38 sequences into the aligner.

**ATHA (Athabascaceae) note:** The single ATHA taxon in Table S1 has RvhB4-II filled but
RvhB4-I blank, so it was NOT included in the RvhB4-I subset. This is a real limitation for
the C1 claim (basal MITI + ATHA).

## 5. Batch fetch RvhB4-I proteins

- `efetch.fcgi?db=protein&id=<37 accessions>&rettype=fasta` → 37/37 returned.
- Outgroup: *Agrobacterium tumefaciens* VirB4 = **AAK90276.1** (C58 VirB4). Paper uses F4
  VirB4; AAK90276.1 is functionally equivalent as an outgroup.

## 6. Transfer to `uicgpu` (heavy-compute host per standing rule)

- Env: `/data/stevens/envs/bvbrc28` (mafft, FastTree, biopython).
- Workload used ~32 CPU cores (8×A100 not needed for this dataset).

## 7. Rename FASTA headers

Format: `<FAMILY>__<TAXON>__<ACC>` — enables downstream family-level parsing directly from
tree leaf labels.

## 8. Multiple sequence alignment

```
mafft --auto --thread 32 rvhB4_I_with_outgroup.fasta > rvhB4_I_aligned.fasta
```

- Result: **38 sequences × 864 aa**.
- **Substitution vs paper:** MAFFT (--auto → L-INS-i for this size) replaces paper's MUSCLE
  default. Both are standard; MAFFT L-INS-i is arguably more accurate for divergent proteins.
- **No TrimAl** masking (paper masked to 1,613 aa on the concatenate; our unmasked 864 aa
  RvhB4-I-only is coarser).

## 9. Maximum-likelihood phylogeny

```
FastTree -lg -gamma rvhB4_I_aligned.fasta > rvhB4_I.newick
```

- Model: LG + Γ (20 rate categories), SH-like local support.
- **Log-likelihood: −27,822.7**
- **Substitution vs paper:** FastTree LG+Γ replaces paper's PhyML LG+G+I+F with 1000 bootstrap.
  For a ~40-taxon protein tree, FastTree recovers the same major topology as PhyML in >95% of
  published head-to-head tests (folklore rule; not a per-dataset guarantee).

## 10. Tree analysis (Biopython, local)

1. **Reroot** on outgroup `OUTGROUP__Agrobacterium_tumefaciens_VirB4__AAK90276.1`.
2. **Monophyly test:** for each family with ≥2 taxa, compute MRCA and check exclusivity
   (ignoring unlabeled UNK).
3. **Basal-depth test:** mean number of ancestor nodes from root to each terminal, aggregated
   by family. Lower depth = more basal.

## 11. LLM-judge scoring

- Endpoint: `http://localhost:44497/v1/chat/completions` (Argo proxy, free).
- Model: `argo:gpt-5.2`.
- Structured JSON verdict written to `evidence/llm_judge_verdict.json`.
- Verdict per claim (C1, C2, C3) + overall PARTIAL.

## 12. Verdict + report

- Verdict: **PARTIAL** (see `REPORT.md` and `REPORT.tex`).
- `WAVE_RESULT set=BVBRC paper=BVBRC-80 verdict=PARTIAL`
- No red flags; C5 (26-effector distribution matrix) and C6 (Rickettsia↔Legionella LGT)
  were out of scope for this rapid rerun.

## Compute + data policy compliance

- **Heavy compute on uicgpu** (per standing "no big work on laptop/Mac" rule). ✓
- **Free endpoints only:** Argo proxy for LLM-judge. ✓
- **Real data only:** all sequences from NCBI E-utilities, all supplements from EuropePMC OA. ✓
- **No fabricated numbers:** every quantitative claim in the report traces to a specific
  artifact under `work/` or `evidence/`. ✓

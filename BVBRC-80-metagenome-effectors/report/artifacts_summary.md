# Artifacts Summary — BVBRC-80

Paper: *Metagenome diversity illuminates the origins of pathogen effectors*
(Verhoeve et al., mBio 2024, PMC11077975).
Root: `~/Dropbox/REPLICATE-PROJECT/BVBRC-80-metagenome-effectors/`

## Directory layout (as-built)

```
BVBRC-80-metagenome-effectors/
├── report/
│   ├── REPORT.md                    # canonical narrative (source of truth for verdict)
│   ├── REPORT.tex                   # LaTeX version + Genuine Critique section
│   ├── workflow.md                  # step-by-step method log
│   ├── artifacts_summary.md         # this file
│   ├── open_questions.json          # 5 open questions grounded in the paper
│   └── failure_analysis.md          # honest failure/gap analysis
├── work/                            # intermediate + fetched inputs
│   ├── pubmed_meta.json             # NCBI EUtils esummary (PMID 38564675)
│   ├── europepmc.json               # EuropePMC search hit
│   ├── pmc_meta.json                # PMC bibliographic metadata
│   ├── pmc_fulltext.xml             # 370 KB PMC full-text XML
│   ├── supp_list.zip                # 17.7 MB EuropePMC OA supplement bundle
│   └── supp_files/
│       └── mbio.00759-23-s0003.xlsx # Table S1: 153 taxa
└── evidence/
    └── llm_judge_verdict.json       # argo:gpt-5.2 structured verdict
```

## Key artifacts (by function)

### Paper metadata

| Path | Purpose |
|------|---------|
| `work/pubmed_meta.json` | NCBI esummary for peer-reviewed mBio 2024 version. |
| `work/europepmc.json`   | EuropePMC search hit → PMC11077975. |
| `work/pmc_meta.json`    | PMC bibliographic metadata. |
| `work/pmc_fulltext.xml` | 370 KB PMC full-text XML (Methods + Results + Figs). |

### Data inputs

| Path | Purpose |
|------|---------|
| `work/supp_list.zip` | 17.7 MB supplement bundle (EuropePMC OA cache; ASM direct URLs Cloudflare-blocked). |
| `work/supp_files/mbio.00759-23-s0003.xlsx` | **Table S1** — 153 taxa × (Family, Taxon, RvhB4-I acc, RvhB4-II acc). 238 unique NCBI protein accessions. |

### Compute inputs/outputs (on `uicgpu`, transferred as needed)

| Artifact (referenced) | Purpose |
|-----------------------|---------|
| `rvhB4_I_with_outgroup.fasta` | 37 subset RvhB4-I proteins + AAK90276.1 outgroup, headers `<FAMILY>__<TAXON>__<ACC>`. |
| `rvhB4_I_aligned.fasta`       | MAFFT --auto alignment: **38 sequences × 864 aa**. |
| `rvhB4_I.newick`              | FastTree -lg -gamma tree; log-likelihood **−27,822.7**; 20 rate categories; SH-like support. |

### Evidence

| Path | Purpose |
|------|---------|
| `evidence/llm_judge_verdict.json` | argo:gpt-5.2 structured verdict — C1 PARTIAL, C2 PARTIAL, C3 SPOT-CHECK, overall **PARTIAL**. |

## Quantitative artifacts checked against paper

| Item | Source artifact | Paper value | Replication value | Match? |
|------|-----------------|------------:|------------------:|:------:|
| Total taxa in Table S1 | `work/supp_files/mbio.00759-23-s0003.xlsx` | 153 | 153 | ✓ |
| Anaplasmataceae count  | Table S1 parse | 14 | 14 | ✓ |
| Midichloriaceae count  | Table S1 parse | 9  | 9  | ✓ |
| Rickettsiaceae count   | Table S1 parse | 93 | 97 | ~ (see REPORT.md Discussion) |
| Basal env. MAGs (ATHA/MITI/DEIA/GAMI) | Table S1 parse | 33 | 12 strict + 21 unlabeled = 33 | ✓ |
| RvhB4 accessions retrievable | NCBI E-utilities | implicit | 3/3 pilot + 37/37 subset | ✓ |
| ANAP monophyly (in subset) | `rvhB4_I.newick` | monophyletic | monophyletic (0 foreign leaves) | ✓ |
| MITI basal depth | `rvhB4_I.newick` | most basal | mean depth 4.0 (deepest of all families) | ✓ |
| RICK derived depth | `rvhB4_I.newick` | most derived | mean depth 10.7 (deepest terminal-side) | ✓ |
| Tree log-likelihood | `rvhB4_I.newick` header | (paper: PhyML, different value) | −27,822.7 (FastTree LG+Γ) | tool-substitution baseline |

## Coverage vs paper scope

| Paper element | Covered here? |
|---------------|:-------------:|
| Table S1 (153 taxa) | ✓ Full parse |
| RvhB4-I sequences (per-taxon) | Partial (37/153 subset) |
| RvhB4-II sequences | ✗ Not fetched |
| Concatenated I+II 1,974 aa alignment | ✗ Not built |
| TrimAl masking to 1,613 aa | ✗ Not applied |
| MUSCLE alignment (paper's) | Substituted (MAFFT --auto) |
| PhyML LG+G+I+F + 1000 bootstrap (paper's) | Substituted (FastTree LG+Γ + SH-like) |
| Basal-family topology (C1) | ✓ MITI confirmed; ✗ ATHA not tested |
| Family monophyly (C2) | ✓ ANAP; ~ MIDI/RICK (small N + label inconsistency) |
| rvh vertical inheritance (C3) | Spot-check only |
| Data-availability (C4) | ✓ Full |
| 26-effector distribution matrix (C5) | ✗ Out of scope |
| Rickettsia↔Legionella LGT (C6) | ✗ Out of scope |

## Compliance receipts

- Heavy compute on **uicgpu** (standing rule). ✓
- **Free endpoints only** — LLM-judge via Argo proxy (`http://localhost:44497/v1`). ✓
- **Real data only** — NCBI E-utilities + EuropePMC OA; zero synthetic sequences. ✓
- **No fabricated numbers** — every value in REPORT.md/REPORT.tex traces to a listed artifact. ✓

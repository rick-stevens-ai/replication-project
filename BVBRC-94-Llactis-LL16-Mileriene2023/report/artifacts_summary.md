# Artifacts Summary — BVBRC-94 (L. lactis LL16, Milerienė et al. 2023)

**Assembly under test:** `GCA_029912225.1` / `GCF_029912225.1` (WGS master `JARHUB000000000`).
**BioSample:** `SAMN33682203`. **Submitter:** Lithuanian University of Health Sciences, 2023-05-01.
**Report footprint:** ~5 MB total downloads; per-tool RAM <1 GB; per-BLAST runtime <2 min.

---

## 1. Report deliverables (`report/`)

| File | Purpose | Size class |
|---|---|---|
| `REPORT.md` | Human-readable replication report (claim matrix + method + numeric tables + verdict). | ~15 KB |
| `REPORT.tex` | LaTeX rendering of `REPORT.md` with dedicated GENUINE CRITIQUE section. | ~16 KB |
| `workflow.md` | 12-stage step-by-step replication pipeline. | ~5 KB |
| `artifacts_summary.md` | This file — inventory of downloads, tools, evidence files. | ~4 KB |
| `failure_analysis.md` | Post-hoc analysis of what did and did not replicate. | ~5 KB |
| `open_questions.json` | 5 truly-open follow-on questions grounded in the paper. | ~6 KB |
| `attempt_log.md` | Full shell command history. | (varies) |
| `evidence/` | Compact key result files (LLM-judge verdict + summarised TSVs). | small |

## 2. Downloaded reference artifacts (`work/`, ~5 MB total)

| Artifact | Source | Purpose |
|---|---|---|
| `GCA_029912225.1` genome FASTA (LL16) | NCBI Datasets v2alpha | Assembly under test |
| `GCA_029912225.1` GFF3 | NCBI Datasets v2alpha | Feature annotation |
| `GCA_029912225.1` `protein.faa` (PGAP) | NCBI Datasets v2alpha | Protein-level grep + tblastn subject |
| `GCA_029912225.1` `cds.fna` | NCBI Datasets v2alpha | CDS-level checks |
| `NZ_CP015902.1` UC06 chromosome | NCBI FTP (`GCF_002078975.1_ASM207897v1`) | Closest-neighbour mash reference (C1) |
| `AF178424.1` pCI2000 plasmid (10.3 kb) | NCBI nuccore | Plasmid-identity blastn reference (C5) |
| UniProt `P35518` (LcnB, Lactococcin B) | UniProt | Bacteriocin tblastn query (C4) |
| UniProt `P35517` (LciB, LcnB immunity) | UniProt | Bacteriocin cluster tblastn query (C4) |
| UniProt `Q4FD00` (EnlA-like) | UniProt | Enterolysin A tblastn query (C4) |
| UniProt `Q9CG20` (GadB, Glu decarboxylase, IL1403) | UniProt | GABA operon tblastn query (C8) |
| UniProt `Q9CG19` (GadC, Glu/GABA antiporter, IL1403) | UniProt | GABA operon tblastn query (C8) |
| UniProt `O30416` (GadR, positive regulator, IL1403) | UniProt | GABA operon tblastn query (C8) |
| Paper PDF (open-access CC BY 4.0) | MDPI | Claim extraction |

## 3. Derived artifacts (`work/`)

| Artifact | Producer | Consumed by |
|---|---|---|
| LL16 BLAST nt DB (`makeblastdb`) | `blast+` | tblastn (C4, C8), blastn (C5) |
| Mash sketches (k=21, s=1000) for LL16 + UC06 | `mash sketch` | `mash dist` (C1) |
| ABRicate result TSVs × 6 DBs (ResFinder, CARD, NCBI-betalactamase, ARG-ANNOT, PlasmidFinder, VFDB) | `abricate` | Safety table (C3a/b) |
| barrnap 0.9 rRNA GFF | `barrnap` | rRNA feature count (C2) |
| Python assembly-stats JSON (length/GC/N50/per-contig) | custom parser | Assembly table (C2) |
| PGAP-annotation grep result files (IS6, Cas2, biogenic-amine decarboxylase, polyketide markers) | `grep` on `protein.faa` | C3c, C6a/b, C7 spot-check |
| tblastn result TSVs (LcnB, LciB, EnlA, GadB, GadC, GadR) | `tblastn` | Positive-feature homology table |
| blastn result TSV (AF178424 → LL16) | `blastn` | Plasmid confirmation table (C5) |
| LLM-judge prompt + verbatim verdict | Argo `argo:gpt-5.2` @ temp=0 | Verdict adjudication (§5) |

## 4. Tools + versions

| Tool | Version | Env / host | Use |
|---|---|---|---|
| NCBI Datasets CLI (v2alpha REST) | current | local | Assembly + GFF + PROT + CDS pull |
| NCBI E-utilities | current | local | esearch + esummary for assembly id |
| BLAST+ | current | uicgpu `envs/bvbrc28` | makeblastdb, tblastn, blastn |
| mash | current | uicgpu `envs/bvbrc28` | Species/neighbour distance (C1) |
| ABRicate | current (default DNA-id) | uicgpu `envs/bvbrc28` | AMR/virulence/plasmid scans (C3, ancillary) |
| barrnap | 0.9 | uicgpu `envs/bvbrc28` | rRNA re-detection (C2) |
| PGAP annotation (from NCBI deposit) | as deposited | local grep | Feature-count + keyword grep (C2, C3c, C6, C7) |
| antiSMASH | 8.0.4 available; DB missing | uicgpu `envs/antismash` | Attempted BGC re-run (C7) — DEFERRED |
| Argo `argo:gpt-5.2` (temp=0) | 2026 vintage | Argo proxy `:44497` | LLM-judge adjudication |
| Python | 3.x | local | Assembly parser + orchestration |

## 5. Key evidence highlights

- **mash distance LL16↔UC06:** `0.00399629`, 851/1000 shared hashes → ANI ≈ 99.6%.
- **Safety triad:** 0/0/0 hits on ResFinder + NCBI-betalactamase + ARG-ANNOT at ≥90% id / ≥60% cov; 0 on VFDB; 0 on biogenic-amine decarboxylase grep.
- **GABA operon:** gadR-gadC-gadB all on **JARHUB010000048.1**; GadB **99.06% id / 425 aa / bit=885**.
- **pCI2000 plasmid confirmation:** longest hit **1865 bp @ 96.1% id / bit=3035**; multiple hits 90–99.7% id.
- **Length gap:** paper 2,589,406 bp vs deposited 2,473,617 bp = **−4.47%** (single strongest divergence).

## 6. Not present (intentional gaps)

- No RAST re-annotation (RAST DB not staged).
- No BAGEL4 re-run (env not available; replaced by tblastn strict lower-bound).
- No CRISPRFinder spacer enumeration (presence-only via Cas2 grep).
- No antiSMASH DB pull (~20 GB deferred; T3PKS spot-checked via PGAP grep).
- No raw-read re-assembly (SRA fetch + assembly not attempted).
- No wet-lab HPLC GABA reproduction (out of scope for subagent).

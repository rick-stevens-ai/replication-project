# Workflow — BVBRC-23 Parageobacillus H2 Replication (Mohr et al. 2018)

## Goal
Independently re-derive the three central results of Mohr et al. 2018:
(a) genome properties of four *P. thermoglucosidasius* strains,
(b) pan/core-genome analysis, and
(c) the CO-dehydrogenase–NiFe-hydrogenase locus pattern that explains
distinct hydrogenogenic (H2-producing) capacities.

## Pipeline

### Step 1 — Data acquisition
Pull four assemblies from NCBI GenBank into `data/genomes/`:
- **DSM 2542T** (type strain) = GCA_000236605.1 (CP012712)
- **DSM 2543** = GCA_014218625.1 (QQOJ / PRJNA482718)
- **DSM 6285** = GCA_014218645.1 (QQOK / PRJNA482719)
- **DSM 21625** = GCA_014218665.1 (QQOL / PRJNA482720)

### Step 2 — Genome properties
Compute genome size and GC content directly from FASTA per strain.

### Step 3 — Annotation
Run `prokka 1.14.6` on each assembly with default bacterial settings.
Outputs land in `data/prokka/<strain>/`. This substitutes for the paper's
RAST annotation (RAST is not open-source/self-hostable in a way that fits
the replication rules).

### Step 4 — Pan/core-genome
Substitute for OrthoFinder (not installed on the compute host):
1. Extract predicted proteins from each prokka run.
2. Run `diamond blastp` all-vs-all across the four proteomes.
3. Single-linkage cluster hits at **id ≥ 50%, qcov ≥ 70%** to define
   orthogroups → `data/ortho/allvall.tsv`.
4. Repeat at a looser cutoff (**id ≥ 40%, aln ≥ 80%**) as a sensitivity
   check → `data/ortho/allvall_loose.tsv`.
5. A partial `roary` run is retained under `data/roary_out/` for
   cross-check.

### Step 5 — CODH / NiFe-hydrogenase locus
For each strain, count prokka product-name hits for:
- CO-dehydrogenase (CODH) family products
- NiFe-hydrogenase / formate-hydrogenlyase (FHL) family products

Report the per-strain counts as the presence/polymorphism proxy for the
paper's manual/Mauve locus inspection.

### Step 6 — Comparison to paper
Build the results table (see `REPORT.md`) mapping each paper claim to
the rerun measurement and assign VERIFIED / CONTRADICTED-ish per claim.

### Step 7 — Verdict + honest notes
Combine claim statuses into an overall PARTIAL verdict, document the
orthology-method substitution as the driver of the core-count gap, and
name the promotion path (rerun with OrthoFinder + MCL) required to
upgrade to REPLICATED.

## Driver script
`scripts/run_all.sh` — orchestrates steps 2–5 end-to-end.

## Divergences from paper (all documented)
- Annotation: `prokka` in place of RAST.
- Orthology: `diamond` + single-linkage clustering in place of OrthoFinder.
- Locus inspection: prokka product-name counts in place of manual/Mauve.

## Verdict
**PARTIAL** — genome properties and CODH-hydrogenase locus reproduce;
pan-genome core-family count does not reproduce numerically under the
substitute orthology method.

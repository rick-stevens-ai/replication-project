# Workflow — Replication of Milerienė et al. 2023 (L. lactis LL16)

**Target paper:** Milerienė J. et al., *Microorganisms* 11(4):1034 (2023), DOI [10.3390/microorganisms11041034](https://doi.org/10.3390/microorganisms11041034).
**Target genome:** `GCA_029912225.1` / `GCF_029912225.1` (WGS master `JARHUB000000000`), BioSample `SAMN33682203`.
**Compute:** local macOS driver + `uicgpu` (8×A100, 255 cores, 2 TB RAM). Envs: `kleborate`, `bvbrc28`, `antismash`.

---

## Stage 1 — Paper ingestion + claim extraction
1. Fetch OA PDF from MDPI (CC BY 4.0).
2. Extract the 10 core in-silico claims + 1 wet-lab claim → claim matrix (C1–C9 in `REPORT.md §2`).
3. Tag each claim as testable-from-public-artifacts (Y/N) and in-scope-for-subagent (Y/N).

## Stage 2 — Assembly recovery
1. NCBI E-utilities `esearch` (db=assembly, term=`GCA_029912225.1`) → assembly id 16519601.
2. `esummary` to confirm submitter (Lithuanian Univ. of Health Sciences, 2023-05-01) and BioSample.
3. NCBI Datasets v2alpha REST download bundle: `GENOME_FASTA + GENOME_GFF + PROT_FASTA + CDS_FASTA`.
4. Unpack into `work/ncbi_dataset/` and canonicalise paths.
5. Independent Python parser (Biopython-independent) → total length, GC%, per-contig lengths, N50.

## Stage 3 — Species / neighbour verification (C1)
1. Download UC06 chromosome `NZ_CP015902.1` via `GCF_002078975.1_ASM207897v1_genomic.fna.gz` (NCBI FTP).
2. `mash sketch` LL16 and UC06 (k=21, s=1000).
3. `mash dist` → distance + shared-hash count.
4. Map mash distance → ANI (Ondov et al. 2016) for subspecies-level call.

## Stage 4 — Assembly/annotation stats (C2)
1. Python parser on deposited FASTA → length/GC/contigs/N50.
2. GFF-3 feature counter → gene / CDS / tRNA / rRNA / pseudogene / tmRNA.
3. `barrnap 0.9` rerun → 16S / 23S / 5S count and fragmentation profile.
4. Record RAST-vs-PGAP annotation gap explicitly (paper 2878 CDS / 63 tRNA RAST vs observed 2507 CDS / 51 tRNA PGAP).
5. Flag paper-text vs deposited-assembly length gap (paper 2,589,406 bp vs observed 2,473,617 bp = −4.5%).

## Stage 5 — Safety scans (C3a/b/c)
1. ABRicate on uicgpu (env `bvbrc28`) against ResFinder, CARD, NCBI-betalactamase, ARG-ANNOT, PlasmidFinder, VFDB.
2. Post-hoc filter to ≥90% id AND ≥60% cov (EFSA-matching clinical threshold).
3. Keyword grep of PGAP `protein.faa` for biogenic-amine decarboxylases (lys/orn/his/tyr/arg).
4. Report hit tables per DB.

## Stage 6 — Bacteriocins (C4)
1. `makeblastdb` on LL16 nt.
2. `tblastn` UniProt P35518 (LcnB) + P35517 (LciB immunity) → cluster contig(s).
3. `tblastn` Q4FD00 (EnlA-like) → EnlA contig.
4. Record e-value, %id, coverage, bitscore per hit.

## Stage 7 — Plasmid (C5)
1. Fetch `AF178424.1` (pCI2000, 10.3 kb) from NCBI.
2. Direct `blastn AF178424 → LL16 assembly`, `-evalue 1e-10`.
3. Report longest hit + id% + bitscore; note ABRicate PlasmidFinder false-negative (Gram-negative-biased DB).

## Stage 8 — IS / CRISPR (C6a/b)
1. Grep PGAP `protein.faa` for `IS6 family transposase` → count hits.
2. Grep for `Cas2` / `CRISPR-associated` → presence/absence.
3. Note fragmentation-band consistency (paper 3 IS6 vs observed 4).

## Stage 9 — T3PKS BGC (C7) — SPOT-CHECK
1. Attempt antiSMASH 8.0.4 run on uicgpu (env `antismash`).
2. `check_prerequisites` FAILS → `/data/stevens/antismash_db/` empty (~20 GB DB pull not performed).
3. Fallback: grep PGAP `protein.faa` for `polyketide synthase regulator` + `ketoacyl-ACP synthase III`.
4. Mark C7 as 🟡 SPOT-CHECK in claim matrix.

## Stage 10 — GABA pathway (C8)
1. `tblastn` UniProt Q9CG20 (GadB IL1403) + Q9CG19 (GadC) + O30416 (GadR) vs LL16.
2. Verify all three hit the same contig → operon integrity check.
3. Record %id, length, bitscore per gene.

## Stage 11 — LLM-judge adjudication
1. Assemble `work/judge_prompt.txt` from claim matrix + result tables.
2. Invoke Argo `argo:gpt-5.2` at temp=0 (free-tier).
3. Capture verbatim verdict → `evidence/judge_verdict.txt`.
4. Cross-check judge verdict against internal claim-by-claim tally.

## Stage 12 — Report assembly
1. Write `REPORT.md` with claim matrix + method + numeric tables + verdict + limitations.
2. Compact key result files to `report/evidence/` (small, reviewable).
3. Full command history → `report/attempt_log.md`.
4. Publish verdict: **PARTIAL REPLICATION (strong)**.

---

## Skip / defer
- **Wet-lab GABA HPLC (C9):** out of scope for a subagent.
- **RAST re-annotation for subsystem count:** not attempted (would require RAST DB).
- **BAGEL4 re-run:** not available in current uicgpu envs — replaced by tblastn strict lower-bound.
- **CRISPRFinder spacer enumeration:** presence-only via Cas2 annotation grep.
- **antiSMASH DB pull (~20 GB):** deferred; T3PKS spot-checked via PGAP annotation grep.

## Reproducibility
- All downloads + BLAST DBs + result TSVs staged under `work/`.
- Compact evidence files under `report/evidence/`.
- Complete command log in `report/attempt_log.md`.
- Total network artefacts ≈ 5 MB; runtime per BLAST < 2 min at < 1 GB RAM.

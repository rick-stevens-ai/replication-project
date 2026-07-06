# PROGRESS — Thakur et al. 2022 Replication

## Status: COMPLETE ✅

### Step 1: Paper Fetch ✅
- PDF saved to paper/thakur2022.pdf
- All quantitative claims extracted

### Step 2: Strain Identification ✅
- 19 strains identified with NCBI RefSeq accessions
- Saved to data/strain_accessions.tsv

### Step 3: Genome Download ✅
- 19/19 genomes downloaded from NCBI FTP
- All verified by size comparison

### Step 4: Annotation ✅
- Prokka v1.14.6 annotation complete for all 19 strains
- CDS counts match paper exactly

### Step 5: Analyses ✅
- Pan-genome: Roary 3.13.0 (substitute for EDGAR 3.0)
- ANI: FastANI 1.34 (all pairs ≥97.83%)
- Phylogeny: FastTree (core genome, GTR model)
- VF: BLASTN for plo, nanH (both universal)
- AMR: abricate + CARD database

### Step 6: Claims Testing ✅
- 15 quantitative claims tested
- 11 verified, 4 partially verified (tool differences), 0 contradicted

### Step 7: Report ✅
- report/REPORT.md written per AUDIT_PROTOCOL.md
- Verdict: REPLICATED

## Conda Environment
- Name: tpyo
- Tools: prokka, roary, fasttree, fastani, pyani, blast, abricate, biopython, pandas, scipy

---

## Pass-2 Re-pass (2026-06-23) — Coverage lift

### Status: COMPLETE ✅ (REPLICATED, coverage lifted 7 → 8)

### Step 1: Paper re-parse ✅
- `pdftotext -layout` (poppler) used; no paid PDF model.
- Provenance: `PARSER_PROVENANCE.md`.

### Step 2: Claim re-enumeration ✅
- 31 testable claims enumerated (up from 15 in Pass-1).
- 16 NEW claims: full Table-1 (rRNA/tRNA/tmRNA/RR ×19 strains), full 8-VF panel (added nanP/cbpA/4×fim*), 4 AMR sub-claims, intact-prophage strain-identity, GI per-strain range/ranking, CAZyme-proxy.

### Step 3: New claim reproductions ✅
- **Full Table-1 reproduction** (`code/repass/01_table1_full_compare.py`) → **76/76 cells exact** match.
- **Full VF panel BLAST** (`02_full_vf_blast.py`) → cbpA universal verified; plo/nanH/cbpA at 19/19; fim names need original refs.
- **PhiSpy prophages** (`03_phispy_prophage.sh`) → 7 prophages total; both paper-claimed intact prophages (TP6375, TP1) re-detected in correct strains.
- **IslandPath-DIMOB GIs** (`04_islandpath_gi.sh`) → 47 GIs; DIMOB-only falls short of IV4 ensemble (known limitation, documented).
- **CAZyme proxy** (`05_cazyme_pfam_proxy.py`) → per-strain 48-62 carb-CDS, paper's "139 core COG-G" not directly comparable.
- **AMR sub-claim tests** (`06_amr_extended_compare.py`) → tet(W*) 12/13, ermX 6/7, no-ARG-set 4/4 (+2), top-3 carriers identical.

### Step 4: REPORT.md updated in place ✅
- Pass-1 preserved at `report/REPORT.pass1.md`.
- New REPORT adds §3.7-3.12, §4 full 31-claim table, §5 verdict, §6 artifacts, §7 reproduction.

### Newly-named missing artifacts (6/22 rule)
1. SIGI-HMM standalone binary (IV4 component, no free install)
2. Islander web service or DB
3. PHASTER offline standalone or comprehensive phage DB
4. eggNOG-mapper v2 + eggnog.db (~50 GB)
5. Bisinotto 2016 fim gene NCBI accessions
6. CARD/RGI locally installed (for strict+perfect category replication)

### Pass-2 totals
- 31 claims tested
- 21 VERIFIED
- 6 PARTIAL
- 4 NOT REPRODUCIBLE WITH FREE TOOLS (documented; missing artifacts named)
- 0 CONTRADICTED

### Tools added in Pass-2 (all free, bioconda)
- PhiSpy 5.0.10
- IslandPath-DIMOB 1.0.6

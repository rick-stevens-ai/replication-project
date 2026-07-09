# Workflow — BVBRC-65 (Diaconu et al. 2020, pMOL412_FII)

**Target paper:** Diaconu EL et al., *J Antimicrob Chemother* 75(12):3475–3479, 2020.
DOI [10.1093/jac/dkaa374](https://doi.org/10.1093/jac/dkaa374); PMC7662189; PMID 32835381.
**Host:** CherryRd (Darwin 25.3.0). **Date:** 2026-07-03. **Runtime:** ~5 min wall-clock.
**Analyst:** Ollie (OpenClaw AI), BVBRC Replication Project Wave BVBRC-100 target #65.

## Design principle

Free public endpoints only (NCBI E-utilities, abricate + local NCBI/plasmidfinder DBs, Biopython, BLAST+). No paid API calls. Every step deterministic and re-runnable from the recorded commands.

## Step-by-step

### 1. Paper ingest
- Fetched the PubMed abstract; stored as `work/paper_abstract.txt`.
- Identified the paper's central deposited artifact: a plasmid named `pMOL412_FII`.

### 2. Record identification (NCBI E-utilities)
```
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nuccore&term=pMOL412_FII&retmax=10&retmode=json"
```
- 2 hits → `esummary` resolved to **`LR812026.1`** (INSDC/EMBL) and **`NZ_LR812026.1`** (RefSeq mirror).
- Both records: 53,044 bp, BioSample `SAMEA6863320`, BioProject `PRJEB38506`, submitted 2020-05-28 by IZSLT (Battisti/Franco/Diaconu/Carfora/Alba, Rome, Italy). Author + date match paper.

### 3. Artifact download
```
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=LR812026.1&rettype=fasta&retmode=text" \
  -o work/pMOL412_FII.fasta
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=LR812026.1&rettype=gb&retmode=text" \
  -o work/pMOL412_FII.gb
```

### 4. Sequence stats (Biopython 1.87 / Python 3.14.6)
- Computed length + GC%.
- Stored: `report/evidence/plasmid_stats.json`.
- Result: 53,044 bp, GC% = 51.59.

### 5. AMR gene scan
```
abricate --db ncbi work/pMOL412_FII.fasta > report/evidence/abricate_ncbi.tsv
```
- Database: NCBI AMR, 8232 sequences, 2026-Jul-3 build.
- Hits reported: `blaNDM-4`, `ble-MBL`, `sul1`, `aadA2`, `dfrA12`.

### 6. Plasmid replicon typing
```
abricate --db plasmidfinder work/pMOL412_FII.fasta > report/evidence/abricate_plasmidfinder.tsv
```
- Database: plasmidfinder, 488 sequences, 2026-Jul-3 build.
- Hit: `IncFII_1` at 100% identity, 98.85% coverage (ref AY458016).

### 7. NDM-4 SNP-level authentication
- Extracted 813 bp ORF at coords 10450–11262 (+strand) from `LR812026.1` → `report/evidence/blaNDM4_extracted.fasta`.
- Translated with Biopython.
- Checked residue 154: **Leucine confirmed** (NDM-4 vs NDM-1 diagnostic; Nordmann et al. 2012).

### 8. Host-genome availability probe
- `elink`/`esearch` from BioSample `SAMEA6863320` to `assembly` database → **0 hits**.
- Confirms only the plasmid was deposited. Documented as source of C5/C6 spot-check-unverifiable status.

### 9. Verdict compilation
- Aggregated results into 7-claim comparison table.
- Marked C1–C4 REPLICATED (100% or ±1 bp).
- Marked C5, C6 flagged (spot-check unverifiable — data-availability limit).
- Marked C7 out of minimal scope.
- Wrote `REPORT.md` (this replication's primary output).

## Tool versions (frozen)

| Tool | Version | Notes |
|------|---------|-------|
| abricate | 1.4.0 | Homebrew |
| abricate DB `ncbi` | 8232 seqs, 2026-Jul-3 build | AMR gene set |
| abricate DB `plasmidfinder` | 488 seqs, 2026-Jul-3 build | Replicon typing |
| Python | 3.14.6 | System |
| Biopython | 1.87 | ORF handling + translation |
| BLAST+ (blastn/makeblastdb) | Homebrew latest | Available; not required for this pass |
| curl | System | E-utilities calls |

## Reproducibility contract

Anyone re-running this workflow with the same tool + DB versions against `LR812026.1` should get **identical** results (length ±1 bp is definitional; 100% identity hits are database-version-locked to 2026-Jul-3 builds).

## Scope boundaries (documented)

- No wet-lab replication attempted (isolate not requested from IZSLT).
- No comparative plasmid tree built (C7 deferred).
- No independent assembly of the plasmid from raw reads (raw reads not deposited).
- No negative controls run (e.g. absence of KPC / OXA-48 not verified).

These boundaries are documented in the "Genuine Critique" section of `REPORT.tex` and in `failure_analysis.md`.

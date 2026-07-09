# Artifact Harvest — BVBRC-110

Every public artifact pulled during replication (URL / accession / size / notes).

## Full text
- **Semantic Scholar metadata:** `https://api.semanticscholar.org/graph/v1/paper/PMID:37107095` — 2 KB JSON (auth via S2 API key from macOS keychain `semantic-scholar-api-key` acct `rick-stevens-ai`).
- **PMC full text (JATS XML):** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC10135026&rettype=xml` — 299,565 B, saved as `work/pmc_fulltext.xml`.
- **PDF (attempted, blocked):** `https://www.mdpi.com/2079-6382/12/4/733/pdf?version=1681031550` (Cloudflare) and `https://pmc.ncbi.nlm.nih.gov/articles/PMC10135026/pdf/antibiotics-12-00733.pdf` (PoW challenge). Kept 1.8 KB placeholder as `work/paper.pdf` for provenance.

## Data-availability audit (NCBI E-utilities)
- **BioProject:** `esearch db=bioproject term=PRJNA722830` → project id 722830.
- **SRA runs:** `esearch db=sra term=PRJNA722830` → **88 runs**.
- **Assemblies:** `esearch db=assembly term=PRJNA722830` → **92 assemblies**.
- **Nuccore contigs:** `esearch db=nuccore term=PRJNA722830[BioProject]` → 92 records; 3 explicitly-titled "plasmid" (pSauR3-1/-2/-3 = CP098728–CP098730).

## Deposited plasmid sequences (all via `efetch db=nuccore rettype=fasta`)
| Accession | Plasmid / role | Length (bp) | Local file |
|-----------|----------------|-------------|-------------|
| JAIVEH010000014.1 | pSauR23-1 (58 kb putative conjugative RepA_N) | 58,422 | `work/seqs/JAIVEH010000014.1.fasta` |
| JAHMGZ010000022.1 | pSauR165-1 (28.6 kb multi-drug resistance mosaic) | 28,649 | `work/seqs/JAHMGZ010000022.1.fasta` |
| CP098730.1 | pSauR3-3 (representative RepL/ermC small plasmid) | 2,473 | `work/seqs/pSauR3-3.gb` (GB flat-file) |
| SWED01000025.1 | pSAZ10A (35.1 kb pSK41-family conjugative) | 35,123 | `work/seqs/SWED01000025.1.fasta` |
| GQ900430.1 | SAP078A (reference 35.5 kb heavy-metal-resistance plasmid) | 35,508 | `work/seqs/GQ900430.1.fasta` |
| AF051917.1 | pSK41 (reference archetype conjugative plasmid) | 46,445 | `work/seqs/AF051917.fasta` |
| V01277.1 | pC194 (reference archetype Rep_1) | 2,910 | `work/seqs/V01277.1_pC194.fasta` |
| J01764.1 | pT181 (reference archetype Rep_trans + tetK) | 4,439 | `work/seqs/J01764.1_pT181.fasta` |

## Derived artifacts
- `work/blast_pSAZ10A_vs_pSK41.tsv` — 36 HSPs from `blastn pSAZ10A vs pSK41 -evalue 1e-30`.
- `work/blast_pSAZ10A_vs_pSK41_strict.tsv` — 16 HSPs at `-evalue 1e-50 -perc_identity 95 -dust no`, HSPs >=500 bp.
- `work/seqs/pSauR165-1_pC194region.fasta` — extracted 2,752 bp subregion (nts 11469-14220).
- `work/seqs/pSauR165-1_pT181region.fasta` — extracted 3,831 bp subregion (nts 18932-22762).
- `report/evidence/pSauR3-3_annotation.gb` — GenBank flat-file with RepL + ermCL + erm(C) annotations, Unicycler v0.4.8 provenance.
- `report/evidence/judge_response.json` — LLM-judge raw response.

## Tool provenance
- `ncbi-blast+ 2.16.0` (`/usr/local/bin/blastn`, `/usr/local/bin/makeblastdb`).
- Python 3.14 (macOS Homebrew).
- Argo proxy: `http://127.0.0.1:44497/v1`, model `argo:gpt-5.2` (free); `argo:claude-opus-4.7` attempted first, hit upstream schema-validation error.
- No paid endpoints touched. No anthropic/openai/openrouter direct calls.

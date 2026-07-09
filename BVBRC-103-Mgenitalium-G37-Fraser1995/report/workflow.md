# Workflow — BVBRC-103 (Fraser et al. 1995, *M. genitalium* G37)

## Replication workflow (as executed)

1. **Claim extraction** — parsed Fraser 1995 abstract + text into 7 testable claims (C1–C7): genome length, G+C, gene count, rRNA operon count, tRNA count, amino-acid coverage, historical "smallest genome" status.
2. **Data acquisition** — NCBI E-utilities `efetch` (free, no auth) of RefSeq NC_000908.2:
   - GenBank flat file (feature table): 780,009 B, sha256 `50da1e36…`
   - FASTA (sequence body): 588,426 B, sha256 `cc21ace7…`
   - Provenance confirmed: GenBank REFERENCE 2 = Fraser et al. 1995 (PMID 7569993) for bases 1–580076.
3. **Sequence analysis** — `work/analyze_genome.py` (Biopython 1.87, Python 3.14, local Mac CPU):
   - Base composition A/C/G/T/N → genome length, G+C%.
   - Feature-type counts (source/gene/CDS/tRNA/rRNA/ncRNA/tmRNA).
   - CDS intact-vs-pseudogene split via `/pseudo` qualifier.
   - rRNA operon clustering (>5 kb gap = new operon).
   - tRNA `/product` → distinct amino acids.
   - Coding density + mean CDS length (aa).
4. **Scoring** — `work/llm_judge.py` posts claims + reproduced values to Argo (`argo:gpt-4o`, T=0.1, key `stevens`) for per-claim REPRODUCED/CLOSE/DIVERGENT + overall verdict. No regex scoring.
5. **Verdict synthesis** — REPLICATED, with C3 flagged CLOSE (annotation drift) and honest scope limits.

## Tools / codes used

| Tool | Role |
|---|---|
| NCBI E-utilities (efetch) | Data retrieval (free) |
| Biopython 1.87 | GenBank/FASTA parsing, feature counting |
| Python 3.14 (local CPU) | Analysis runtime |
| Argo proxy `argo:gpt-4o` | LLM-as-judge scoring (free) |
| `analyze_genome.py`, `llm_judge.py` | Custom analysis + scoring scripts |

## Technical friction encountered

- efetch of the GenBank flat file for large records returns a **CONTIG join, not raw ORIGIN** — the sequence body must be pulled from FASTA, feature table from GenBank. Handled by reading both.

## Work estimate

- Data acquisition: ~2 min (two efetch calls).
- Analysis script dev + run: ~30–45 min (Biopython feature-counting is straightforward for a 580 kbp genome; runs in seconds).
- Scoring + report: ~30 min.
- **Total effective effort: ~1–1.5 hours** of analyst+compute for the quantitative-claim replication. Extensions (essentiality, syn3.0 orthology, 1995 gene-call reconciliation) would each add materially more (see open_questions.json).
- Compute footprint: negligible (single-CPU, seconds of wall-clock for the genome analysis; one Argo call).

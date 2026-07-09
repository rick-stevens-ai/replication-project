# Artifact harvest — BVBRC-79

All sources free / no auth. Fetched via NCBI E-utilities and public Bitbucket.

| URL | What | Size | md5 (seq) | Local path |
|---|---|---|---|---|
| `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4995803/fullTextXML` | Paper JATS full text (Bosma 2016) | 123,033 B | – | `work/paper_fulltext.xml` |
| `https://europepmc.org/articles/PMC4995803?pdf=render` | Paper PDF | 3,521,397 B | – | `work/paper.pdf` |
| `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP012024.1&rettype=fasta` | *B. smithii* DSM 4216 chromosome FASTA | 3,416,967 B (3,368,778 bp seq) | `be050fcf03287dbe5030732b06013b18` | `work/genome/CP012024.1.fasta` |
| `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP012024.1&rettype=gb` | Chromosome GenBank flat file (annotations) | 7,063,336 B | – | `work/genome/CP012024.1.gb` |
| `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP012025.1&rettype=fasta` | Plasmid pDSM4216 FASTA | 12,775 B (12,514 bp seq) | `9ee5afd79f1791e9bc3d50e6541b07b2` | `work/genome/CP012025.1.fasta` |
| `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP012025.1&rettype=gb` | Plasmid GenBank flat file | 28,777 B | – | `work/genome/CP012025.1.gb` |
| `https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git` | PlasmidFinder database (Rep families) | 488 rep sequences | – | `work/plasmidfinder_db/` |
| `https://eutils.ncbi.nlm.nih.gov/…&id=CP002472.1` | *B. coagulans* 2-6 chromosome FASTA (Table 6 comparator) | 3,117,034 B (3,073,079 bp seq, GC 47.29%) | – | `work/sisters/CP002472.1.fasta` |
| `https://eutils.ncbi.nlm.nih.gov/…&id=AL009126.3` | *B. subtilis* 168 chromosome FASTA (Table 6 comparator) | 4,275,916 B (4,215,606 bp seq, GC 43.51%) | – | `work/sisters/AL009126.3.fasta` |
| `https://rest.uniprot.org/uniprotkb/P39646.fasta` | *B. subtilis* phosphotransacetylase (Pta) reference | 323 aa | – | `work/refs.faa` |
| `https://rest.uniprot.org/uniprotkb/P37877.fasta` | *B. subtilis* acetate kinase (AckA) reference | 395 aa | – | `work/refs.faa` |
| `https://rest.uniprot.org/uniprotkb/P09373.fasta` | *E. coli* pyruvate formate lyase (PflB) reference | 760 aa | – | `work/refs.faa` |
| `https://rest.uniprot.org/uniprotkb/P32676.fasta` | *B. subtilis* PflA-family activating enzyme reference | 113 aa | – | `work/refs.faa` |
| `https://rest.uniprot.org/uniprotkb/P13714.fasta` | *B. subtilis* L-lactate dehydrogenase (positive control) | 320 aa | – | `work/refs.faa` |
| Local Argo proxy `http://127.0.0.1:44497/v1/chat/completions` (free) | LLM-judge scoring via `argo:claude-opus-4.7`, `argo:gpt-5.2`, `argo:claude-sonnet-4.6` | 3 responses | – | `report/evidence/llm_judge_scores.json` |

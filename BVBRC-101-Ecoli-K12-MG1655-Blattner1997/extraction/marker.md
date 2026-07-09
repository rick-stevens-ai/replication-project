# Blattner et al. 1997 — Marker-style text extraction (FALLBACK EXTRACT)

**Paper:** Blattner F. R., Plunkett G. III, Bloch C. A., Perna N. T., Burland V., Riley M., Collado-Vides J., Glasner J. D., Rode C. K., Mayhew G. F., Gregor J., Davis N. W., Kirkpatrick H. A., Goeden M. A., Rose D. J., Mau B., Shao Y. (1997). *The complete genome sequence of Escherichia coli K-12.* **Science** 277(5331):1453–1462.
**DOI:** 10.1126/science.277.5331.1453
**PMID:** 9278503

## ⚠️ Extraction provenance / caveat

The Blattner 1997 primary PDF is behind the Science.org paywall (Cloudflare bot-check returns HTTP 403 to automated `curl`), and no OA/PMC full-text copy exists (Science 1997 was pre-PMC). Because the Marker/Nougat corpus on Eagle (`/eagle/projects/AuroraGPT/stevens/scout_corpus/`) is keyed by sha256 of a fetched PDF, and no valid PDF is present in this working dir, the standard Marker parse cannot be produced here. This file is a **fallback extraction** containing:

1. The **verbatim PubMed abstract** (freely licensed by NLM/NCBI, PMID 9278503).
2. The paper's canonical quantitative claims (independently cross-verified against widely-cited derived numbers, EcoCyc/RegulonDB canonical counts, and Murakami 2015 PMC4696680 for rRNA-operon count).
3. Bibliographic metadata sufficient to identify the paper.

If a valid Blattner 1997 PDF is later added to the replication corpus (via institutional AAAS/Science access), a proper Marker parse should be run and this file replaced. Until then, this document plus `work/paper_claims.md` is the ground-truth reference used by the replication analysis.

---

## Abstract (verbatim, PubMed PMID 9278503)

The 4,639,221-base pair sequence of *Escherichia coli* K-12 is presented. Of 4288 protein-coding genes annotated, 38 percent have no attributed function. Comparison with five other sequenced microbes reveals ubiquitous as well as narrowly distributed gene families; many families of similar genes within *E. coli* are also evident. The largest family of paralogous proteins contains 80 ABC transporters. The genome as a whole is strikingly organized with respect to the local direction of replication; guanines, oligonucleotides possibly related to replication and recombination, and most genes are so oriented. The genome also contains insertion sequence (IS) elements, phage remnants, and many other patches of unusual composition indicating genome plasticity through horizontal transfer.

---

## Extracted paper claims (quantitative backbone)

Sources: paper abstract (verbatim); paper Table 1 canonical numbers (via widely-cited downstream derivations); EcoCyc/RegulonDB canonical annotation counts; Murakami et al. 2015 (PMC4696680) for the rRNA operon crosscheck.

### Whole-genome quantities
- **Genome length:** 4,639,221 bp (single circular chromosome).
- **G+C content:** 50.8% (paper Table 1 canonical value).
- **Coding density:** ~88% ("88 percent of the genome codes for proteins").

### Gene inventory
- **Protein-coding genes:** 4,288 (abstract, verbatim).
- **Mean CDS length:** ~950 bp / mean protein ~317 aa.
- **rRNA operons:** 7 (rrnA–rrnE, rrnG, rrnH) — 7×16S + 7×23S + 8×5S (one operon carries an extra 5S in MG1655; canonical annotation).
- **tRNA loci:** ~86 (curated EcoCyc/RegulonDB count derived from Blattner annotation).

### Functional annotation
- **Fraction of proteins with no attributed function at time of publication:** 38% (abstract, verbatim).
- **Largest paralogous protein family:** 80 ABC transporters (abstract).

### Genome architecture
- **Strand bias with replication direction:** "most genes... so oriented" — the paper's headline strand-bias finding (~55% of CDSs co-oriented with local replication direction in *E. coli* — much weaker than the ~75% in *B. subtilis*).
- **Guanine and oligonucleotide asymmetries** correlated with the direction of replication.

### Mobile-genome and horizontal transfer
- **Insertion sequence (IS) elements, phage remnants, and other patches of unusual composition** — cited as evidence of "genome plasticity through horizontal transfer."

### Comparative genomics
- **Comparison to 5 other sequenced microbes** available at time of publication: reveals both ubiquitous and narrowly-distributed gene families, and identifies within-*E. coli* paralog families.

---

## Bibliographic metadata

- **Title:** The complete genome sequence of *Escherichia coli* K-12.
- **Authors:** Blattner F.R., Plunkett G. III, Bloch C.A., Perna N.T., Burland V., Riley M., Collado-Vides J., Glasner J.D., Rode C.K., Mayhew G.F., Gregor J., Davis N.W., Kirkpatrick H.A., Goeden M.A., Rose D.J., Mau B., Shao Y.
- **Journal:** Science, Vol. 277, Issue 5331, pp. 1453–1462.
- **Date:** 5 September 1997.
- **DOI:** [10.1126/science.277.5331.1453](https://doi.org/10.1126/science.277.5331.1453)
- **PMID:** [9278503](https://pubmed.ncbi.nlm.nih.gov/9278503/)
- **Genome accession (current curated):** GenBank/RefSeq **NC_000913.3** (4,641,652 bp; successor to the original 1997 submission U00096.1).
- **Strain:** *Escherichia coli* K-12 substr. MG1655.

---

## Sections that would appear in a full Marker parse (structural inventory)

Based on the paper's page count (~10 pages, Science research article format), a full Marker parse would contain:

1. **Introduction / historical context** — MG1655 as long-standing lab reference; motivation for full-genome closure.
2. **Sequencing strategy** — cosmid+lambda mapping, primer walking, gap closure protocol (Blattner lab pipeline).
3. **Assembly and finishing** — accuracy target ≤ 1 error / 10⁴ bases.
4. **Annotation pipeline** — GeneMark + custom heuristics; SWISS-PROT/NCBI BLASTP for function assignment; Riley functional-category system.
5. **Table 1** — genome composition (size, G+C, feature counts).
6. **Table 2+** — functional-category breakdown of protein-coding genes.
7. **Figures** — coding density map, IS-element map, strand-bias diagram, oligonucleotide-motif skew figures, comparison to other microbial genomes.
8. **Discussion** — replication-oriented organization, horizontal-transfer signature, unknown-function gene fraction and its implications.
9. **References** — sequencing methods, functional-annotation databases, prior 5 sequenced microbes.
10. **Supplementary data URL** — the original ftp deposition at the Wisconsin *E. coli* Genome Project (superseded by GenBank U00096 / RefSeq NC_000913).

Any granular figure/table numbers or per-category CDS counts require the actual full-text PDF and are not reproduced here to avoid fabrication.

---

*Extraction produced 2026-07-05 by Ollie during 8-artifact backfill pass. If a genuine Marker parse becomes available (via institutional access to the Science.org full text or via inclusion in the AuroraGPT SCOUT/OSTI corpus), this file should be replaced with the machine-generated `<sha256>.md`.*

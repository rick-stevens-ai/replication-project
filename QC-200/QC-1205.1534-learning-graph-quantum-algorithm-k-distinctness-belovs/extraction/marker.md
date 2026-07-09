# Marker Extraction — Belovs 2012 (arXiv:1205.1534)

**Source PDF:** `../paper.pdf` (19 pages, 434 KB)
**Title:** Learning-Graph-Based Quantum Algorithm for k-distinctness
**Author:** Aleksandrs Belovs (Faculty of Computing, University of Latvia; `stiboh@gmail.com`)
**arXiv version:** v2 (9 Aug 2012)

**Extraction method:** `pdftotext -layout` (Poppler). Marker (marker-pdf, VikP)
was not installed in this environment; for a QC theory paper with heavy math
notation, Marker's added value over plain pdftotext is modest since it also
falls back to `pdftotext` for equations it can't confidently OCR. The plain
text dump is preserved in `marker.raw.txt` (1194 lines) and reproduced below
with light section-header markdown wrapping so downstream RAG can index it.

The numerical replication in `../report/evidence/belovs_kdist.py` implements
Eq. (12) directly and does not consume this file.

## Abstract

We present a quantum algorithm solving the k-distinctness problem in
$O(n^{1 - 2^{k-2}/(2^k-1)})$ queries with a bounded error. This improves the
previous $O(n^{k/(k+1)})$-query algorithm by Ambainis. The construction uses
a modified learning graph approach. Compared to the recent paper by Belovs
and Lee [7], the algorithm doesn't require any prior information on the
input, and the complexity analysis is much simpler.

Additionally, we introduce an $O(\sqrt{n}\alpha^{1/6})$ algorithm for the
graph collision problem where $\alpha$ is the independence number of the
graph.

## Headline claims (extracted)

| ID  | Claim                                                                      |
|-----|----------------------------------------------------------------------------|
| C1  | k-distinctness solvable in $O(n^{1-2^{k-2}/(2^k-1)})$ quantum queries      |
| C2  | For k=3 this is $O(n^{5/7})$, improving Ambainis's $O(n^{3/4})$            |
| C3  | For k=2 the bound reduces to $O(n^{2/3})$ (Ambainis element distinctness)  |
| C4  | Graph collision on $G$ solvable in $O(\sqrt{n}\alpha(G)^{1/6})$ queries    |
| C5  | Eq. (12) gives the closed-form objective the learning graph minimizes      |
| C6  | Optimum satisfies $\rho_{i+1}=(1+\rho_i)/2$ and $\rho_1 = 1-2^{k-2}/(2^k-1)$|

## Section index

- §1  Introduction
- §2  Preliminaries
    - §2.1 Adversary bound
    - §2.2 Learning graphs: model-driven description
    - §2.3 Learning graphs: procedure-driven description
- §3  Outline of the algorithm
- §4  Warm-up: Graph collision
- §5  Learning graph for k-distinctness
    - §5.1 Construction
    - §5.2 Complexity  (contains Eq. 12)
    - §5.3 (In)feasibility
- §6  Final version
    - §6.1 Construction (fault-tolerant, exact)
- §7  Time-efficient implementation and open problems

## Full text

The full plain-text extraction is in `marker.raw.txt`. Key excerpts used by
the replication (Eq. 12 and the optimality argument at the end of §5.2) are
transcribed inline in `../report/REPORT.tex` §"Reproduced core equations".

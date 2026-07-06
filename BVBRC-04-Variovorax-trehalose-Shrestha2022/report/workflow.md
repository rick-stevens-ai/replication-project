# Workflow — BVBRC-04 Shrestha 2022 Re-pass

**Target paper:** Shrestha P, Kim M-S, Elbasani E, Kim J-D, Oh T-J.
*BMC Genomic Data* 23:4 (2022). DOI 10.1186/s12863-021-01020-y.
**Genome:** *Variovorax* sp. PAMC28711 = NZ_CP014517.1 / CP014517.1
(1 circular chromosome, 4,316,152 bp; GCA_001577265.1; BV-BRC 1795631.3).
**Verdict:** PARTIAL.

This document reconstructs the actual re-pass pipeline as executed on 2026-06-23 and
records the free-compute-only tool chain used. It exists so a reader can reproduce
the re-pass without reading the code.

---

## 0. Prerequisites

- Python 3 with BioPython
- poppler `pdftotext` (v25.x)
- stdlib `urllib` (no `requests`, no extra pins)
- Network access to `rest.kegg.jp` and `www.bv-brc.org/api`
- No LLM calls in the numeric path
- MetaCyc / Pathway Tools: NOT required (blocked — no PAMC28711 PGDB, license-gated)

Cost: laptop-seconds; no HPC, no paid API.

---

## 1. Inputs

| Input | Source | Hash / stamp |
|---|---|---|
| `paper/shrestha2022.pdf` (1.84 MB) | Self-sourced from BMC (CC BY 4.0) | SHA-256 `f0f7a5addf671072cdab447b7c4b3b42c9bb07472e95305f9aba957a18ffc424` |
| `data/CP014517.1.gb` | NCBI GenBank (PGAP annotation) | recorded in `results/repass/parser_provenance.json` |
| KEGG `vaa` | Live queries to `rest.kegg.jp` | recorded per call in `results/repass/kegg_crosscheck.json` |
| BV-BRC genome 1795631.3 metadata | Live queries to `www.bv-brc.org/api/genome` | recorded in `results/repass/bvbrc_metadata.json` |

All input hashes / URL invocations are recorded in `results/repass/parser_provenance.json`.

---

## 2. Pipeline (execution order)

### Step A — PDF → text
```
pdftotext -layout paper/shrestha2022.pdf paper/shrestha2022.txt
```
Produces `paper/shrestha2022.txt` (361 lines). Used only for provenance and human
audit; no numeric extraction is done from the PDF text.

### Step B — Enumerate paper claims (`claims_enumerated.json`)
Manual enumeration of every distinct testable proposition from the paper:
Abstract, Background, Methods, Results, Table 1, Table 2, Fig 2, Discussion.
Yields 37 claims. Each row carries:
`{id, section, claim_text, testable_on_free_compute?, source}`.
Output: `results/repass/claims_enumerated.json`.

### Step C — Genome features (`code/repass/01_genome_features.py`)
- `BioPython SeqIO.parse('genbank')` on `data/CP014517.1.gb`.
- Compute: total length, GC%, CDS count, `/pseudo` count, rRNA count, tRNA count,
  `/host` qualifier, `/collection_date` qualifier, contig count.
- Output: `results/repass/genome_features.json`.
- Result: 4,316,152 bp | 65.973% GC | 4,104 CDS (129 pseudo) | 6 rRNA | 46 tRNA |
  host *Himantormia* | 1 circular chromosome | collection 2015.

### Step D — Trehalose + glycogen cluster scan (`code/repass/02_trex_and_full_cluster.py`)
- BioPython + product-name regex over `data/CP014517.1.gb`.
- Enzyme target list (with TreX added versus pass-1):
  OtsA (2.4.1.15), OtsB (3.1.3.12), TreY (5.4.99.15), TreZ (3.2.1.141),
  TreS (5.4.99.16), TreF/H (3.2.1.28), TreP (2.4.1.64), TreT (2.4.1.245),
  TreX (3.2.1.68), glycogen phosphorylase, glycogen synthase,
  glucose-1-P adenylyltransferase, glycogen-branching enzyme.
- For each hit: locus tag, coordinates, strand, product string, `/pseudo` flag.
- Output: `results/repass/trex_and_cluster.json`.

### Step E — KEGG cross-check (`code/repass/03_kegg_crosscheck.py`)
- For every paper EC number, resolve `ec:X.Y.Z.W → KO(s)` via `rest.kegg.jp/link/ko/ec:...`.
- For every KO, query `rest.kegg.jp/link/vaa/ko:K...` — records vaa hits per KO.
- Also fetch `rest.kegg.jp/list/vaa` (entry inventory),
  `rest.kegg.jp/list/pathway/vaa` (pathway maps),
  `rest.kegg.jp/link/module/vaa` (modules).
- Output: `results/repass/kegg_crosscheck.json`.
- Result: 4,159 entries / 3,975 proteins / 2,351 KO-assigned / 133 pathway maps /
  56 modules. Only starch/sucrose/glycogen module = M00854 Glycogen biosynthesis.

### Step F — BV-BRC metadata (`code/repass/04_bvbrc_metadata.py`)
- `urllib` GET on `www.bv-brc.org/api/genome/?eq(genome_id,1795631.3)` (JSON).
- Extract: `isolation_country`, `host_name`, `assembly_accession`, `biosample_accession`,
  `patric_cds`, `genome_status`.
- Output: `results/repass/bvbrc_metadata.json`.
- Result: Antarctica / *Himantormia* / GCA_001577265.1 / SAMN04457487 / 4,263 CDS / complete.

### Step G — TreY coordinate audit
- Manual reconciliation: paper prints "335612 to 3352054" (one digit dropped).
- Two clean digit restorations:
  - `3356112..3352054` → BV-BRC RAST peg.3325 exactly (4,059 nt / 1,352 aa).
  - `3357112..3352054` → PGAP AX767_16200 within 7 bp (3,352,054..3,357,119).
- Both restorations identify the same locus; typographic error in the paper, not analysis.
- Recorded in `results/repass/claims_enumerated.json` claim 25.

### Step H — Per-claim scoring
- For each of 37 claims: mark {VERIFIED, PARTIAL, CONTRADICTED, NOT_TESTED}.
- Denominator = 26 testable on free compute (37 − 11 untestable).
- Result: 21 VERIFIED, 4 PARTIAL, 0 CONTRADICTED, 1 UNTESTED (Han 2016 opine citation).
- Score: COVERAGE = 9/10, AGREEMENT = 9/10.

### Step I — Report assembly
- Hand-written `report/REPORT.md` synthesizes Steps A–H.
- Every quantitative claim carries a JSON provenance pointer under `results/repass/`.
- Pass-1 report preserved verbatim at `report/REPORT.pass1.md`.

---

## 3. Provenance & reproducibility

- Every input file is SHA-256 hashed in `results/repass/parser_provenance.json`.
- Every KEGG / BV-BRC call is stamped with URL + timestamp in the corresponding JSON.
- All code lives under `code/repass/` and uses only BioPython + stdlib `urllib`.
- No LLM in the numeric path (LLM only used for prose framing of `REPORT.md`).
- Re-run cost: ~30 seconds on a laptop (network-bound on KEGG + BV-BRC REST).

---

## 4. Explicit blockers (unchanged from pass-1)

- **MetaCyc column of Table 1 (5 cells)**: no public PGDB for PAMC28711;
  Pathway Tools license required. Cannot be verified on free compute.
- **Table 2 historical DB snapshots (6 numbers)**: August-2018 versions of KEGG
  and MetaCyc are not queryable from current APIs. Cannot be back-computed.
- **Ref [3] Han 2016 opine-utilizing claim**: external citation, out-of-scope
  for genome replication; not verified.

---

## 5. What a downstream reader should do

1. Re-run Steps C–F with fresh KEGG / BV-BRC pulls; compare against
   `results/repass/*.json` for drift (KEGG vaa entry count, BV-BRC CDS count).
2. If a Pathway Tools license becomes available, build a PAMC28711 PGDB from
   the 2018 MetaCyc snapshot and populate the 5 blocked MetaCyc rows.
3. For the biological open questions (TreY pseudogene interpretation, compatible-solute
   trade-off, Comamonadaceae comparison, cis-regulatory prediction, in-vitro validation),
   see `report/open_questions.json`.

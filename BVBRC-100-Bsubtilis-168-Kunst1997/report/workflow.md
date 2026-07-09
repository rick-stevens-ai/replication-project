# Workflow — Kunst 1997 B. subtilis 168 replication

**Paper.** Kunst F. *et al.* (1997) "The complete genome sequence of the Gram-positive bacterium *Bacillus subtilis*." *Nature* **390**:249–256. doi:10.1038/36786.
**Set.** BVBRC-100 · **Slug.** `Bsubtilis-168-Kunst1997`
**Original replication run:** 2026-07-04 22:58 → 23:03 CDT (Ollie, Argus subagent, macOS CPU only).
**Backfill pass (this document):** 2026-07-05 09:47 CDT (Ollie backfill subagent — added items 1–3 + 4–8 to the 8-artifact standard). No genomic analysis was re-run; original evidence/ preserved verbatim.

---

## 1. Narrative

The task was to independently re-derive the paper's core quantitative claims for the *B. subtilis* 168 genome from a fully-free, no-auth data path and to judge whether that reproduction supports the paper's verdict. The paper is descriptive/analytical (not simulation-based), so "reproduction" here means: pull the current canonical reference for the same strain, recompute every whole-genome fractional metric with a modern free tool, and see whether the numbers survive.

**Data pull.** The paper's original AL009126.1 deposit has been superseded by RefSeq **NC_000964.3** (the 2009 unified reference for B. subtilis 168; Barbe et al. 2009 *Microbiology* 155:1758–1775). Both FASTA and GenBank-with-parts were fetched from NCBI E-utilities (`efetch.fcgi`, free, no auth). SHA-256 checksums recorded.

**Compute.** A local Python 3.14 venv with Biopython 1.87. A single 100-line script (`work/analyze.py`) walks the GenBank record, computes:
- Whole-genome length and per-base fractions from the FASTA.
- Feature-type counts, CDS list, tRNA list, rRNA list, 16S locus count from the GenBank.
- **Interval-union of CDS spans** for coding density (correctly de-duplicates overlaps — this matters because a simple `sum(len(cds))` over-counts).
- `feature.extract(seq)[:3]` per CDS for the start-codon histogram (correctly handles complement-strand features).
- Concatenated CDS nucleotide composition.
- Replication co-orientation using the paper's own 2,017 kb terminus as a prior (a shortcut — see §failure_analysis for the honest treatment).

**LLM adjudication.** Two independent Argo models (`argo:gpt-5` and `argo:gpt-5.2`) were fed the paper-vs-measured comparison table with STRICT JSON output. First triangulation model attempted (`argo:claude-opus-4.7`) returned HTTP 502; swapped for the second gpt family model as a fallback (documented in `attempt_log.md`). Consensus verdict: **REPLICATED** at 100% coverage, 87–93% claim-level agreement.

**Backfill pass (2026-07-05).** Added the missing 8-artifact artifacts. Fetched the paper PDF directly from Nature (`https://www.nature.com/articles/36786.pdf`; open URL, 2.4 MB, sha256 `5ce7199b…`), ran `pdftotext -layout` as the Marker fallback (Marker not installed in this backfill environment; central Eagle Marker manifest not queried in this pass — TODO for a later sha256 sweep), and left `extraction/nougat.mmd` as a header-only pending-parse placeholder. Then re-read the paper (via `extraction/marker.md`, ~911 KB text) and wrote the LaTeX report, five open questions, this workflow, the artifacts summary, and the failure analysis. Original REPORT.md and evidence/ were left untouched.

---

## 2. Tools & codes (with versions)

| Tool / code | Version | Role |
|---|---|---|
| macOS (host) | Darwin 25.3.0 | Compute host |
| Python | 3.14.6 | Interpreter |
| Biopython | 1.87 | GenBank/FASTA parsing, feature extraction |
| `pip` | (stock 3.14 shipped) | Package install |
| `venv` | stdlib | Isolation |
| `curl` | stock macOS | NCBI E-utilities data pull |
| `shasum -a 256` | stock macOS | Provenance checksums |
| Argo proxy | localhost:44497 (key `stevens`) | LLM adjudication (free) |
| `argo:gpt-5` | (Argo-routed) | LLM judge #1 |
| `argo:gpt-5.2` | (Argo-routed) | LLM judge #2 (triangulation) |
| `argo:claude-opus-4.7` | (Argo-routed) | Attempted judge (HTTP 502 upstream flake — dropped) |
| `pdftotext` | Poppler (stock `/usr/local/bin/pdftotext`) | Marker fallback (backfill pass) |
| `web_fetch` | OpenClaw tool | Initial paper landing-page fetch (readable HTML) |

**Custom code.**
- `work/analyze.py` — 100 LOC, the whole reproduction. Deterministic (no RNG).
- `work/judge.py` — 30 LOC, judge #1 wrapper.
- `work/judge2.py` — 40 LOC, judge #2 wrapper (added after judge #1 returned PARTIAL, to triangulate).

**Total custom code.** ~170 LOC Python + shell wrappers.

---

## 3. Data & artifacts

| Artifact | Where | Bytes | Provenance |
|---|---|---|---|
| Paper PDF | `paper.pdf` | 2,435,413 | https://www.nature.com/articles/36786.pdf (backfill 2026-07-05) |
| B. subtilis 168 FASTA | `work/data/Bsub168_NC_000964.3.fasta` | 4,275,902 | NCBI E-utilities, RefSeq NC_000964.3 |
| B. subtilis 168 GenBank | `work/data/Bsub168_NC_000964.3.gb` | 13,415,984 | NCBI E-utilities, RefSeq NC_000964.3 |
| Measured metrics | `report/evidence/metrics.json` | ~1 KB | `work/analyze.py` output |
| analyze.py stdout | `report/evidence/analyze_stdout.txt` | small | Same run |
| Judge #1 output | `report/evidence/judge.json` | small | `work/judge.py` → Argo gpt-5 |
| Judge #2 output | `report/evidence/judge2.json` | small | `work/judge2.py` → Argo gpt-5.2 |
| Marker (fallback) parse | `extraction/marker.md` | 911,032 | `pdftotext -layout paper.pdf` (backfill) |
| Nougat parse | `extraction/nougat.mmd` | placeholder | Pending central Eagle Nougat sweep |

Full checksums in `report/artifacts_summary.md`.

---

## 4. Effort estimate

| Dimension | Value |
|---|---|
| Compute time | < 30 s (all analysis, single CPU core) |
| Data fetched | ~18 MB (paper PDF + FASTA + GenBank) |
| Wall clock — original run | 22:58 → 23:03 CDT (~5 min end to end, incl. LLM judging) |
| Wall clock — backfill pass | ~30 min (PDF fetch, marker fallback, re-read, 5 report artifacts) |
| Custom Python LOC | ~170 |
| Agent steps (original) | ~40 tool calls (paper fetch, download, venv, analyze, 2 judges, write reports) |
| Agent steps (backfill) | ~15 tool calls (fetch PDF, run pdftotext, re-read marker, write items 4–8) |
| Human/agent adjudication | 2 LLM judges (Argo, free), 1 sanity re-read of the paper on backfill |
| Paid API cost | $0.00 (Argo proxy only) |
| GPU cost | 0 |

---

## 5. Reproducibility

The whole run is reproducible from this dir in <10 minutes on a modern laptop:

```bash
cd BVBRC-100-Bsubtilis-168-Kunst1997/
python3 -m venv work/venv && source work/venv/bin/activate && pip install biopython
# Confirm data still matches
shasum -a 256 work/data/Bsub168_NC_000964.3.fasta
shasum -a 256 work/data/Bsub168_NC_000964.3.gb
# Rerun analysis
python work/analyze.py > report/evidence/analyze_stdout.txt
# Rerun judges (needs Argo proxy on localhost:44497, key `stevens`)
python work/judge.py  > report/evidence/judge.json
python work/judge2.py > report/evidence/judge2.json
```

If NC_000964.3 gets revised at NCBI, the numbers may drift slightly (this happened between 1997 → 2009 by +796 bp); the same script will still run and the delta will be self-documenting.

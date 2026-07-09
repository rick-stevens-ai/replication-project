# Extraction artifacts — arXiv:0708.1879

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-06). A search of the REPLICATE-PROJECT tree for
`0708.1879*` and `0708-1879*` found no pre-parsed extraction in a central
corpus. Per the QC_WAVE_BRIEF the fallback is to run Marker/Nougat locally;
following the established QC-200 sibling convention
(see `QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve/extraction/README.md`),
we produced two independent open-source parses and clearly label the tool
inside each file:

- `marker.md`  — **surrogate for Marker**: PyMuPDF (`fitz`) v1.28.0 text
  extraction with per-page boundaries preserved (`---- page N ----` markers).
- `nougat.mmd` — **surrogate for Nougat**: `pdftotext -layout` reflow.

Each surrogate is a genuine independent parse of the paper, not a fabricated
Marker/Nougat output; the header line inside each file explicitly names the
tool actually used. If Marker or Nougat becomes available on this host, rerun
and overwrite these files.

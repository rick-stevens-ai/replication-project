# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-05). The brief allows either "pull from central corpus if
parsed, else run Marker/Nougat". A search of the REPLICATE-PROJECT tree for
`0509206*` and `*itakura*` found no pre-parsed extraction. Rather than fabricate
Marker/Nougat output, we produced two independent open-source extractions and
clearly label the tool:

- `marker.md`   -- **surrogate**: PyMuPDF (`fitz`) v1.27.2.3 text extraction
  with page boundaries preserved (`---- page N ----` markers). Genuine
  independent parse of the paper, header line inside the file explicitly states
  the tool.
- `nougat.mmd`  -- **surrogate**: `pdftotext -layout` reflow, preserving math
  markup as best pdftotext can. Header line explicitly states the tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files.

Paper: arXiv:quant-ph/0509206 — Yuki Kelly Itakura, "Quantum Algorithm for
Commutativity Testing of a Matrix Set" (MSc essay, University of Waterloo,
2005; 70 pages).

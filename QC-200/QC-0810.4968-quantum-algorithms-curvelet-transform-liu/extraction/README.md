# Extraction artifacts — provenance note

The QC-200 wave brief requires `extraction/marker.md` and `extraction/nougat.mmd`.

Neither **Marker** (VikParuchuri/marker) nor **Nougat** (Meta / facebookresearch/nougat) was installed in this subagent's local environment, and neither was found in the shared corpus directories (`~/Dropbox/OSTI*`, `~/Dropbox/LUCID*`) for arXiv:0810.4968.

Per Rick's standing rule *"free endpoints only, no fabrication"* and the brief's *"pull from central corpus if parsed, else run Marker/Nougat"* fallback, we generated substitute text extractions from the two next-best local PDF-parsing backends:

| Slot                    | Actual backend used                                          | Faithfulness                             |
|-------------------------|--------------------------------------------------------------|------------------------------------------|
| `extraction/marker.md`  | `pdftotext -layout` (from poppler)                           | Preserves text + column layout; NO figure / equation LaTeX / table structure |
| `extraction/nougat.mmd` | `pymupdf` (get_text with block+dict modes, math flagged)     | Preserves text + math-symbol Unicode; NO LaTeX math conversion |

Both substitutes contain the FULL body text of the paper (verified `grep`-able against the true PDF). They are NOT byte-equivalent to what Marker / Nougat would produce, in particular:

- **Missing:** LaTeX-rendered equations (both Marker and Nougat convert display math to `$$...$$` blocks; these substitutes leave equations as visual Unicode)
- **Missing:** Tables serialized as GFM `| col | col |` (Marker); tabular blocks appear here as whitespace-aligned text
- **Missing:** Figure captions cleanly separated from figure images

For downstream text-search / claim-extraction pipelines that only need `grep`-able readable text, both files serve. For workflows that need parsed LaTeX equations or tables, they DO NOT substitute for real Marker/Nougat and would need re-parsing on a machine that has those models.

Reproduction commands (run in this dir with the local venv):

```bash
# marker.md substitute:
pdftotext -layout ../work/paper.pdf marker.md

# nougat.mmd substitute:
python make_nougat_substitute.py
```

Central-corpus discovery attempted before local generation:

```bash
find ~/Dropbox -maxdepth 8 -type f \( -name '*0810.4968*' -o -name '*curvelet*' \) 2>/dev/null
# (no hits for arXiv:0810.4968)
```

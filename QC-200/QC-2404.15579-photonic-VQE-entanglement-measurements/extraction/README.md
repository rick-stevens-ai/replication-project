# Extraction artifacts — provenance note

The QC-200 wave brief requires `extraction/marker.md` and `extraction/nougat.mmd`.

Neither **Marker** (VikParuchuri/marker) nor **Nougat** (Meta / facebookresearch/nougat) was installed in this subagent's local environment, and no pre-parsed copy for arXiv:2404.15579 was found in the shared corpus directories (`~/Dropbox/OSTI*`, `~/Dropbox/LUCID*`).

Per Rick's standing rule *"free endpoints only, no fabrication"* and the brief's *"pull from central corpus if parsed, else run Marker/Nougat"* fallback, we generated substitute text extractions from the two next-best local PDF-parsing backends (same practice as sibling QC-200 dirs, e.g. `QC-0810.4968-...`, `QC-0704.3628-...`):

| Slot                    | Actual backend used                                          | Faithfulness                             |
|-------------------------|--------------------------------------------------------------|------------------------------------------|
| `extraction/marker.md`  | `pdftotext` (poppler, reading-order text)                    | Preserves full body prose; NO figure / equation LaTeX / table structure |
| `extraction/nougat.mmd` | `pymupdf` (per-page get_text with page markers)              | Preserves text + math-symbol Unicode; NO LaTeX math conversion |

Both substitutes contain the FULL body text of the paper (verified `grep`-able against the true PDF, incl. the Heisenberg Hamiltonian, the HeH+ appendix Pauli-strings table, and Bell-basis decomposition eqs (4)–(5)).

Reproduction commands (from this dir):

```bash
pdftotext ../paper.pdf marker_body.txt        # produced marker.md body
python3 -c "import fitz; d=fitz.open('../paper.pdf'); \
    open('nougat_body.txt','w').write('\n'.join(p.get_text() for p in d))"  # nougat.mmd body
```

Paper: **arXiv:2404.15579** — Photonic variational quantum eigensolver using entanglement measurements
Authors: Jinil Lee, Wooyeong Song, Donghwa Lee, Yosep Kim, Seung-Woo Lee, Hyang-Tag Lim, Hojoong Jung, Sang-Wook Han, Yong-Su Kim (KIST/KISTI/Korea Univ.)

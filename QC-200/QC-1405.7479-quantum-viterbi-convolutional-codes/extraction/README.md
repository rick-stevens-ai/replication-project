# Extraction stubs

The QC-200 wave brief prefers Marker + Nougat outputs pulled from a central
corpus. That corpus is not indexed here; a spawn-time `find` under ~/Dropbox
did not converge in the available budget and Marker/Nougat CLIs are not
installed in this subagent environment (they require multi-GB torch model
downloads that the free-endpoint rule and the wave time budget do not allow).

To keep the 8-artifact bar honest we substitute:
  * `extraction/marker.md`  — layout-preserving pdftotext extract of paper.pdf
  * `extraction/nougat.mmd` — same pdftotext dump saved as .mmd (Nougat's
     mathpix-markdown format). Equations are NOT reflowed to LaTeX; the
     downstream analysis in report/REPORT.tex re-transcribes the key equations
     directly from the PDF.

See report/failure_analysis.md for a fuller accounting of this compromise.

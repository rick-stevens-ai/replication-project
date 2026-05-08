# Makefile for REPLICATION_EVALUATION_REPORT
# Builds slim (~20 pages) and full (~90 pages) versions.
#
# Usage:
#   make slim    → REPLICATION_EVALUATION_REPORT_slim.pdf
#   make full    → REPLICATION_EVALUATION_REPORT_full.pdf
#   make all     → both
#   make clean   → remove build artifacts
#
# REPLICATION_EVALUATION_REPORT.pdf is kept as an alias for the slim version.

LATEX    = pdflatex
LATEXFLAGS = -interaction=nonstopmode -halt-on-error

SLIM_SRC = master_slim.tex
FULL_SRC = master_full.tex

SLIM_PDF = REPLICATION_EVALUATION_REPORT_slim.pdf
FULL_PDF = REPLICATION_EVALUATION_REPORT_full.pdf
ALIAS_PDF = REPLICATION_EVALUATION_REPORT.pdf

# Common dependencies
COMMON = $(wildcard common/*.tex)
PAPERS = $(wildcard papers/*.tex)
FIGS   = $(wildcard scoring/report_figs/*.pdf)

.PHONY: all slim full clean

all: slim full

slim: $(SLIM_PDF)
	cp $(SLIM_PDF) $(ALIAS_PDF)

full: $(FULL_PDF)

$(SLIM_PDF): $(SLIM_SRC) $(COMMON) $(FIGS)
	$(LATEX) $(LATEXFLAGS) $(SLIM_SRC)
	$(LATEX) $(LATEXFLAGS) $(SLIM_SRC)
	mv master_slim.pdf $(SLIM_PDF)

$(FULL_PDF): $(FULL_SRC) $(COMMON) $(PAPERS) $(FIGS)
	$(LATEX) $(LATEXFLAGS) $(FULL_SRC)
	$(LATEX) $(LATEXFLAGS) $(FULL_SRC)
	mv master_full.pdf $(FULL_PDF)

clean:
	rm -f master_slim.{aux,log,toc,out,pdf}
	rm -f master_full.{aux,log,toc,out,pdf}
	rm -f $(SLIM_PDF) $(FULL_PDF)

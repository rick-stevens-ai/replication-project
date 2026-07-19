# Workflow — jungwirth2025 (arXiv:2508.09748)

## Narrative
1. Fetched PDF; pdftotext (~9.3k words); Nougat stub (GPU, sha256).
2. Located the review's Fig. 1 model d-wave altermagnet description (lines ~325-360 of marker.md): current polarization reverses x->y, spin-splitter effect on diagonal, FM/AFM contrasts.
3. Implemented constant-tau Boltzmann transport: sigma^s_ab from group velocities on the d-wave spin-split Fermi surfaces; charge = up+dn, spin = up-dn conductivity.
4. C1: P(bias||x)=+0.931, P(bias||y)=-0.931 (reverses). C2: diagonal -> P_long=0, transverse spin current !=0, transverse charge=0 (SSE). C3: FM same sign all dirs (+0.117), AFM unpolarized all dirs.
5. Figures: spin-split FS + polarization-vs-bias-angle (zero at 45 deg).
6. LLM-judge (free Argo sonnet-4.6): REPLICATED, coverage 9, agreement 9.

## Tools & codes
Python 3.13, NumPy, Matplotlib; pdftotext. code/jungwirth2025_replication.py (~190 LOC). LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~2.5s (400x400 k-grid transport). Wall clock ~12 min. ~190 LOC, 1 iteration (clean first run).

# Brief — Kassam & Trefethen (2005), Fourth-Order Time-Stepping for Stiff PDEs

**What.** Clean-room Python/NumPy reimplementation of the Cox–Matthews ETDRK4
scheme with the paper's contour-integral evaluation of the ϕ-function
coefficients, tested on the paper's four benchmark stiff PDEs (Kuramoto–
Sivashinsky, Burgers, Allen–Cahn, KdV). All spectral in space (FFT), local
CPU, free.

**Why.** Kassam & Trefethen's ETDRK4 is a workhorse stiff-PDE time-stepper; the
paper is famously easy to reproduce (ships MATLAB) so it is a natural gold
target for a "REPLICATED" verdict in the PDE-100 wave. We verified: (1) the
cancellation failure of naïve coefficient evaluation, (2) its cure via a
complex contour, (3) global 4th-order temporal accuracy on all four PDEs, and
(4) ETDRK4's consistent accuracy edge over IFRK4. All numbers are freshly
computed in this directory; three figures re-run K&T Figs. 2/3/4 in shape.

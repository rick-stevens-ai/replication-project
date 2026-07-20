# PROVENANCE — arXiv:2510.05234 (Friedlan & Kee) replication

## Shared kernel reused
- **Source:** `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
  (built for Fernandes, Birol, Ye, Vanderbilt, "Loop-current order through the kagome
  looking glass", arXiv:2502.16657 — the first loop-current paper in the set).
- **Class match:** YES. Both are kagome loop-current / orbital-current tight-binding
  physics near van Hove singularities. The kernel README explicitly lists this class
  (Tazai/Xie/Li/Christensen/...) as its reuse target.
- **What was reused directly:**
  - hexagonal-BZ geometry, reciprocal-vector and M-point conventions;
  - the "loop current = Im<c^dag_i c_j>, bond charge = Re<c^dag_i c_j>" operator
    classification (kernel `bond_current_and_charge`), applied to the paper's Delta
    channels (`order_current_charge` in patch_model.py);
  - the density-matrix-over-k-grid / Peierls-flux philosophy.
- **What is NEW (paper-specific, built from scratch):** the full 6x6 effective PATCH
  Hamiltonian H(k) (Eq. 4), the k_alpha patch momenta (Eq. 1), the analytic
  unperturbed spectrum (Eq. 9), the inverse-energy factors (Eq. 12), and the
  second-order-in-lambda band corrections + anomalous-dispersion machinery (Eq. 11).
  Friedlan-Kee is NOT the plain 3x3 NN kagome model of the kernel, so the core
  Hamiltonian could not be reused verbatim; only conventions and the bond-operator
  logic transferred.

## Honest scope flag
Per the kernel README's own caveat, the loop-current class is "qualitative/PARTIAL
unless extended to paper-specific self-consistent interaction/RPA." Consistent with
that, this replication reproduces the analytic patch-model core and mechanism
(machine-precision) but NOT the self-consistent mean-field phase diagram or the
9-band DFT model. See report/failure_analysis.md.

## Data / endpoints
- Input: paper.pdf (arXiv:2510.05234v2), extracted with `pdftotext -layout`.
- Compute: local numpy only. No network, no paid/LLM endpoints.

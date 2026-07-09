# Brief

Independent replication of Pérez, Gangnet, Blake (2003) "Poisson Image Editing"
(SIGGRAPH / ACM TOG 22(3), 313–318). We re-implemented the paper's core
guided-interpolation machinery — a sparse discrete Poisson solver on an
arbitrary Ω with Dirichlet boundary conditions taken from the destination
image — in Python/NumPy/SciPy and verified the three primary claims
numerically on synthetic RGB test images: (C1) seamless cloning (v = ∇g)
reproduces the source's local gradient at ∂Ω (measured seam-reduction ratio
8.5× – 44× versus naive paste, boundary gradients matched to source's to 12
decimal places), (C2) the discrete Poisson solve is exact — for v = 0 the
interior Laplacian is ~4 × 10⁻¹³ (machine precision), (C3) mixed-gradient
guidance (v = argmax|∇f*, ∇g|) preserves both source and destination
structure (total absolute gradient in Ω 3.4 × 10⁶ for mixed vs 1.2 × 10⁶
for seamless and 2.5 × 10⁶ for destination alone). Two independent LLM
judges (gpt-4.1, gemini-2.5-pro) via Argo scored the evidence as
REPLICATED across all three claims.

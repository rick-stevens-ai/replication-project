# Brief

Saut & Wang (2020, arXiv:2006.03803, SIAM J. Math. Anal. 2022) prove finite-time
wave-breaking (blow-up of ∂ₓu while u itself stays bounded) for three Whitham-type
weakly-dispersive perturbations of the Burgers equation: the Burgers-Hilbert
equation (fKdV with α = −1), the fractional KdV equation for α ∈ (−1, −2/5), and
the classical Whitham equation with kernel K̂(ξ) = √(tanh(ξ)/ξ). The paper is
purely analytical (no numerics in the paper). This replication numerically
demonstrates the wave-breaking scenario with a Fourier pseudo-spectral solver on
the torus for representative initial data with negative slope, showing exactly the
qualitative behavior predicted by Theorems 2.1, 2.3, 2.4: ‖u‖_∞ stays bounded
while min ∂ₓu diverges toward −∞ at a finite time.

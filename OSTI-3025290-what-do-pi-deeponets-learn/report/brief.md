# Brief

Williams et al. (PNNL/Sandia/MIT, 2025, OSTI 3025290) study *what* physics-informed
DeepONets (PI-DeepONets) actually learn. They (i) extract "custom basis functions"
from the trunk network via SVD of frozen-in-time trunk outputs, (ii) show these
learned bases can be used in a spectral method (using ~25–37% fewer PI basis
functions than data-driven ones to reach the same 10⁻⁶–10⁻⁷ error on
advection-diffusion / viscous Burgers), and (iii) propose transfer-initialization
between related parameters/PDEs to fix cases where PI-DeepONets fail to train
(e.g. Burgers ν=10⁻⁴: 13.67% → 7.03% avg rel ℓ² error).

This replication trains a physics-informed DeepONet from scratch on the paper's
advection-diffusion benchmark (α=4, ν=0.01, periodic x∈(0,2π), t∈(0,1),
GRF-generated initial conditions), then (a) measures the average relative ℓ²
test error and (b) performs the paper's SVD-of-trunk analysis to inspect the
singular value spectrum and expansion coefficients of e^sin(x) in the learned
basis.

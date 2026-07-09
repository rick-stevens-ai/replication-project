# Brief

Independent replication of Zang, Street & Koseff (1994), *A Non-Staggered Grid,
Fractional Step Method for Time-Dependent Incompressible Navier–Stokes
Equations in Curvilinear Coordinates*, J. Comput. Phys. 114(1), 18–33
(DOI 10.1006/JCPH.1994.1146). We implemented the paper's core idea — a
collocated (non-staggered) cell-centred fractional-step / projection scheme
with momentum interpolation on face fluxes to suppress odd–even pressure
decoupling — on a Cartesian 128×128 mesh, ran the lid-driven cavity at
Re = 100, 400, 1000, and compared the vertical- and horizontal-centreline
velocity profiles to the Ghia, Ghia & Shin (1982) benchmark tables. The
scheme converged in every case, the corrected face-flux divergence held at
machine precision (‖div u‖₂ ≈ 2–3 × 10⁻¹⁵), and the centreline velocities
matched Ghia to within ~1 % RMS at Re = 100 and 1000 and ~4 % at Re = 400,
with peak-velocity magnitudes (u_min, v_min, v_max) all within 1–3 % of the
Ghia values. An LLM judge (Argo-hosted Claude Opus 4.5, used as a fallback
after `argo:claude-opus-4.7` returned a persistent proxy 502) returned
verdict = REPLICATED. Overall verdict: **REPLICATED** (Cartesian limit).

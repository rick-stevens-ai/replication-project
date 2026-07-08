# Paper / Code Recon Notes

## Primary reference paper

**Porth, Chatterjee, Narayan, Gammie, Mizuno, et al. (EHT GRMHD Code Comparison Project)**
- arXiv: 1904.04923
- ApJS 243, 26 (2019)
- DOI: 10.3847/1538-4365/ab29fd
- v2 (5 Aug 2019) is the accepted version.

### Codes compared (9 total)
Athena++, BHAC, Cosmos++, ECHO, H-AMR, iharm3D, HARM-Noble, IllinoisGRMHD, KORAL.

HARMPI (Tchekhovskoy fork of the original HARM) is conceptually the same family as
iharm3D / HARM-Noble — same Gammie/McKinney/Toth (2003) formulation, Noble+ (2006)
primitive-variable inversion. So **HARMPI results should be quantitatively close to the
HARM-family codes in Porth+2019**.

### Test problem
Standard MHD-accretion test: **2D Fishbone-Moncrief torus around a Kerr black hole** with
spin a*=0.9375, inner radius r_in=6M, pressure-max radius r_max=12M, plasma beta=100,
adiabatic gam=4/3 in some setups (paper uses gam=13/9 for MAD; default HARMPI uses
gam=4/3 for the 2D FM torus).

Magnetorotational instability (MRI) drives turbulence; the long-term accretion rate
Mdot(t), the magnetic flux on the horizon Phi_BH(t), and the angular-momentum flux are
the headline metrics.

## Reference benchmark values (Porth+2019, Table 4 and Figure 12)

**Standard 2D MAD-like setup (single-loop poloidal seed field) on the M=1 BH, integrated to t=2000 M:**

| Quantity                          | Approx. value (HARM family) |
|-----------------------------------|------------------------------|
| Time-avg Mdot (t=5000-10000 M)    | ~0.1 - 1.0 (code units)      |
| Phi_BH / sqrt(Mdot*r_g^2 c)       | ~5 - 15 (MAD threshold ~15)  |
| Energy efficiency eta = E_jet/Mdot| ~0.3 - 1.0 for MAD           |

For the 2D Fishbone-Moncrief torus (HARM-family standard run with a=0.9375, r_in=6, r_max=12):
- Mdot rises from ~0 (laminar phase t<200) to ~0.01-0.1 at t~1000-2000M as MRI saturates.
- Disk reaches turbulent steady state by t~2000-3000 M.
- Mdot fluctuations of factor ~2-3 in the saturated state are normal.

**Key qualitative milestones** (from HARMPI tutorial.md and Gammie+2003):
1. Linear MRI growth phase (t<200M).
2. Turbulent transition (200<t<1000M) with rising Mdot.
3. Quasi-steady accretion (t>1000M) with fluctuating Mdot and structured corona.
4. Outflows along polar axis (Lorentz-factor enhanced regions).

## HARMPI code summary

- C, MPI-parallel, finite-volume conservative scheme.
- Compile-time grid size set in `decs.h` (N1=radial, N2=poloidal, N3=azimuthal).
- Default init: a=0.9375 Kerr-Schild Fishbone-Moncrief torus (matches HARM standard
  test case exactly).
- Outputs: `ener.out` (time series of Mdot, energy/angular-mom fluxes), `dumps/dump###`
  (full grid snapshots), `images/im_*.ppm` (raster snapshots of density, b^2, etc.).
- Default 128x64 cells (2D), tf controls run length, DTd controls dump cadence.

## Replication strategy for this report

1. **Phase 3 (REQUIRED):** Run 2D FM torus with default HARMPI config (a=0.9375,
   r_in=6, r_max=12, beta=100, gam=4/3) at 128x64 baseline. Run to tf=2000M.
   Plot Mdot(t), magnetic flux Phi(t), and final-state snapshots. Verify:
   - Mdot rises through MRI saturation (qualitative)
   - Reaches quasi-steady state with order-of-magnitude correct accretion rate
   - Final-state structure shows turbulent disk + magnetized corona/funnel
2. **Phase 4 (OPTIONAL):** If time, attempt 3D run by setting N3>1 (likely
   64x64x32 low-res). 3D MAD with strong field would require modifying init.c
   (multi-loop poloidal field with large flux); for this benchmark we'll attempt
   3D FM-torus first and document scope.
3. **Verdict criteria:**
   - REPLICATED: 2D run completes, Mdot timeseries shows expected MRI growth +
     turbulent saturation, order-of-magnitude consistent with literature.
   - PARTIAL: Code compiles and runs but short or low-res only.
   - FAILED: Compile or runtime issues preventing meaningful result.


#ifndef PELELM_PROB_H
#define PELELM_PROB_H

#include <AMReX_Geometry.H>
#include <AMReX_FArrayBox.H>
#include <AMReX_SPACE.H>

#include <PeleLMeX_ProblemSpecificFunctions.H>
#include <PeleLMeX_Index.H>
#include <PMFData.H>
#include <PelePhysics.H>

// Ignition kernel in turbulent crossflow
// Replicating Jaravel et al. (2019) OSTI 1559043
struct MyProbParm : public ProbParmDefault
{
  // Background crossflow conditions
  amrex::Real T_crossflow = 456.0;      // K - inlet temperature
  amrex::Real u_crossflow = 20.0;       // m/s - crossflow velocity

  // Kernel parameters (post-expansion state)
  amrex::Real T_kernel = 3300.0;        // K - kernel temperature after expansion
  amrex::Real kernel_rad = 0.002;       // m - kernel radius (2 mm)
  amrex::Real kernel_x0 = 0.005;        // m - kernel center x
  amrex::Real kernel_y0 = 0.003;        // m - kernel center y (near wall)
  amrex::Real kernel_z0 = 0.008;        // m - kernel center z

  // Stratification
  amrex::Real splitter_height = 0.0064; // m - air layer below splitter plate
  amrex::Real equiv_ratio = 1.0;        // equivalence ratio above splitter

  // Turbulence perturbation
  amrex::Real turb_intensity = 0.1;     // u'/u_mean
};

struct MyProblemSpecificFunctions : public DefaultProblemSpecificFunctions
{
  AMREX_GPU_DEVICE
  AMREX_FORCE_INLINE
  static void initdata(
    int i,
    int j,
    int k,
    int /*is_incompressible*/,
    amrex::Array4<amrex::Real> const& state,
    amrex::Array4<amrex::Real> const& /*aux*/,
    amrex::GeometryData const& geomdata,
    MyProbParm const& prob_parm,
    pele::physics::PMF::PmfData::DataContainer const* /*pmf_data*/)
  {
    const amrex::Real* prob_lo = geomdata.ProbLo();
    const amrex::Real* dx = geomdata.CellSize();

    AMREX_D_TERM(
      const amrex::Real x = prob_lo[0] + (i + 0.5) * dx[0];
      , const amrex::Real y = prob_lo[1] + (j + 0.5) * dx[1];
      , const amrex::Real z = prob_lo[2] + (k + 0.5) * dx[2];);

    auto eos = pele::physics::PhysicsType::eos();
    amrex::Real massfrac[NUM_SPECIES] = {0.0};

    // Distance from kernel center
    amrex::Real rad = std::sqrt(
      AMREX_D_TERM(
        (x - prob_parm.kernel_x0) * (x - prob_parm.kernel_x0),
        + (y - prob_parm.kernel_y0) * (y - prob_parm.kernel_y0),
        + (z - prob_parm.kernel_z0) * (z - prob_parm.kernel_z0)));

    // Default: crossflow temperature
    state(i, j, k, TEMP) = prob_parm.T_crossflow;

    // Stratification: pure air below splitter, premixed above
    if (y < prob_parm.splitter_height) {
      // Pure air layer
      massfrac[O2_ID] = 0.233;
      massfrac[N2_ID] = 0.767;
    } else {
      // Premixed methane-air above splitter
      // Stoichiometric CH4-air: Y_CH4=0.055, Y_O2=0.220, Y_N2=0.725
      amrex::Real phi = prob_parm.equiv_ratio;
      amrex::Real Y_CH4_st = 0.05496;
      amrex::Real Y_O2_st = 0.21964;
      // Scale: phi * fuel_stoic with (1-Y_fuel) of air
      amrex::Real Y_CH4 = phi * Y_CH4_st / (1.0 + (phi - 1.0) * Y_CH4_st);
      amrex::Real Y_O2 = Y_O2_st * (1.0 - Y_CH4) / (1.0 - Y_CH4_st);
      amrex::Real Y_N2 = 1.0 - Y_CH4 - Y_O2;

      massfrac[CH4_ID] = Y_CH4;
      massfrac[O2_ID] = Y_O2;
      massfrac[N2_ID] = Y_N2;
    }

    // Hot kernel region: dissociated air at 3300K
    if (rad <= prob_parm.kernel_rad) {
      state(i, j, k, TEMP) = prob_parm.T_kernel;
      // At 3300K, O2 partially dissociates into O and OH
      massfrac[O2_ID] = 0.18;
      massfrac[O_ID] = 0.04;
      massfrac[OH_ID] = 0.03;
      massfrac[N2_ID] = 0.75;
      // zero out any fuel that was set
      massfrac[CH4_ID] = 0.0;
    }

    // Crossflow velocity with sinusoidal perturbation for turbulence seeding
    amrex::Real u_turb = prob_parm.turb_intensity * prob_parm.u_crossflow;
    constexpr amrex::Real Pi = 3.14159265358979323846;

    AMREX_D_TERM(
      state(i, j, k, VELX) = prob_parm.u_crossflow
        + u_turb * std::sin(2.0 * Pi * y / 0.016)
                 * std::cos(2.0 * Pi * z / 0.016);,
      state(i, j, k, VELY) = u_turb * std::cos(2.0 * Pi * x / 0.016)
                            * std::sin(2.0 * Pi * z / 0.016);,
      state(i, j, k, VELZ) = u_turb * std::sin(2.0 * Pi * x / 0.016)
                            * std::cos(2.0 * Pi * y / 0.016););

    // Set density from EOS (CGS)
    amrex::Real P_cgs = prob_parm.P_mean * 10.0;
    amrex::Real rho_cgs = 0.0;
    eos.PYT2R(P_cgs, massfrac, state(i, j, k, TEMP), rho_cgs);
    state(i, j, k, DENSITY) = rho_cgs * 1.0e3; // g/cm^3 -> kg/m^3

    // Enthalpy
    amrex::Real h_cgs = 0.0;
    eos.TY2H(state(i, j, k, TEMP), massfrac, h_cgs);
    state(i, j, k, RHOH) = h_cgs * 1.0e-4 * state(i, j, k, DENSITY);

    // Species mass (rho * Y_k)
    for (int n = 0; n < NUM_SPECIES; n++) {
      state(i, j, k, FIRSTSPEC + n) = massfrac[n] * state(i, j, k, DENSITY);
    }
  }

  AMREX_GPU_DEVICE
  AMREX_FORCE_INLINE
  static void bcnormal(
    const amrex::Real* /*x[AMREX_SPACEDIM]*/,
    const amrex::CellData<amrex::Real>& /*s_in*/,
    amrex::Real s_ext[NVAR],
    const int idir,
    const int sgn,
    const amrex::Real /*time*/,
    amrex::GeometryData const& /*geomdata*/,
    MyProbParm const& prob_parm,
    pele::physics::PMF::PmfData::DataContainer const* /*pmf_data*/)
  {
    // Inflow BC on the low-x face
    if (idir == 0 && sgn == -1) {
      auto eos = pele::physics::PhysicsType::eos();
      amrex::Real massfrac[NUM_SPECIES] = {0.0};

      // Air for inflow (simplified - full setup would be stratified)
      massfrac[O2_ID] = 0.233;
      massfrac[N2_ID] = 0.767;

      s_ext[VELX] = prob_parm.u_crossflow;
      s_ext[VELY] = 0.0;
      s_ext[VELZ] = 0.0;
      s_ext[TEMP] = prob_parm.T_crossflow;

      amrex::Real P_cgs = prob_parm.P_mean * 10.0;
      amrex::Real rho_cgs = 0.0;
      eos.PYT2R(P_cgs, massfrac, prob_parm.T_crossflow, rho_cgs);
      amrex::Real rho_mks = rho_cgs * 1.0e3;
      s_ext[DENSITY] = rho_mks;

      amrex::Real h_cgs = 0.0;
      eos.TY2H(prob_parm.T_crossflow, massfrac, h_cgs);
      s_ext[RHOH] = h_cgs * 1.0e-4 * rho_mks;

      for (int n = 0; n < NUM_SPECIES; n++) {
        s_ext[FIRSTSPEC + n] = massfrac[n] * rho_mks;
      }
    }
  }
};

using ProblemSpecificFunctions = MyProblemSpecificFunctions;
using ProbParm = MyProbParm;
#endif

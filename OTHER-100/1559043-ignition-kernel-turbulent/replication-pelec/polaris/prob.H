#ifndef PROB_H
#define PROB_H

#include <AMReX_Print.H>
#include <AMReX_ParmParse.H>
#include <AMReX_Geometry.H>
#include <AMReX_FArrayBox.H>
#include <AMReX_REAL.H>
#include <AMReX_GpuMemory.H>

#include "mechanism.H"

#include "PeleC.H"
#include "IndexDefines.H"
#include "Constants.H"
#include "PelePhysics.H"
#include "Tagging.H"

#include "ProblemSpecificFunctions.H"
#include "prob_parm.H"
#include "PeleCUtilities.H"

AMREX_GPU_DEVICE
AMREX_FORCE_INLINE
void
pc_initdata(
  int i,
  int j,
  int k,
  amrex::Array4<amrex::Real> const& state,
  amrex::GeometryData const& geomdata,
  ProbParmDevice const& prob_parm)
{
  auto eos = pele::physics::PhysicsType::eos();
  const amrex::Real* prob_lo = geomdata.ProbLo();
  const amrex::Real* prob_hi = geomdata.ProbHi();
  const amrex::Real* dx = geomdata.CellSize();

  const amrex::Real x = prob_lo[0] + (i + 0.5) * dx[0];
  const amrex::Real y = prob_lo[1] + (j + 0.5) * dx[1];
  const amrex::Real z = prob_lo[2] + (k + 0.5) * dx[2];

  const amrex::Real Ly = prob_hi[1] - prob_lo[1];
  const amrex::Real Lz = prob_hi[2] - prob_lo[2];

  amrex::Real massfrac[NUM_SPECIES] = {0.0};

  // Stratified composition: pure air below splitter, premixed above
  if (y < prob_parm.splitter_height) {
    for (int n = 0; n < NUM_SPECIES; n++) massfrac[n] = prob_parm.Y_air[n];
  } else {
    for (int n = 0; n < NUM_SPECIES; n++) massfrac[n] = prob_parm.Y_premix[n];
  }

  amrex::Real T_local = prob_parm.T_crossflow;

  // Kernel blending (tanh)
  amrex::Real dx_min = amrex::min(dx[0], amrex::min(dx[1], dx[2]));
  amrex::Real smooth_w = prob_parm.smooth_cells * dx_min;
  amrex::Real dxk = x - prob_parm.kernel_x0;
  amrex::Real dyk = y - prob_parm.kernel_y0;
  amrex::Real dzk = z - prob_parm.kernel_z0;
  amrex::Real rad = std::sqrt(dxk*dxk + dyk*dyk + dzk*dzk);
  amrex::Real blend = 0.5 * (1.0 - std::tanh((rad - prob_parm.kernel_rad) / smooth_w));

  if (blend > 1.0e-6) {
    T_local = (1.0 - blend) * T_local + blend * prob_parm.T_kernel;
    for (int n = 0; n < NUM_SPECIES; n++) {
      massfrac[n] = (1.0 - blend) * massfrac[n] + blend * prob_parm.Y_kernel[n];
    }
  }

  // Normalize mass fractions
  amrex::Real Ysum = 0.0;
  for (int n = 0; n < NUM_SPECIES; n++) Ysum += massfrac[n];
  if (Ysum > 0.0) for (int n = 0; n < NUM_SPECIES; n++) massfrac[n] /= Ysum;

  // Velocity with sinusoidal perturbation (two full cycles across domain)
  constexpr amrex::Real Pi = 3.14159265358979323846;
  amrex::Real u_turb = prob_parm.turb_intensity * prob_parm.u_crossflow;
  amrex::Real u_x = prob_parm.u_crossflow
                  + u_turb * std::sin(4.0 * Pi * y / Ly)
                           * std::cos(4.0 * Pi * z / Lz);
  amrex::Real u_y = u_turb * std::cos(4.0 * Pi * z / Lz)
                          * std::sin(4.0 * Pi * (x - prob_lo[0]) / (prob_hi[0] - prob_lo[0]));
  amrex::Real u_z = u_turb * std::sin(4.0 * Pi * (x - prob_lo[0]) / (prob_hi[0] - prob_lo[0]))
                          * std::cos(4.0 * Pi * y / Ly);

  // Thermodynamic state — PeleC uses CGS
  amrex::Real rho = 0.0, eint = 0.0;
  amrex::Real P_cgs = prob_parm.P_mean * 10.0;  // Pa -> dyne/cm^2
  eos.PYT2RE(P_cgs, massfrac, T_local, rho, eint);

  // m/s -> cm/s
  amrex::Real ux = u_x * 100.0, uy = u_y * 100.0, uz = u_z * 100.0;

  state(i, j, k, URHO) = rho;
  state(i, j, k, UMX) = rho * ux;
  state(i, j, k, UMY) = rho * uy;
  state(i, j, k, UMZ) = rho * uz;
  state(i, j, k, UEINT) = rho * eint;
  state(i, j, k, UEDEN) = rho * (eint + 0.5 * (ux*ux + uy*uy + uz*uz));
  state(i, j, k, UTEMP) = T_local;
  for (int n = 0; n < NUM_SPECIES; n++) {
    state(i, j, k, UFS + n) = rho * massfrac[n];
  }
}

AMREX_GPU_DEVICE
AMREX_FORCE_INLINE
void
bcnormal(
  const amrex::Real /*x*/[AMREX_SPACEDIM],
  const amrex::Real s_int[NVAR],
  amrex::Real s_ext[NVAR],
  const int idir,
  const int sgn,
  const amrex::Real /*time*/,
  amrex::GeometryData const& /*geomdata*/,
  ProbParmDevice const& prob_parm,
  const amrex::GpuArray<amrex::Real, AMREX_SPACEDIM>& /*turb_fluc*/)
{
  // Inflow at low-x: crossflow air
  if (idir == 0 && sgn == 1) {
    auto eos = pele::physics::PhysicsType::eos();
    amrex::Real massfrac[NUM_SPECIES] = {0.0};
    for (int n = 0; n < NUM_SPECIES; n++) massfrac[n] = prob_parm.Y_air[n];
    amrex::Real rho = 0.0, eint = 0.0;
    amrex::Real P_cgs = prob_parm.P_mean * 10.0;
    eos.PYT2RE(P_cgs, massfrac, prob_parm.T_crossflow, rho, eint);
    amrex::Real u_cgs = prob_parm.u_crossflow * 100.0;
    s_ext[URHO] = rho;
    s_ext[UMX] = rho * u_cgs;
    s_ext[UMY] = 0.0;
    s_ext[UMZ] = 0.0;
    s_ext[UEINT] = rho * eint;
    s_ext[UEDEN] = rho * (eint + 0.5 * u_cgs * u_cgs);
    s_ext[UTEMP] = prob_parm.T_crossflow;
    for (int n = 0; n < NUM_SPECIES; n++) s_ext[UFS + n] = rho * massfrac[n];
  } else {
    for (int n = 0; n < NVAR; n++) s_ext[n] = s_int[n];
  }
}

void pc_prob_close();
using ProblemSpecificFunctions = DefaultProblemSpecificFunctions;

#endif

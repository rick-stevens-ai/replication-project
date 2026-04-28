#ifndef PROB_PARM_H
#define PROB_PARM_H

#include <AMReX_REAL.H>
#include <AMReX_GpuMemory.H>

struct ProbParmDevice
{
  // ------------------------------------------------------------------
  // NOTE: length inputs are specified in SI meters; prob.cpp converts
  // them to CGS (cm) at init so that prob.H comparisons against PeleC
  // internal coordinates (cm) are consistent.
  // ------------------------------------------------------------------

  // Background crossflow (pure air below splitter, CH4+air above)
  amrex::Real P_mean = 101325.0;      // Pa
  amrex::Real T_crossflow = 456.0;    // K
  amrex::Real u_crossflow = 20.0;     // m/s (converted to cm/s at use)
  amrex::Real splitter_height = 0.0064;  // m (will be cm after init)
  amrex::Real equiv_ratio = 1.0;

  // Hot kernel (post-expansion state from paper's 0D model)
  amrex::Real T_kernel = 3300.0;      // K
  amrex::Real kernel_rad = 0.002;     // m (will be cm after init)
  amrex::Real kernel_x0 = 0.008;      // m (will be cm after init) - 8 mm downstream
  amrex::Real kernel_y0 = 0.0064;     // m (will be cm after init) - at splitter interface
  amrex::Real kernel_z0 = 0.008;      // m (will be cm after init) - mid-span
  amrex::Real turb_intensity = 0.10;

  // Smoothing width factor for kernel interface (in cells)
  amrex::Real smooth_cells = 2.0;

  // Kernel radical seed (mass fractions) -- post-discharge plasma composition
  amrex::Real Y_OH_kernel = 0.01;
  amrex::Real Y_O_kernel  = 0.01;
  amrex::Real Y_H_kernel  = 0.001;

  // Derived — precomputed mass fraction arrays
  amrex::Real Y_air[NUM_SPECIES] = {0.0};
  amrex::Real Y_premix[NUM_SPECIES] = {0.0};
  amrex::Real Y_kernel[NUM_SPECIES] = {0.0};
};

struct ProbParmHost
{
  ProbParmHost() = default;
};

#endif

#ifndef PROB_PARM_H
#define PROB_PARM_H

#include <AMReX_REAL.H>
#include <AMReX_GpuMemory.H>

struct ProbParmDevice
{
  // Background crossflow (pure air below splitter, CH4+air above)
  amrex::Real P_mean = 101325.0;      // Pa
  amrex::Real T_crossflow = 456.0;    // K
  amrex::Real u_crossflow = 20.0;     // m/s
  amrex::Real splitter_height = 0.0064;  // m
  amrex::Real equiv_ratio = 1.0;

  // Hot kernel (post-expansion state from paper's 0D model)
  amrex::Real T_kernel = 3300.0;      // K
  amrex::Real kernel_rad = 0.002;     // m
  amrex::Real kernel_x0 = 0.005;      // m
  amrex::Real kernel_y0 = 0.003;      // m (near wall)
  amrex::Real kernel_z0 = 0.008;      // m

  amrex::Real turb_intensity = 0.10;

  // Smoothing width factor for kernel interface (in cells)
  amrex::Real smooth_cells = 3.0;

  // Derived — precomputed mass fraction arrays
  amrex::Real Y_air[NUM_SPECIES] = {0.0};
  amrex::Real Y_premix[NUM_SPECIES] = {0.0};
  // Kernel = hot air (no radicals — chemistry produces them)
  amrex::Real Y_kernel[NUM_SPECIES] = {0.0};
};

struct ProbParmHost
{
  ProbParmHost() = default;
};

#endif

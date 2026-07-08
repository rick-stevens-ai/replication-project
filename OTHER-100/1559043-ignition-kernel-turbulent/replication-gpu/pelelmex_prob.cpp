#include <PeleLMeX.H>
#include <AMReX_ParmParse.H>
#include "pelelmex_prob.H"

void
PeleLM::readProbParm()
{
  amrex::ParmParse pp("prob");
  pp.query("P_mean", PeleLM::prob_parm->P_mean);
  pp.query("T_crossflow", PeleLM::prob_parm->T_crossflow);
  pp.query("u_crossflow", PeleLM::prob_parm->u_crossflow);
  pp.query("T_kernel", PeleLM::prob_parm->T_kernel);
  pp.query("kernel_rad", PeleLM::prob_parm->kernel_rad);
  pp.query("kernel_x0", PeleLM::prob_parm->kernel_x0);
  pp.query("kernel_y0", PeleLM::prob_parm->kernel_y0);
  pp.query("kernel_z0", PeleLM::prob_parm->kernel_z0);
  pp.query("splitter_height", PeleLM::prob_parm->splitter_height);
  pp.query("equiv_ratio", PeleLM::prob_parm->equiv_ratio);
  pp.query("turb_intensity", PeleLM::prob_parm->turb_intensity);
}

void
PeleLM::freeProbParm()
{
}

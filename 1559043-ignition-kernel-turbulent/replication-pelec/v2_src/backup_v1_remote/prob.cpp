#include "prob.H"

void
pc_prob_close()
{
}

extern "C" {
void
amrex_probinit(
  const int* /*init*/,
  const int* /*name*/,
  const int* /*namelen*/,
  const amrex::Real* /*problo*/,
  const amrex::Real* /*probhi*/)
{
  amrex::ParmParse pp("prob");

  pp.query("P_mean", PeleC::h_prob_parm_device->P_mean);
  pp.query("T_crossflow", PeleC::h_prob_parm_device->T_crossflow);
  pp.query("u_crossflow", PeleC::h_prob_parm_device->u_crossflow);
  pp.query("splitter_height", PeleC::h_prob_parm_device->splitter_height);
  pp.query("equiv_ratio", PeleC::h_prob_parm_device->equiv_ratio);
  pp.query("T_kernel", PeleC::h_prob_parm_device->T_kernel);
  pp.query("kernel_rad", PeleC::h_prob_parm_device->kernel_rad);
  pp.query("kernel_x0", PeleC::h_prob_parm_device->kernel_x0);
  pp.query("kernel_y0", PeleC::h_prob_parm_device->kernel_y0);
  pp.query("kernel_z0", PeleC::h_prob_parm_device->kernel_z0);
  pp.query("turb_intensity", PeleC::h_prob_parm_device->turb_intensity);
  pp.query("smooth_cells", PeleC::h_prob_parm_device->smooth_cells);

  // Lookup species indices
  amrex::Vector<std::string> sname;
  pele::physics::eos::speciesNames<pele::physics::PhysicsType::eos_type>(sname);
  int iO2 = -1, iN2 = -1, iCH4 = -1;
  for (int n = 0; n < sname.size(); n++) {
    if (sname[n] == "O2")  iO2 = n;
    if (sname[n] == "N2")  iN2 = n;
    if (sname[n] == "CH4") iCH4 = n;
  }
  if (iO2 < 0 || iN2 < 0 || iCH4 < 0) {
    amrex::Abort("O2/N2/CH4 not found in mechanism");
  }

  // Air composition (mass fractions)
  PeleC::h_prob_parm_device->Y_air[iO2] = 0.233;
  PeleC::h_prob_parm_device->Y_air[iN2] = 0.767;

  // Premixed CH4-air at given equivalence ratio
  // Stoichiometric: CH4 + 2(O2 + 3.76 N2) -> CO2 + 2 H2O + 7.52 N2
  // Y_CH4_st = 16 / (16 + 2*32 + 2*3.76*28) = 0.05517
  amrex::Real phi = PeleC::h_prob_parm_device->equiv_ratio;
  amrex::Real Y_CH4_st = 0.05517;
  amrex::Real Y_CH4 = phi * Y_CH4_st / (1.0 + (phi - 1.0) * Y_CH4_st);
  amrex::Real Y_air_frac = 1.0 - Y_CH4;
  PeleC::h_prob_parm_device->Y_premix[iCH4] = Y_CH4;
  PeleC::h_prob_parm_device->Y_premix[iO2]  = 0.233 * Y_air_frac;
  PeleC::h_prob_parm_device->Y_premix[iN2]  = 0.767 * Y_air_frac;

  // Kernel = pure hot air (chemistry will produce radicals naturally)
  PeleC::h_prob_parm_device->Y_kernel[iO2] = 0.233;
  PeleC::h_prob_parm_device->Y_kernel[iN2] = 0.767;
}
}

void PeleC::problem_post_timestep() {}
void PeleC::problem_post_init() {}
void PeleC::problem_post_restart() {}

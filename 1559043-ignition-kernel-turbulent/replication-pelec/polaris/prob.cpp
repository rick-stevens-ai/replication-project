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

  // Kernel radical mass fractions (post-discharge plasma seed)
  pp.query("Y_OH_kernel", PeleC::h_prob_parm_device->Y_OH_kernel);
  pp.query("Y_O_kernel",  PeleC::h_prob_parm_device->Y_O_kernel);
  pp.query("Y_H_kernel",  PeleC::h_prob_parm_device->Y_H_kernel);

  // ------------------------------------------------------------------
  // UNITS FIX: inputs are SI meters; PeleC coordinates are CGS (cm).
  // Convert all length scales to cm here so prob.H comparisons match.
  // ------------------------------------------------------------------
  PeleC::h_prob_parm_device->splitter_height *= 100.0;
  PeleC::h_prob_parm_device->kernel_rad      *= 100.0;
  PeleC::h_prob_parm_device->kernel_x0       *= 100.0;
  PeleC::h_prob_parm_device->kernel_y0       *= 100.0;
  PeleC::h_prob_parm_device->kernel_z0       *= 100.0;

  // Lookup species indices
  amrex::Vector<std::string> sname;
  pele::physics::eos::speciesNames<pele::physics::PhysicsType::eos_type>(sname);
  int iO2 = -1, iN2 = -1, iCH4 = -1, iOH = -1, iO = -1, iH = -1;
  for (int n = 0; n < sname.size(); n++) {
    if (sname[n] == "O2")  iO2 = n;
    if (sname[n] == "N2")  iN2 = n;
    if (sname[n] == "CH4") iCH4 = n;
    if (sname[n] == "OH")  iOH = n;
    if (sname[n] == "O")   iO = n;
    if (sname[n] == "H")   iH = n;
  }
  if (iO2 < 0 || iN2 < 0 || iCH4 < 0) {
    amrex::Abort("O2/N2/CH4 not found in mechanism");
  }
  if (iOH < 0 || iO < 0 || iH < 0) {
    amrex::Print() << "WARNING: radical species (OH/O/H) missing; kernel will not be seeded.\n";
  }

  // Air composition (mass fractions)
  PeleC::h_prob_parm_device->Y_air[iO2] = 0.233;
  PeleC::h_prob_parm_device->Y_air[iN2] = 0.767;

  // Premixed CH4-air at given equivalence ratio.
  // Stoichiometric: CH4 + 2(O2 + 3.76 N2) -> CO2 + 2 H2O + 7.52 N2
  // Y_CH4_st = 16 / (16 + 2*32 + 2*3.76*28) = 0.05517
  amrex::Real phi = PeleC::h_prob_parm_device->equiv_ratio;
  amrex::Real Y_CH4_st = 0.05517;
  amrex::Real Y_CH4 = phi * Y_CH4_st / (1.0 + (phi - 1.0) * Y_CH4_st);
  amrex::Real Y_air_frac = 1.0 - Y_CH4;
  PeleC::h_prob_parm_device->Y_premix[iCH4] = Y_CH4;
  PeleC::h_prob_parm_device->Y_premix[iO2]  = 0.233 * Y_air_frac;
  PeleC::h_prob_parm_device->Y_premix[iN2]  = 0.767 * Y_air_frac;

  // Hot kernel = post-discharge plasma: radicals + remainder air
  amrex::Real Y_OH = PeleC::h_prob_parm_device->Y_OH_kernel;
  amrex::Real Y_O  = PeleC::h_prob_parm_device->Y_O_kernel;
  amrex::Real Y_H  = PeleC::h_prob_parm_device->Y_H_kernel;
  amrex::Real Y_rad_tot = 0.0;
  if (iOH >= 0) { PeleC::h_prob_parm_device->Y_kernel[iOH] = Y_OH; Y_rad_tot += Y_OH; }
  if (iO  >= 0) { PeleC::h_prob_parm_device->Y_kernel[iO]  = Y_O;  Y_rad_tot += Y_O; }
  if (iH  >= 0) { PeleC::h_prob_parm_device->Y_kernel[iH]  = Y_H;  Y_rad_tot += Y_H; }
  amrex::Real Y_air_rem = 1.0 - Y_rad_tot;
  PeleC::h_prob_parm_device->Y_kernel[iO2] = 0.233 * Y_air_rem;
  PeleC::h_prob_parm_device->Y_kernel[iN2] = 0.767 * Y_air_rem;

  amrex::Print() << "IgnitionKernel setup:\n"
                 << "  P_mean         = " << PeleC::h_prob_parm_device->P_mean       << " Pa\n"
                 << "  T_crossflow    = " << PeleC::h_prob_parm_device->T_crossflow  << " K\n"
                 << "  T_kernel       = " << PeleC::h_prob_parm_device->T_kernel     << " K\n"
                 << "  splitter_h (cm)= " << PeleC::h_prob_parm_device->splitter_height << "\n"
                 << "  kernel_x0 (cm) = " << PeleC::h_prob_parm_device->kernel_x0    << "\n"
                 << "  kernel_y0 (cm) = " << PeleC::h_prob_parm_device->kernel_y0    << "\n"
                 << "  kernel_z0 (cm) = " << PeleC::h_prob_parm_device->kernel_z0    << "\n"
                 << "  kernel_rad (cm)= " << PeleC::h_prob_parm_device->kernel_rad   << "\n"
                 << "  equiv_ratio    = " << PeleC::h_prob_parm_device->equiv_ratio  << "\n"
                 << "  Y_CH4 (premix) = " << Y_CH4 << "\n"
                 << "  Y_OH/O/H kern  = " << Y_OH << " / " << Y_O << " / " << Y_H << "\n";
}
}

void PeleC::problem_post_timestep() {}
void PeleC::problem_post_init() {}
void PeleC::problem_post_restart() {}

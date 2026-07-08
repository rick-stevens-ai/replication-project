#!/usr/bin/env python3
"""
Drift-Flux Particle Transport Model
Replication of Chen, Yu & Lai (2006), Atmospheric Environment 40, 357-367

This script:
1. Reads steady-state airflow solution from OpenFOAM
2. Solves transient particle transport with gravitational settling
3. Applies Lai & Nazaroff (2000) wall deposition boundary conditions
4. Outputs concentration fields for post-processing

Can also run standalone with a simplified analytical flow field for testing.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
import os
import sys

# Physical constants
K_BOLTZMANN = 1.38e-23     # J/K
G = 9.81                    # m/s^2
T_AIR = 293.0              # K (20 C)
RHO_AIR = 1.205            # kg/m^3
MU_AIR = 1.81e-5           # Pa.s
NU_AIR = MU_AIR / RHO_AIR  # m^2/s (kinematic viscosity)
LAMBDA_AIR = 6.6e-8        # m (mean free path)
RHO_PARTICLE = 1400.0      # kg/m^3

# Room geometry
LX, LY, LZ = 0.8, 0.4, 0.4  # m

# Grid
NX, NY, NZ = 40, 20, 20

# Inlet/outlet
INLET_CENTER = (0.0, 0.2, 0.36)
OUTLET_CENTER = (0.8, 0.2, 0.04)
INLET_SIZE = (0.04, 0.04)  # y x z


@dataclass
class ParticleProperties:
    """Properties for a single particle size group."""
    dp: float           # diameter (m)
    Cc: float           # Cunningham slip correction
    vs: float           # settling velocity (m/s)
    D_brown: float      # Brownian diffusion coefficient (m^2/s)
    tau_p: float        # relaxation time (s)

    @classmethod
    def compute(cls, dp_um: float) -> 'ParticleProperties':
        """Compute particle properties from diameter in micrometers."""
        dp = dp_um * 1e-6  # convert to meters

        # Cunningham slip correction
        Kn = 2 * LAMBDA_AIR / dp
        Cc = 1 + Kn * (2.514 + 0.800 * np.exp(-0.55 / Kn))

        # Relaxation time
        tau_p = RHO_PARTICLE * dp**2 * Cc / (18 * MU_AIR)

        # Settling velocity (Stokes)
        vs = tau_p * G

        # Brownian diffusion coefficient
        D_brown = K_BOLTZMANN * T_AIR * Cc / (3 * np.pi * MU_AIR * dp)

        return cls(dp=dp, Cc=Cc, vs=vs, D_brown=D_brown, tau_p=tau_p)


def compute_all_particle_properties():
    """Compute properties for all 10 particle sizes."""
    sizes_um = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    props = []
    for dp_um in sizes_um:
        p = ParticleProperties.compute(dp_um)
        props.append(p)
        print(f"dp={dp_um:6.2f} um: Cc={p.Cc:.3f}, vs={p.vs:.3e} m/s, "
              f"D={p.D_brown:.3e} m^2/s, tau_p={p.tau_p:.3e} s")
    return sizes_um, props


def lai_nazaroff_deposition_velocity(dp_um: float, u_star: float,
                                      orientation: str = 'floor') -> float:
    """
    Compute particle deposition velocity using Lai & Nazaroff (2000) model.

    Parameters:
        dp_um: particle diameter in micrometers
        u_star: friction velocity (m/s)
        orientation: 'floor', 'ceiling', or 'vertical'

    Returns:
        vd: deposition velocity (m/s)

    Reference: Lai, A.C.K., Nazaroff, W.W. (2000).
    Modeling indoor particle deposition from turbulent flow onto smooth surfaces.
    J. Aerosol Sci. 31(4), 463-476.
    """
    pp = ParticleProperties.compute(dp_um)

    # Dimensionless particle relaxation time
    tau_plus = pp.tau_p * u_star**2 / NU_AIR

    # Dimensionless settling velocity
    vs_plus = pp.vs / u_star

    # Schmidt number
    Sc = NU_AIR / pp.D_brown

    # Dimensionless diffusion coefficient
    # D_plus = D / nu = 1/Sc

    # The Lai-Nazaroff model integrates the concentration equation
    # through the boundary layer with a turbulent diffusivity profile
    # fitted from DNS data (Kim et al. 1987)

    # Simplified implementation using the three-layer model:
    # Layer 1: viscous sublayer (y+ < 0.5) - molecular diffusion only
    # Layer 2: buffer layer (0.5 < y+ < 5.0) - linear turbulent diffusivity
    # Layer 3: turbulent layer (y+ > 5.0) - quadratic turbulent diffusivity

    # Resistance integral (dimensionless)
    # R = integral from 0 to y+_edge of dy+ / (D/nu + ep/nu)

    # For smooth surfaces, the deposition velocity is:
    # vd+ = 1 / (R + 1/vs+ correction)

    # Numerical integration through the boundary layer
    n_points = 10000
    y_plus_max = 100.0  # outer edge of boundary layer
    dy_plus = y_plus_max / n_points

    R = 0.0
    for i in range(n_points):
        y_plus = (i + 0.5) * dy_plus

        # Turbulent diffusivity profile from DNS (Kim et al. 1987)
        # ep/nu follows a cubic profile near the wall
        if y_plus < 0.5:
            ep_plus = 0.0  # viscous sublayer
        elif y_plus < 5.0:
            # Buffer: ep/nu = (y+/A)^3, A ~ 14.5 (from DNS)
            ep_plus = (y_plus / 14.5)**3
        else:
            # Log layer: ep/nu = kappa * y+ - 1
            # von Karman constant kappa = 0.4
            ep_plus = 0.4 * y_plus - 1.0

        # Total dimensionless diffusivity
        D_total_plus = 1.0 / Sc + ep_plus

        # Gravitational correction for floor/ceiling
        if orientation == 'floor':
            # gravity aids deposition
            R += dy_plus / D_total_plus
        elif orientation == 'ceiling':
            R += dy_plus / D_total_plus
        else:  # vertical
            R += dy_plus / D_total_plus

    # Deposition velocity
    if orientation == 'floor':
        # Floor: gravity assists deposition
        vd_plus = pp.vs / u_star + 1.0 / R
    elif orientation == 'ceiling':
        # Ceiling: gravity opposes deposition
        vs_p = pp.vs / u_star
        if vs_p * R > 50:  # avoid overflow
            vd_plus = 1.0 / R
        else:
            vd_plus = vs_p / (np.exp(vs_p * R) - 1.0)
    else:
        # Vertical wall: no gravitational component normal to wall
        vd_plus = 1.0 / R

    vd = vd_plus * u_star
    return vd


class DriftFluxSolver:
    """
    3D finite volume solver for the drift-flux particle transport equation.

    Solves: dC/dt + div[(u + vs)C] = div[(D + ep)*grad(C)]
    with wall deposition BC: J = vd * C_wall_cell
    """

    def __init__(self, nx=NX, ny=NY, nz=NZ):
        self.nx, self.ny, self.nz = nx, ny, nz
        self.dx = LX / nx
        self.dy = LY / ny
        self.dz = LZ / nz

        # Cell centers
        self.xc = np.linspace(self.dx/2, LX - self.dx/2, nx)
        self.yc = np.linspace(self.dy/2, LY - self.dy/2, ny)
        self.zc = np.linspace(self.dz/2, LZ - self.dz/2, nz)

        # Fields (3D arrays indexed [ix, iy, iz])
        self.u = np.zeros((nx, ny, nz))  # x-velocity
        self.v = np.zeros((nx, ny, nz))  # y-velocity
        self.w = np.zeros((nx, ny, nz))  # z-velocity
        self.nut = np.zeros((nx, ny, nz))  # turbulent viscosity
        self.C = np.zeros((nx, ny, nz))  # particle concentration

        # Wall shear stress / friction velocity (for deposition model)
        self.u_star = np.zeros((nx, ny, nz))  # approximate

    def set_flow_field_from_openfoam(self, case_dir: str):
        """Read OpenFOAM solution and map to structured grid."""
        # TODO: implement OpenFOAM field reading
        # For now, use analytical approximation
        raise NotImplementedError("OpenFOAM field reading not yet implemented")

    def set_analytical_flow_field(self, u_inlet: float = 0.225):
        """
        Set up an approximate recirculating flow field for testing.
        This is a placeholder - the real simulation should use OpenFOAM.
        """
        print(f"Setting up analytical flow field with u_inlet={u_inlet} m/s")

        # Identify inlet/outlet cells
        inlet_y_range = (0.18, 0.22)
        inlet_z_range = (0.34, 0.38)
        outlet_y_range = (0.18, 0.22)
        outlet_z_range = (0.02, 0.06)

        # Simple jet + recirculation model
        # The inlet jet creates a primary circulation cell
        for ix in range(self.nx):
            for iy in range(self.ny):
                for iz in range(self.nz):
                    x = self.xc[ix]
                    y = self.yc[iy]
                    z = self.zc[iz]

                    # Distance from jet centerline
                    dy_jet = y - 0.2
                    dz_jet = z - 0.36

                    # Jet half-width grows with x
                    jet_width = 0.02 + 0.15 * x  # spreading

                    # Jet velocity (Gaussian profile, decaying)
                    r_jet = np.sqrt(dy_jet**2 + dz_jet**2)
                    u_jet = u_inlet * np.exp(-2 * (r_jet / jet_width)**2) * \
                            np.exp(-0.5 * x / LX)

                    # Recirculation (return flow along bottom)
                    z_norm = z / LZ
                    x_norm = x / LX
                    u_recirc = -0.3 * u_inlet * np.sin(np.pi * x_norm) * \
                               (1 - z_norm) * np.exp(-3 * z_norm)

                    self.u[ix, iy, iz] = u_jet + u_recirc

                    # Vertical component (continuity-driven)
                    self.w[ix, iy, iz] = -0.1 * u_inlet * \
                        np.sin(np.pi * x_norm) * np.cos(np.pi * z_norm)

        # Turbulent viscosity (rough estimate)
        # nut ~ 0.09 * k^2/epsilon ~ 5-50 * nu for indoor flows
        self.nut[:] = 10 * NU_AIR  # placeholder

        # Friction velocity estimate
        self.u_star[:] = 0.05 * u_inlet  # rough estimate

    def solve_particle_transport(self, particle: ParticleProperties,
                                  dt: float, t_end: float,
                                  save_interval: float = 60.0,
                                  output_dir: str = None) -> dict:
        """
        Solve transient particle transport equation using explicit FVM.

        Parameters:
            particle: ParticleProperties for this size group
            dt: time step (s)
            t_end: end time (s)
            save_interval: save concentration field every N seconds
            output_dir: directory to save outputs

        Returns:
            dict with time series of CV, saved fields, etc.
        """
        C = np.zeros((self.nx, self.ny, self.nz))
        dx, dy, dz = self.dx, self.dy, self.dz

        # Effective diffusivity = Brownian + turbulent
        D_eff = particle.D_brown + self.nut  # array

        # Settling velocity (downward = negative z)
        vs = particle.vs

        # Precompute deposition velocities for each wall orientation
        dp_um = particle.dp * 1e6
        u_star_mean = np.mean(self.u_star)
        if u_star_mean < 1e-6:
            u_star_mean = 0.01  # minimum

        vd_floor = lai_nazaroff_deposition_velocity(dp_um, u_star_mean, 'floor')
        vd_ceiling = lai_nazaroff_deposition_velocity(dp_um, u_star_mean, 'ceiling')
        vd_vertical = lai_nazaroff_deposition_velocity(dp_um, u_star_mean, 'vertical')

        print(f"  Deposition velocities: floor={vd_floor:.3e}, "
              f"ceiling={vd_ceiling:.3e}, vertical={vd_vertical:.3e} m/s")

        # Inlet cell indices
        inlet_iy = [iy for iy in range(self.ny)
                    if 0.18 <= self.yc[iy] <= 0.22]
        inlet_iz = [iz for iz in range(self.nz)
                    if 0.34 <= self.zc[iz] <= 0.38]

        # Time stepping
        n_steps = int(t_end / dt)
        save_step = int(save_interval / dt)

        results = {
            'times': [],
            'cv': [],          # coefficient of variation
            'mean_c': [],      # volume-averaged concentration
            'saved_fields': {}
        }

        print(f"  Solving for dp={dp_um:.2f} um, dt={dt:.4f}s, "
              f"{n_steps} steps, t_end={t_end}s")

        for step in range(1, n_steps + 1):
            t = step * dt
            C_old = C.copy()

            # Interior cells: explicit finite volume update
            for ix in range(self.nx):
                for iy in range(self.ny):
                    for iz in range(self.nz):
                        # Convective fluxes (upwind)
                        # x-direction
                        if ix > 0:
                            u_face = 0.5 * (self.u[ix-1, iy, iz] + self.u[ix, iy, iz])
                            if u_face >= 0:
                                flux_xm = u_face * C_old[ix-1, iy, iz]
                            else:
                                flux_xm = u_face * C_old[ix, iy, iz]
                        else:
                            # x=0 boundary (inlet face)
                            if iy in inlet_iy and iz in inlet_iz:
                                flux_xm = self.u[ix, iy, iz] * 1.0  # C_inlet = 1
                            else:
                                flux_xm = 0.0  # wall

                        if ix < self.nx - 1:
                            u_face = 0.5 * (self.u[ix, iy, iz] + self.u[ix+1, iy, iz])
                            if u_face >= 0:
                                flux_xp = u_face * C_old[ix, iy, iz]
                            else:
                                flux_xp = u_face * C_old[ix+1, iy, iz]
                        else:
                            # x=Lx boundary (outlet or wall)
                            outlet_iy = [j for j in range(self.ny) if 0.18 <= self.yc[j] <= 0.22]
                            outlet_iz = [k for k in range(self.nz) if 0.02 <= self.zc[k] <= 0.06]
                            if iy in outlet_iy and iz in outlet_iz:
                                flux_xp = max(0, self.u[ix, iy, iz]) * C_old[ix, iy, iz]
                            else:
                                flux_xp = 0.0  # wall

                        # y-direction
                        if iy > 0:
                            v_face = 0.5 * (self.v[ix, iy-1, iz] + self.v[ix, iy, iz])
                            if v_face >= 0:
                                flux_ym = v_face * C_old[ix, iy-1, iz]
                            else:
                                flux_ym = v_face * C_old[ix, iy, iz]
                        else:
                            flux_ym = 0.0  # wall

                        if iy < self.ny - 1:
                            v_face = 0.5 * (self.v[ix, iy, iz] + self.v[ix, iy+1, iz])
                            if v_face >= 0:
                                flux_yp = v_face * C_old[ix, iy, iz]
                            else:
                                flux_yp = v_face * C_old[ix, iy+1, iz]
                        else:
                            flux_yp = 0.0  # wall

                        # z-direction (includes settling velocity)
                        w_total = self.w[ix, iy, iz] - vs  # settling is downward

                        if iz > 0:
                            w_face = 0.5 * (self.w[ix, iy, iz-1] + self.w[ix, iy, iz]) - vs
                            if w_face >= 0:
                                flux_zm = w_face * C_old[ix, iy, iz-1]
                            else:
                                flux_zm = w_face * C_old[ix, iy, iz]
                        else:
                            # Floor: deposition removes particles
                            flux_zm = 0.0  # handled by deposition term

                        if iz < self.nz - 1:
                            w_face = 0.5 * (self.w[ix, iy, iz] + self.w[ix, iy, iz+1]) - vs
                            if w_face >= 0:
                                flux_zp = w_face * C_old[ix, iy, iz]
                            else:
                                flux_zp = w_face * C_old[ix, iy+1, iz] if iy+1 < self.ny else 0
                        else:
                            flux_zp = 0.0  # ceiling

                        # Net convective flux
                        conv = (flux_xp - flux_xm) / dx + \
                               (flux_yp - flux_ym) / dy + \
                               (flux_zp - flux_zm) / dz

                        # Diffusive fluxes (central differencing)
                        D_here = D_eff[ix, iy, iz] if isinstance(D_eff, np.ndarray) else D_eff

                        diff = 0.0
                        # x-direction
                        if ix > 0:
                            diff += D_here * (C_old[ix-1, iy, iz] - C_old[ix, iy, iz]) / dx**2
                        if ix < self.nx - 1:
                            diff += D_here * (C_old[ix+1, iy, iz] - C_old[ix, iy, iz]) / dx**2

                        # y-direction
                        if iy > 0:
                            diff += D_here * (C_old[ix, iy-1, iz] - C_old[ix, iy, iz]) / dy**2
                        if iy < self.ny - 1:
                            diff += D_here * (C_old[ix, iy+1, iz] - C_old[ix, iy, iz]) / dy**2

                        # z-direction
                        if iz > 0:
                            diff += D_here * (C_old[ix, iy, iz-1] - C_old[ix, iy, iz]) / dz**2
                        if iz < self.nz - 1:
                            diff += D_here * (C_old[ix, iy, iz+1] - C_old[ix, iy, iz]) / dz**2

                        # Wall deposition sink terms
                        dep = 0.0
                        if iz == 0:  # floor cell
                            dep += vd_floor * C_old[ix, iy, iz] / dz
                        if iz == self.nz - 1:  # ceiling cell
                            dep += vd_ceiling * C_old[ix, iy, iz] / dz
                        if iy == 0 or iy == self.ny - 1:  # side walls
                            dep += vd_vertical * C_old[ix, iy, iz] / dy
                        if ix == 0:  # front wall (non-inlet)
                            if not (iy in inlet_iy and iz in inlet_iz):
                                dep += vd_vertical * C_old[ix, iy, iz] / dx
                        if ix == self.nx - 1:  # back wall (non-outlet)
                            outlet_iy = [j for j in range(self.ny) if 0.18 <= self.yc[j] <= 0.22]
                            outlet_iz = [k for k in range(self.nz) if 0.02 <= self.zc[k] <= 0.06]
                            if not (iy in outlet_iy and iz in outlet_iz):
                                dep += vd_vertical * C_old[ix, iy, iz] / dx

                        # Update concentration (explicit Euler)
                        C[ix, iy, iz] = C_old[ix, iy, iz] + dt * (-conv + diff - dep)

                        # Clamp to non-negative
                        C[ix, iy, iz] = max(0.0, C[ix, iy, iz])

            # Compute statistics
            if step % save_step == 0 or step == n_steps:
                C_mean = np.mean(C)
                if C_mean > 0:
                    C_std = np.std(C)
                    cv = C_std / C_mean
                else:
                    cv = 1.0

                results['times'].append(t)
                results['cv'].append(cv)
                results['mean_c'].append(C_mean)

                print(f"    t={t:.0f}s: mean(C+)={C_mean:.4f}, CV={cv:.3f}")

                # Save field at key times
                if t in [60, 180, 300, 600, 1200, 1800] or step == n_steps:
                    results['saved_fields'][t] = C.copy()
                    if output_dir:
                        np.save(os.path.join(output_dir, f'C_t{t:.0f}.npy'), C)

        return results


def run_full_simulation(u_inlet: float = 0.225, output_base: str = None):
    """Run the complete drift-flux simulation for all particle sizes."""

    if output_base is None:
        output_base = os.path.join(
            os.path.expanduser('~'),
            'Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles/results'
        )

    case_name = f'case_U{u_inlet}'
    output_dir = os.path.join(output_base, case_name)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print(f"Drift-Flux Particle Transport Simulation")
    print(f"Inlet velocity: {u_inlet} m/s")
    print(f"Output: {output_dir}")
    print("=" * 70)

    # Compute particle properties
    print("\nParticle properties:")
    sizes_um, props = compute_all_particle_properties()

    # Initialize solver
    solver = DriftFluxSolver()

    # Set up flow field
    # TODO: Replace with OpenFOAM field reading
    solver.set_analytical_flow_field(u_inlet)

    # Time step (CFL-limited)
    dx_min = min(solver.dx, solver.dy, solver.dz)
    u_max = max(np.max(np.abs(solver.u)), np.max(np.abs(solver.v)),
                np.max(np.abs(solver.w)), 0.01)
    dt_conv = 0.5 * dx_min / u_max
    dt_diff = 0.25 * dx_min**2 / (np.max(solver.nut) + NU_AIR)
    dt = min(dt_conv, dt_diff, 1.0)
    print(f"\nTime step: dt={dt:.4f}s (CFL conv={dt_conv:.4f}, diff={dt_diff:.4f})")

    # Solve for each particle size
    all_results = {}
    for dp_um, prop in zip(sizes_um, props):
        print(f"\n{'='*50}")
        print(f"Solving for dp = {dp_um} um")
        print(f"{'='*50}")

        size_dir = os.path.join(output_dir, f'dp_{dp_um}um')
        os.makedirs(size_dir, exist_ok=True)

        results = solver.solve_particle_transport(
            particle=prop,
            dt=dt,
            t_end=1800.0,
            save_interval=60.0,
            output_dir=size_dir
        )

        all_results[dp_um] = results

    # Save summary
    summary = {
        'u_inlet': u_inlet,
        'sizes_um': sizes_um,
        'mixing_times': {},
        'final_cv': {},
        'final_mean_c': {}
    }

    for dp_um, results in all_results.items():
        # Find mixing time (CV < 0.1)
        mix_time = None
        for t, cv in zip(results['times'], results['cv']):
            if cv < 0.1:
                mix_time = t
                break
        summary['mixing_times'][str(dp_um)] = mix_time
        summary['final_cv'][str(dp_um)] = results['cv'][-1] if results['cv'] else None
        summary['final_mean_c'][str(dp_um)] = results['mean_c'][-1] if results['mean_c'] else None

    with open(os.path.join(output_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*70}")
    print("SIMULATION COMPLETE")
    print(f"{'='*70}")
    print("\nMixing times (s):")
    for dp_um in sizes_um:
        mt = summary['mixing_times'][str(dp_um)]
        cv = summary['final_cv'][str(dp_um)]
        print(f"  dp={dp_um:6.2f} um: mixing_time={mt}, final CV={cv:.3f}")

    return all_results, summary


if __name__ == '__main__':
    # Default: run Case 1 (0.225 m/s)
    u_inlet = 0.225
    if len(sys.argv) > 1:
        u_inlet = float(sys.argv[1])

    all_results, summary = run_full_simulation(u_inlet)

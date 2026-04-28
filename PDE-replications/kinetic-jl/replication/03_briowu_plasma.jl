#!/usr/bin/env julia
# =============================================================================
# Replication 3: Brio-Wu MHD Shock Tube (Two-Species Plasma Kinetic)
# =============================================================================
# The Brio-Wu problem is a standard MHD test case. Kinetic.jl solves it
# using a two-species (ion + electron) kinetic formulation with the
# BGK collision operator, demonstrating multi-species plasma capability.
#
# Paper: Xiao 2021, "Kinetic.jl: A portable finite volume toolbox..."
# Reference: Brio & Wu (1988), J. Comput. Phys. 75, 400-422
# Example: example/plasma/briowu_1d.jl in Kinetic.jl repository
# =============================================================================

using KitBase
using KitBase.ProgressMeter: @showprogress
using Plots
using Printf

println("="^70)
println("REPLICATION 3: Brio-Wu MHD Shock Tube (Plasma Kinetic)")
println("="^70)

# ---- Setup from config ----
cd(@__DIR__)

# Write the config file
config = """
# Brio-Wu shock tube with 1D settings
matter = plasma
case = brio-wu
space = 1d4f1v
flux = kcu
collision = bgk
nSpecies = 2
interpOrder = 2
limiter = minmod
boundary = extra
cfl = 0.3
maxTime = 0.1

# physical space
x0 = 0
x1 = 1
nx = 200
pMeshType = uniform
nxg = 2

# velocity space
umin = -5
umax = 5
nu = 25
vMeshType = rectangle
nug = 0

# gas
knudsen = 0.000001
mach = 0.0
prandtl = 1
inK = 0

mi = 1
ni = 0.5
me = 0.0005446623
ne = 0.5
lD = 0.01
rL = 0.003

# electromagnetic field
sol = 100
echi = 1
bnu = 1
"""

configfile = joinpath(@__DIR__, "briowu_config.txt")
open(configfile, "w") do io
    print(io, config)
end

println("Initializing Brio-Wu plasma solver...")
ks, ctr, face, t = initialize(configfile)

println("Grid points: $(ks.ps.nx)")
println("Velocity points: $(ks.vs.nu)")
println("Species: ions (mi=$(ks.gas.mi)) + electrons (me=$(ks.gas.me))")
println("Knudsen: $(ks.gas.Kn)")
println("Max time: $(ks.set.maxTime)")

# ---- Time stepping ----
dt = timestep(ks, ctr, t)
nt = Int(floor(ks.set.maxTime / dt)) + 1
res = zeros(5, 2)

println(@sprintf("Time step dt = %.6e", dt))
println("Number of steps: $nt")
println("\nRunning plasma kinetic solver...")

t_start = time()
@showprogress for iter = 1:nt
    reconstruct!(ks, ctr)
    evolve!(ks, ctr, face, dt; mode = :kcu, isPlasma = true)
    update!(ks, ctr, face, dt, res; coll = :bgk, bc = :extra, isMHD = true)
end
t_elapsed = time() - t_start
@printf("Completed in %.2f seconds\n", t_elapsed)

# ---- Extract solution ----
nx = ks.ps.nx
x = [ks.ps.x[i] for i in 1:nx]

# Ion quantities
ρ_i = [ctr[i].prim[1, 1] for i in 1:nx]
u_i = [ctr[i].prim[2, 1] for i in 1:nx]
v_i = [ctr[i].prim[3, 1] for i in 1:nx]
w_i = [ctr[i].prim[4, 1] for i in 1:nx]
T_i = [1.0 / (2.0 * ctr[i].prim[5, 1]) for i in 1:nx]

# Electron quantities
ρ_e = [ctr[i].prim[1, 2] / ks.gas.me for i in 1:nx]  # number density
u_e = [ctr[i].prim[2, 2] for i in 1:nx]
T_e = [ks.gas.me / (2.0 * ctr[i].prim[5, 2]) for i in 1:nx]

# EM fields
By = [ctr[i].B[2] for i in 1:nx]
Ex = [ctr[i].E[1] for i in 1:nx]

# Total density (ions dominate)
ρ_total = ρ_i

println("\n" * "="^50)
println("SOLUTION SUMMARY")
println("="^50)
@printf("Ion density range: [%.4f, %.4f]\n", minimum(ρ_i), maximum(ρ_i))
@printf("Ion velocity range: [%.4f, %.4f]\n", minimum(u_i), maximum(u_i))
@printf("By field range: [%.4f, %.4f]\n", minimum(By), maximum(By))

# ---- Reference MHD solution comparison ----
# The Brio-Wu problem has known wave structure:
# - Fast rarefaction (left-going)
# - Compound wave (slow shock + rarefaction)
# - Contact discontinuity at x=0.5
# - Slow shock (right-going)
# - Fast rarefaction (right-going)
#
# Known reference values for ideal MHD at t=0.1:
# Left state: ρ=1, By=1, p=1
# Right state: ρ=0.125, By=-1, p=0.1
# Post-shock states are well-documented in literature

# Verify key features
println("\n" * "="^50)
println("WAVE STRUCTURE VERIFICATION")
println("="^50)

# Find discontinuities by gradient magnitude
dρ = diff(ρ_i)
sorted_grad = sort(abs.(dρ), rev=true)
println("Top 3 density gradient magnitudes (wave locations):")
for k in 1:min(3, length(sorted_grad))
    idx = findfirst(abs.(dρ) .== sorted_grad[k])
    if idx !== nothing
        @printf("  |dρ/dx| = %.4f at x ≈ %.4f\n", sorted_grad[k], x[idx])
    end
end

# Check boundary states preserved
@printf("\nLeft boundary:  ρ=%.4f (expected 1.0000)\n", ρ_i[1])
@printf("Right boundary: ρ=%.4f (expected 0.1250)\n", ρ_i[end])
@printf("Left By:  %.4f (expected  1.0000)\n", By[1])
@printf("Right By: %.4f (expected -1.0000)\n", By[end])

# Contact discontinuity should be near x=0.5
contact_region = findall(0.45 .< x .< 0.55)
if !isempty(contact_region)
    contact_dρ = maximum(abs.(diff(ρ_i[contact_region])))
    @printf("Contact discontinuity strength (near x=0.5): Δρ ≈ %.4f\n", contact_dρ)
end

# ---- Save Plots ----
outdir = joinpath(@__DIR__, "..", "report", "figures")
mkpath(outdir)

# Ion density
p1 = plot(x, ρ_i, label="Ion density ρᵢ", linewidth=2, color=:blue,
    xlabel="x", ylabel="ρ", title="Brio-Wu: Ion Density (t=0.1)")

# Ion velocity components
p2 = plot(x, u_i, label="uₓ (ion)", linewidth=2, color=:blue,
    xlabel="x", ylabel="velocity", title="Brio-Wu: Ion Velocity (t=0.1)")
plot!(p2, x, v_i, label="uᵧ (ion)", linewidth=2, color=:red, linestyle=:dash)

# Magnetic field By
p3 = plot(x, By, label="By", linewidth=2, color=:purple,
    xlabel="x", ylabel="By", title="Brio-Wu: Magnetic Field By (t=0.1)")

# Ion temperature
p4 = plot(x, T_i, label="Ion temperature", linewidth=2, color=:orange,
    xlabel="x", ylabel="T", title="Brio-Wu: Ion Temperature (t=0.1)")

p_all = plot(p1, p2, p3, p4, layout=(2,2), size=(1000,700),
    plot_title="Brio-Wu MHD Shock Tube via Kinetic.jl (Plasma Kinetic)")
savefig(p_all, joinpath(outdir, "briowu_combined.png"))

# Individual plots
savefig(p1, joinpath(outdir, "briowu_density.png"))
savefig(p2, joinpath(outdir, "briowu_velocity.png"))
savefig(p3, joinpath(outdir, "briowu_By.png"))

# Ion + electron comparison
p_species = plot(x, ρ_i, label="Ion density", linewidth=2,
    xlabel="x", ylabel="density", title="Brio-Wu: Ion vs Electron Density")
plot!(p_species, x, ρ_e, label="Electron number density", linewidth=2, linestyle=:dash)
savefig(p_species, joinpath(outdir, "briowu_species.png"))

println("\nPlots saved to: $outdir")

# Save data
datadir = joinpath(@__DIR__, "data")
mkpath(datadir)
open(joinpath(datadir, "briowu_results.csv"), "w") do io
    println(io, "x,rho_i,u_i,v_i,T_i,rho_e,u_e,T_e,By,Ex")
    for i in 1:nx
        @printf(io, "%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            x[i], ρ_i[i], u_i[i], v_i[i], T_i[i], ρ_e[i], u_e[i], T_e[i], By[i], Ex[i])
    end
end
println("Data saved to: $(joinpath(datadir, "briowu_results.csv"))")

println("\n✓ Brio-Wu plasma replication complete")

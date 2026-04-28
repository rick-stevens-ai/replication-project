#!/usr/bin/env julia
# =============================================================================
# Replication 2: Homogeneous Relaxation — BGK / Shakhov / ES-BGK
# =============================================================================
# Validates the three collision operators in Kinetic.jl by evolving a
# bimodal distribution function toward equilibrium.
#
# This demonstrates the core collision kernel infrastructure of KitBase:
#   - BGK model (Bhatnagar-Gross-Krook)
#   - Shakhov model (corrects Prandtl number)
#   - ES-BGK model (ellipsoidal statistical BGK)
#
# Paper: Xiao 2021, "Kinetic.jl: A portable finite volume toolbox..."
# Example: example/gas/homogeneous.jl in Kinetic.jl repository
# =============================================================================

using KitBase, OrdinaryDiffEq, Plots
using Printf

println("="^70)
println("REPLICATION 2: Homogeneous Relaxation (Collision Operators)")
println("="^70)

# ---- Configuration ----
# Use config_ntuple for a compact setup
set = config_ntuple(u0 = -8, u1 = 8, nu = 80, t1 = 8, nt = 30, Kn = 1)

tspan = (0.0, set.t1)
tsteps = KitBase.linspace(tspan[1], tspan[2], set.nt)
γ = 3.0  # monatomic 1D: γ = (K+3)/(K+1) with K=0 → γ=3
vs = VSpace1D(set.u0, set.u1, set.nu)

# Bimodal initial distribution
f0 = @. 0.5 * (1/π)^0.5 * (exp(-(vs.u - 2)^2) + 0.5 * exp(-(vs.u + 2)^2))

# Compute macroscopic quantities
prim0 = conserve_prim(moments_conserve(f0, vs.u, vs.weights), γ)
M0 = maxwellian(vs.u, prim0)

println(@sprintf("Initial state: ρ=%.4f, u=%.4f, T=%.4f", prim0[1], prim0[2], 1/(2*prim0[3])))
println(@sprintf("Knudsen number: %.2f", set.Kn))
println(@sprintf("γ = %.1f (monatomic 1D)", γ))

# Collision time
mu0 = ref_vhs_vis(set.Kn, set.α, set.ω)
τ0 = mu0 * 2.0 * prim0[end]^0.5 / prim0[1]
println(@sprintf("Collision time τ = %.4f", τ0))

# ---- 1. BGK Model ----
println("\nSolving BGK model...")
t1 = time()
prob_bgk = ODEProblem(bgk_ode!, copy(f0), tspan, [M0, τ0])
sol_bgk = solve(prob_bgk, Tsit5(), saveat=tsteps)
println(@sprintf("  Done in %.2f s, %d time snapshots", time()-t1, length(sol_bgk.t)))

# ---- 2. Shakhov Model ----
println("Solving Shakhov model...")
t2 = time()
q = heat_flux(f0, prim0, vs.u, vs.weights)
S0 = shakhov(vs.u, M0, q, prim0, 2/3)
prob_shakhov = ODEProblem(bgk_ode!, copy(f0), tspan, [M0 .+ S0, τ0])
sol_shakhov = solve(prob_shakhov, Tsit5(), saveat=tsteps)
println(@sprintf("  Done in %.2f s, %d time snapshots", time()-t2, length(sol_shakhov.t)))

# ---- 3. ES-BGK Model ----
println("Solving ES-BGK model...")
t3 = time()
prob_esbgk = ODEProblem(esbgk_ode!, copy(f0), tspan, [vs.u, vs.weights, prim0, 2/3, τ0])
sol_esbgk = solve(prob_esbgk, Tsit5(), saveat=tsteps)
println(@sprintf("  Done in %.2f s, %d time snapshots", time()-t3, length(sol_esbgk.t)))

# ---- Analysis ----
println("\n" * "="^50)
println("ANALYSIS: Relaxation to Maxwellian Equilibrium")
println("="^50)

# Compute H-function (entropy proxy) over time for each model
H_bgk = zeros(length(sol_bgk.t))
H_shakhov = zeros(length(sol_shakhov.t))
H_esbgk = zeros(length(sol_esbgk.t))
L2_to_max_bgk = zeros(length(sol_bgk.t))
L2_to_max_shakhov = zeros(length(sol_shakhov.t))
L2_to_max_esbgk = zeros(length(sol_esbgk.t))

for (i, t) in enumerate(sol_bgk.t)
    f = sol_bgk[i]
    f_pos = max.(f, 1e-30)
    H_bgk[i] = sum(f_pos .* log.(f_pos) .* vs.weights)
    L2_to_max_bgk[i] = sqrt(sum((f .- M0).^2 .* vs.weights))
end
for (i, t) in enumerate(sol_shakhov.t)
    f = sol_shakhov[i]
    f_pos = max.(f, 1e-30)
    H_shakhov[i] = sum(f_pos .* log.(f_pos) .* vs.weights)
    L2_to_max_shakhov[i] = sqrt(sum((f .- M0).^2 .* vs.weights))
end
for (i, t) in enumerate(sol_esbgk.t)
    f = sol_esbgk[i]
    f_pos = max.(f, 1e-30)
    H_esbgk[i] = sum(f_pos .* log.(f_pos) .* vs.weights)
    L2_to_max_esbgk[i] = sqrt(sum((f .- M0).^2 .* vs.weights))
end

println("\nTime    L2(BGK-M)    L2(Shk-M)    L2(ES-M)")
println("-"^55)
for idx in [1, 5, 10, 15, 20, 25, 30]
    if idx <= length(sol_bgk.t)
        @printf("t=%.1f   %.4e   %.4e   %.4e\n", 
            sol_bgk.t[idx], L2_to_max_bgk[idx], L2_to_max_shakhov[idx], L2_to_max_esbgk[idx])
    end
end

# Verify conservation
println("\nConservation check (final state vs initial):")
for (name, sol) in [("BGK", sol_bgk), ("Shakhov", sol_shakhov), ("ES-BGK", sol_esbgk)]
    f_final = sol[end]
    prim_final = conserve_prim(moments_conserve(f_final, vs.u, vs.weights), γ)
    @printf("  %s: ρ=%.6f (err=%.2e), u=%.6f (err=%.2e)\n", 
        name, prim_final[1], abs(prim_final[1]-prim0[1]), 
        prim_final[2], abs(prim_final[2]-prim0[2]))
end

# Verify convergence to Maxwellian
println("\nFinal-state convergence to Maxwellian:")
@printf("  BGK:     L2 = %.4e (should be ~0)\n", L2_to_max_bgk[end])
@printf("  Shakhov: L2 = %.4e (should be ~0)\n", L2_to_max_shakhov[end])
@printf("  ES-BGK:  L2 = %.4e (should be ~0)\n", L2_to_max_esbgk[end])

# ---- Save Plots ----
outdir = joinpath(@__DIR__, "..", "report", "figures")
mkpath(outdir)

# Distribution snapshots
tidx = [1, 8, 15, 30]
labels = [@sprintf("t=%.1f", sol_bgk.t[min(i, length(sol_bgk.t))]) for i in tidx]

p1 = plot(title="BGK Relaxation", xlabel="u", ylabel="f(u)", legend=:topright)
for (j, i) in enumerate(tidx)
    i = min(i, length(sol_bgk.t))
    plot!(p1, vs.u, sol_bgk[i], label=labels[j], linewidth=1.5)
end
plot!(p1, vs.u, M0, label="Maxwellian", linestyle=:dash, linewidth=2, color=:black)

p2 = plot(title="Shakhov Relaxation", xlabel="u", ylabel="f(u)", legend=:topright)
for (j, i) in enumerate(tidx)
    i = min(i, length(sol_shakhov.t))
    plot!(p2, vs.u, sol_shakhov[i], label=labels[j], linewidth=1.5)
end
plot!(p2, vs.u, M0, label="Maxwellian", linestyle=:dash, linewidth=2, color=:black)

p3 = plot(title="ES-BGK Relaxation", xlabel="u", ylabel="f(u)", legend=:topright)
for (j, i) in enumerate(tidx)
    i = min(i, length(sol_esbgk.t))
    plot!(p3, vs.u, sol_esbgk[i], label=labels[j], linewidth=1.5)
end
plot!(p3, vs.u, M0, label="Maxwellian", linestyle=:dash, linewidth=2, color=:black)

# L2 convergence
p4 = plot(sol_bgk.t, L2_to_max_bgk, label="BGK", linewidth=2,
    xlabel="Time", ylabel="L²(f - M)", title="Convergence to Equilibrium",
    yscale=:log10, legend=:topright)
plot!(p4, sol_shakhov.t, L2_to_max_shakhov, label="Shakhov", linewidth=2, linestyle=:dash)
plot!(p4, sol_esbgk.t, L2_to_max_esbgk, label="ES-BGK", linewidth=2, linestyle=:dot)

p_all = plot(p1, p2, p3, p4, layout=(2,2), size=(1000,700),
    plot_title="Homogeneous Relaxation: BGK / Shakhov / ES-BGK")
savefig(p_all, joinpath(outdir, "relaxation_combined.png"))

# Individual plots
savefig(p1, joinpath(outdir, "relaxation_bgk.png"))
savefig(p4, joinpath(outdir, "relaxation_convergence.png"))

println("\nPlots saved to: $outdir")

# Save data
datadir = joinpath(@__DIR__, "data")
mkpath(datadir)
open(joinpath(datadir, "relaxation_convergence.csv"), "w") do io
    println(io, "t,L2_bgk,L2_shakhov,L2_esbgk,H_bgk,H_shakhov,H_esbgk")
    for i in eachindex(sol_bgk.t)
        @printf(io, "%.4f,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e\n",
            sol_bgk.t[i], L2_to_max_bgk[i], L2_to_max_shakhov[i], L2_to_max_esbgk[i],
            H_bgk[i], H_shakhov[i], H_esbgk[i])
    end
end

println("\n✓ Homogeneous relaxation replication complete")

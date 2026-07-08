import time, json, stim, numpy as np
d=100
circ = stim.Circuit.generated("surface_code:rotated_memory_z", rounds=d, distance=d,
    after_clifford_depolarization=0.001, before_measure_flip_probability=0.001,
    after_reset_flip_probability=0.001, before_round_data_depolarization=0.001)
ms=circ.compile_sampler()
ms.sample(shots=1)  # warm reference
res={}
for N in (1000, 4000, 16384):
    # bit-packed to minimize python-side data movement (paper samples in bulk frames)
    t0=time.monotonic(); a=ms.sample(shots=N, bit_packed=True); dt=time.monotonic()-t0
    res[f"{N}_bitpacked"]={"total_s":dt,"shots_per_s":N/dt,"kHz":N/dt/1000,
                           "out_shape":list(a.shape)}
    print(f"N={N:>6} bitpacked {dt:.3f}s -> {N/dt:,.0f} shots/s ({N/dt/1000:.3f} kHz)", flush=True)
json.dump(res, open("results_c1_ratebig.json","w"), indent=2)
print("done", flush=True)

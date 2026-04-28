// wl3_mpi.cpp -- distributed 3-WL (folklore variant) color refinement
//
// 3-WL update rule (folklore / oblivious k-WL with k=3):
//   new_color(u,v,w) = hash( old_color(u,v,w),
//      sorted multiset over x in V of (c(x,v,w), c(u,x,w), c(u,v,x)) )
//
// Distribution strategy: each rank holds the full color array (n^3 uint64 ~
// 8 MB at n=100). Triples are partitioned across ranks for the update step.
// Each rank computes 64-bit signatures for its partition; we Allgatherv the
// signatures, then perform a global canonicalization (sort by signature,
// assign sequential IDs to equivalence classes). Resulting color array is
// fully replicated for the next iteration.
//
// Memory: O(n^3) per rank for colors. At n=100 that is 8 MB. The work per
// iteration is O(n^4) which is the bottleneck distributed here.
//
// Build: mpiicpc -O3 -xHost -qopenmp -std=c++17 wl3_mpi.cpp -o wl3_mpi
// Run:   mpiexec -n 8 ./wl3_mpi --n 60 --m 200 --seed 7 --maxiter 8
//
// Author: Ollie (subagent) for Rick Stevens, 2026-04-28.

#include <mpi.h>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = std::uint64_t;
using u32 = std::uint32_t;

static inline u64 splitmix64(u64 x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}
static inline u64 mix2(u64 a, u64 b) { return splitmix64(a ^ (b + 0x9e3779b97f4a7c15ULL + (a << 6) + (a >> 2))); }

struct Args {
    int n = 60;
    int m = 200;
    int seed = 7;
    int maxiter = 8;
    int verbose = 0;
    const char *out = nullptr;
};

static Args parse_args(int argc, char **argv) {
    Args a;
    for (int i = 1; i < argc; i++) {
        std::string s = argv[i];
        auto next = [&](int &dst) { dst = std::atoi(argv[++i]); };
        auto nexts = [&](const char *&dst) { dst = argv[++i]; };
        if (s == "--n") next(a.n);
        else if (s == "--m") next(a.m);
        else if (s == "--seed") next(a.seed);
        else if (s == "--maxiter") next(a.maxiter);
        else if (s == "--verbose") a.verbose = 1;
        else if (s == "--out") nexts(a.out);
    }
    return a;
}

// Generate Erdos-Renyi-like graph G(n,m): undirected, no self-loops, exactly m edges.
static std::vector<uint8_t> gen_graph(int n, int m, int seed) {
    std::vector<uint8_t> A(static_cast<size_t>(n) * n, 0);
    std::mt19937_64 rng(static_cast<u64>(seed));
    int placed = 0;
    int max_edges = n * (n - 1) / 2;
    if (m > max_edges) m = max_edges;
    while (placed < m) {
        std::uniform_int_distribution<int> d(0, n - 1);
        int u = d(rng), v = d(rng);
        if (u == v) continue;
        size_t a = (size_t)u * n + v;
        if (A[a]) continue;
        A[a] = 1;
        A[(size_t)v * n + u] = 1;
        placed++;
    }
    return A;
}

// Initial 3-WL color = atomic isomorphism type of induced ordered subgraph on (u,v,w):
//   bits encode equalities and edges among components.
static u64 init_color(int u, int v, int w, const uint8_t *A, int n) {
    u64 sig = 0;
    sig |= (u64)(u == v) << 0;
    sig |= (u64)(u == w) << 1;
    sig |= (u64)(v == w) << 2;
    sig |= (u64)A[(size_t)u * n + v] << 3;
    sig |= (u64)A[(size_t)u * n + w] << 4;
    sig |= (u64)A[(size_t)v * n + w] << 5;
    return sig;
}

// 1D triple index: idx = u*n*n + v*n + w  (u,v,w in [0,n))
static inline size_t tidx(int u, int v, int w, int n) {
    return ((size_t)u * n + v) * n + w;
}

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank = 0, nranks = 1;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nranks);

    Args a = parse_args(argc, argv);
    const int n = a.n;
    const size_t N3 = (size_t)n * n * n;

    if (rank == 0) {
        std::printf("[wl3_mpi] n=%d m=%d seed=%d ranks=%d N3=%zu mem_per_rank=%.1f MB\n",
                    n, a.m, a.seed, nranks, N3, (double)(N3 * sizeof(u64)) / (1024.0 * 1024.0));
        std::fflush(stdout);
    }

    // Generate graph (rank 0) and broadcast adjacency.
    std::vector<uint8_t> A((size_t)n * n);
    if (rank == 0) A = gen_graph(n, a.m, a.seed);
    MPI_Bcast(A.data(), (int)A.size(), MPI_UNSIGNED_CHAR, 0, MPI_COMM_WORLD);

    // Partition triples [0, N3) across ranks contiguously.
    std::vector<int> counts(nranks), displs(nranks);
    {
        size_t base = N3 / nranks;
        size_t rem = N3 % nranks;
        size_t off = 0;
        for (int r = 0; r < nranks; r++) {
            size_t c = base + (size_t)((r < (int)rem) ? 1 : 0);
            counts[r] = (int)c;
            displs[r] = (int)off;
            off += c;
        }
    }
    const int my_count = counts[rank];
    const int my_disp = displs[rank];

    // Color arrays, fully replicated.
    std::vector<u64> color(N3);

    // --- Initialization
    auto t_init0 = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for schedule(static)
    for (int u = 0; u < n; u++) {
        for (int v = 0; v < n; v++) {
            for (int w = 0; w < n; w++) {
                color[tidx(u, v, w, n)] = init_color(u, v, w, A.data(), n);
            }
        }
    }
    // Canonicalize initial colors to 0..k-1 globally.
    {
        std::vector<u64> uniq(color);
        std::sort(uniq.begin(), uniq.end());
        uniq.erase(std::unique(uniq.begin(), uniq.end()), uniq.end());
        std::unordered_map<u64, u64> map;
        map.reserve(uniq.size() * 2);
        for (size_t i = 0; i < uniq.size(); i++) map[uniq[i]] = (u64)i;
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < N3; i++) color[i] = map[color[i]];
    }
    auto t_init1 = std::chrono::high_resolution_clock::now();

    if (rank == 0) {
        double ms = std::chrono::duration<double, std::milli>(t_init1 - t_init0).count();
        std::printf("[wl3_mpi] init: %.1f ms\n", ms);
        std::fflush(stdout);
    }

    // --- Iteration
    u64 last_count = 0;
    u64 final_count = 0;
    int converged_iter = -1;
    std::vector<double> iter_times;
    std::vector<double> iter_compute_times;
    std::vector<double> iter_comm_times;

    for (int it = 1; it <= a.maxiter; it++) {
        MPI_Barrier(MPI_COMM_WORLD);
        auto t0 = std::chrono::high_resolution_clock::now();

        // Each rank computes signatures for its triple partition.
        std::vector<u64> local_sig(my_count);

        #pragma omp parallel
        {
            // Per-thread scratch buffer of n triples to sort.
            std::vector<u64> buf((size_t)n);
            #pragma omp for schedule(static)
            for (int i = 0; i < my_count; i++) {
                size_t gi = (size_t)my_disp + (size_t)i;
                int u = (int)(gi / ((size_t)n * n));
                int rem = (int)(gi % ((size_t)n * n));
                int v = rem / n;
                int w = rem % n;

                // For each x in V, mix the three substituted colors into a u64.
                for (int x = 0; x < n; x++) {
                    u64 c1 = color[tidx(x, v, w, n)];
                    u64 c2 = color[tidx(u, x, w, n)];
                    u64 c3 = color[tidx(u, v, x, n)];
                    buf[x] = mix2(mix2(c1, c2), c3);
                }
                // Sort to make multiset canonical.
                std::sort(buf.begin(), buf.end());

                u64 h = color[gi];
                for (int x = 0; x < n; x++) h = mix2(h, buf[x]);
                local_sig[i] = h;
            }
        }

        auto tc = std::chrono::high_resolution_clock::now();

        // Allgatherv signatures.
        std::vector<u64> all_sig(N3);
        MPI_Allgatherv(local_sig.data(), my_count, MPI_UINT64_T,
                       all_sig.data(), counts.data(), displs.data(), MPI_UINT64_T,
                       MPI_COMM_WORLD);

        // Global canonicalization: sort unique signatures, build map, relabel.
        // Done identically on every rank (deterministic, no further comm).
        std::vector<u64> uniq = all_sig;
        std::sort(uniq.begin(), uniq.end());
        uniq.erase(std::unique(uniq.begin(), uniq.end()), uniq.end());
        u64 ncolors = uniq.size();

        // Use binary search instead of unordered_map for deterministic perf.
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < N3; i++) {
            auto it2 = std::lower_bound(uniq.begin(), uniq.end(), all_sig[i]);
            color[i] = (u64)(it2 - uniq.begin());
        }

        auto t1 = std::chrono::high_resolution_clock::now();
        double ms_total = std::chrono::duration<double, std::milli>(t1 - t0).count();
        double ms_comp = std::chrono::duration<double, std::milli>(tc - t0).count();
        double ms_comm = ms_total - ms_comp;
        iter_times.push_back(ms_total);
        iter_compute_times.push_back(ms_comp);
        iter_comm_times.push_back(ms_comm);

        if (rank == 0) {
            std::printf("[wl3_mpi] iter %2d: colors=%llu  total=%.1f ms  compute=%.1f ms  comm=%.1f ms\n",
                        it, (unsigned long long)ncolors, ms_total, ms_comp, ms_comm);
            std::fflush(stdout);
        }
        if (ncolors == last_count) {
            final_count = ncolors;
            converged_iter = it;
            break;
        }
        last_count = ncolors;
        final_count = ncolors;
    }

    if (rank == 0) {
        // Print summary JSON line.
        std::printf("{\"n\":%d,\"m\":%d,\"seed\":%d,\"ranks\":%d,\"colors\":%llu,\"iters_run\":%d,\"converged_iter\":%d",
                    n, a.m, a.seed, nranks, (unsigned long long)final_count,
                    (int)iter_times.size(), converged_iter);
        std::printf(",\"iter_times_ms\":[");
        for (size_t i = 0; i < iter_times.size(); i++) std::printf("%s%.3f", i ? "," : "", iter_times[i]);
        std::printf("],\"iter_compute_ms\":[");
        for (size_t i = 0; i < iter_compute_times.size(); i++) std::printf("%s%.3f", i ? "," : "", iter_compute_times[i]);
        std::printf("],\"iter_comm_ms\":[");
        for (size_t i = 0; i < iter_comm_times.size(); i++) std::printf("%s%.3f", i ? "," : "", iter_comm_times[i]);
        std::printf("]}\n");
        std::fflush(stdout);

        if (a.out) {
            FILE *f = std::fopen(a.out, "a");
            if (f) {
                std::fprintf(f, "{\"n\":%d,\"m\":%d,\"seed\":%d,\"ranks\":%d,\"colors\":%llu,\"iters_run\":%d,\"converged_iter\":%d",
                             n, a.m, a.seed, nranks, (unsigned long long)final_count,
                             (int)iter_times.size(), converged_iter);
                std::fprintf(f, ",\"iter_times_ms\":[");
                for (size_t i = 0; i < iter_times.size(); i++) std::fprintf(f, "%s%.3f", i ? "," : "", iter_times[i]);
                std::fprintf(f, "],\"iter_compute_ms\":[");
                for (size_t i = 0; i < iter_compute_times.size(); i++) std::fprintf(f, "%s%.3f", i ? "," : "", iter_compute_times[i]);
                std::fprintf(f, "],\"iter_comm_ms\":[");
                for (size_t i = 0; i < iter_comm_times.size(); i++) std::fprintf(f, "%s%.3f", i ? "," : "", iter_comm_times[i]);
                std::fprintf(f, "]}\n");
                std::fclose(f);
            }
        }
    }

    MPI_Finalize();
    return 0;
}

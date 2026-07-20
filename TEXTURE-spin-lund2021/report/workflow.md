# Workflow — lund2021 replication

## Method class
Analytic effective-action / linear spin-wave theory (LSWT). CPU-only.

## Pipeline
1. **Acquire/parse.** Read `work/textures-spin-lund2021.txt` (1145 lines) and
   `report/evidence/replication_recipe.json`. Ran `pdftotext -layout` →
   `extraction/_pdftotext.txt` as extraction interim.
2. **Extract physics.** Identified the true claim: this is a *spin-pumping*
   paper, not thermal Hall. The "three spin-wave bands" are the k=0
   uniform-precession resonance modes (Eqs. 15–16, Sec. III), with
   mutually orthogonal x/y/z polarizations. Pulled the kagome Hamiltonian
   (Eq. 14), 120° easy axes, and App. A constants (a1, a2, K1, K2).
3. **Build from scratch** (`work/lund2021_lswt.py`, runner
   `/home/stevens/comfyui-env/bin/python`):
   - (A) Holstein–Primakoff LSWT of the 120° kagome Heisenberg AFM in local
     frames → BdG matrix → Colpa diagonalization (eig of gM) on a 12×12 grid
     + Γ-K-M-Γ path. Checks for the zero-energy flat band.
   - (B) k=0 uniform modes: diagonalize `w^2 = 4 a2 K / a1^2` with
     K=diag(K1,K1,K2); extract frequencies + polarization eigenvectors;
     test orthogonality and the analytic ratio √(K2/K1).
4. **SAVE-EARLY** to `work/lund2021_result.json` (single dump at end of a
   fast-running script).
5. **Compare & score** (see `artifacts_summary.md`).
6. **Package** 8 artifacts; copy result JSON + code to `report/evidence/`.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-spin-lund2021
/home/stevens/comfyui-env/bin/python work/lund2021_lswt.py
```

## Key decisions
- Coarse 12×12 BZ grid — sufficient to establish flatness (std ~1e-8) and
  band ranges; SAVE-EARLY prioritized.
- Set S=a=ℏ=1, J=1, K=0.10, Kz=0.05 as representative; the *ratios* and
  orthogonality (the paper's actual claims) are parameter-independent.

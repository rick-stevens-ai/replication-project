# Failure Analysis

## 1. Target directory did not exist
- **Symptom:** `cd TEXTURE-multipolar-lai2018` failed; no `*multipolar*` or `*lai2018*` dir
  under REPLICATE-PROJECT (only `PDE-lai-*` and dozens of `TEXTURE-{orbital,polar,spin}-*`).
- **Root cause:** the directory was never created; the "dir has paper.pdf + extraction/marker.md"
  premise was false at task start.
- **Fix:** per task rule ("if paper.pdf missing, fetch arxiv.org/abs/1807.09258"), created
  the 8-artifact dir skeleton and fetched `paper.pdf` from arXiv. All writes confined to the
  target dir (WRITE SCOPE respected).

## 2. PDF vision tool unavailable
- **Symptom:** `pdf` tool errored — path not under allowed dir (Dropbox), and after copying
  into workspace, all image/PDF models failed (Anthropic "credit balance too low",
  gemini model unknown, openai PDF-extract disabled).
- **Root cause:** no available PDF-vision backend; Dropbox not in the pdf tool allowlist.
- **Fix:** used `pdftotext` (poppler) to extract raw text (2233 lines) and read it directly.
  Equations rendered as unicode-ish text but were fully legible; all needed operator
  definitions, identities, and matrices were recovered from the Supplemental Material.
- **Cleanup:** removed the temporary workspace copy `_tmp_lai2018.pdf`.

## 3. ED first run hung (dense kron blowup)
- **Symptom:** initial `ed_structure_factor.py` did not finish within ~90 s.
- **Root cause:** built the Hamiltonian and every two-site operator as DENSE 6561x6561
  matrices via repeated `np.kron` of full 3x3 ops for all 64 (i,j) pairs, per q-point —
  O(N^2 * n_q) dense kron products, memory + time blowup.
- **Fix:** rewrote with `scipy.sparse` (csr) throughout, sparse Lanczos `eigsh(k=1,which='SA')`
  for the ground state, and a **one-time** precomputed correlation cache
  `<Si.Sj>, <Qi.Qj>` reused across all q. Runtime dropped to ~7 s for both clusters.

## 4. Positive ground-state energy on 2x4 looked suspicious
- **Symptom:** E0(2x4) = +2.71081 (positive), unlike E0(2x2) = -0.998.
- **Root cause / resolution:** NOT a bug. With K1=1.2 dominating and the positive
  (S.S)^2 biquadratic term, the ground-state energy on a small periodic cluster can be
  positive. Cross-checked eigsh against a full dense `np.linalg.eigvalsh` on the 6561-dim
  matrix: lowest three eigenvalues agree exactly ([2.71081, 3.86936, 3.86936]). Solver
  validated; physics (dominant (pi,pi) quad peak) is robust and matches the paper.

## Lessons
- Always sparse-ify spin-S ED beyond ~6 sites; precompute correlators once.
- When a "given" input dir/file is absent, honor the explicit fallback rule rather than aborting.
- pdftotext is a reliable fallback when PDF-vision models are down.

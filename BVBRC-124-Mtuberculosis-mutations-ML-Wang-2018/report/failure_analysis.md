# Failure analysis — BVBRC-124

Documented per Rick's mandatory failure-learning rule (workspace AGENTS.md): every failure is tuition, log it once, apply forward.

## Failure #1 — Argo `argo:claude-opus-4.8` returned HTTP 502 (transient upstream)

**What happened.** First LLM-judge call to `localhost:44497/v1/chat/completions` with `model=argo:claude-opus-4.8` returned HTTP 502 Bad Gateway. Retried 3× at 5-second intervals — all 502.

**Root cause.** Not this replication's fault: the Argo proxy's upstream Anthropic path was transiently down. A minimal `curl` to `argo:gpt-5.2` on the same proxy at the same time returned HTTP 200. So the proxy itself was up; only the Claude sub-provider was 502ing.

**Fix.** Switched judge model to `argo:gpt-5.2` (also free, also on the same proxy). Judge produced a well-formed JSON verdict in one call. Cost impact: zero (both models are free).

**Lesson for future.** LLM-judge scripts should have a model-fallback list: try Claude first (best JSON compliance) → fall back to GPT-5 series → fall back to Gemini. Attempted here manually; could be automated.

**Prevention.** Add a helper `argo_call(models=[...])` that iterates through a preference list until one returns non-5xx.

## Failure #2 — NaN-vs-0 cast bug wiped every feature (data pipeline)

**What happened.** First run of `auc_replicate.py` reported "0 drugs evaluated" for all 15 drugs. Traceback showed `ValueError: Found array with 0 feature(s) (shape=(1250, 0))` from `SGDClassifier.fit`.

**Root cause.** The authors' allele CSV encodes "strain does not have this allele" as `NaN`, not `0`. My binarisation was:
```python
A_vals = (A.values != 0).astype(np.int8)   # WRONG
```
Under NumPy semantics `NaN != 0` returns `True`, so every cell became `1`. Then the frequency filter `(col_sum >= 5) & (col_sum <= N-5)` removed EVERY column because all sums equaled `N`.

**Fix.** Two lines:
```python
A_vals = np.nan_to_num(A.values, nan=0.0)
A_vals = (A_vals > 0).astype(np.int8)
```
Post-fix, column-sum distribution: min=1, max=1595, mean≈100 — consistent with pan-genome sparsity.

**Debug method that worked.** Loaded the raw matrix directly with pandas and inspected:
```python
V = (A.values != 0).astype(np.int8)
print("V col sums summary: max=", V.sum(axis=0).max(), "mean=", V.sum(axis=0).mean())
# max=1595, mean=1595.0  <-- diagnostic: something's wrong
```
The instant the max == mean == N, you know every column is saturated.

**Lesson for future.** For sparse presence/absence matrices distributed as CSV with `NaN` for absent: NEVER cast with `!= 0` directly. Always `nan_to_num` first, then compare. Also **always log column-sum stats immediately after binarisation** — trivial cost, catches this class of bug instantly.

**Prevention.** Added `log()` line after binarisation in `auc_replicate.py` that prints min/max/mean of column sums. Future forks of this pattern should keep that.

## Failure #3 (near-miss, not actual failure) — assignment title said "Wang-2018" but PMID:30333483 is Kavvas

**What happened.** Wave-brief header:
> `paper id = PMID:30333483` and `title: "Machine learning and structural analysis of Mycobacterium tuberculosis pan-genome…"` — the title matches Kavvas 2018 exactly, but the target dir was named `…Wang-2018`. Two sibling replications BVBRC-25 and BVBRC-90 both correctly named the paper Kavvas.

**Root cause.** Typo in the assignment header. PMID:30333483 resolved via NCBI Eutils returned first author Kavvas, not Wang.

**Fix.** Documented in REPORT.md § header ("Note on assignment"). Kept the target-dir name as assigned (`BVBRC-124-Mtuberculosis-mutations-ML-Wang-2018`) to avoid accidentally clobbering someone else's Wang-2018 assignment.

**Lesson for future.** Always verify PMID → title+authors via NCBI Eutils before starting, especially when the assignment metadata is manually authored.

## Failure #4 (potential, not observed) — near-clobber of sibling completed replications

**What happened.** Two prior fully-complete replications of the same paper exist (BVBRC-25 and BVBRC-90). A naive read of the assignment might have caused me to overwrite one of them or produce a fourth redundant copy.

**Root cause.** Wave brief clearly says "NEVER overwrite completed sibling dirs. Write ONLY inside your target dir." Followed correctly.

**Fix (preventive).** Before writing any file, I:
1. `ls`'d the parent to enumerate prior BVBRC dirs matching the paper.
2. Read each sibling's `brief.md` and claim table.
3. Designed my angle to add previously-untested claims (ML AUC, structural availability), not to duplicate their work.
4. Only wrote inside my assigned `BVBRC-124…` dir. Copied (not moved / not modified) files from sibling `work/data/` directories to avoid touching their state.

**Lesson for future.** When a paper has multiple prior replications, always design an orthogonal angle. The rule "solid where evidence supports it" is better served by extending coverage than by re-doing what's already done.

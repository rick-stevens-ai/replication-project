# HPC Job Submission Checklist

**READ THIS BEFORE EVERY qsub.** No exceptions.

## Pre-Submit Checklist

- [ ] **Checkpoint-restart implemented?** Code must save progress to a file and resume on restart. SIGTERM handler saves state. Script is idempotent.
- [ ] **Runtime estimated?** Measure or extrapolate from prior runs. Request `predicted × 1.3 + 10min`. Never blindly request max walltime.
- [ ] **Right queue?** debug (≤1h, quick tests only), preemptable (≤72h, real work), prod (≥10 nodes only)
- [ ] **PBS -r y set?** (rerunnable flag)
- [ ] **Signal forwarding?** Shell trap forwards SIGTERM/SIGUSR1 to Python PID
- [ ] **Starting state cached?** Expensive setup (equilibration, structure generation) saved to disk and reloaded on restart

## Pattern

```python
signal.signal(signal.SIGTERM, save_checkpoint_and_exit)
# On start: load checkpoint if exists, skip completed work
# After each unit of work: update checkpoint
# On resubmit: same script, same args — resumes automatically
```

## Rick's Rule

> Any job that *could* timeout or be preempted MUST save progress and resume on resubmit. Same failure twice is unacceptable.

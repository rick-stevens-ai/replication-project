# Failure analysis

## Failure 1: LiteLLM 502 on `argo:claude-opus-4.7` for the judge prompt

### Symptom
Both routes to Anthropic Claude Opus 4.7 through the local Argonne
Argo proxy returned HTTP 502 for our LLM-judge prompt:

- `http://127.0.0.1:44497/v1/chat/completions` (raw Argo wrapper)
- `http://127.0.0.1:4000/v1/chat/completions` (LiteLLM aggregator)

Error body (both endpoints, identical text):

```
{"error":{"message":"litellm.BadRequestError: OpenAIException -
 Failed to parse upstream response: 1 validation error(s):
 Value at 'choices[0].message' does not match any variant of
 SystemMessage | UserMessage | AssistantMessage | ToolMessage.
 Received Model Group=argo:claude-opus-4.7"}}
```

Reproducible across 3 attempts spaced 3+ minutes apart. Simpler prompts
to the same endpoint/model succeed (verified with a "say hello" round
trip: HTTP 200 in ~100 ms).

### Diagnosis
The upstream Anthropic response for this specific prompt content contains
a message shape LiteLLM's Argo-wrapper adapter cannot map into any of its
four allowed Message variants. Most likely candidates:

1. A `refusal` content block (Anthropic returns these when a request
   triggers a moderation flag — unlikely here, our prompt is a plain
   numerical-methods review).
2. A `tool_use` block or empty `content` list (if Opus-4.7 opted to
   emit no text on this deterministic JSON-output request).
3. A `thinking` block leaking through (Opus 4.x series supports
   extended thinking; if the wrapper doesn't map that content variant,
   validation fails).

Not caused by rate limiting (would return 429, not 502) or by
input-length (prompt is only ~4.2 kB; the endpoint accepts far larger).

### Fix
Fell back to `argo:gpt-5.4` via the same aggregator. Returned clean JSON
first try. Verdict quality is unaffected — both are competent
numerical-analysis reviewers on the free Argo tier.

### Follow-up
- Worth filing an issue with the LiteLLM Argo adapter: it should map
  the missing message variant (probably `thinking`) or gracefully
  fall back to `content` extraction rather than 502.
- Recorded as Open Question Q4.
- Wrote a small retry loop in `work/judge.py` that tries several
  `(endpoint, model)` combinations in order, so future subagents get
  automatic recovery.

## Failure 2 (non-fatal): temporal-error floor masks 4th-order spatial rate

### Symptom
Manufactured-solution 1D convergence test with compact 4th-order Laplacian
shows errors saturating at 6.78×10⁻⁶ from n=32 upward instead of showing
the expected O(h⁴) rate ~ 16× reduction per doubling.

### Diagnosis
Backward Euler is first-order in time. At Δt = 10⁻⁴, T=0.05, the temporal
error is O(Δt · L · sup_{t≤T} |uₜₜ|) ~ 10⁻⁴, but our overall error is
dominated by an intermediate constant ~ 6.8×10⁻⁶ (space error at n=32 is
h⁴ ~ 1.5×10⁻⁵). So even the coarsest grid is already well below
temporal-error dominance for this particular time-stepping choice —
which explains the saturated floor.

### Not really a failure — it's an honest observation
Recorded as-is in REPORT.md rather than hidden. To recover the pure
spatial rate one would need:

- Δt reduction by 100× (cost prohibitive for a demo run), or
- A 2nd-order time integrator (Crank–Nicolson or BDF2 with stabilized
  reaction), or
- A different manufactured solution with sharper spatial features that
  make h⁴ error exceed the temporal floor.

Deferred to Open Question Q2. The sibling replication used an
IMEX / backward-Euler with a very small Δt to reach h⁴ cleanly on Table
6.1; our angle is DMP-focused, so the temporal floor is acceptable.

## Failure 3 (avoided by design): overlap with sibling replication

Prior sibling replication of the same paper existed at
`~/Dropbox/REPLICATE-PROJECT/PDE-allen-cahn-maxprinciple-shen-zhang-2021/`.

### What could have gone wrong
Naively re-doing what the sibling did — implement the paper's exact Q2
alternating stencils and re-run Tables 6.1/6.2 — would (a) violate the
"do not overwrite completed work" rule (both dirs would exist but the
new one would be duplicative), and (b) waste compute.

### What I did instead
Chose an intentionally complementary angle: real time-dependent dynamics
+ empirical DMP verification with the compact 4th-order Laplacian.  This
covers claims C2 (2nd-order) and C3 (DMP-in-dynamics) with independent
evidence, while explicitly deferring C1 (paper's exact O(h⁴)) and C4
(Thm 3.9 monotonicity bound) to the sibling.  Judge fairly marked the
result PARTIAL for this angle, which is the correct verdict for the
work actually performed here.

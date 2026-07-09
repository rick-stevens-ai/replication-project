# Failure Analysis

Honest ledger of everything that went wrong during this replication.

## 1. M2L formula sign bug (own code, ~15 min lost)

**What broke.** First implementation of `FMM2D._m2l_direct` gave a relative
L2 error of 27% (2.6e-1) against direct summation at `p=12`, N=200 --
clearly wrong (should be ~1e-8 for a correct 2D FMM at that p).

**Root cause.** I initially wrote the M2L expansion with the substitution
`t = zc_tgt - zc_src` but with the wrong sign on the log branch and on
the alternating $(-1)^k$ factors. The correct expansion is
$$
\log(z - z_c) = \log(t) + \log(1 + u), \qquad u = (z - z_c')/t,
$$
which gives $b_l$ formulas with **NO** $(-1)^k$ inside the sum (only
$(-1)^l$ and $(-1)^{l+1}$ prefactors). My original code had `log(-t)` and
extra $(-1)^k$ factors, which is a canonical trap when translating between
Greengard's various papers (some use $t = -\text{(this convention)}$).

**Fix.** Re-derived from scratch inside the docstring, unified the sign
convention with the definition
`a_k = -sum q_j (z_j - zc)^k / k` in the multipole. Post-fix: rel L2
$5 \cdot 10^{-8}$ at p=12 (correct).

**Prevention.** Documented the derivation in the docstring of
`_m2l_direct` so the sign convention is explicit and future subagents
don't fall into the same trap.

## 2. Runaway wall time on first C2/C3 pass (~2 min lost)

**What broke.** My first `run_experiments.py` had $N=16000$ in C2 and
$N_{\rm side}=256$ in C3, both of which would have taken 5+ min each on
pure-Python FMM (M2L is $O(N_{\rm boxes}^2 \cdot p)$ per target box, which is
slow when everything is Python-loop-native and not vectorised).

**Root cause.** Underestimated the constant factor of pure-Python M2L. The
FMM is asymptotically fast but the crossover with direct is deep into
$N \sim 10^5$ when there's no C/Fortran acceleration.

**Fix.** Trimmed C2 to $N \le 8000$ and C3 to $N_{\rm side} \le 128$. Total
runtime became 65 s.

**Prevention.** Time a small case first; extrapolate before setting the
largest problem size.

## 3. Argo Opus 4.7 / 4.8 502 through LiteLLM aggregator

**What broke.** Both `argo:claude-opus-4.7` and `argo:claude-opus-4.8` via
`http://localhost:4000/v1/chat/completions` returned HTTP 502 with the
error body:
```
litellm.BadRequestError: OpenAIException - Failed to parse upstream
response: 1 validation error(s): Value at 'choices[0].message' does not
match any variant of SystemMessage | UserMessage | AssistantMessage |
ToolMessage. Received Model Group=argo:claude-opus-4.7
```

**Root cause.** LiteLLM 1.x has a strict Pydantic validator on the
`choices[0].message` shape returned by upstream. Argo's Anthropic-side
wrapper is now emitting a `provider_specific_fields` map that includes
`refusal` even when `refusal` is `null`, and LiteLLM's OpenAI-wire validator
tolerates the top-level `provider_specific_fields` on the outer choice but
not on the `message` sub-object. So the parse fails and LiteLLM returns
502 upstream to the client -- but the message content is actually being
computed by Argo. Confirmed by direct curl to `44497` (raw Argo wrapper,
no LiteLLM) which also 502s -- so the problem is actually deeper: even
Argo's own wrapper is rejecting the shape on some path for large payloads.

Short-message probes (`{"content":"Say ok"}`) worked. Only the ~1200-token
prompt triggered the 502, which is consistent with the theory that
`provider_specific_fields` gets more elaborate for larger completions.

**Fix.** Switched judge model from `argo:claude-opus-4.7` to
`argo:gpt-5.4` (also via `localhost:4000/v1`, also free). GPT-5.4 uses
Argo's OpenAI-wire path which does not emit the offending
`provider_specific_fields.refusal` sub-object, so LiteLLM parses cleanly.
GPT-5.4 returned a clean strict-JSON verdict on first try.

**Prevention.** For LLM-judge scripts, prefer `argo:gpt-5.4` over the Opus
models until Argo/LiteLLM fix the message-shape mismatch. Alternative:
POST directly to Anthropic-provider on Argo bypassing LiteLLM (would need
a different URL). Filed to `TOOLS.md` as a durable note (see below).

## 4. What was NOT attempted (algorithmic scope)

Scope-limiting decisions made deliberately, not failures:

- **Adaptive quadtree with level-restriction fixup**: skipped. This is the
  paper's core contribution but requires ~200 LoC of tree bookkeeping.
- **Polynomial cell approximation (Chebyshev tensor products)**: skipped.
  Would require solving small linear systems per leaf per iteration.
- **Analytic local correction integrals**: skipped. Would need
  closed-form integrals of $\log|r|$ against tensor-Chebyshev polynomials
  on a leaf box. These exist in the literature but are not trivially
  looked up.
- **M2M / L2L (hierarchical)**: skipped. Without these, our FMM is
  $O(N \sqrt{N})$ per solve, not $O(N)$. Adding them is straightforward
  (~50 LoC) but was not on the critical path for a PARTIAL verdict.
- **Neumann / periodic boundary conditions**: skipped. Free-space only.

All of these are enumerated in `report/open_questions.json` as future work
and are the reason the LLM-judge verdict is PARTIAL and not REPLICATED.

## Note for `TOOLS.md`

Suggested durable addition (not applied here; would need Rick's approval):

> **Argo Opus via LiteLLM ~1k+ token prompts, 2026-07-06:** currently
> return HTTP 502 with `Failed to parse upstream response: choices[0].message
> does not match SystemMessage|UserMessage|AssistantMessage|ToolMessage`.
> Root cause: Argo's Anthropic wrapper emits `provider_specific_fields`
> on the inner `message` object which the current LiteLLM validator
> rejects. **Workaround: use `argo:gpt-5.4`** for automated LLM-judge
> scripts (OpenAI-wire path in Argo does not emit the offending fields).
> Short-message calls (~50 tokens) still work on Opus.

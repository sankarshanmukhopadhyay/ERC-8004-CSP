# Conformance Checklist

## L1 — Integrity-aware

| Area | Check | Pass criteria |
|---|---|---|
| Fetch | Safe-fetch sandbox | Timeouts, size caps, media-type enforcement, isolated retrieval |
| Integrity | Anchoring classification | Content is classified as anchored, unanchored, mismatch, unavailable, or malformed |
| UX | Control change | Transfers trigger a prominent control-change banner |
| UX | Wallet binding | `agentWallet` is explicit as current, cleared, or stale |
| Safety | `data:` URI policy | Only allowlisted inert media types are accepted |

## L2 — Sybil-aware reputation

| Area | Check | Pass criteria |
|---|---|---|
| Reputation | Weighting policy | Default weights exist, are disclosed, and are inspectable |
| Spam | Rate limits | Bursts do not degrade UX or indexer stability |
| Responses | Gating | `appendResponse()` is policy-gated and typed correctly |
| Revocation | Transparency | Revoked feedback remains visible as revoked |
| Continuity | `registrations[]` cross-check | Mismatches are surfaced and policy-handled |

## L3 — Validation-meaningful

| Area | Check | Pass criteria |
|---|---|---|
| Validators | Policy | Validator set, methodology, and weights are published |
| Semantics | Scope | Display includes validator, method, scope, freshness, and request linkage |
| Finality | Deterministic | Conflicts and progressive states resolve by explicit rule |
| Drift | Revalidation | Material `agentURI` changes stale dependent validations |
| Freshness | Window | Expired validations are marked expired or stale |

## L4 — Economically secured

| Area | Check | Pass criteria |
|---|---|---|
| Economics | External protocol | Claims are backed by staking, slashing, bonds, or insurance |
| Disclosures | Dependencies | User-visible dependency disclosure is present and accurate |

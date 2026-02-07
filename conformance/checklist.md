# Conformance Checklist

## L1 — Integrity-checked

| Area | Check | Pass criteria |
|---|---|---|
| Fetch | Safe-fetch sandbox | Timeouts + size caps + content-type enforcement |
| Verify | Hash verification | No content displayed/used unless hash matches |
| UX | Control change | Transfers trigger a prominent banner |
| UX | Wallet binding | `agentWallet` state is explicit |

## L2 — Sybil-aware reputation

| Area | Check | Pass criteria |
|---|---|---|
| Reputation | Weighting policy | Default weights exist and are disclosed |
| Spam | Rate limits | Bursts do not degrade UX |
| Responses | Gating | `appendResponse` is gated by policy |
| Revocation | Transparency | Revoked feedback visible as revoked |

## L3 — Validation-meaningful

| Area | Check | Pass criteria |
|---|---|---|
| Validators | Policy | Validator set + methodology published |
| Semantics | Scope | Badge includes scope/method/freshness |
| Finality | Deterministic | Conflicts resolved by explicit rule |
| Freshness | Window | Expired validations marked expired |

## L4 — Economically secured

| Area | Check | Pass criteria |
|---|---|---|
| Economics | External protocol | Claims backed by staking/slashing/insurance |
| Disclosures | Dependencies | User-visible dependency disclosure |

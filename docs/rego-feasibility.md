# Rego policy-engine feasibility for ERC-8004 CSP

**Decision:** suitable for a bounded, optional policy-decision prototype; **not implemented** by this document.

The existing `policy/policy.schema.json` defines CSP consumer configuration. It does not evaluate live evidence. [Open Policy Agent (OPA)](https://www.openpolicyagent.org/docs) and Rego can provide deterministic consumer policy decisions over a normalized evidence snapshot without replacing ERC-8004 registries or declaring delegated authorization.

## Ownership and trust boundaries

1. **Upstream registries:** authoritative for chain-recorded identity, reputation, and validation state within their supported semantics.
2. **Evidence resolver/indexer:** verifies chain, block/finality, signatures or hashes as applicable; retrieves untrusted URI content through safe-fetch; normalizes provenance, freshness and unknown state. It must not call a successful HTTP fetch equivalent to verified trust.
3. **CSP Rego policy:** consumes **validated and provenance-bearing normalized facts** plus an explicitly versioned consumer policy. It returns display/admissibility decisions and reason codes.
4. **Execution authorization:** remains with the relying system's authoritative delegation and runtime enforcement process. A CSP `permit_display` or `admit_validation` decision is **not** `authorize_action`.

OPA does not independently verify Ethereum consensus, ERC-1271 proofs, network safety, signed delegations, or historical on-chain state. Those responsibilities must be fulfilled and evidenced outside Rego. Do not fetch live resources from within policy evaluation.

## Smallest proposed decision contract

Use one consumer operation first: **admit an ERC-8004 validation signal for an identified artifact and scope**. This avoids prematurely implementing ranking, scoring, fetch sandboxing, or broad authorization.

Input should be a schema-validated JSON object containing at least:

- `policy_version` and `evaluation_time` (explicit UTC timestamp; deterministic evaluation);
- `subject`: `agent_registry`, `agent_id`, and current resolved chain-state reference;
- `request`: `request_hash`, requested scope and artifact digest/version;
- `response`: validator address, value (0–100), response chronology, selected policy interpretation, provenance and supersession state;
- `evidence`: integrity result, source verification state, observed/verified times, freshness and conflict state;
- `control`: transfer and relevant `agentURI` drift indicators;
- `consumer_policy`: permitted validators, scopes, response thresholds and freshness rules.

Output should distinguish `admit` (boolean), `status` (`admitted`, `denied`, `indeterminate`) and stable `reason_codes`, with the policy and evidence snapshot identifiers. An indeterminate result is not admitted. No policy decision is an authorization grant.

The existing CSP example policy is **illustrative**, not a trust root. Its example validator address and methodology URI must not be treated as real endorsed validators.

## Required falsification fixtures

| ID | Evidence condition | Expected |
| --- | --- | --- |
| P01 | Correct request, validator, method, artifact, scope, fresh evidence, policy threshold | Admitted for **display** only |
| P02 | Missing `requestHash` binding or incorrect validator | Not admitted |
| P03 | Unknown/unavailable chain verification or absent provenance | Indeterminate; not admitted |
| P04 | Validation older than consumer freshness window | Not admitted |
| P05 | `agentURI` materially changed after evaluated artifact | Not admitted pending reassessment |
| P06 | Identity transfer invalidates relevant continuity assumptions | Not admitted pending reassessment |
| P07 | Conflicting or superseded response under unresolved finality rule | Indeterminate; not admitted |
| P08 | Valid 0–100 response but scope/method does not match | Not admitted |
| P09 | Valid registry presence and reputation score but no delegated authority | No action authorization can be emitted |
| P10 | Input missing a required property, unexpected enum or numeric value outside 0–100 | Reject at input validation boundary |

Use a policy-specific schema, `opa fmt --fail`, `opa check --strict`, and `opa test --fail-on-empty` once code exists. In CI, verify at least one *positive* and multiple *false-success* cases through the actual evaluator entry point, not merely helper tests. Pin OPA tooling; record version and test output. Test a stale indexer snapshot and an explicit reorg/unknown-finality condition.

## Adoption gate

Implement in this repository only if an adopter can pass a canonical input through the evaluator and reproduce a stable reasoned result. Keep the first increment isolated under `policy/rego/` and `conformance/`; do not modify `policy/policy.schema.json` or claim a new conformance level by implication. Define a versioned input/output schema and include an example command before introducing an HTTP sidecar or service.

A later tranche may address reputation weighting, continuity policy or runtime integration after the narrow proof-of-value demonstrates utility. Avoid a new repository: consumer policy is already a CSP responsibility.

## Known limitations

Rego cannot ensure the evidence resolver is honest; test and attest that boundary independently. A successful local policy test does not establish blockchain finality, ecosystem interoperability, validator quality, authorization or independent assurance.

## References

- [OPA documentation](https://www.openpolicyagent.org/docs)
- [OPA policy testing](https://www.openpolicyagent.org/docs/policy-testing)
- [ERC-8004 draft](https://eips.ethereum.org/EIPS/eip-8004)

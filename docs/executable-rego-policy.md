# Executable CSP validation-admission policy

**Status:** experimental consumer-policy evaluator, independent of the published CSP v0.9.1 policy configuration and normative conformance levels.

This prototype evaluates whether an **already verified and normalized ERC-8004 validation response** may be admitted for display by a particular consumer. It does not verify Ethereum state, fetch content, implement a validation registry, derive reputation, authorize agent operations, or certify a system.

## Execution contract

- Input: `policy/rego/input.schema.json` (v1.0.0). A **purpose-bound synthetic** example is in `conformance/rego/admissible.json`.
- Rego module: `policy/rego/validation.rego`, query `data.csp.validation.decision`.
- Output: `policy/rego/output.schema.json` (v1.0.0).
- Runner: `scripts/evaluate_validation.py`.
- Test corpus: `conformance/rego/cases.json`, with canonical input mutations and expected status/reason-code outcomes.
- Paired deliberately defective policy: `conformance/rego/defective.rego`, usable **only** to demonstrate a false-positive admission under missing verification evidence.

All timestamps in the input are explicit Unix seconds UTC. The engine does not read wall-clock time. The `subject`, `request`, `response`, `evidence`, and `control` objects must be produced by a trusted, external evidence-resolution process. Schema validity does not establish their authenticity.

The `consumer_policy.validators` and `methodology_uri` example values are fictional and confer no recognition. Validator qualification, conflict-resolution governance and external data verification remain implementation responsibilities.

## Upstream identifier and commitment adapter

The [ERC-8004 Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry) identifies an agent using the namespace-qualified `agentRegistry` string and `agentId`. The current experimental Rego input instead exposes `subject.chain_id` and `subject.agent_registry` (an EVM address). A trusted resolver **must** verify the full upstream namespace/chain/address relationship before constructing the Rego input. Its `request.request_hash` must be bound to the on-chain KECCAK-256 commitment; the `sha256:` artifact digest in the local input is a *different local identifier* and cannot substitute for an upstream `responseHash` or `feedbackHash`. This adapter and hash verification **are not implemented by the Rego evaluator**.

See [CSP §§2, 6, 9 and 13](../spec/erc-8004-csp.md) and the [upstream traceability matrix](upstream-alignment-2026-11.md).

## Minimal reproduction

Install Python 3.12+, `jsonschema==4.23.0`, and independently obtain and verify [OPA v1.9.0](https://github.com/open-policy-agent/opa/releases/tag/v1.9.0) for your platform. The CI Linux amd64 static artifact is pinned to SHA-256 `66fa66f3b730b2fb086003863428b382b2898d343adb4b5dfab5598b4d739eed` (the hash used by the DTFC OPA experiment).

```sh
python -m pip install 'jsonschema==4.23.0'
export CSP_OPA_BIN=/path/to/verified/opa
$CSP_OPA_BIN check --strict policy/rego/validation.rego
python -m unittest discover -s tests -v
python scripts/evaluate_validation.py --opa "$CSP_OPA_BIN" --input conformance/rego/admissible.json --output /tmp/csp-evaluation.json
```

A successful CLI invocation returns exit code 0 for **any structurally valid policy decision**, including `denied` and `indeterminate`. Invalid input, an undefined/nonconforming output, OPA failure, or an invalid executable must produce a nonzero process exit. Consumers **must** inspect `decision.status` and `decision.admit`, not the shell exit code, for the policy outcome.

The record contains the OPA version and SHA-256, policy digest, canonical input digest, raw output digest, execution time and result. The record is not attested by OPA or by an independent evaluator; it can only support reproducible local testing. Evidence digests establish reproducibility, not truth of the input assertions.

## Decision precedence

1. `indeterminate` if required source verification is absent, finality is unresolved, response is conflicting, the evidence snapshot is stale or temporally inconsistent.
2. Otherwise `denied` if the validator, methodology, scope, request hash, assessed artifact, threshold, content anchor, control continuity or validation freshness violates policy.
3. Otherwise `admitted` **for consumer display only**.

All recognized reasons are emitted deterministically in alphabetical order. An input with simultaneous denial and indeterminate reasons remains **indeterminate** (never admitted); the result preserves all reasons for diagnosis. Unknown fields and unexpected enum values are rejected by the JSON Schema at the runner boundary. No `authorize_action` field can be emitted under the output schema.

## DTFC mapping (informative)

[DTFC](https://github.com/qbf-consulting/digital-trust-failure-corpus) owns generic falsification propositions; CSP owns the domain-specific policy.

| DTFC case | CSP scenario | Meaning of mapping |
| --- | --- | --- |
| DTF-001 | P06 (transfer) | Similar temporal invalidation; **not** a claim that wallet binding alone was delegated authority |
| DTF-010 | P03 (missing verification) | Missing evidence cannot be treated as admission |
| DTF-011 | P12 (stale snapshot) | Unresolved freshness cannot establish an affirmative decision |
| DTF-023 | Future composition fixture | Independent component PASS results cannot establish composition-level assurance without seam obligations; **not yet directly tested** by this narrow evaluator |
| DTF-027 | Runner/CI assurance boundary | Successful CLI execution and schema validation do **not** constitute substantive assurance; this is a documentation-level mapping, **not yet a canonical DTFC execution vector** |

These are **informative proposed mappings**; they are not executed DTFC canonical conformance vectors and do not imply the external corpus has adopted, approved or certified CSP.

The paired test presents identical unverified evidence to the safe and intentionally defective Rego policy; the latter returns a false positive. The integration test checks that the input/engine digests match while the policy digest differs.

## Safety and limitation

The evaluation result is a *derived consumer-policy judgment*. It must not be interpreted as delegated authority, transaction permission, validator certification, or historical truth. The upstream ERC-8004 registries remain authoritative for their own chain semantics. A production system would additionally need authenticated chain-state resolution, reorganization handling, secure fetch and integrity verification, validator identity resolution, artifact binding, revocation handling, policy lifecycle governance, and independent evidence validation.

The working-draft [CSP specification](../spec/erc-8004-csp.md) expands evidence and assurance requirements without changing `policy/policy.schema.json` or CSP L0–L4 level names. Passing these synthetic tests does not establish production readiness or independent assurance.

## Red-team provenance and candidate-policy separation

The [pinned ERC-8004 Draft revision](../spec/upstream-erc8004-pin.json) and [consumer policy v0.10.0 candidate](../policy/policy-v0.10.0.schema.json) are independent of this **experimental Rego runtime input/output contract 1.0.0**. Changes to registry-recognition lists, owner epoch, chain-finality proof, external content byte-verification and validator independence remain **upstream input resolver obligations**, not checks the example Rego has implemented. Consumers MUST NOT infer production L3 or L4 assurance from green OPA execution. The [red-team normalized-evidence harness](../scripts/run_conformance.py) is a distinct synthetic test system, not a new Rego adapter or replacement runtime.

# ERC-8004 CSP v0.10.0 — release notes (DRAFT, NOT PUBLISHED)

**Type:** consumer-security specification working-draft milestone.  
**Upstream:** [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004) (draft); this release does not modify or speak for the upstream ERC.

## What's new

The CSP now specifies consumer behavior with individually identifiable requirements, section-level upstream citations, defined source/evidence/decision boundaries, a cumulative L0–L4 conformance interpretation, and expanded threat/architecture and test material. It distinguishes source integrity, provenance, content truth, reputation selection, validation scope, economic evidence and delegated-action authorization.

## Compatibility implications

This release is a **semantic tightening** of the 0.9.1 working draft. Embedded `data:` bytes are treated as bound to a verified URI observation, not independent external digest verification. The full namespace-qualified `agentRegistry` is distinct from the experimental Rego schema's address-only field. ERC-8004's KECCAK-256 request/feedback/response commitments are distinct from the optional Rego example's local SHA-256 artifact identifier. Adopters who previously collapsed these distinctions should reassess their evidence mappings and consumer-facing claims. Historic results remain identified by the profile version under which they were evaluated.

The existing policy configuration schema **still has version 0.9.1** and is not upgraded by this release. The Rego schema contract **remains 1.0.0** and experimental. The L0–L4 level names remain stable.

## Validation and evidence

The repository contains 24 textual acceptance scenarios; this is **not** evidence that a production consumer passes them. Separate synthetic OPA/Rego fixtures are exercised in CI. Neither the documentation nor green CI provides canonical Ethereum verification, recognized validator selection, delegated-action permission, third-party assessment or certification.

## Known limitations

The ERC-8004 source is still a draft and can change. The consumer profile has no standardized full-stack conformance test suite or independent deployment evidence. External economic security and runtime authorization remain dependent on independently governed mechanisms.

## Release provenance

**Release tag, commit SHA, specific CI runs and publication checks: pending acceptance.** Fill these fields from the final immutable release head; do not copy draft branch results into published evidence.

See [specification](../spec/erc-8004-csp.md), [upstream crosswalk](upstream-alignment-2026-11.md), [conformance checklist](../conformance/checklist.md), and [release assessment](release-assessment-2026-11.md).

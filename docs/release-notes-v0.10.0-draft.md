# ERC-8004 CSP v0.10.0 — release notes (DRAFT, NOT PUBLISHED)

**Type:** consumer-security specification working-draft milestone.  
**Upstream:** [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004) (draft); this release does not modify or speak for the upstream ERC.

## What's new

The CSP now records **105 candidate normative requirement IDs**, a pinned Draft ERC-8004 revision, **47 descriptive acceptance cases**, a separate candidate v0.10.0 consumer-policy schema and bounded synthetic regression vectors. It specifies consumer behavior with individually identifiable requirements, section-level upstream citations, defined source/evidence/decision boundaries, a cumulative L0–L4 conformance interpretation, and expanded threat/architecture and test material. It distinguishes source integrity, provenance, content truth, reputation selection, validation scope, economic evidence and delegated-action authorization.

## Compatibility implications

This release is a **semantic tightening** of the 0.9.1 working draft. Embedded `data:` bytes are treated as bound to a verified URI observation, not independent external digest verification. The full namespace-qualified `agentRegistry` is distinct from the experimental Rego schema's address-only field. ERC-8004's KECCAK-256 request/feedback/response commitments are distinct from the optional Rego example's local SHA-256 artifact identifier. Adopters who previously collapsed these distinctions should reassess their evidence mappings and consumer-facing claims. Historic results remain identified by the profile version under which they were evaluated.

The existing policy configuration schema **still has version 0.9.1** and is not upgraded in-place. An additive **candidate v0.10.0 configuration contract** and example are supplied separately, requiring explicit adoption and independent enforcement. The Rego schema contract **remains 1.0.0** and experimental. The L0–L4 level names remain stable.

## Validation and evidence

The repository contains **47 textual acceptance scenarios**; this is **not** evidence that a production consumer passes them. A bounded subset also runs under the normalized-evidence red-team harness, and the separate synthetic OPA/Rego fixtures are exercised in CI. The harness does not execute live chain, networking, LLM or economic validation. Neither the documentation nor green CI provides canonical Ethereum verification, recognized validator selection, delegated-action permission, third-party assessment or certification.

## Known limitations

The ERC-8004 source is still a draft and can change. The consumer profile has no standardized full-stack conformance test suite or independent deployment evidence. External economic security and runtime authorization remain dependent on independently governed mechanisms.

## Release provenance

**Release tag, commit SHA, specific CI runs and publication checks: pending acceptance.** Fill these fields from the final immutable release head; do not copy draft branch results into published evidence.

See [specification](../spec/erc-8004-csp.md), [upstream crosswalk](upstream-alignment-2026-11.md), [conformance checklist](../conformance/checklist.md), and [release assessment](release-assessment-2026-11.md).

## Red-team security tightening and migration

**BREAKING CHANGE (behavioral, despite compatibility of the legacy JSON schema):** embedded `data:` URI bytes are tied to a verified on-chain URI observation, not to an independently authenticated external digest. Consumers displaying an unqualified anchored-content badge based on the old interpretation must migrate or qualify their display. Additionally, an upstream namespace-qualified `agentRegistry` cannot be replaced without proof by the experimental Rego address field, and upstream `keccak256` commitments are distinct from local `sha256:` evidence identifiers.

Consumers who adopt the new candidate policy configuration must explicitly configure registry/ABI recognition, code changes, finality, owner epochs, verified-byte handling, reviewer selection and validator qualification. **No claim of production conformance follows merely from successful schema validation.** See [finding-by-finding resolution](red-team-resolution-2026-11.md) and [migration/release assessment](release-assessment-2026-11.md).

## Publication and assurance caveat

The working draft may be available through GitHub Pages prior to a tag; its content remains unreleased and subject to change. No independent reviewer evidence, live Ethereum source validation, secure network fetch proof or external economic security is claimed by this package.

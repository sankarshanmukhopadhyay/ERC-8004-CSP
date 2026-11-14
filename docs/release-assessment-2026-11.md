# Release assessment: CSP specification expansion (2026-11-14)

**Decision:** **Release warranted after acceptance and validation**, as a new **CSP v0.10.0 working-draft specification milestone**; **do not tag or publish a release yet** while the revision remains in review.

## Why this is a release-worthy compatibility event

The revised [CSP specification](../spec/erc-8004-csp.md) is not merely an editorial rewrite. It provides explicit requirement identifiers, a section-cited upstream-to-local authority crosswalk, more precise treatment of KECCAK-256 commitments and namespace-qualified identifiers, stronger evidence-state and fail-closed obligations, refined embedded-data URI semantics, detailed lifecycle requirements, and 24 acceptance scenarios. Consumers who used the broader v0.9.1 “cryptographically anchored” label for embedded data URIs, assumed the Rego sample's SHA-256 artifact digest was an ERC commitment, or conflated address-only and namespace-qualified registry identities may need to change displayed claims or mapping logic.

These are **semantic compatibility changes**, even though no published JSON Schema is modified. A silently replaced v0.9.1 specification would be misleading. A new documented version should identify the supersession, preserve the historical tag and state the local consumer obligations unambiguously.

## Proposed release identity

| Dimension | Proposed disposition |
| --- | --- |
| Spec/profile milestone | **v0.10.0** (next working draft after v0.9.1) |
| Prior published baseline | v0.9.1 dated 2026-03-07, retained by tag |
| Normative scope | ERC-8004 **consumer security profile**, not upstream ERC-8004 |
| Policy configuration contract | Existing `policy/policy.schema.json` continues to accept **version 0.9.1** only; no migration of that schema is implied |
| Experimental Rego input/output | Version **1.0.0**, separate from CSP and v0.9.1 policy schema |
| Conformance levels | L0–L4 preserved, with more exact evidence and falsification requirements |
| Independent assurance | **Not claimed** |
| Evidence status | Prose scenarios T01–T24 are not an executed full-stack CTS; Rego integration tests are bounded synthetic local evidence |
| Documentation publication | GitHub Pages derives from `main`; tag contents remain the definitive release snapshot |

A tag `v0.10.0` would version the **specification milestone**. It must not be presented as `policy.schema.json` version 0.10.0 or an independently tested implementation. The different version axes should remain visibly separate.

## Acceptance checks before tagging

- [ ] Specification citations verified against the **current upstream draft**, especially ERC-8004 interface and section references.
- [ ] Stable requirement IDs unique; conformance test IDs unique; all tests and checklist references resolve.
- [ ] Maintainers accept revised **embedded-data URI** and **hash/identifier** semantics as substantive, potentially migration-requiring changes.
- [ ] README, architecture, threat model, upstream crosswalk, conformance guidance, Rego limits and release notes align.
- [ ] Required GitHub Actions checks green on the *intended tag commit*, including documentation Pages publication and Rego conformance.
- [ ] Internal/public documentation links reachable and no misleading claims of external evidence.
- [ ] Version and citation metadata updated for the **specification release only**, with no silent mutation of existing consumer policy JSON contracts.
- [ ] DCO/CLA and contribution controls, if enabled, pass.
- [ ] Human acceptance of the normative interpretation; automated lint and AI-assisted review do not replace it.

## Compatibility and migration advice

Consumers of the released 0.9.1 policy schema need not rewrite configuration files solely because of this spec revision. They do need to reassess the meaning of any current display/assurance claims that (a) collapse embedded URI bytes into verified external anchoring; (b) substitute SHA-256 for KECCAK-256; (c) discard chain namespace; (d) promote missing or stale evidence to positive trust; or (e) infer action authorization from registry signals. Historical conformance claims should retain their evaluated version.

## Release notes

A publication-ready draft is in [v0.10.0 release notes](release-notes-v0.10.0-draft.md). It explicitly distinguishes verified local execution from unimplemented end-to-end assurance and identifies documentation-only and runtime boundaries.

## Current disposition

**Implement as a reviewable PR, validate it, and merge only with accepted normative changes.** The current work does not justify a premature release while the profile interpretation is still under review. Once merged, complete the checklist above and tag v0.10.0. Until then, v0.9.1 remains the last published release.

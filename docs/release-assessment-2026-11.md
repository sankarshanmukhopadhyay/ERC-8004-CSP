# Release decision: ERC-8004 CSP v0.10.0 (14 November 2026)

**Disposition: release warranted as a published working-draft specification milestone.**

The maintainer requested publication after the red-team convergence tranche. This decision authorizes a **versioned working draft**, not an external conformance or production-readiness attestation. The publication workflow is required to verify the exact release-head CI evidence before creating the tag or GitHub Release.

## Scope accepted

The v0.10.0 source records **105 individually indexed consumer requirements**, **47 descriptive acceptance scenarios**, pinned ERC-8004 Draft revision `ethereum/ERCs@503591a6e80e6e1affdd6403341e25269141f046`, **26 author-supplied normalized-evidence test vectors**, bounded Rego/OPA execution, and accompanying architecture, threat, conformance and red-team disposition documentation. These are reproducible *source and local regression* outputs. They do not establish independent verification of an operational CSP consumer.

## Compatibility and breaking changes

**BREAKING CHANGE (semantic):** embedded `data:` URI bytes are bound to the observed on-chain URI snapshot; they are not automatically an independently authenticated external digest. Consumers that previously showed an unqualified external-anchor claim must reclassify or re-evaluate that evidence.

For adopters: retain the full ERC-8004 namespace-qualified registry identity; do not substitute the experimental Rego address-only field for it without a verified adapter. Use ERC-8004 KECCAK-256 for upstream request, feedback and response commitments; local `sha256:` identifiers do not replace them. Reconsider previous-owner reputation and validation, source finality, validator independence and economic effective-time evidence before making strengthened claims.

| Contract or artifact | v0.10.0 release disposition |
| --- | --- |
| CSP normative source | **v0.10.0 published working draft** |
| `policy/policy.schema.json` | **v0.9.1 retained**, backward compatible |
| `policy/policy-v0.10.0.schema.json` | **Candidate**, explicitly adopted and externally enforced |
| Rego input/output contracts | **v1.0.0**, experimental display-admission only |
| Conformance evidence-record/claim schemas | **Candidate illustrative formats** |
| L0–L4 level names | Retained; no automatic implementation conformance |

## Acceptance and evidence

The release workflow uses the validated `main` commit and requires the existing **Pages/traceability** and **OPA/Rego/security** workflows to succeed for that exact SHA before publishing. The GitHub Release body records the immutable source commit, run URLs and a link to the [red-team disposition](red-team-resolution-2026-11.md). Source snapshot and tests are reproducible from the tag. GitHub Pages continues to render the `main` source and is not the immutable release artifact.

**Outstanding independent evidence is not waived:** no live on-chain registry/ABI resolver, full CID/network safe-fetch verifier, agent prompt-injection isolation demonstration, qualified independent validator/TEE/zk verifier, effective economic insurance proof or separately governed action-authority evaluator is represented as completed. They remain evidence obligations for consumers claiming operational CSP conformance. See [Issue #10](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/issues/10).

## Release notes and audit trail

The [published release notes](releases/v0.10.0.md) are the canonical migration and limitation record. The release API supplies tag, source SHA, and the two green CI run identities; do not hard-code unobserved run IDs into this decision document.

**No assertion of independent third-party audit, upstream ERC endorsement, agent authorization, L0–L4 implementation certification, or production interoperability is made.**

# Release assessment: CSP specification expansion (2026-11-14)

**Decision: release not yet warranted.** A **v0.10.0 working-draft specification milestone** is justified because the semantic contract has materially changed, but it should be tagged only after release-level acceptance and validation. The source working draft remains publishable in `main`; **no new release has been tagged**.

## Why this is a release-worthy compatibility event

The [red-team convergence analysis](red-team-resolution-2026-11.md) and revised [CSP specification](../spec/erc-8004-csp.md) establish 105 tracked requirements and 47 descriptive acceptance scenarios (including new positive cases at L0 and L4). This is not merely an editorial rewrite. It provides explicit requirement identifiers, a section-cited upstream-to-local authority crosswalk, more precise treatment of KECCAK-256 commitments and namespace-qualified identifiers, stronger evidence-state and fail-closed obligations, refined embedded-data URI semantics, detailed lifecycle requirements, and 24 acceptance scenarios. Consumers who used the broader v0.9.1 “cryptographically anchored” label for embedded data URIs, assumed the Rego sample's SHA-256 artifact digest was an ERC commitment, or conflated address-only and namespace-qualified registry identities may need to change displayed claims or mapping logic.

These are **semantic compatibility changes**, even though no published JSON Schema is modified. A silently replaced v0.9.1 specification would be misleading. A new documented version should identify the supersession, preserve the historical tag and state the local consumer obligations unambiguously.

## Proposed release identity

| Dimension | Proposed disposition |
| --- | --- |
| Spec/profile milestone | **v0.10.0** (next working draft after v0.9.1) |
| Prior published baseline | v0.9.1 dated 2026-03-07, retained by tag |
| Normative scope | ERC-8004 **consumer security profile**, not upstream ERC-8004 |
| Policy configuration contract | Legacy `policy/policy.schema.json` remains **v0.9.1**. Separate `policy/policy-v0.10.0.schema.json` is a **candidate contract** with its own validated example, not a silent in-place change |
| Experimental Rego input/output | Version **1.0.0**, separate from CSP and v0.9.1 policy schema |
| Conformance levels | L0–L4 preserved, with more exact evidence and falsification requirements |
| Independent assurance | **Not claimed** |
| Evidence status | Prose scenarios T01–T47 are not an executed full-stack CTS; a bounded subset has normalized synthetic evidence. Rego integration tests remain separate bounded synthetic local evidence |
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

**BREAKING CHANGE (semantic, 0.x candidate milestone):** Consumers of the released 0.9.1 policy schema need not rewrite configuration files solely because of this spec revision, but must reassess claims that treated embedded on-chain `data:` bytes as independently digest-authenticated external content. Other behavioral dependencies are recorded in the red-team disposition and migration note below. They do need to reassess the meaning of any current display/assurance claims that (a) collapse embedded URI bytes into verified external anchoring; (b) substitute SHA-256 for KECCAK-256; (c) discard chain namespace; (d) promote missing or stale evidence to positive trust; or (e) infer action authorization from registry signals. Historical conformance claims should retain their evaluated version.

## Release notes

A publication-ready draft is in [v0.10.0 release notes](release-notes-v0.10.0-draft.md). It explicitly distinguishes verified local execution from unimplemented end-to-end assurance and identifies documentation-only and runtime boundaries.

## Current disposition

**The expanded specification is now integrated into `main` as a working draft; the repository and its Pages site do not acquire a new release version by that merge.** Complete the checklist above, obtain the appropriate release-level acceptance of its substantive normative interpretations, and then tag v0.10.0 against the validated source commit. Until then, v0.9.1 remains the last published release.

## Red-team release blockers and acceptance classes

The [candidate conformance claim schema](../schemas/conformance-claim.v0.10.0.schema.json) and [not-assessed example](../examples/conformance-claim.v0.10.0.json) prevent a synthetic unrun claim from being represented as an executed result at the schema boundary. Schema validation still cannot verify the independence or truth of attached evidence.

The issue of a new specification tag is distinct from merging the draft and publishing its source. The [red-team disposition](red-team-resolution-2026-11.md) separates **specified normative controls**, **bounded runnable synthetic checks**, and **real-world evidence not yet supplied by an adopter**. The repository includes no independent proof of canonical Ethereum registry state, secured fetchers, independent validators, model-injection containment, or L4 economic enforceability.

The release head must carry coherent citation and compatibility metadata, a completed source-pin/anchor check, green scenario/schema/Keccak and Rego tests, correct GitHub Pages output, and explicit acceptance of changed normative semantics. **Do not convert unrun T01–T47 descriptive scenarios into passing implementation results.**

### Dependency and migration disposition

- Legacy policy consumers may continue to load `policy/policy.schema.json` version 0.9.1; there is no implicit automatic upgrade.
- A consumer electing to implement candidate 0.10.0 must separately adopt `policy/policy-v0.10.0.schema.json`, configure recognized registry/ABI identity, finality, epoch and source-admission rules, and provide actual enforcement evidence.
- External Rego integrators retain input/output contract 1.0.0 and must supply their own verified namespace/chain/address and Keccak-to-artifact binding adapter; no adapter runtime is provided here.
- Historic CSP claim records remain associated with their original specification and policy versions; claims depending on prior embedded-content interpretation require reassessment before presentation under the new candidate.
- Use the [red-team convergence issue](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/issues/10) for remaining externally dependent acceptance evidence. No completed external conformance is implied by closure of the original #4 alignment issue.

**Release decision:** `release not yet warranted` until the above release acceptance is explicit; **commit-only** publication of the complete working draft is appropriate in the meantime.

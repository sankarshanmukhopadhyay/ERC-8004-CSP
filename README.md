# ERC-8004 Consumer Security Profile (CSP)

A **consumer-side** security profile for **ERC-8004 (Trustless Agents)** implementers: wallets, agent directories, marketplaces, explorers, and indexers.

This repository packages the CSP as:
- A **human-readable profile** with normative **MUST/SHOULD/MAY** language.
- A **machine-readable policy schema** for consumer policy enforcement.
- A **conformance checklist** and **test cases** that can be wired into CI and release gates.
- A **GitHub Actions Pages publication workflow** that builds a navigable, complete repository-content catalogue from tracked source files.

> ERC-8004 is a discovery and signal layer, not a guarantee layer. This CSP defines how to consume those signals without wandering into badge theater.

## Contents

| Path | What it is |
|---|---|
| `spec/erc-8004-csp.md` | Expanded working-draft CSP specification with identified requirements and upstream section citations |
| `policy/policy.schema.json` | JSON Schema for a consumer policy |
| `policy/example-policy.json` | Example consumer policy (L3-oriented baseline) |
| `policy/rego/` | Experimental Rego validation-admission policy and versioned contracts |
| `docs/executable-rego-policy.md` | OPA installation, decision semantics, evidence and DTFC mapping |
| `conformance/rego/` | Synthetic positive and adversarial fixtures |
| `conformance/checklist.md` | Evidence-oriented checklist by conformance level |
| `conformance/requirements.json` | Machine-readable index of 71 normative requirements and scenario coverage |
| `conformance/test-cases.md` | 24 negative, boundary and acceptance scenarios (descriptive; not an executed full-stack CTS) |
| `docs/architecture.md` | Reference architecture for implementers |
| `docs/threat-model.md` | Consumer-focused threat model and attacker playbooks |
| `docs/upstream-alignment-2026-11.md` | Upstream traceability, authority and evidence boundaries |
| `docs/rego-feasibility.md` | Historical Rego feasibility decision and falsification requirements |
| `docs/release-assessment-2026-11.md` | New specification milestone compatibility and release decision |
| `docs/release-notes-v0.10.0-draft.md` | Draft v0.10.0 release notes (not yet published) |
| `.github/workflows/rego-conformance.yml` | Executable Rego conformance checks |
| `.github/workflows/pages.yml` | Full-content GitHub Pages build, validation and deployment |
| `scripts/build_pages.py` | Static site build script |

## Conformance levels

- **L0**: basic parsing only. Suitable for demos.
- **L1**: integrity-aware and safe-fetch capable.
- **L2**: Sybil-aware reputation consumption.
- **L3**: validation-meaningful consumption with deterministic rules.
- **L4**: externally economically secured profile claims.

See the [expanded working-draft specification](spec/erc-8004-csp.md) for the section-cited upstream interface assumptions, identified consumer requirements, evidence states and crosswalk. The L0–L4 labels are preserved; the expanded document is **not yet a tagged new CSP release**.

## Proposed next specification milestone

A substantive revision is being prepared as a **v0.10.0 working-draft candidate**. Its [machine-readable index](conformance/requirements.json) derives 71 normative requirement IDs from the Markdown specification, with descriptive-scenario coverage explicitly separated from executed evidence. It adds detailed consumer evidence and threat requirements, upstream citations, identity/hash semantics and a broader acceptance-case catalogue. The [release assessment](docs/release-assessment-2026-11.md) determines that a new **specification** release is justified after acceptance and validation, since some wording changes are semantically significant. The [draft release notes](docs/release-notes-v0.10.0-draft.md) are not a published release. The last issued CSP tag remains **v0.9.1**.

**Compatibility:** the existing `policy/policy.schema.json` remains version `0.9.1`; the optional Rego input/output schemas remain experimental `1.0.0`. Neither is silently version-bumped by an editorial or normative draft expansion.

## v0.9.1 baseline highlights

- The v0.9.1 baseline grouped content-addressed URIs, embedded `data:` URIs and extension-level digests within its anchoring classification. **The expanded working draft narrows this interpretation:** embedded bytes are tied to the observed on-chain URI but do not independently establish an external digest commitment. Plain HTTPS without a binding digest remains unanchored.
- Added explicit handling for **`agentWallet` freshness**, **post-transfer invalidation**, and **EOA vs ERC-1271 wallet binding semantics**.
- Added **`registrations[]` cross-check requirements** to reduce continuity spoofing across registries and chains.
- Tightened **validation request/response linkage** around `requestHash`, supersession, finality, and drift after `agentURI` changes.
- Added stricter **`data:` URI safety controls** and clearer **`supportedTrust` interpretation**.
- The current repository also includes a full GitHub Actions Pages publication pipeline, added after the v0.9.1 release.

## Quick start

1. Copy `policy/example-policy.json` and tailor it to your consumer risk tolerance.
2. Implement the L1 baseline:
   - safe-fetch sandbox
   - integrity anchoring detection
   - transfer and control-change UX
   - explicit `agentWallet` state handling
3. Add L2 and L3 capabilities:
   - weighting and anomaly controls
   - validator policy and finality rules
   - stale-validation handling on profile drift
4. Run `conformance/checklist.md` and `conformance/test-cases.md` in release gates.

## Experimental executable validation policy

An optional [OPA/Rego validation-admission evaluator](docs/executable-rego-policy.md) consumes externally verified, normalized ERC-8004 evidence and makes an explicit consumer display decision (`admitted`, `denied`, or `indeterminate`). It records deterministic reason codes and reproducible execution digests. It does **not** authorize agent actions or establish on-chain verification, validator qualification, or independent assurance. The implementation is experimental and does not modify the released v0.9.1 normative CSP or its L0–L4 levels.

## Repository status

- Version: **CSP v0.9.1**
- Date: **2026-03-07**
- License: **Apache-2.0**

## GitHub Pages publication

The [public documentation catalogue](https://sankarshanmukhopadhyay.github.io/ERC-8004-CSP/) is generated from tracked files by `scripts/build_pages.py` and published by `.github/workflows/pages.yml` using the GitHub Actions Pages source. It includes a safely rendered or escaped page for every tracked source file, navigable directory indexes, and downloadable original-source copies. Generated `site/` HTML is intentionally excluded to avoid an alternative canonical source.

**Source files in the repository remain authoritative.** GitHub Pages is a derived publication surface, not a separate normative version, certification or conformance claim. The experimental Rego evaluator retains its own limitations.

To reproduce the site locally:

```sh
python -m pip install 'Markdown==3.7' 'bleach==6.2.0'
python scripts/build_pages.py
python -m unittest tests/test_pages.py -v
```

The workflow builds and validates on pull requests and deploys on pushes to `main` or manual dispatch. Any new tracked file is automatically included in the catalogue on the next `main` deployment. Repository settings must retain **Pages → Build and deployment → Source: GitHub Actions**.

## Upstream alignment and executable policy

The [November 2026 upstream mapping](docs/upstream-alignment-2026-11.md) now provides section-level traceability and explicitly distinguishes ERC-8004 namespace-qualified identifiers and KECCAK-256 commitments from local Rego adapter fields and SHA-256 evidence identifiers. The [Rego feasibility assessment](docs/rego-feasibility.md) proposes a narrow optional consumer-decision evaluator with false-success fixtures. **The released v0.9.1 baseline did not include executable Rego; the current repository includes an experimental evaluator without changing that published baseline.** Identity, reputation and validation signals must not be treated as authority to act.

## Upstream references

The CSP is designed against the current draft and adjacent standards listed below:

- ERC-8004: Trustless Agents: `https://eips.ethereum.org/EIPS/eip-8004`
- EIP-712: Typed structured data hashing and signing: `https://eips.ethereum.org/EIPS/eip-712`
- ERC-721: Non-Fungible Token Standard: `https://eips.ethereum.org/EIPS/eip-721`
- ERC-1271: Standard Signature Validation Method for Contracts: `https://eips.ethereum.org/EIPS/eip-1271`
- RFC 2119: `https://www.rfc-editor.org/rfc/rfc2119`
- RFC 8174: `https://www.rfc-editor.org/rfc/rfc8174`

## Contributing

See `CONTRIBUTING.md`. Useful contribution areas include:
- new conformance tests
- validator methodology registries
- policy schema extensions
- implementation notes and interoperability writeups

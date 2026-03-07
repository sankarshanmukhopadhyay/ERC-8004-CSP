# ERC-8004 Consumer Security Profile (CSP)

A **consumer-side** security profile for **ERC-8004 (Trustless Agents)** implementers: wallets, agent directories, marketplaces, explorers, and indexers.

This repository packages the CSP as:
- A **human-readable profile** with normative **MUST/SHOULD/MAY** language.
- A **machine-readable policy schema** for consumer policy enforcement.
- A **conformance checklist** and **test cases** that can be wired into CI and release gates.
- A **GitHub Pages build pipeline** that publishes the profile as a static documentation site.

> ERC-8004 is a discovery and signal layer, not a guarantee layer. This CSP defines how to consume those signals without wandering into badge theater.

## Contents

| Path | What it is |
|---|---|
| `spec/erc-8004-csp.md` | The normative CSP document |
| `policy/policy.schema.json` | JSON Schema for a consumer policy |
| `policy/example-policy.json` | Example consumer policy (L3-oriented baseline) |
| `conformance/checklist.md` | Checklist by conformance level |
| `conformance/test-cases.md` | Test case suite |
| `docs/architecture.md` | Reference architecture for implementers |
| `docs/threat-model.md` | Consumer-focused threat model and attacker playbooks |
| `.github/workflows/pages.yml` | GitHub Pages deployment workflow |
| `scripts/build_pages.py` | Static site build script |

## Conformance levels

- **L0**: basic parsing only. Suitable for demos.
- **L1**: integrity-aware and safe-fetch capable.
- **L2**: Sybil-aware reputation consumption.
- **L3**: validation-meaningful consumption with deterministic rules.
- **L4**: externally economically secured profile claims.

See `spec/erc-8004-csp.md` for the full requirements matrix.

## v0.9.1 highlights

- Corrected the integrity model for registration files so that **content-addressed URIs, `data:` URIs, or extension-level digests** are treated as cryptographically anchored, while plain `https://` retrieval without a digest is treated as retrieved but **not cryptographically anchored**.
- Added explicit handling for **`agentWallet` freshness**, **post-transfer invalidation**, and **EOA vs ERC-1271 wallet binding semantics**.
- Added **`registrations[]` cross-check requirements** to reduce continuity spoofing across registries and chains.
- Tightened **validation request/response linkage** around `requestHash`, supersession, finality, and drift after `agentURI` changes.
- Added stricter **`data:` URI safety controls** and clearer **`supportedTrust` interpretation**.
- Added a **GitHub Pages** workflow and static site build path.

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

## Repository status

- Version: **CSP v0.9.1**
- Date: **2026-03-07**
- License: **Apache-2.0**

## GitHub Pages

The repository includes an Actions-based Pages workflow in `.github/workflows/pages.yml`.

After pushing to the default branch:
1. In repository settings, set **Pages** to use **GitHub Actions** as the source.
2. The workflow will build a static site from the repository Markdown.
3. The deployed site will expose the CSP and supporting docs as browsable HTML.

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

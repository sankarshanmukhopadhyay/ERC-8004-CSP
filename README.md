# ERC-8004 Consumer Security Profile (CSP)

A **consumer-side** security profile for **ERC-8004 (Trustless Agents)** implementers: wallets, agent directories, marketplaces, explorers, and indexers.

This repository packages the CSP as:
- A **human-readable profile** (normative **MUST/SHOULD/MAY** language)
- A **machine-readable policy schema** (JSON Schema)
- A **conformance checklist** and **test cases** template you can use in CI

> ⚠️ ERC-8004 is a **signal bus**. This CSP defines how to consume those signals safely and avoid “badge theater”.

## Contents

| Path | What it is |
|---|---|
| `spec/erc-8004-csp.md` | The CSP document (tables + requirements) |
| `policy/policy.schema.json` | JSON Schema for a consumer policy |
| `policy/example-policy.json` | Example consumer policy (L3-ish) |
| `conformance/checklist.md` | Checklist by conformance level |
| `conformance/test-cases.md` | Test case suite template |
| `docs/architecture.md` | Reference architecture for implementers |
| `docs/threat-model.md` | Consumer-focused threat model + attacker playbooks |

## Conformance levels

- **L0**: basic parsing (demo)
- **L1**: integrity-checked + safe-fetch
- **L2**: Sybil-aware reputation consumption
- **L3**: validation-meaningful (method/scope/freshness + deterministic finality)
- **L4**: economically secured (depends on external protocols)

See: `spec/erc-8004-csp.md`.

## Quick start (adopt CSP in a product)

1. Copy `policy/example-policy.json` and customize it.
2. Implement:
   - safe-fetch sandbox
   - hash verification
   - transfer/control-change UX
   - scoring + weighting (L2+)
   - validator policy + finality (L3+)
3. Run the checklist in `conformance/checklist.md` during release gates.

## Repository status

- Version: **CSP v0.9**
- Date: **2026-02-07**
- License: **Apache-2.0** (see `LICENSE`)

## Contributing

See `CONTRIBUTING.md`. Use issues/PRs for:
- additional conformance test cases
- validator scope taxonomies
- policy schema extensions
- implementation notes and reference code links

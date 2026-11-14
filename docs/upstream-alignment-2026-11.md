# ERC-8004 upstream alignment and consumer authority boundary

**Review date:** 2026-11-14  
**Local baseline:** CSP v0.9.1; this note does not change its normative requirements or policy schema.  
**Upstream:** [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004) (draft, maintained outside this repository).

This document records how the existing CSP consumes ERC-8004. The upstream ERC controls registry interface semantics. This repository controls only its separately maintained consumer security profile. An upstream editorial or protocol change does not automatically amend the CSP.

## Traceability

| Upstream behavior | CSP consumer interpretation | Evidence and limit |
| --- | --- | --- |
| The identity registry identifies an agent by `agentRegistry` and `agentId` and uses ERC-721 ownership. | Resolve against a specified chain and registry; treat transfer as a change of control, not continuous authorization. | `spec/erc-8004-csp.md` §§6.1, 10–11; registry data does not prove authority to perform a requested operation. |
| `agentURI` can reference HTTPS, IPFS or embedded data. | Classify retrieval and anchoring separately; apply safe-fetch before interpretation. | CSP §§7–8; retrieval or digest match does not establish endpoint safety or authorization. |
| `agentWallet` is reserved, set through wallet-control proof, and cleared on ERC-721 transfer. | Invalidate previous wallet binding upon transfer; require current chain-state and proof before using a new binding. | CSP §§6.1, 10; a payment/signing wallet is not by itself an action mandate. |
| Registration `supportedTrust` is optional; absent/empty means discovery only. | Do not convert a profile advertisement into an assurance finding. | CSP §§2, 6.1; even a nonempty value is a claim, not independently verified evidence. |
| Reputation feedback is submitted by client addresses; `getSummary` requires a nonempty selected `clientAddresses` set. | Record selection/filter provenance, revocation and weighting; never imply an ecosystem-wide objective score. | CSP §§6.2, 9; the choice and governance of the client set are consumer policy. |
| Feedback `appendResponse` may be called by anyone; feedback may be revoked. | Distinguish authorship, third-party annotations and revoked state. | CSP §§6.2, 9; response annotations are not adjudicated truth. |
| `validationRequest` commits to the request payload with `requestHash`; a designated validator responds. | Bind the selected response to its request, validator, agent and assessed artifact or scope. | CSP §§6.3, 12; request integrity and authorization for execution are different claims. |
| Validation responses range from 0 to 100 and a validator may update the same request multiple times. | Treat the number as protocol data; interpretation, thresholds, freshness, conflict handling and finality are consumer-defined. | CSP §§6.3, 12; ERC-8004 does not impose universal pass/fail or finality semantics. |
| Validator incentives and slashing are external to the validation registry. | Do not assert L4 economic security without evidence from the actual external mechanism. | CSP §5; an L4 label is not external certification. |

## Authority and enforcement invariant

An ERC-8004 agent record identifies a registry subject. Reputation and validation are evidence signals, not delegated-action authorization. Consumer display policy may decide whether to show, suppress, warn, or qualify those signals. It **MUST NOT** manufacture a permission to act from identity, reputation, validation, `supportedTrust`, domain control or wallet-control evidence alone.

An executing system needs a separate authoritative delegation and runtime authorization mechanism that checks the principal, permitted operation, target, scope, time, context and revocation state. CSP policy evaluations may be one input to that enforcement decision, but never its substitute.

## Historical and uncertain evidence

A latest indexed snapshot is a derived observation, not necessarily the present canonical state. Consumers should retain chain identity, block or observation reference, verification time, source and policy version as appropriate. Transfer, wallet reset, changed `agentURI`, revoked feedback, superseded validator responses, chain reorganization, stale caches, and unavailable evidence must remain distinguishable. Unknown, missing, contradictory or stale data must not become an affirmative assurance assertion.

## Compatibility and review status

This note is an informative interpretation of upstream semantics under CSP v0.9.1, not a normative revision. No wire format, policy schema, conformance level, or released artifact is changed. Any new executable policy contract must be versioned and tested independently before it is described as implemented.

## Sources

- [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004)
- [EIP-712: Typed structured data hashing and signing](https://eips.ethereum.org/EIPS/eip-712)
- [ERC-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [ERC-1271: Standard Signature Validation Method for Contracts](https://eips.ethereum.org/EIPS/eip-1271)

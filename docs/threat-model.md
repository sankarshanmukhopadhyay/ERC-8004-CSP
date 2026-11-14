# CSP Threat Model: Consumer-Side False Success

**Scope:** wallets, indexers, marketplaces, explorers, directories and relying clients that interpret [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) signals. This document supports the [CSP working draft](../spec/erc-8004-csp.md) and is informative.

## Protected propositions and attacker control

| Proposition a consumer might assert | Attacker controls or influences | False-success path | Required defense | Negative test |
| --- | --- | --- | --- | --- |
| Current agent identity | Registration URI, token transfers, operator permissions | Previous owner's reputation survives token transfer | Explicit block and `Transfer` history, wallet invalidation | T03, T15 |
| Valid source content | HTTP endpoint, IPFS gateway, embedded content | HTTP 200 or embedded bytes called verified integrity | Per-scheme classification and KECCAK/CID checks | T01, T02, T16 |
| Safe service | Advertised endpoint URLs and redirected hosts | SSRF, scriptable metadata or private-network redirect | All-hop network policy, strict parser, inert rendering | T05, T06, T17 |
| Verified domain | Well-known registration file, controlled DNS | Domain control inflated into agent authorization | Scope-qualified domain-control label only | T19 |
| Reliable reputation | Many client accounts, tags, appendResponse and selective filters | Colluding reviewer set looks like objective global quality | Client-set provenance, weighting disclosures, rate limits | T07–T09, T20 |
| Current feedback | Revocation and indexer timing | Revoked feedback remains active in score | Historical/revoked distinction | T09 |
| Meaningful validation | Request payload, responseURI, validator collusion, response updates | `response=100` turns into permanent agent-wide trust | Request/validator/artifact binding and explicit policy finality | T11–T14, T21 |
| Current state | RPC/indexer snapshot, block reorg | Stale state shown as finalized | Reorg handling, source freshness, indeterminate | T18 |
| Economic protection | External stake/coverage claims | `supportedTrust` or numerical stake treated as effective guarantee | Resolve external instrument, scope and effective lifecycle | T23–T24 |
| Action authorization | Inferred wallet control and “validated” badge | Signal-based execution without delegated mandate | Separate authority evaluator and runtime revocation | T22 |

## Trust boundary failures

1. **Registry-to-index boundary.** The indexed record is an observation. It can lag, omit an event or derive from a non-canonical branch. Current-state assertions require chain-context and finality evidence. [ERC-8004 Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry).
2. **URI-to-byte boundary.** HTTP success, CID resolution and `data:` decoding are different facts. Even an exact byte commitment says nothing about the truth or non-maliciousness of the payload. [ERC-8004 Agent URI](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file); [RFC 3986 `7](https://www.rfc-editor.org/rfc/rfc3986#section-7).
3. **Reputation-to-judgment boundary.** `getSummary` operates on chosen `clientAddresses`. An actor that selects a biased population can obtain a misleading score without violating upstream ABI rules. [ERC-8004 Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions).
4. **Validation-to-assurance boundary.** The validator's numeric response is a request-specific signal, potentially updated over time. A client-supplied methodology or display badge must not imply upstream endorsement. [ERC-8004 Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response).
5. **Consumer-to-execution boundary.** A correctly parsed registry record, valid wallet signature or admitted validation cannot itself grant the right to transact or act for a principal. [CSP `1.3](../spec/erc-8004-csp.md).

## High-priority adversarial pairings

- A **valid** CID or KECCAK-256 hash paired with **unverified chain state** must not yield a present-day trusted claim.
- A **valid** wallet-control signature paired with **missing delegation** must not yield permission to act.
- A **valid** validation response paired with **wrong scope, stale artifact or changed agentURI** must not yield a permanent validation badge.
- **Two independently valid component checks** must not establish a broader composed assurance assertion when the seam obligation is untested.
- **Green CI** must not be represented as independent third-party adoption, live Ethereum verification or production conformance.

## Tests and disposition

The [conformance test catalogue](../conformance/test-cases.md) specifies expected safe results for these failures. Implementers should create observable test outputs with relevant source snapshots and policy identity. Unknown, missing, stale and conflicting evidence must remain distinct from a proven negative. The experimental [Rego tests](executable-rego-policy.md) exercise only their bounded input contract, not the end-to-end threat model.

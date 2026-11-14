# CSP Reference Architecture and Trust Boundaries

**Status:** companion implementation guidance to the [working-draft CSP](../spec/erc-8004-csp.md), not a separate normative source.

The [ERC-8004 Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry), [Reputation Registry](https://eips.ethereum.org/EIPS/eip-8004#reputation-registry) and [Validation Registry](https://eips.ethereum.org/EIPS/eip-8004#validation-registry) provide source records. This architecture represents how a *consumer* derives appropriately limited determinations from those records. It does not introduce new ERC contract interfaces or action authorization.

## Dataflow and authority

| Stage | Input and authoritative source | Local responsibility | Evidence retained | Failure boundary |
| --- | --- | --- | --- | --- |
| Chain resolver | ERC-8004 registry address, chain and ERC-721 state | Resolve subject, owner, wallet and URI at explicit block | `agentRegistry`, `agentId`, block/hash/finality, call/receipt | Reorg/unknown chain state is indeterminate |
| Indexer and reconciler | ERC-721 `Transfer`, ERC-8004 `Registered`/`URIUpdated`/`MetadataSet`, feedback and validation events | Replay-safe materialized state with revision history | Event order, source blocks, supersessions | Derived index is not chain authority |
| Constrained fetcher | On-chain `agentURI`, `feedbackURI`, `requestURI`, `responseURI` | SSRF-safe, bounded resolution; no execution | URI, redirects, bytes/CID, media type, retrieval time | Timeout and untrusted content cannot become PASS |
| Integrity verifier | On-chain CID or KECCAK-256 commitment | Hash exact bytes using correct algorithm; classify embedded/unanchored/mismatch | Algorithm, content address or digest, observed source, result | A digest match is not verified truth |
| Identity continuity guard | Owner, `agentWallet`, URI, `registrations[]` | Invalidate stale control/continuity assumptions | Prior and current source, transfer or URI event | No inheritance of former owner's trust |
| Reputation consumer | `clientAddress`, feedback index, revocation, selected `getSummary` clients | Rate-limit, weight, disclose selection and uncertainty | Client-set definition/digest, filters, policy version | Score is selected population, not objective quality |
| Validation consumer | `requestHash`, designated validator, responses and off-chain data | Verify request/artifact binding, freshness, method, conflict/finality | Request/response mapping, provenance, chronology | `response=100` is not universal authorization |
| Policy evaluator | Verified normalized facts + local consumer policy | Issue admitted/denied/indeterminate consumer display decision | Policy digest, input snapshot and output | Decision cannot grant execution mandate |
| Presentation/API | Qualified consumer decision and evidence | Show warnings, scope, history and provenance | Claim text and source reference | No unconditional badge on uncertainty |
| Audit evidence | All above records | Reproduce and contest consumer decisions | Block/time, content and policy identities | Log existence is not independent assurance |

## Canonical subject and adapter boundary

The upstream subject is a pair: `agentRegistry = {namespace}:{chainId}:{identityRegistry}` and `agentId`. Preserve it in indexes and audit records. The [experimental Rego input](../policy/rego/input.schema.json) instead takes `subject.chain_id` and `subject.agent_registry` (an EVM contract address). **The adapter must verify the namespace, chain and contract equivalence; it must never silently treat the two representations as the same wire field.** The Rego `sha256:` artifact digest is similarly local and cannot replace ERC-8004's `keccak256` commitments. See [CSP ``2, 6 and 9](../spec/erc-8004-csp.md).

## State transitions and invalidation

| Event | Required state transition | User-facing disposition |
| --- | --- | --- |
| `Transfer` | Supersede prior owner continuity; clear old wallet binding until current state re-established | Control changed; current wallet unbound/unverified |
| `URIUpdated` | Re-fetch and reclassify; re-evaluate artifact-bound validations | Updated; dependent validations under reassessment |
| `FeedbackRevoked` | Exclude from current positive scoring, retain historical provenance | Revoked, not silently deleted |
| Repeated `ValidationResponse` | Track latest vs selected final vs superseded under declared policy | Exact request and methodology shown |
| Reorg or stale indexer | Invalidate current-state conclusions from affected block range | Indeterminate until reconciled |
| External economic-security revocation | Reassess L4 independent of validation registry status | Downgrade / withdraw coverage claim |

## Implementation examples and assurance limits

The optional [OPA/Rego implementation](executable-rego-policy.md) executes one display-admission policy, not the entire CSP pipeline. It assumes a verified and normalized input. Its JSON Schema validation and SHA-256 execution digests establish input/output reproducibility but not Ethereum finality, authenticity of data or delegated action authority.

For test evidence, use [CSP conformance cases](../conformance/test-cases.md) and the [checklist](../conformance/checklist.md). The prose cases represent obligations to test in an adopter's actual consumer path. Only the experimental Rego fixtures currently have real-engine CI coverage. A service that executes actions needs a distinct authorization and revocation enforcement layer with its own tests.

## Architecture threats

Protect against SSRF on each redirect and DNS resolution, decompression/size bombs, malicious HTML and service metadata, correlation leaks to external gateways, duplicate/replayed events, indexer chain forks, unbounded feedback fan-out, false reviewer independence, and validator-policy drift. See [consumer threat model](threat-model.md), [RFC 3986 `7](https://www.rfc-editor.org/rfc/rfc3986#section-7), and [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

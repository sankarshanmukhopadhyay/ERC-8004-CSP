# ERC-8004 Consumer Security Profile (CSP) v0.9.1

**Audience:** wallets, marketplaces, agent directories, explorers, and indexers that consume ERC-8004 signals.  
**Goal:** safe-by-default consumption with integrity-aware retrieval, Sybil-aware reputation, and validation that does not collapse into empty signaling.  
**Normative keywords:** **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**.

---

## 1) Scope and non-goals

| Item | In scope | Out of scope |
|---|---|---|
| Integrity-aware retrieval of registration, feedback, and validation content | ✅ | Cryptographic guarantees not present in upstream registries |
| Safe retrieval, caching, and inert rendering of URIs | ✅ | Rich active-content rendering |
| Anti-spam and Sybil-resilient reputation display | ✅ | Perfect Sybil resistance |
| Meaningful validation display and deterministic finality semantics | ✅ | Defining validator economics or slashing |
| UX patterns for control change, drift, and risk warnings | ✅ | Policing off-chain agent behavior |
| Privacy and data minimization for consumers | ✅ | Full legal or regulatory compliance framework |

---

## 2) Upstream assumptions and design posture

This profile is written for the current **draft** of ERC-8004 and aligns to the following upstream properties:

1. ERC-8004 defines three lightweight registries for **identity**, **reputation**, and **validation**. It is intentionally composable and leaves scoring, validator economics, and downstream policy largely open.
2. The identity registry is based on **ERC-721**, so transfer of the token is a real control-change event and MUST be treated that way by consumers.
3. The `agentURI` may use `https://`, `ipfs://`, or `data:` URIs. The draft does **not** define a universal on-chain digest for registration files. Consumers therefore MUST distinguish between **cryptographically anchored retrieval** and mere successful retrieval.
4. `agentWallet` is special. It is reserved, requires proof of control using **EIP-712** or **ERC-1271**, and is automatically cleared when the ERC-721 token is transferred.
5. Validation is request-centric and keyed by `requestHash`. Multiple validation responses may exist for the same request, including progressive states.
6. If `supportedTrust` is absent or empty, the registration is being used for discovery only, not for trust.

---

## 3) Roles and trust boundaries

| Role | What they control | What consumers MUST NOT assume |
|---|---|---|
| Agent owner (ERC-721 holder) | `agentURI` updates, transfer control, wallet rebinding | Same token means same operator over time |
| Agent wallet (`agentWallet`) | Optional payment and signing endpoint | Always set, always current, always EOA, always safe |
| Client / feedback author | Feedback creation, revocation, appended material | Human uniqueness, honesty, or non-collusion |
| Validator | Methodology, response semantics, update cadence | Consistent meaning of “validated” across validators |
| Consumer UI / indexer | Aggregation, filtering, ranking, rendering | Raw chain signals are safe or meaningful without policy |

---

## 4) Threat model summary

| Threat | Typical attacker path | Consumer harm | CSP posture |
|---|---|---|---|
| Reputation Sybil swarm | Many clients emit cheap feedback | Inflated or buried reputation | Weighting, quotas, anomaly controls |
| Identity continuity hijack | Transfer or buy the NFT | Brand takeover, stale trust carryover | Control-change detection and reset |
| Endpoint substitution | Swap registration or service endpoints | Phishing, malware, impersonation | Safe-fetch, endpoint tiering, diff visibility |
| Availability rug | Remove or censor blobs | Claims cannot be re-verified | Verified cache, retry, unavailable semantics |
| Validation theater | Friendly validators or vague scopes | False assurance | Method, scope, freshness, request binding |
| Indexer griefing | Spam events or slow URIs | Downtime, hidden centralization | Quotas, backpressure, fetch sandbox |
| Cross-registry continuity spoofing | Claim extra registrations without proof | Fake multi-chain legitimacy | `registrations[]` cross-check rules |

---

## 5) Conformance levels

A consumer MUST NOT claim a higher level unless all requirements in that level and below are met.

| Level | Label | Minimum bar | Typical safe use case |
|---|---|---|---|
| L0 | ERC-8004 compatible | Basic parsing only | Demos and local experiments |
| L1 | Integrity-aware | Safe-fetch plus integrity anchoring classification | Casual browsing |
| L2 | Sybil-aware reputation | Weighted reputation and spam controls | Consumer directories and marketplaces |
| L3 | Validation-meaningful | Validator policy, request linkage, freshness, deterministic finality | Enterprise evaluation |
| L4 | Economically secured (profiled) | External staking, slashing, bond, or insurance integration | High-stakes automation |

---

## 6) Requirements matrix

### 6.1 Identity consumption

| Requirement | L1 | L2 | L3 | L4 | Notes |
|---|---:|---:|---:|---:|---|
| Detect ERC-721 transfer and treat it as a control change | MUST | MUST | MUST | MUST | Show date and transaction reference; reset continuity |
| Show `agentWallet` as current, cleared, or stale | MUST | MUST | MUST | MUST | Zero address is not neutral; it is unbound |
| Re-verify `agentWallet` after transfer before routing trust to it | MUST | MUST | MUST | MUST | Old bindings MUST be invalidated |
| Distinguish EOA proof from ERC-1271 contract-wallet proof where available | SHOULD | SHOULD | MUST | MUST | Helpful for integrator risk models |
| Registration retrieval MUST be classified as cryptographically anchored, unanchored, mismatched, unavailable, or malformed | MUST | MUST | MUST | MUST | Retrieval state is not trust state |
| If `registrations[]` is present, the active on-chain `(agentRegistry, agentId)` MUST appear in it | SHOULD | MUST | MUST | MUST | Prevent continuity spoofing |
| If `supportedTrust` is absent or empty, the consumer MUST treat the profile as discovery-only | SHOULD | MUST | MUST | MUST | No implied assurance from registration alone |
| Endpoint domain verification MUST be labeled as domain control only | SHOULD | MUST | MUST | MUST | Do not convert domain control into safety claims |

### 6.2 Reputation consumption

| Requirement | L1 | L2 | L3 | L4 | Notes |
|---|---:|---:|---:|---:|---|
| Display raw feedback counts without implying quality | MUST | MUST | MUST | MUST | No stars or scalar quality score at L1 |
| Weight feedback using transparent policy inputs | — | MUST | MUST | MUST | Age, proof, reliability, stake, or similar |
| Rate-limit ingestion and rendering per agent and per source | SHOULD | MUST | MUST | MUST | Protect both UI and indexer |
| Treat `appendResponse()` as untrusted unless policy admits it | MUST | MUST | MUST | MUST | Third-party annotations are not first-party truth |
| Distinguish author feedback, agent response, and third-party annotation | SHOULD | MUST | MUST | MUST | Asymmetry matters |
| Revoked feedback remains visible as revoked | MUST | MUST | MUST | MUST | No silent erasure |
| Summary outputs MUST declare the client set or policy basis used | SHOULD | MUST | MUST | MUST | Prevent hidden centralization |

### 6.3 Validation consumption

| Requirement | L1 | L2 | L3 | L4 | Notes |
|---|---:|---:|---:|---:|---|
| Never show “validated” without method, scope, freshness, and validator identity | — | — | MUST | MUST | Kill badge inflation |
| Preserve and expose `requestHash -> validatorAddress -> response(s)` linkage | — | SHOULD | MUST | MUST | Validation is request-scoped |
| Distinguish latest response, final response under policy, and superseded response | — | SHOULD | MUST | MUST | Progressive states are allowed upstream |
| Validation payload integrity MUST be checked using the same anchoring model used elsewhere | MUST | MUST | MUST | MUST | Same retrieval rules apply |
| Validation status MUST be tied to the specific artifact or scope evaluated | — | SHOULD | MUST | MUST | “Validated once” is not enough |
| Material `agentURI` changes MUST stale or downgrade prior validations until re-evaluated | — | SHOULD | MUST | MUST | Drift is real |
| Consumer MUST maintain a validator policy | — | SHOULD | MUST | MUST | Allowlist, weighted allowlist, or open-but-downrank |
| Consumer MUST define a deterministic finality rule | — | SHOULD | MUST | MUST | Multiple responses are expected upstream |

---

## 7) Integrity anchoring model

ERC-8004 allows `https://`, `ipfs://`, and `data:` registration URIs. The upstream draft does not provide a universal registration-file digest for every URI scheme. Therefore this profile uses an **integrity anchoring model**, not a pretend universal hash fairy.

### 7.1 Classification states

| State | Meaning | Consumer behavior |
|---|---|---|
| Cryptographically anchored | Content is anchored by a content-addressed URI, embedded `data:` URI, or an extension-level digest | MAY be used subject to normal safety checks |
| Retrieved but unanchored | Content was fetched, but no digest or content-addressed anchor exists | MUST be labeled unanchored; MUST NOT be marketed as integrity-verified |
| Mismatch | Expected anchor and retrieved content disagree | MUST quarantine and block normal use |
| Unavailable | Content could not be fetched | SHOULD use last verified snapshot if present |
| Malformed | Content is syntactically or structurally invalid | MUST show minimal safe metadata only |

### 7.2 Anchoring rules

1. `ipfs://` or similar content-addressed retrieval SHOULD be treated as cryptographically anchored when the content resolution preserves the expected content identifier.
2. `data:` URIs MAY be treated as cryptographically anchored because the content is embedded, but they MUST still pass size, media-type, and inert-rendering controls.
3. Plain `https://` retrieval without an external digest or profile extension MUST be labeled **retrieved but unanchored**.
4. If an implementation adds an extension-level digest for `https://` content, that digest MAY be used as the anchoring basis.
5. A consumer MUST NOT use successful retrieval alone as evidence that content is immutable, authentic, safe, or still policy-worthy.

---

## 8) Content retrieval and rendering policy (safe-fetch)

### 8.1 URI handling

| Category | MUST | SHOULD | MUST NOT |
|---|---|---|---|
| URI schemes | Support `https://`; support `ipfs://` through controlled gateways; support `data:` only under strict policy | Support more than one IPFS gateway | Auto-execute unknown schemes |
| Fetch sandbox | Enforce timeouts, size caps, media-type checks, and isolated execution | Log resolved URI and anchor classification | Fetch in a privileged UI thread |
| Redirect handling | Log redirect chain and policy outcome | Limit redirect depth tightly | Silently trust redirects |
| Rendering | Render inert text or JSON only | Strip active content and dangerous attributes | Render HTML, script, or SVG as active content |
| PII and malware | Classify and warn before display | Offer suppression controls | Display sensitive content by default |

### 8.2 `data:` URI controls

| Control | Requirement |
|---|---|
| Allowed media types | MUST be explicitly allowlisted, for example `application/json` or `text/plain` |
| Size | MUST be capped separately from normal fetch size |
| Parsing | MUST be inert-only |
| Active content | MUST NOT render HTML, JavaScript, or scriptable SVG |

### 8.3 Availability semantics

| State | UI label | Consumer behavior | Indexer behavior |
|---|---|---|---|
| Anchored and valid | Verified content | Show normally with anchor disclosure | Cache by anchor |
| Retrieved but unanchored | Retrieved, not cryptographically anchored | Show warning and lower trust | Cache separately from anchored content |
| Mismatch | Tampered or mismatched | Block normal use | Quarantine and alert |
| Unavailable | Unavailable | Show last verified snapshot if present | Retry with backoff |
| Malformed | Invalid content | Show minimal safe metadata only | Record error and rate-limit source |

---

## 9) Reputation scoring baseline (L2+)

### 9.1 Weighting inputs

| Signal | Default guidance | Rationale | Abuse resistance |
|---|---|---|---|
| Feedback age | Decay over time | Prevent frozen reputation | Medium |
| Client account age | Upweight older accounts | Adds friction to cheap swarms | Medium |
| Client proof | Optional upweight for DID, VC, KYC, or similar | Raises cost of spoofing | Variable |
| Stake or bond | Strong upweight if present | Adds economic cost | High when real |
| Prior reliability | Upweight proven signal sources | Anti-spam effect | Medium |

### 9.2 Output constraints

| Level | Allowed display | Disallowed display |
|---|---|---|
| L1 | Counts and chronological views | Scalar reputation score |
| L2+ | Score with policy disclosure and confidence | Score without policy transparency |
| L3+ | Score plus validation overlays and freshness | “Validated” badge with no scope or method |

---

## 10) Control change and continuity UX

| Event | MUST show | MUST do | SHOULD do |
|---|---|---|---|
| ERC-721 transfer | Control changed with date and tx reference | Reset continuity indicators and invalidate prior wallet trust | Require re-consent before risky actions |
| `agentURI` update | Profile updated with diff view or changed fields | Re-run retrieval classification and stale dependent validations | Highlight endpoint changes |
| `agentWallet` set, cleared, or rebound | Wallet bound, unbound, or reverified state | Update routing constraints immediately | Show EOA vs contract-wallet status |
| Mismatch between active registration and `registrations[]` | Registration continuity warning | Downrank or block continuity claims per policy | Require manual review in high-stakes flows |

---

## 11) Cross-registry continuity rules

1. When `registrations[]` is present, the currently resolved on-chain `(agentRegistry, agentId)` pair SHOULD appear there at L1 and MUST appear there at L2+.
2. Additional registration entries MUST be treated as **claims** unless independently resolved.
3. Cross-chain or cross-registry continuity MUST NOT be treated as verified identity continuity without separately resolving each referenced registry/token pair.
4. A consumer SHOULD surface mismatches between the active registration and declared linked registrations.

---

## 12) Validator governance and request linkage (L3+)

### 12.1 Validator policy fields

| Field | Type | Requirement | Meaning |
|---|---|---|---|
| `validatorAddress` | address | MUST | On-chain validator identity |
| `methodologyURI` | URI | MUST | Human-readable method description |
| `scopeTags` | string[] | MUST | What was actually validated |
| `weight` | number | MUST | Consumer-side influence |
| `conflictRule` | enum | MUST | Tie-break or resolution policy |
| `freshnessWindowHours` | number | MUST | Validity window |

### 12.2 Request and response handling

| Requirement | Why it exists |
|---|---|
| Preserve `requestHash` as the primary linkage key | Upstream validation is request-centric |
| Allow multiple responses per request | Upstream supports progressive states |
| Distinguish latest, final, and superseded responses | Prevent semantic collapse |
| Bind validation display to the artifact version or scope evaluated | Avoid generic “validated once” theater |
| Stale prior validations on material `agentURI` change | Validation may no longer describe the live artifact |

---

## 13) Indexer operational controls

| Control | MUST | SHOULD | Notes |
|---|---|---|---|
| Event ingestion quotas | ✅ |  | Per-agent and per-source burst controls |
| Backpressure on slow URIs | ✅ |  | Prevent fetch storms |
| Cache by anchor or digest | ✅ |  | Deduplicate and preserve provenance |
| Audit logs of fetch, classification, and verification | ✅ |  | Incident response and explainability |
| Health checks for IPFS gateways | ✅ |  | Automatic fallback |
| Abuse reporting channel |  | ✅ | Social layer still matters |

---

## 14) Privacy and data minimization

| Risk | CSP requirement |
|---|---|
| Correlation graphs | SHOULD provide privacy-mode views |
| Accidental PII in blobs | MUST classify and permit suppression while keeping a pointer visible |
| Long-term local retention | SHOULD allow cache purge and MUST label on-chain immutability |

---

## 15) Compliance test suite summary

| Test | Expected result | Level |
|---|---|---|
| Plain `https://` registration with no digest | Show retrieved but unanchored | L1+ |
| Transfer clears `agentWallet` trust | Control-change banner and wallet invalidation | L1+ |
| `registrations[]` mismatch | Warning or block per policy | L2+ |
| Multiple validation responses for one request | Deterministic latest/final/superseded output | L3+ |
| `agentURI` changes after validation | Validation becomes stale or downgraded | L3+ |
| Oversized or active `data:` URI | Blocked by safe-fetch | L1+ |

---

## 16) Upstream references

- ERC-8004 draft: `https://eips.ethereum.org/EIPS/eip-8004`
- EIP-712: `https://eips.ethereum.org/EIPS/eip-712`
- ERC-721: `https://eips.ethereum.org/EIPS/eip-721`
- ERC-1271: `https://eips.ethereum.org/EIPS/eip-1271`
- RFC 2119: `https://www.rfc-editor.org/rfc/rfc2119`
- RFC 8174: `https://www.rfc-editor.org/rfc/rfc8174`

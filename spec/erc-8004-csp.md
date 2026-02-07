# ERC-8004 Consumer Security Profile (CSP) v0.9

**Audience:** wallets, marketplaces, agent directories, explorers, and indexers that consume ERC-8004 signals.  
**Goal:** safe-by-default consumption: integrity checks, Sybil-aware reputation, and validation that avoids “badge theater”.  
**Normative keywords:** **MUST**, **SHOULD**, **MAY**.

---

## 1) Scope and non-goals

| Item | In scope | Out of scope (explicitly) |
|---|---|---|
| Integrity of fetched metadata (registration/feedback/validation payloads) | ✅ | |
| Safe retrieval, caching, and rendering of URIs | ✅ | |
| Anti-spam and Sybil-resilient reputation display | ✅ | Perfect Sybil resistance |
| Meaningful validation display and finality semantics | ✅ | Defining validator economics/slashing |
| UX patterns for control-change and risk warnings | ✅ | Policing agent behavior off-chain |
| Privacy & data minimization for consumers | ✅ | Full legal compliance framework |

---

## 2) Roles and trust boundaries

| Role | What they control | What you must not assume |
|---|---|---|
| Agent Owner (ERC-721 holder) | `agentURI` updates; transfer control | “same token == same operator” after transfer |
| Agent Wallet (`agentWallet`) | Optional signing identity for the agent | Always set / always safe / always unique |
| Client (feedback author) | Feedback creation/revocation | Clients are human, unique, or honest |
| Validator | Validation responses, methodology (often off-chain) | “validated” has consistent meaning |
| Consumer UI / Indexer (you) | Aggregation, ranking, filtering, display | Raw chain data is user-safe without policy |

---

## 3) Threat model summary (consumer-focused)

| Threat | Typical attacker path | Consumer harm | CSP posture |
|---|---|---|---|
| Reputation Sybil swarm | Many clients post feedback | Users misled, market capture | Weighting + rate limits + anomaly detection |
| Identity continuity hijack | Buy/transfer agent NFT | Brand takeover | Control-change detection + warnings |
| Endpoint substitution | Malicious registration file endpoints | Phishing, data theft | Endpoint risk tiering + safe-fetch |
| Availability rug | URIs disappear / gateways fail | Users can’t verify claims | Cache/pin + “unavailable” semantics |
| Validation theater | Friendly validators, vague scopes | False assurance | Method + scope + freshness required |
| Indexer griefing | Spam events + slow URIs | Centralization, downtime | Fetch sandbox + quotas + backpressure |

---

## 4) Conformance levels

You MUST NOT claim a higher level unless all requirements in that level and below are met.

| Level | Label (marketing-safe) | Minimum bar | Safe use-case |
|---|---|---|---|
| L0 | “ERC-8004 compatible” | Basic parsing | demos only |
| L1 | “Integrity-checked” | Hash-verified content + safe-fetch | casual browsing |
| L2 | “Sybil-aware reputation” | Weighted reputation + spam controls | consumer marketplace |
| L3 | “Validation-meaningful” | Validator policy + finality + freshness | enterprise procurement |
| L4 | “Economically secured (profiled)” | External staking/slashing/insurance integration | high-stakes automation |

---

## 5) Requirements matrix

### 5.1 Identity consumption

| Requirement | L1 | L2 | L3 | L4 | Notes |
|---|---:|---:|---:|---:|---|
| Detect ERC-721 transfer and treat as control change | MUST | MUST | MUST | MUST | Show date/tx; reset continuity |
| Show “agentWallet unset/cleared” state explicitly | MUST | MUST | MUST | MUST | Avoid silent routing assumptions |
| Registration file MUST be hash-verified before use | MUST | MUST | MUST | MUST | Integrity, not safety |
| Endpoint risk tiering (https/ipfs/data/etc.) | SHOULD | MUST | MUST | MUST | Higher tiers get warnings/limits |
| Domain verification labeled “domain control only” | SHOULD | MUST | MUST | MUST | Avoid safety-badge theater |

### 5.2 Reputation consumption

| Requirement | L1 | L2 | L3 | L4 | Notes |
|---|---:|---:|---:|---:|---|
| Display feedback counts without implying quality | MUST | MUST | MUST | MUST | No “stars” at L1 |
| Weight feedback (age, stake, identity proof, reliability) | — | MUST | MUST | MUST | Default policy must be inspectable |
| Rate-limit ingestion / rendering per agent | SHOULD | MUST | MUST | MUST | Protect indexer + UX |
| Treat `appendResponse()` as untrusted annotation | MUST | MUST | MUST | MUST | Gate display by responder policy |
| Revoked feedback remains visible as revoked | MUST | MUST | MUST | MUST | No silent deletion |
| “Summary” outputs declare client set used | SHOULD | MUST | MUST | MUST | Prevent hidden centralization |

### 5.3 Validation consumption

| Requirement | L1 | L2 | L3 | L4 | Notes |
|---|---:|---:|---:|---:|---|
| Never show “Validated” without method/scope/freshness | — | — | MUST | MUST | Kill badge inflation |
| Maintain a validator policy (allowlist/weights) | — | SHOULD | MUST | MUST | Transparent governance |
| Finality rule for multiple responses | — | SHOULD | MUST | MUST | Deterministic rule required |
| Validation payload hash verification | MUST | MUST | MUST | MUST | Same integrity rules |
| Tie validations to scope labels | — | SHOULD | MUST | MUST | “what was validated” is not optional |

---

## 6) Content retrieval and rendering policy (safe-fetch)

### 6.1 URI handling

| Category | MUST | SHOULD | MUST NOT |
|---|---|---|---|
| URI schemes | Support `https://`, `ipfs://` (via gateway), `data:` (cautiously) | Multiple IPFS gateways | Auto-execute unknown schemes |
| Fetch sandbox | Timeouts, size caps, content-type checks | Isolated worker/runtime | Fetch in privileged UI thread |
| Canonicalization | Log resolved URI + hash | Cache by hash | Treat redirects as trusted silently |
| Rendering | Render inert text/JSON | Strip active content | Render HTML/scripts from blobs |
| Malware/PII | Classify and warn | Provide suppression controls | Display sensitive content by default |

### 6.2 Availability semantics

| State | UI label | Consumer behavior | Indexer behavior |
|---|---|---|---|
| Available + hash matches | Verified content | Show normally | Cache by hash |
| Available + hash mismatch | Tampered / mismatch | Block use; show red alert | Quarantine + alert |
| Unavailable | Unavailable | Show last verified snapshot if present | Retry with backoff |
| Malformed | Invalid content | Show minimal safe metadata | Record error + rate-limit source |

---

## 7) Reputation scoring policy baseline (L2+)

### 7.1 Weighting inputs

| Signal | Default weight guidance | Rationale | Abuse resistance |
|---|---|---|---|
| Feedback age | Decay over time | Prevent frozen reputation | Medium |
| Client account age | Upweight older | Sybil friction | Medium |
| Client proof (DID/VC/KYC etc.) | Optional strong upweight | Raises cost | High if proof is real |
| Stake / bond (external) | Strong upweight | Economic cost | High |
| Prior reliability (internal graph) | Upweight | Anti-spam | Medium |

### 7.2 Output constraints

| Level | Allowed display | Disallowed display |
|---|---|---|
| L1 | Counts, chronological feed | Scalar “score” or stars |
| L2+ | Score with policy disclosure + confidence | Score without policy transparency |
| L3+ | Score + validator overlays + freshness | “Validated” badge without scope/method |

---

## 8) Control change and continuity UX

| Event | MUST show | MUST do | SHOULD do |
|---|---|---|---|
| ERC-721 transfer | Control changed + date/tx | Reset continuity indicators | Require re-consent before transactions |
| `agentURI` update | Profile updated + diff link | Re-verify hash + endpoints | Highlight endpoint changes |
| `agentWallet` set/cleared | Wallet bound/unbound | Update routing constraints | Warn on breaking changes |

---

## 9) Validator governance (L3+)

### 9.1 Validator policy fields

| Field | Type | MUST/SHOULD | Meaning |
|---|---|---|---|
| validatorAddress | address | MUST | On-chain identity |
| methodologyURI | URI | MUST | Method and evidence |
| scopeTags | array | MUST | What it validates |
| freshnessWindow | duration | MUST | Valid-until semantics |
| weight | number | SHOULD | Aggregation weight |
| conflictRule | enum | MUST | Disagreement handling |

### 9.2 Finality rules

| Rule | When to use | Failure mode |
|---|---|---|
| Latest-within-window | Fast-moving validations | Susceptible to last-minute flips |
| Quorum-of-validators | Higher assurance | Slow + governance-heavy |
| Two-phase (provisional→final) | Mixed | Needs clear UI |

---

## 10) Indexer operational controls

| Control | MUST | SHOULD | Notes |
|---|---|---|---|
| Event ingestion quotas | ✅ | | Per-agent/per-client bursts |
| Backpressure on slow URIs | ✅ | | Prevent fetch storms |
| Cache by hash | ✅ | | Deduplicate storage |
| Audit logs of fetch + verification | ✅ | | Incident response |
| Health checks for gateways | ✅ | | Automatic fallback |
| Abuse reporting channel |  | ✅ | Social layer matters |

---

## 11) Privacy and data minimization

| Risk | CSP requirement |
|---|---|
| Correlation graphs | SHOULD provide privacy-mode views |
| Accidental PII in blobs | MUST classify + allow suppression while keeping pointer visible |
| Long-term retention | SHOULD allow purge of local caches; MUST label on-chain immutability |

---

## 12) Compliance test suite

| Test | Expected result | Level |
|---|---|---|
| Hash mismatch on registration file | Block endpoint usage; show mismatch | L1+ |
| Transfer event occurs | Control-change banner; reset continuity | L1+ |
| 10k spam feedback events | UI stays usable; throttling | L2+ |
| `appendResponse()` spam | Responses gated; no UI DoS | L2+ |
| Conflicting validator responses | Deterministic finality output | L3+ |
| Content disappears | Show unavailable; use cached snapshot | L1+ |

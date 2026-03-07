# Threat Model (Consumer-side)

| Playbook | Goal | Path | Primary defenses |
|---|---|---|---|
| Reputation Sybil swarm | Inflate or bury reputation | Cheap repeated feedback | Weighting, rate limits, anomaly detection |
| Identity hijack via transfer | Take over a brand or reputation shell | Transfer the ERC-721 token | Control-change banner, stale-state reset |
| Endpoint substitution | Route users to malicious infrastructure | Change registration or service endpoints | Safe-fetch, endpoint tiering, diff visibility |
| Availability rug | Break verifiability | Remove or censor blobs | Cache, retry, unavailable semantics |
| Validation theater | Fake assurance without substance | Friendly validators or vague scope | Method, scope, freshness, request linkage |
| Cross-registry continuity spoofing | Pretend multi-chain legitimacy | Fake or unverifiable `registrations[]` claims | Cross-check and independent resolution |
| Indexer griefing | Degrade consumer infrastructure | Spam events and slow URIs | Quotas, backpressure, sandboxed retrieval |

## High-priority consumer mistakes to avoid

1. Treating successful retrieval as proof of integrity.
2. Treating transfer as a cosmetic event instead of a trust reset.
3. Treating `agentWallet` as permanently trustworthy after it has once been verified.
4. Treating `supportedTrust` silence as if it were a positive trust claim.
5. Treating validation as an agent-wide permanent badge when upstream semantics are request-specific.

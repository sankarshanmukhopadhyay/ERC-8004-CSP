# Threat Model (Consumer-side)

| Playbook | Goal | Path | Primary defenses (CSP) |
|---|---|---|---|
| Reputation Sybil Swarm | Inflate / bury | Many clients post feedback | L2 weighting + rate limits |
| Identity Hijack via Transfer | Take over brand | Transfer agent NFT | Control-change banner |
| Endpoint Substitution | Route to malicious | Poison endpoints | Endpoint tiering + safe-fetch |
| Availability Rug | Break verifiability | Remove blobs | Cache + unavailable semantics |
| Validation Theater | Fake assurance | Friendly validators | L3 scope/method/freshness |
| Indexer Griefing | DoS | Spam + slow URIs | Quotas + backpressure |

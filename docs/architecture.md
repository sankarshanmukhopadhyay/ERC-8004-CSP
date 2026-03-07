# Reference Architecture

| Component | Responsibilities | Hard requirements |
|---|---|---|
| Event indexer | Ingest identity, reputation, and validation events; derive continuity and freshness views | Replay-safe ingestion, quotas, and request linkage |
| Safe fetcher | Retrieve registration and validation artifacts | Timeouts, size caps, media-type checks, anchor classification |
| Content cache | Store anchored and unanchored blobs separately | Deduplication, retention controls, provenance metadata |
| Policy engine | Apply weighting, validator policy, and drift rules | Transparent defaults, deterministic finality, stale-state logic |
| Continuity guard | Detect transfer, wallet reset, `agentURI` drift, and `registrations[]` mismatch | Immediate invalidation of stale trust state |
| UI risk layer | Surface warnings, disclosures, and gated trust displays | No silent badges, no silent continuity carryover |
| Audit log | Preserve fetch, classification, validation, and policy decisions | Append-only event trail |

## Design notes

- The safe fetcher and continuity guard should be treated as first-class components, not garnish sprinkled on the plate after the kitchen fire starts.
- Anchored and unanchored content should not share the same cache namespace.
- Validation views should be keyed by `requestHash` and linked to the artifact or scope actually evaluated.

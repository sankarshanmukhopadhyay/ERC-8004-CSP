# Reference Architecture

| Component | Responsibilities | Hard requirements |
|---|---|---|
| Event indexer | Ingest events, derived views | Quotas, replay-safe |
| Safe fetcher | Fetch URIs, verify hashes | Timeouts, size caps |
| Content cache | Store verified blobs by hash | Deduplicate, retention |
| Policy engine | Weighting + validator rules | Transparent defaults |
| UI risk layer | Warnings + consent gates | No silent badges |
| Audit log | Provenance of decisions | Append-only logs |

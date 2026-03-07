# Conformance Test Cases

| ID | Scenario | Setup | Action | Expected | Level |
|---|---|---|---|---|---|
| T01 | Plain HTTPS registration with no digest | `agentURI` is `https://...` and no extension digest exists | Fetch and classify | Show `retrieved but unanchored`; do not claim integrity verified | L1 |
| T02 | Registration mismatch | Expected anchor and retrieved content differ | Fetch and classify | Quarantine and show mismatch | L1 |
| T03 | Agent transfer clears wallet trust | Transfer the ERC-721 token after wallet was set | Refresh state | Show control-change banner and wallet as stale or cleared until rebound | L1 |
| T04 | Unavailable content | 404 or timeout | Fetch | Show unavailable and last verified snapshot if present | L1 |
| T05 | Oversized `data:` URI | Valid `data:` URI over policy byte limit | Fetch | Block and record policy violation | L1 |
| T06 | Active-content `data:` URI | `data:text/html` or scriptable SVG | Fetch and render | Reject active rendering and show policy warning | L1 |
| T07 | Feedback spam burst | 10k events emitted cheaply | Index and render | Throttling and quotas keep system usable | L2 |
| T08 | `appendResponse()` spam | 5k third-party responses | Render | Gated display, no UI DoS, typed as third-party annotations | L2 |
| T09 | Revocation | Feedback is later revoked | Render | Prior feedback remains visible as revoked | L2 |
| T10 | `registrations[]` mismatch | Active `(agentRegistry, agentId)` absent from declared `registrations[]` | Resolve registration file | Warning or block continuity claim per policy | L2 |
| T11 | Validator conflict | Multiple validators disagree | Render | Deterministic finality output by explicit policy rule | L3 |
| T12 | Progressive validation states | Same `requestHash` receives soft and hard finality responses | Render | Show latest, final, and superseded states distinctly | L3 |
| T13 | Expired validation | Freshness window has elapsed | Render | Mark expired or stale; suppress affirmative badge | L3 |
| T14 | `agentURI` drift after validation | Validation exists, then `agentURI` changes materially | Refresh | Downgrade or stale prior validation until re-evaluated | L3 |

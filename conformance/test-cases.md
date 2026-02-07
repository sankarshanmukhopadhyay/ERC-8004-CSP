# Conformance Test Cases

| ID | Scenario | Setup | Action | Expected | Level |
|---|---|---|---|---|---|
| T01 | Registration hash mismatch | wrong hash | fetch | block + mismatch | L1 |
| T02 | Agent transfer | transfer token | refresh | control-change banner | L1 |
| T03 | Unavailable content | 404 | fetch | unavailable + cached snapshot | L1 |
| T04 | Feedback spam burst | 10k events | index | throttling active | L2 |
| T05 | appendResponse spam | 5k responses | render | gated; no DoS | L2 |
| T06 | Revocation | revoke | render | show revoked | L2 |
| T07 | Validator conflict | disagree | render | deterministic finality | L3 |
| T08 | Expired validation | stale | render | expired; no badge | L3 |

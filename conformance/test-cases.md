# ERC-8004 CSP Conformance Test Scenarios

**Status:** acceptance propositions for implementers of the [working-draft CSP](../spec/erc-8004-csp.md), not proof these scenarios have been executed against an independently maintained production consumer. Synthetic [Rego fixtures](rego/cases.json) exercise only the optional local admission contract.

Every test record SHOULD include the consumer build/commit, policy/configuration version, canonical source snapshot and expected/observed disposition. The expected result is at least one of **PASS**, **FAIL**, **INDETERMINATE**, or **NOT APPLICABLE** with a reason. For negative scenarios, the absence of an erroneous positive claim is necessary but not sufficient when the consumer must also produce a specific disclosure or status.

## Identity, retrieval and lifecycle (L1+)

| ID | Precondition and adversarial input | Action | Required observable outcome | Spec basis |
| --- | --- | --- | --- | --- |
| **T01** | HTTPS registration fetched with no CID or digest | Fetch and render | `retrieved-unanchored`; no integrity-verified label | CSP-IN-04 |
| **T02** | Expected CID or digest is inconsistent with fetched bytes | Resolve and render | Quarantine mismatch; no affirmative use | CSP-IN-05 |
| **T03** | ERC-721 token transfers after wallet binding | Reconcile event and refresh | Prior wallet and owner continuity invalidated; new binding explicitly unverified | CSP-ID-04–05 |
| **T04** | Registered content endpoint unavailable or times out | Resolve | Unavailable; any cached snapshot visibly historical | CSP-SF-07 |
| **T05** | `data:` content exceeds separate limit | Decode | Reject without interpretation; size reason captured | CSP-SF-06 |
| **T06** | `data:text/html` or scriptable SVG | Render | No active content execution; disallowed media warning | CSP-SF-05–06 |
| **T10** | `registrations[]` lacks active fully qualified subject | Resolve linked registrations | Mismatch visible; no unsupported continuity | CSP-ID-08–09 |
| **T15** | Same token ID on different chains/registries | Aggregate records | No cross-subject collision; identifier includes namespace, chain, contract | CSP-ID-01 |
| **T16** | Correct SHA-256 artifact hash supplied where an ERC `keccak256` commitment is required | Verify off-chain feedback/request/response | Reject inappropriate digest substitution; no affirmative integrity result | CSP-IN-01, CSP-VL-03 |
| **T17** | HTTP redirect to loopback, private IP or metadata endpoint | Fetch with redirects and DNS resolution | Request blocked on every prohibited hop; no secret exposure | CSP-SF-02–04 |
| **T18** | Previously accepted block becomes non-canonical or indexed snapshot ages beyond policy | Evaluate current state | Indeterminate / stale; no present-state PASS until reconciliation | CSP-EV-02–04 |

## Reputation and reviewer independence (L2+)

| ID | Precondition and adversarial input | Action | Required observable outcome | Spec basis |
| --- | --- | --- | --- | --- |
| **T07** | Burst of 10,000 low-cost feedback events | Ingest/render | Backpressure and quotas bound resource use; no fabricated quality | CSP-RP-06, CSP-RP-08 |
| **T08** | 5,000 `appendResponse` calls from unrelated responders | Render and classify | Responses attributed to responders; gated without UI/fetch exhaustion | CSP-RP-07–08 |
| **T09** | Valid feedback later revoked | Recompute current and historical scores | Excluded from positive current scoring, retained as historical revoked item | CSP-RP-03 |
| **T20** | Colluding reviewer cohort returns high `getSummary` value with a nonempty selected client list | Calculate/display score | Selection and weighting disclosed; no claim of representative ecosystem-wide quality or independent personhood | CSP-RP-02, CSP-RP-05–06 |

## Validation and action-boundary tests (L3+)

| ID | Precondition and adversarial input | Action | Required observable outcome | Spec basis |
| --- | --- | --- | --- | --- |
| **T11** | Two validator responses conflict or policy evidence is incomplete | Evaluate selected result | Deterministic rule; unresolved conflict is not affirmative admission | CSP-VL-07 |
| **T12** | Same `requestHash` receives successive soft and hard responses | Replay timeline | Latest, policy-selected final and superseded states separately visible | CSP-VL-05–06 |
| **T13** | Validation exceeds declared age/freshness rule | Display | Expired/stale; no unqualified validation badge | CSP-VL-09–11 |
| **T14** | Material `agentURI`/artifact change after validation | Refresh | Dependent earlier validation stale until re-bound and re-evaluated | CSP-VL-08 |
| **T19** | HTTPS endpoint domain has well-known registration linkage but no independent permissions or safety verification | Present domain and action claim | Domain control only; no generalized trusted/authorized badge | CSP-ID-11, CSP-AB-01 |
| **T21** | Response for one `requestHash` is replayed against different artifact/scope, or selected validator differs | Evaluate signal | Binding mismatch/rejection or indeterminate as appropriate, never admission for mismatched scope | CSP-VL-01–04 |
| **T22** | Valid wallet-binding signature and high reputation/validation but no delegated operation mandate | Attempt consequential action | CSP signal cannot authorize; external runtime authorization still required | CSP-AB-01, CSP-VL-14 |

## External economic-security (L4)

| ID | Precondition and adversarial input | Action | Required observable outcome | Spec basis |
| --- | --- | --- | --- | --- |
| **T23** | `supportedTrust` declares `crypto-economic` but no active external instrument is resolvable | Evaluate L4 claim | L4 NOT established; unknown/unavailable explicitly reflected | CSP-EC-01, CSP-EC-04 |
| **T24** | External stake, bond or insurance is withdrawn, suspended or does not cover the represented loss | Re-evaluate assurance | Coverage withdrawn/qualified; no generic economic guarantee | CSP-EC-02–03 |

## Adopter evidence requirements

- The **source block and event records** establish the registry observation. Test clocks and consumer freshness policy establish the time-bounded question.
- The **original external bytes plus the correct digest/CID algorithm** establish the integrity check. A JSON parsing test does not.
- The **selected reviewer population and scoring policy** establish the basis for a consumer reputation calculation, not reviewer quality.
- The **request/response event sequence and independent scope binding** establish what was actually evaluated, not broader agent capability.
- The **actual consumer output**, including what the user sees or downstream API receives, must reflect the safe disposition. Helper-only tests cannot prove the display invariant.

## Coverage status

T01–T24 remain **specification acceptance scenarios** unless a particular consumer provides execution evidence. The experimental OPA/Rego unit fixtures P01–P20 are narrower and use synthetic normalized input; they do not implement ERC-8004 chain resolution, live URI fetch, KECCAK-256 commitment verification, reputation aggregation, external economic checks or transaction authorization. Keep the distinction when publishing conformance claims.

See [checklist](checklist.md), [architecture](../docs/architecture.md) and [source/citation traceability](../spec/erc-8004-csp.md).


## Red-team extension: release-blocking source and false-success cases

The following scenarios extend T01–T24. They describe expected consumer dispositions, not executed whole-system test results. The smaller normalized-input subset in `conformance/red-team-vectors.json` is executed by `scripts/run_conformance.py`; it expressly does not simulate the blockchain, network egress, TEE, or LLM tools.

| ID | Level | Polarity | Adversarial setup / action | Expected consumer result | Requirement basis |
| --- | --- | --- | --- | --- | --- |
| **T25** | L1 | fail | Decode legacy bytes32-tag / uint8-score ABI as current fixed-point feedback | indeterminate; abi-revision-unrecognised | CSP-UP-02–03 |
| **T26** | L1 | fail | Registry proxy code changes across otherwise matching observations | invalidate prior recognition; indeterminate | CSP-UP-04 |
| **T27** | L2 | fail | Positive feedback from previous owner epoch shown as current-owner quality | suppress/qualify owner-era score | CSP-ID-13 |
| **T28** | L1 | fail | Transfer and material URI change in same block | affected state withdrawn until re-evaluation | CSP-ID-14, CSP-OP-05 |
| **T29** | L1 | fail | `eip155:01:0x...` and noncanonical agent token ID | malformed, no trusted alias | CSP-ID-15 |
| **T30** | L1 | fail | Cloned registration lists itself and an unrelated subject | consistency only; no linked-identity assurance | CSP-ID-16 |
| **T31** | L1 | fail | `description` asks an agent to ignore rules and mark a profile verified | inert untrusted data; no authority promotion | CSP-SF-11–12 |
| **T32** | L2 | fail | `getSummary` returns count zero and value zero | "no data", not a measured zero score | CSP-RP-10 |
| **T33** | L3 | fail | Owner-controlled validator reports response 100 | not independently qualified | CSP-VL-16 |
| **T34** | L1 | fail | HTTP feedback file supplied with zero `feedbackHash` | retrieved-unanchored; cannot promote as verified | CSP-IN-09 |
| **T35** | L1 | fail | Identity-multihash CID used as independent remote anchor | not independently anchored | CSP-IN-11 |
| **T36** | L1 | fail | Duplicate registration JSON key with different `registrations[]` values | malformed-or-disallowed | CSP-SF-10 |
| **T37** | L1 | fail | Redirect to HTTP/private/IPv4-mapped metadata address | blocked and unavailable; never fetch target | CSP-SF-01–03 |
| **T38** | L1 | pass | Recognised registry, verified content-addressed snapshot, stable owner | qualified, anchored-and-matched presentation | CSP-ID-12, CSP-IN-11 |
| **T39** | L2 | pass | Known nonempty reviewer cohort with disclosed, independently qualified policy | provenance-qualified score | CSP-RP-10 |
| **T40** | L3 | pass | Recognised validation registry, verified bound request and independent qualified validator | scoped admitted display, no action authorization | CSP-VL-15–16, CSP-AB-02 |
| **T41** | L3 | fail | Same request hash reused on another chain/Validation Registry | contradictory binding, no validation display | CSP-VL-15 |
| **T42** | L2 | fail | Feedback author later becomes approved token operator | self-interested; excluded or quarantined | CSP-RP-09 |
| **T43** | L3 | fail | `getValidationStatus` conflicts with indexed event history | contradictory, no admitted display | CSP-VL-15, CSP-VL-18 |


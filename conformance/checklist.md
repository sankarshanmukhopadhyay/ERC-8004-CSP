# ERC-8004 CSP Conformance Checklist

**Authority:** [working-draft specification](../spec/erc-8004-csp.md). This checklist summarizes its obligations and does not replace its normative text. **Claiming Lx requires every applicable prerequisite level**, and a passing unit test alone is not an independent assurance finding.

## Evidence package required for any declaration

| Evidence | Acceptance condition | Requirement |
| --- | --- | --- |
| Subject and scope | Full namespace-qualified `agentRegistry` and `agentId`, consumer role, version and supported capabilities | CSP-ID-01, CSP-CF-01 |
| Version provenance | Implementation commit, policy version/digest, evaluation date and test suite | CSP-CF-01–03, CSP-EV-01 |
| Source basis | Chain, contract, canonical block or explicit uncertainty, URI/content identifiers | CSP-EV-01–04 |
| False-success results | Negative tests demonstrate no positive claim on missing/contradictory/stale evidence | CSP-EV-02, CSP-CF-02 |
| Claim limitation | Local self-declaration vs independently assessed assurance clearly marked | CSP-CF-02–04 |

## L0: Discovery and parsing only

| Check | Required evidence | Requirement |
| --- | --- | --- |
| Do not invent trust or authorization from registry existence | Output inspection with nonempty source record and absent trust evidence | CSP-AB-01, CSP-CF-04 |
| Preserve upstream versus consumer-enriched field ownership | Traceable source-to-derived field inventory | CSP-UP-01 |

## L1: Integrity-aware identity consumption

| Check | Required evidence | Requirement |
| --- | --- | --- |
| Resolve complete canonical subject and source block | Trace including namespace, chain, contract and token | CSP-ID-01–03 |
| Reset wallet/owner continuity after transfer | T03/T15 with current and prior snapshots | CSP-ID-04–07 |
| Reclassify agentURI and inspect active registration | T10/T14, correct domain/URI scope | CSP-ID-06, CSP-ID-08–11 |
| Keep embedded, anchored, unanchored, mismatch and unavailable distinct | T01/T02/T04 and digest/CID evidence | CSP-IN-01–07 |
| Enforce constrained fetch and inert media rendering | T05/T06/T17 plus redirect/all-hop network policy | CSP-SF-01–09 |
| Fail closed on indexer uncertainty and reorganization | T18 | CSP-EV-01–04 |

## L2: Sybil-aware reputation

| Check | Required evidence | Requirement |
| --- | --- | --- |
| Fixed-point signed values and revocation respected | Input/output showing scaling and revoked status | CSP-RP-01–03 |
| `getSummary` client-set provenance exposed | Nonempty source cohort or policy/digest | CSP-RP-02 |
| Scoring policy and exclusions inspectable | Weighting and freshness disclosure | CSP-RP-04–06 |
| No false independence/credential-derived personhood | Collusion and misleading reviewer tests | CSP-RP-05–06 |
| Third-party annotation differentiated; flood bounded | T07–T09 | CSP-RP-07–08 |

## L3: Validation-meaningful

| Check | Required evidence | Requirement |
| --- | --- | --- |
| Bind request and response with correct KECCAK-256 commitment | T16, T21; source event, exact bytes | CSP-IN-01, CSP-VL-01–03 |
| Threshold/method/scope interpretation explicitly local | Method policy, validator, subject and artifact references | CSP-VL-04, CSP-VL-09–11 |
| Progressive response and conflict resolution deterministic | T11/T12, sorted history and policy rule | CSP-VL-05–07 |
| Expiry, URI drift and indeterminate states not shown as positive | T13/T14/T18 | CSP-VL-08, CSP-VL-11–12 |
| Rego use, if claimed, bounded to display admission | Schema and actual-engine tests, adapter identity binding | CSP-VL-13–14 |

## L4: Externally economically secured

| Check | Required evidence | Requirement |
| --- | --- | --- |
| Active external instrument and scope established | External contract/rule version, beneficiary and effective state | CSP-EC-01–02 |
| Withdrawal/suspension and loss coverage distinguishable | T23/T24, lifecycle/revocation evidence | CSP-EC-02–03 |
| No L4 promotion from registry status alone | Negative fixture with `supportedTrust` only | CSP-EC-04 |

## Disposition

Each check should report **PASS**, **FAIL**, **INDETERMINATE**, or **NOT APPLICABLE** with evidence and reason. An INDETERMINATE or unexplained NOT APPLICABLE cannot satisfy an affirmative level claim. Conformance evidence must be produced by an actual consumer implementation; the repository's experimental Rego integration does **not** certify L3 or L4 consumers.

See [test cases](test-cases.md), [architecture](../docs/architecture.md) and the [upstream traceability matrix](../spec/erc-8004-csp.md).


## Red-team convergence checks for the candidate profile

The [red-team resolution record](../docs/red-team-resolution-2026-11.md) tracks the source review, implementation and still-unevidenced external boundaries.

| Level | Acceptance evidence | Consumer/implementation obligation | Representative case |
| --- | --- | --- | --- |
| L0 | Both a discovery-only positive and an authority-laundering negative | Parsing a registry entry never permits execution | T44/T45 |
| L1 | Registry pin and recognition evidence, ABI/code migration, owner epoch, strict parser and same-byte display | Unknown revisions, code swaps and unsafe source inputs cannot become affirmative | T25/T26/T28/T31/T34–38 |
| L2 | Source-cohort and owner-epoch records; explicit zero-count treatment | Colluding, absent or self-interested reviews cannot form an unqualified quality score | T27/T32/T39/T42 |
| L3 | Chain- and registry-scoped request binding, latest-state reconciliation, competence conflict evidence | Owner-chosen validator responses and cross-chain hashes cannot create permanent assurance | T33/T40/T41/T43 |
| L4 | Effective external mechanism, coverage scope and value-at-risk at reliance time | Expired or withdrawn exposure cannot establish current economic security | T23/T24/T46/T47 |

**Execution distinction:** T01–T47 remain descriptive end-to-end acceptance scenarios. A bounded subset is represented by [normalized red-team vectors](red-team-vectors.json) and run through [the deterministic harness](../scripts/run_conformance.py). Green tests provide only local synthetic-input decision evidence. Full on-chain/HTTP/model/runtime/TEE or independent-conformance evidence remains unestablished. The [requirements index](requirements.json) must not convert scenario linkage to PASS.

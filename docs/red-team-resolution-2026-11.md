# Red-team review disposition and evidence register (2026-11-14)

**Source:** `csp-red-team-review.md`, reviewed against the CSP working draft on 2026-11-14.  
**Tracker:** [Issue #10](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/issues/10).  
**Historical alignment:** [Issue #4](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/issues/4), [PR #5](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/pull/5), [PR #6](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/pull/6), [PR #8](https://github.com/sankarshanmukhopadhyay/ERC-8004-CSP/pull/8).  
**Interpretation:** Requirements below are CSP consumer obligations. The pinned Draft ERC-8004 is authoritative for its registry interface; this repository does not certify deployed registries, consumers or external economic mechanisms.

## Disposition legend

- **Specified:** A required behavior is defined in the working-draft specification but not necessarily implemented in a real consumer.
- **Bounded-tested:** A local deterministic parser, schema, hash or **normalized asserted-evidence** decision has executable coverage. This is not a live integration test.
- **External-evidence gap:** The repository cannot produce independent on-chain/network/agent-system evidence for this control.
- **Deferred design option:** Adding the proposed feature would alter architecture without being needed to resolve a concrete defect.

## Mapping of review findings to remedies

| Review | Remediation | Executable evidence | Remaining assurance boundary |
| --- | --- | --- | --- |
| **U-01/U-02** | Pinned [ERC-8004 commit and blob](../spec/upstream-erc8004-pin.json), recorded ABI/revision obligations, offline anchor tests; repaired section-symbol corruption | `tests/test_upstream_pin.py`; Pages link checks | No deployed registry ABI independently attested; external links can change |
| **U-03/U-04** | CSP-ID-12/UP-04 recognized chain/registry/code tuple and re-recognition after upgrade | T25/T26 normalized status | Live proxy/registry reads not implemented |
| **U-05/U-06** | CSP-EV-05/06 chain-specific finality, provenance, independent-check options | Source-finality negative fixture | No L1/L2 settlement verifier or independent RPC confirmation |
| **I-01/I-02** | CSP-ID-13/14 and OP-05 owner epochs, withdrawal and bounded reassessment | T27, normalized owner-epoch fixture | Actual chain replay and local tombstone enforcement reside in adopter |
| **I-03/I-04** | Owner, token operator, current wallet state and historical role checks specified | Descriptive checklist | No on-chain allowance/approval history resolver |
| **I-05/I-06** | CSP-ID-15 canonical EVM identifier and arbitrary precision; URI `updatedBy` audit | `tests/test_red_team.py` subject parser | Upstream string representation verified; non-EVM namespaces out of scope |
| **I-07/I-08** | CSP-ID-16 distinguishes self-consistency from cross-registration verification; domain-control qualification and shared-host caveat | T30 normalized fixture | Near-duplicate semantic detection/domain-origin control unimplemented |
| **I-09** | CSP-ID-17 forbids inferring liveness from `active`, `x402Support` or service fields | Requirement inspection | No service endpoint liveness test |
| **S-01/S-02/S-03** | CSP-IN-08–10 exact verified bytes, zero-commitment meaning and EVM Keccak (not SHA3) | `tests/test_red_team.py` uses actual Keccak vectors; T34 | Does not fetch actual ERC off-chain content |
| **S-04/S-05/S-06** | CSP-IN-11 CID/DAG restrictions; scheme/SSRF connect-time requirements | URI literal preflight test; T35/T37 disposition fixtures | No live CID verifier, network sandbox or DNS/redirect integration |
| **S-07/S-08/S-09/S-10** | CSP-SF-10–12 strict parser and lower-trust model content; precedence and resource limits | Duplicate key, nonfinite, UTF-8 and depth rejection; T31/T36 status fixtures | No live prompt-injection/tool-boundary or display/inert renderer test |
| **R-01/R-02/R-03** | CSP-RP-09/10 owner/operator conflicts, reviewer selection and zero-count no-data | T32/T42/T39 synthetic decision fixtures | No payment graph/reviewer identity proof |
| **R-04/R-05/R-06** | CSP-RP-11/12 unit scaling, tag consistency, wash-trading limits and counter conventions | Descriptive conformance obligations | No real scoring implementation |
| **V-01/V-02** | CSP-VL-15/16 registry-scoped request identity and qualified validator independence | T33/T41/T40 synthetic decision fixtures | No live `getValidationStatus`, validator-controller or TEE evidence |
| **V-03/V-04/V-05/V-06/V-07** | CSP-VL-17–19 summary/source-count, hash admission, event history reconciliation and TEE/zk limits | T43 fixture plus documented acceptance cases | No cryptographic TEE/zk verifier nor event history reconciliation implementation |
| **E-01** | CSP-EC-05/06 value-at-risk, exposure and effective-time checks | T46/T47 normalized exposure assertions | No enforceable bond/insurance/stake proof |
| **C-01/C-02** | Existing generated [requirement index](../conformance/requirements.json) enriched with minimum level, keyword strength, per-ID source pin and declared test class; T01–T47 and normalized fixtures | `scripts/generate_spec_requirements.py`; `scripts/run_conformance.py`; CI | The 47 prose cases are **not** fully executed against a consumer; descriptive coverage is not conformance |
| **C-03/C-04/C-05** | Domain outcomes and reasons explicitly separated; [schema-valid illustrative evidence record](../examples/evidence-record.v0.10.0.json); RFC 8785 policy-digest rule | JSON Schema example check | Canonical RFC 8785 serializer not implemented by the synthetic harness |
| **C-06/C-08/C-09** | CSP-CF-05/06 validity and lapse; L0 T44/T45; CSP-AB-02 `authorization:not-evaluated` | Synthetic positive/negative cases at L0–L4 | No production consumer claim certification |
| **C-07** | **Deferred design option:** orthogonal track labels | Not applicable | Retain cumulative L0–L4 until actual adopter demand |
| **G-01** | Additive [candidate policy 0.10.0 schema](../policy/policy-v0.10.0.schema.json) and example; retain [v0.9.1 legacy schema](../policy/policy.schema.json) unchanged | JSON Schema validation of old/new examples | Configuration is not runtime enforcement |
| **G-02/G-03/G-04** | Document breaking embedded URI interpretation, explicit version separation and adapter namespace/Keccak distinction | Version assertions in CI, negative cases | Legacy consumer migrations need downstream adopter-specific verification |
| **P-01–P-08** | Repair section symbols, front matter, stable ID split, schema-valid example, composite claim constraint, tightened URI invalidation and claim-record MUST | Pages/link, pin and schema tests | Remaining editorial crosswalk improvement must retain source ownership |

## Execution contract and reproducibility

Run on Python 3.12+ with pinned test dependencies:

```sh
python -m pip install 'jsonschema==4.23.0' 'pycryptodome==3.23.0'
python -m unittest tests.test_red_team tests.test_spec_traceability tests.test_upstream_pin -v
python scripts/run_conformance.py --output /tmp/csp-red-team-report.json
python scripts/generate_spec_requirements.py
```

The runner reports a **local author-supplied normalized-fixture** execution class. It does not use an Ethereum RPC, inspect deployed source code, fetch a URI, execute a real model or validate an independent economic mechanism. Its outcome is never a certification of L1–L4 production behavior. Separate `opa` invocation and existing CI continue to cover the optional Rego policy; no claim of complete CSP policy-engine integration is made.

## Release and issue boundaries

The red-team convergence work is tracked under #10. Issue #4's earlier **upstream-mapping and bounded Rego feasibility/implementation** criteria are already satisfied by #5/#6/#8, and should be closed with a link to #10 rather than redefined as requiring a full ERC-8004 consumer stack.

The v0.10.0 **working-draft specification milestone** is published under tag v0.10.0 with explicit limitations; Pages remains a derived view of `main`. Requirements that only have descriptive fixtures or inspection checks cannot be represented as passed full-stack conformance; no external deployer, independent reviewer or release acceptance is fabricated.

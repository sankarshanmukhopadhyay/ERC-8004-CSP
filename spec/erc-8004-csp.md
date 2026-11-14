# ERC-8004 Consumer Security Profile (CSP)

**Specification:** Consumer Security Profile for ERC-8004  
**Document state:** working-draft revision, **not** an issued release  
**Published baseline:** CSP v0.9.1 (2026-03-07)  
**Audience:** implementers of wallets, directories, indexers, marketplaces, explorers and relying applications  
**Upstream:** [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004) (**Draft**); ERC-721, EIP-712 and ERC-1271  
**Repository authority:** this document specifies *consumer behavior only*. It cannot change Ethereum registry contracts or establish external recognition, delegation or certification.

> **Status and compatibility.** This is a substantially expanded successor candidate to the published v0.9.1 text. It preserves the L0–L4 model and the existing v0.9.1 JSON consumer-policy schema as compatibility baselines. New requirement identifiers and more precise security interpretations are proposed here for review. Until explicitly versioned and released, the prior tag remains the published version. An implementation MUST NOT claim the revised profile or any level solely because its configuration file validates.

## 1. Purpose, authority and interpretation

### 1.1 Problem statement

ERC-8004 standardizes registry interfaces and observable signals for the identity, reputation and validation of agents. It does **not** establish an objective reputation score, universal validation result, safe endpoint, authorized principal, or permission to execute a particular operation. Consumer software that conflates those propositions can produce a convincing but unsupported assurance claim. CSP places checkable obligations on the *consumer* of these registry records, while retaining the upstream semantics of the records themselves. See [ERC-8004, Abstract, Motivation and Specification](https://eips.ethereum.org/EIPS/eip-8004#specification) and [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations).

A conforming consumer distinguishes (1) registry existence and current chain state; (2) artifact location and byte integrity; (3) claimed capabilities or trust-model support; (4) reputation observations and the policy that selects/weights them; (5) validation responses linked to specific requests, validators, scope and time; (6) consumer admission decisions; and (7) external action authorization. A positive result in one layer MUST NOT be converted into a positive result in a later layer without the distinct evidence required for that proposition.

### 1.2 Normative language and authority precedence

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by [RFC 2119 `1](https://www.rfc-editor.org/rfc/rfc2119#section-1) and [RFC 8174 `2](https://www.rfc-editor.org/rfc/rfc8174#section-2) only when capitalized. Requirement IDs of the form **CSP-XX-NN** designate *local* requirements; they are **not** identifiers in ERC-8004. Where this profile explains upstream facts, the upstream specification governs them. Where CSP imposes stricter filtering, display or operational rules, this document governs only consumers claiming CSP conformance. Upstream changes are reviewed, not silently imported.

**Document conventions.** Clauses carrying a CSP requirement ID are normative for the stated consumer conformance level. Supporting explanation, examples, illustrative JSON, non-BPC-14 statements and crosswalk commentary are informative unless explicitly incorporated by a requirement. The profile's primary conformance target is a **registry-signal consumer**; an indexer, wallet, marketplace or explorer declares this target only for the operations it actually performs. The source-derived [requirement index](../conformance/requirements.json) assists traceability but is subordinate to this Markdown specification, and its descriptive test mappings are **not** execution evidence.

Normative dependencies: [ERC-8004, Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry), [Reputation Registry](https://eips.ethereum.org/EIPS/eip-8004#reputation-registry), [Validation Registry](https://eips.ethereum.org/EIPS/eip-8004#validation-registry); [ERC-721, Specification](https://eips.ethereum.org/EIPS/eip-721#specification); [EIP-712, Specification](https://eips.ethereum.org/EIPS/eip-712#specification); [ERC-1271, Specification](https://eips.ethereum.org/EIPS/eip-1271#specification). Informative consumer-security references include [RFC 3986 ``3, 6, 7](https://www.rfc-editor.org/rfc/rfc3986), [RFC 9110 `15](https://www.rfc-editor.org/rfc/rfc9110), and [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html). References to these external standards do not assert that all of their requirements have been independently tested here.

### 1.3 Scope and explicit exclusions

CSP covers chain-state interpretation, safe retrieval and representation of associated registration/feedback/validation content, control-change continuity, Sybil-aware reputation consumption, meaningful validation display, policy disclosure, operational resilience and privacy. It does not prescribe Ethereum consensus, alter upstream contract functions, define validator slashing/economics, require an agent to use a particular communication protocol, resolve legal liability, or issue execution authorization. **CSP-AB-01:** A consumer MUST NOT treat ERC-8004 identity, reputation, validation, endpoint-domain control, an `agentWallet` binding or `supportedTrust` declaration as a sufficient grant to execute an agent action.

The action-enforcement system, if present, must separately determine the authorizing principal, delegation chain, permitted operation and target, temporal and contextual constraints, approval state and revocation. The CSP may supply evidence to that system, never substitute for it.

### 1.4 Terminology

| Term | Meaning in this profile |
| --- | --- |
| **registry subject** | The pair (`agentRegistry`, `agentId`) resolved on a specific chain. |
| **agentRegistry** | ERC-8004 namespace-qualified identifier (`{namespace}:{chainId}:{identityRegistry}`), **not** merely a contract address. |
| **source observation** | Registry event or contract-state read, identified by chain, contract, block and retrieval method. |
| **consumer policy** | Locally governed selection, risk, freshness, display and admissibility rules; not an upstream standard. |
| **anchored content** | Bytes linked to an independently checked content-addressed identifier or verified digest. |
| **embedded content** | Bytes embedded in a `data:` URI; their identity follows the on-chain URI observation, but this alone is not a separately established external digest. |
| **current determination** | Consumer decision over an explicitly identified evaluation time and source snapshot. |
| **historical observation** | What a source showed at a specified historical block; not necessarily current validity or historical authorization. |
| **indeterminate** | The available evidence does not establish the required proposition; never equivalent to PASS. |
| **assurance claim** | A bounded consumer assertion with subject, scope, method, issuer/validator, time, evidence and policy provenance. |

## 2. Upstream registry contract and the consumer boundary

### 2.1 Identity Registry

ERC-8004 identifies agents by the namespace-qualified `agentRegistry` and numeric ERC-721 `agentId`. The owner may transfer the token; ERC-721 provides `Transfer` and ownership/approval mechanisms. `agentURI` resolves to an agent registration file and can change by `setAgentURI`; the URI may use HTTPS, IPFS or embedded `data:`. Agents can declare multiple services and optional `supportedTrust` values. Endpoint-domain proof via `/.well-known/agent-registration.json` is optional and supports a *domain-control* assertion, not endpoint safety or the accuracy of advertised capabilities. Sources: [ERC-8004, Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry), [Agent URI and Agent Registration File](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file), [Endpoint Domain Verification](https://eips.ethereum.org/EIPS/eip-8004#endpoint-domain-verification-optional), [ERC-721 `Specification](https://eips.ethereum.org/EIPS/eip-721#specification).

ERC-8004 reserves `agentWallet`, initially binds it to the owner, requires proof of control to change it, and clears it on transfer. EIP-712 supplies typed data hashing/signing and domain separation but does not itself provide replay protection; ERC-1271 supplies contract signature verification whose result can depend on contract state or time. A wallet-control check cannot by itself establish delegated action scope. Sources: [ERC-8004, On-chain metadata](https://eips.ethereum.org/EIPS/eip-8004#on-chain-metadata), [EIP-712, domainSeparator and Security Considerations](https://eips.ethereum.org/EIPS/eip-712#security-considerations), [ERC-1271 `Specification](https://eips.ethereum.org/EIPS/eip-1271#specification).

### 2.2 Reputation Registry

ERC-8004 feedback is submitted by a `clientAddress` with signed fixed-point `value` (`int128`) and `valueDecimals` (0–18), optional tags, endpoint and optional off-chain `feedbackURI` with KECCAK-256 `feedbackHash`. The on-chain `feedbackIndex` is associated with the submitting client and agent. Feedback can be revoked using `revokeFeedback`. Anyone may append a response using `appendResponse`, so a response's presence is not evidence of agreement or independent adjudication. `getSummary(agentId, clientAddresses, tag1, tag2)` requires a *nonempty selected* client set; the set and tags determine the resulting summary. Sources: [ERC-8004, Giving Feedback](https://eips.ethereum.org/EIPS/eip-8004#giving-feedback), [Revoking Feedback](https://eips.ethereum.org/EIPS/eip-8004#revoking-feedback), [Appending Responses](https://eips.ethereum.org/EIPS/eip-8004#appending-responses), [Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions), [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations).

### 2.3 Validation Registry

ERC-8004 `validationRequest(validatorAddress, agentId, requestURI, requestHash)` identifies a designated validator and request payload commitment (`keccak256`). `validationResponse(requestHash, response, responseURI, responseHash, tag)` is submitted by the designated validator. The response value ranges from 0 to 100, and the validator can update the same request repeatedly. The optional `responseURI` and `responseHash` convey off-chain evidence and its commitment. `getValidationStatus(requestHash)` provides a stored status; the upstream protocol does not impose universal pass/fail thresholds, validator selection, finality tags or external economic security. Sources: [ERC-8004, Validation Request](https://eips.ethereum.org/EIPS/eip-8004#validation-request), [Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response), [Validation Registry Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions-1).

**CSP-UP-01:** Consumers MUST distinguish upstream on-chain fields from inferred/off-chain enrichments such as methodologyURI, artifact digest, scope tags, confidence, economic security and local finality. These additions MUST carry their own evidence or policy provenance and MUST NOT be represented as mandatory upstream fields.

## 3. Consumer architecture and evidence lifecycle

The minimum logical pipeline is **chain resolver → event/state reconciler → constrained artifact fetcher → integrity/semantic parser → consumer policy evaluator → risk presentation or downstream API → evidence/audit record**. These can be combined into fewer deployments, but their trust boundaries remain distinct. Source contracts are upstream; the local consumer policy is repository-controlled; external action authorization belongs to its own competent authority.

**CSP-EV-01:** Every consequential decision at L1+ MUST identify the subject (chain, registry, token), relevant canonical block or explicitly uncertain observation, observation/evaluation time, source and content identifiers, policy version or configuration digest, and decision outcome. **CSP-EV-02:** Consumers MUST distinguish a missing field, unavailable source, unresolved chain finality, contradictory evidence, failed check and established negative. **CSP-EV-03:** A replay or reorganization affecting the selected source snapshot MUST invalidate or re-evaluate dependent current-state decisions. **CSP-EV-04:** Historical evidence MAY remain available for audit but MUST be labelled as historical, with the observation block separated from current validity and from authorization at a past time.

An indexer-generated summary is a derived view; it is never an additional authoritative registry. This applies to cached `agentURI` content, selected reputation sets, validation statuses, display ratings and stored Rego execution records.

### 3.1 Example consumer evidence record (informative)

```json
{
  "subject": {"agentRegistry": "eip155:1:0x1111111111111111111111111111111111111111", "agentId": "42"},
  "source": {"chainId": 1, "blockNumber": 123456, "blockHash": "0x...", "finality": "confirmed-by-consumer-policy"},
  "content": {"uri": "https://example.org/agent.json", "integrityState": "retrieved-unanchored"},
  "decision": {"kind": "registration-display", "status": "qualified", "policyVersion": "consumer-policy-id"},
  "evidenceState": "observed",
  "note": "Illustrative shape, not an upstream ERC or versioned CSP schema"
}
```

The example's block hash is deliberately abbreviated and is **not** an input accepted by a published schema. Implementers MUST NOT infer a canonical JSON evidence API from this example. If such an API is standardized later, it requires its own contract and conformance vectors.

## 4. Conformance model and claims

CSP levels are cumulative: **L0** parsing/discovery; **L1** safe retrieval, integrity classification and control-change awareness; **L2** Sybil-aware, provenance-bearing reputation treatment; **L3** request-bound, method-/scope-aware validation; **L4** evidence-qualified external economic security. These levels are **consumer self-declaration criteria**, not proof that the agent, registry, validator or consumer has been independently certified.

| Level | Consumer requirement | What a level cannot establish |
| --- | --- | --- |
| **L0** | Parse upstream fields and distinguish registry data from consumer inference. | Content integrity, safety, quality or authorization. |
| **L1** | All applicable identity, retrieval and lifecycle requirements in ``5–7. | Meaningful reputation or validation. |
| **L2** | L1 plus provenance, selection, weighting, anti-spam and revocation in `8. | Independent trust in the selected clients. |
| **L3** | L2 plus request/response linkage, method, scope, temporal and conflict policy in `9. | Universal validator quality or runtime action authority. |
| **L4** | L3 plus independently inspectable evidence for a specified external economic mechanism in `10. | An ecosystem-wide security guarantee or legal certification. |

**CSP-CF-01:** A consumer claiming level Lx MUST satisfy all applicable requirements at Lx and below and identify the supported profile version, implementation revision, evaluation date, test evidence and limitations. **CSP-CF-02:** A JSON policy document or successful unit test MUST NOT alone constitute a conformance assertion. **CSP-CF-03:** If a capability at a declared level is inapplicable, the claim MUST record why; omission or failure is not converted to PASS. **CSP-CF-04:** L0 consumers MUST NOT display scalar reputation, validation, integrity or economic assurance as established facts merely because the registry exposes values.

## 5. Identity, ownership, control and continuity (L1+)

### 5.1 Canonical identifiers and state

**CSP-ID-01:** Consumers MUST preserve the full `agentRegistry` namespace, chain ID and contract address plus `agentId` in identifiers, cache keys and audit records; token ID alone or contract address alone is insufficient. **CSP-ID-02:** Consumers MUST resolve ownership, registered URI and wallet-binding state against an explicit block reference or communicate why present state cannot be determined. **CSP-ID-03:** Consumers MUST distinguish agent owner, ERC-721 approved operator, service endpoint operator and `agentWallet` controller. Neither shared addresses nor an approval event establishes a general mandate outside its upstream semantics. Sources: [ERC-8004, Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry), [ERC-721, Specification](https://eips.ethereum.org/EIPS/eip-721#specification).

### 5.2 Transfer, wallet rebinding and agentURI

**CSP-ID-04:** Following ERC-721 `Transfer`, consumers MUST treat prior owner-linked continuity indicators as superseded and any old `agentWallet` binding as cleared until current registry state establishes a new binding. **CSP-ID-05:** A consumer MUST NOT infer new owner-controlled wallet proof from an earlier EOA or ERC-1271 verification. **CSP-ID-06:** When `agentURI` changes, consumers MUST reclassify retrieval and integrity and re-evaluate any validations whose assessed artifact or endpoint could have changed. **CSP-ID-07:** A pending or unresolved chain reorganization MUST prevent affirmative presentation of present owner/wallet/URI state. Sources: [ERC-8004, On-chain metadata](https://eips.ethereum.org/EIPS/eip-8004#on-chain-metadata), [Update agentURI](https://eips.ethereum.org/EIPS/eip-8004#update-agenturi).

An ordinary URI change is not automatically proof that the agent is malicious. It is a provenance and scope break requiring reassessment. For EIP-712 wallet-control verification, consumers MUST preserve which typed domain, chain, verifying contract and expiration/deadline were actually verified; for ERC-1271, the verification result may change as the contract state changes. These are preconditions for claiming verified wallet control, not claims of action delegation.

### 5.3 Registration-file claims and cross-registry continuity

**CSP-ID-08:** When `registrations[]` is available, an L1 consumer SHOULD and an L2+ consumer MUST check that its active (`agentRegistry`, `agentId`) pair is declared, treating a mismatch as a continuity warning. **CSP-ID-09:** Other entries in `registrations[]` MUST remain *claims* until each registry/token reference is resolved independently; they do not prove common ownership or a shared legal entity. **CSP-ID-10:** Absent or empty `supportedTrust` MUST be interpreted as discovery only. Nonempty `supportedTrust` MUST be treated as advertised intent or support, not independently demonstrated quality. **CSP-ID-11:** Endpoint-domain verification based on `/.well-known/agent-registration.json` MUST be labelled proof of domain control only; it MUST NOT imply secure endpoint behavior, valid DID ownership or delegated operation authority. Sources: [ERC-8004, Agent Registration File](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file), [Endpoint Domain Verification](https://eips.ethereum.org/EIPS/eip-8004#endpoint-domain-verification-optional).

## 6. Content integrity, provenance and semantic classification (L1+)

Consumers often see three independently different things: an on-chain reference, retrieved bytes and a claim about those bytes. The link between them is specific to the URI, hash and observation, and does not by itself establish source legitimacy or harmlessness.

### 6.1 Integrity states

| State | Evidence required | Required consumer treatment |
| --- | --- | --- |
| **anchored-and-matched** | A content-addressed identifier or committed digest was independently checked against the observed bytes. | MAY display with source/provenance qualification; still apply safety and semantic checks. |
| **embedded-in-verified-URI** | Bytes decode from the observed on-chain `data:` URI; source block was verified. | MUST disclose embedded provenance; MUST NOT imply an independently verified off-chain digest. |
| **retrieved-unanchored** | Retrieval succeeded but no binding digest/content identifier exists. | MUST label unanchored; MUST NOT call content integrity-verified. |
| **mismatch** | Retrieved bytes fail the applicable hash/CID check. | MUST quarantine and block normal affirmative use. |
| **unavailable** | Target cannot currently be resolved or retrieved. | MUST retain unavailable status; MAY display a clearly historical verified snapshot. |
| **malformed-or-disallowed** | Invalid payload, disallowed scheme/media type, size or syntax. | MUST block active interpretation and provide safe diagnostic metadata only. |
| **indeterminate** | Cannot verify source block, CID resolution or digest algorithm. | MUST NOT convert uncertainty into integrity PASS. |

The prior v0.9.1 wording called embedded `data:` content “cryptographically anchored.” This revision makes the narrower, more defensible assertion: embedded bytes are *bound to the observed on-chain URI*, while independent authenticity, source finality and safety remain separate checks. This is a **semantic clarification with potential compatibility impact** for consumers that previously collapsed both states. See [ERC-8004, Agent URI](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file); [RFC 3986 `7, Security Considerations](https://www.rfc-editor.org/rfc/rfc3986#section-7).

### 6.2 Digest and scheme-specific checks

**CSP-IN-01:** Consumers MUST use the upstream-specified hash algorithm for each committed field: `feedbackHash`, `responseHash` and `requestHash` are KECCAK-256 commitments under ERC-8004. An implementation-specific `sha256:` artifact digest used by the optional Rego prototype is a **separate local evidence identifier** and MUST NOT be presented as equivalent to those on-chain commitments. **CSP-IN-02:** A CID-based check MUST verify that resolved bytes correspond to the expected CID under the applicable content-addressing semantics; an arbitrary gateway HTTP 200 is insufficient. **CSP-IN-03:** A `data:` URI MUST be decoded strictly, subjected to media-type and size policy, and attributed to the verified on-chain URI snapshot. **CSP-IN-04:** A plain HTTPS URI without a binding digest MUST remain unanchored, even when TLS and the HTTP response succeed. Sources: [ERC-8004, Giving Feedback](https://eips.ethereum.org/EIPS/eip-8004#giving-feedback), [Validation Request](https://eips.ethereum.org/EIPS/eip-8004#validation-request), [Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response).

**CSP-IN-05:** If a commitment is present, consumers MUST validate bytes before interpreting the referenced content as evidence. A digest match proves only that the checked bytes satisfy that commitment; it MUST NOT be treated as proof of truthful claims, policy compatibility, validator independence or safe execution. **CSP-IN-06:** Consumers MUST record enough hash algorithm, encoding, raw-byte and source-reference information to reproduce a consequential integrity determination. **CSP-IN-07:** Cache entries for mutable/unanchored HTTPS and immutable/content-addressed objects MUST NOT share a namespace that obscures the distinction.

## 7. Safe retrieval, rendering and resource controls (L1+)

**CSP-SF-01:** All externally supplied URIs MUST pass a scheme allowlist and a bounded parser before fetch. HTTPS, IPFS (through controlled resolution) and limited `data:` are the baseline forms; unsupported schemes MUST be inert, not executed. **CSP-SF-02:** Fetchers MUST bound redirect depth, total bytes (including decompression), deadline, recursion, response processing and memory. **CSP-SF-03:** HTTP redirect targets and all resolved addresses MUST be rechecked against network policy, including DNS rebinding, link-local, loopback, metadata-service, private and otherwise forbidden destinations; TLS success does not override this check. **CSP-SF-04:** Resolver and gateway failures MUST produce unavailable/indeterminate outcomes, not a fabricated anchor match. **CSP-SF-05:** Consumers MUST NOT execute HTML, JavaScript, SVG script, active media or arbitrary referenced instructions from a registration, feedback or validation file. Sources: [ERC-8004, Agent URI](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file), [RFC 3986 `7](https://www.rfc-editor.org/rfc/rfc3986#section-7), [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

**CSP-SF-06:** `data:` media types MUST be explicitly allowlisted with a separate strict byte limit and inert parsing; unknown or active types MUST be rejected. **CSP-SF-07:** Consumers SHOULD preserve a last verified snapshot when permitted by policy, but MUST disclose its historic observation time and MUST NOT substitute it for current evidence. **CSP-SF-08:** Transport and parser logs MUST avoid leaking credentials, sensitive headers or unnecessary full response bodies. **CSP-SF-09:** Content security measures MUST apply equally to endpoints advertised through A2A, MCP, DID or other service descriptions; an advertised protocol label is not a network-safety exception.

For resource exhaustion, rate-limit per subject, source, endpoint and fetch host; schedule external retrieval away from privileged interactive threads; apply retry budgets, bounded queues and backpressure. This is a *consumer operational requirement*, not an ERC-8004 contract rule.

## 8. Reputation admission, selection and interpretation (L2+)

### 8.1 Record semantics and selected client population

**CSP-RP-01:** A consumer MUST preserve the identity and chain of the `clientAddress`, the agent/feedback index, signed `value`, `valueDecimals`, applicable tags, observation block and revocation state. Display or calculation MUST NOT silently discard the sign or decimal scaling. **CSP-RP-02:** A `getSummary` result MUST be accompanied by the selected nonempty `clientAddresses` set or a stable, inspectable definition and digest of the selection policy. A summary without that provenance MUST NOT be presented as a universal agent rating. **CSP-RP-03:** Revoked feedback MUST be excluded from affirmative current scoring unless an explicit, disclosed historical query requires it; audit records SHOULD retain the revoked entry as a historical event. Sources: [ERC-8004, Giving Feedback](https://eips.ethereum.org/EIPS/eip-8004#giving-feedback), [Revoking Feedback](https://eips.ethereum.org/EIPS/eip-8004#revoking-feedback), [Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions).

### 8.2 Weighted scoring and false independence

**CSP-RP-04:** L2+ consumers publishing a score MUST disclose the weighting/selection policy, freshness window, omitted or excluded classes, and an explanation of what the score measures; they SHOULD include a confidence or coverage indication. **CSP-RP-05:** Weighting MAY incorporate observed age, independently qualified evidence, stake or past reliability, but MUST NOT turn possession of a DID/VC, a payment record, stake or a KYC label into a claim of unique humans or honesty without separate evidence. **CSP-RP-06:** Consumer policy MUST address correlated or economically controlled reviewer sets and repeated submissions, for example by group caps, diversity rules, source quotas or explicit uncertainty labels. **CSP-RP-07:** Consumers MUST treat `appendResponse` as material attributable to the `responder` address, not as a first-party correction or independently accepted adjudication. **CSP-RP-08:** Rate limits MUST prevent events and response URIs from producing uncontrolled ingestion, rendering or external-fetch amplification. Sources: [ERC-8004, Appending Responses](https://eips.ethereum.org/EIPS/eip-8004#appending-responses), [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations).

### 8.3 Permitted claims by level

L1 may display counts, signed values, tags and chronology with no implied quality score. L2 may publish a policy-qualified score. L3 may add *separate* validation overlays but MUST NOT aggregate validation and reputation into an undifferentiated badge. L4 may add an external economic-security assertion only under `10. These are boundaries on **presentation**, not on what the upstream registry stores.

## 9. Validation admission, history and presentation (L3+)

### 9.1 Request/response binding

**CSP-VL-01:** An L3+ consumer MUST bind a reported validation to the exact `requestHash`, designated validator address, `agentId` and identity registry, the verified request payload commitment, and the observed response event or stored status. **CSP-VL-02:** When the assessed artifact, service operation, endpoint, scope or methodology is derived off chain, consumers MUST establish and record that linkage separately; `requestHash` alone does not universally encode a CSP-specific scope. **CSP-VL-03:** Consumers MUST verify applicable KECCAK-256 request/response content commitments before promoting off-chain material into evidence. **CSP-VL-04:** The validator's `response` of 0–100 MUST NOT be interpreted as a universal PASS percentage or certification; thresholds and semantics belong to a declared consumer/validator methodology. Sources: [ERC-8004, Validation Request](https://eips.ethereum.org/EIPS/eip-8004#validation-request), [Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response).

### 9.2 Update, finality and contradiction

**CSP-VL-05:** Consumers MUST preserve successive responses to the same `requestHash` with event ordering, block identity, response values, tags and `lastUpdate` or equivalent source evidence. **CSP-VL-06:** Consumers MUST distinguish the *latest observed response*, the *response admitted by the declared local finality rule*, and *superseded/historical responses*. Upstream support for progressive updates does not itself imply a universal hard-finality state. **CSP-VL-07:** A consumer MUST define deterministic conflict handling and MUST NOT treat a contradictory or unresolved finality condition as admitted. **CSP-VL-08:** A materially changed `agentURI` or assessed artifact MUST stale, qualify or invalidate dependent validation displays until the exact relationship is re-established. Sources: [ERC-8004, Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response), [Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions-1).

### 9.3 Validator governance and bounded display

**CSP-VL-09:** An L3+ consumer MUST maintain a validator-selection policy (allowlist, weighted allowlist or open-with-downranking as the existing schema permits), supported methodology, scope, freshness window and conflict rule. **CSP-VL-10:** Each affirmative user-facing validation claim MUST disclose or make directly inspectable the validator, assessed subject/artifact, purpose/scope, methodology, relevant request, freshness and underlying decision-policy identity. **CSP-VL-11:** Missing, unverifiable, stale, conflicting or insufficiently bound validation evidence MUST NOT produce an unqualified “validated” badge. **CSP-VL-12:** An apparent lack of adverse responses MUST NOT be used as affirmative validation evidence.

The method URI, scope tags, validator weights and selected finality rule are **CSP-side interpretation/configuration**, not fields required by ERC-8004's `validationResponse` ABI. See [ERC-8004, Validation Registry](https://eips.ethereum.org/EIPS/eip-8004#validation-registry).

### 9.4 Optional executable Rego evaluation boundary

The repository's [Rego example and execution contract](../docs/executable-rego-policy.md) evaluate **one** consumer-side operation: admission of a previously normalized validation signal for display. The JSON Schema input uses a split numeric `chain_id` and address-valued `agent_registry`, plus a local SHA-256 artifact digest; these are **local adapter fields**, *not* a wire-compatible representation of the upstream namespace-qualified `agentRegistry` and KECCAK-256 `requestHash` commitment. The adapter MUST construct and verify an unambiguous relationship to the upstream identifier before invoking a policy. It must not overwrite upstream identifiers or invent an on-chain SHA-256 artifact commitment.

**CSP-VL-13:** A consumer MAY use Rego or another deterministic decision engine, but MUST maintain the source-verification boundary and return affirmative, negative and indeterminate outcomes distinctly. **CSP-VL-14:** Successful execution, output schema validation or locally generated digest records MUST NOT be described as proof of canonical chain state, independent assurance, action authorization or qualified validators. The currently published Rego policy and fixtures are experimental and do not establish L3 conformance for any production consumer.

## 10. External economic-security evidence (L4)

ERC-8004 expressly leaves validator incentives and slashing to the chosen validation protocol. **CSP-EC-01:** An L4 consumer MUST identify the actual external mechanism, its governing rules, eligible principals, covered scope, stake/bond/insurance asset and applicable loss or claim conditions; merely advertising `crypto-economic` or `tee-attestation` in `supportedTrust` is insufficient. **CSP-EC-02:** It MUST establish evidence of the external mechanism's effective state at the relevant time, including suspension, withdrawal, revocation, depletion, expiry or material governance changes. **CSP-EC-03:** It MUST distinguish *economic exposure evidenced* from *guaranteed recourse*; numeric stake or coverage without enforceability and scope evidence MUST NOT be used as a universal protection claim. **CSP-EC-04:** A consumer MUST NOT derive L4 compliance from an on-chain validation response without separately resolving the external economic protocol. Sources: [ERC-8004, Validation Registry](https://eips.ethereum.org/EIPS/eip-8004#validation-registry), [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations).

## 11. Indexer reliability, privacy and disclosure

**CSP-OP-01:** Consumers MUST bound per-agent/source ingestion and external-fetch work, handle duplicate events idempotently, and reconcile reorganizations without silently retaining obsolete current states. **CSP-OP-02:** Consequential policy decisions MUST be traceable to an event/state source and versioned policy without requiring unnecessary storage of sensitive content. **CSP-OP-03:** Consumers SHOULD expose freshness, availability, conflict and upstream/source provenance in UI and machine-readable API results. **CSP-OP-04:** Consumers SHOULD disclose exclusions, reviewer-set selection, weights and validator concentration when these affect ranking or admission.

**CSP-PR-01:** Consumers MUST avoid presenting personal or sensitive content embedded in public off-chain files by default without an appropriate classification and suppression policy. **CSP-PR-02:** They MUST distinguish deletion of local caches from irrevocable on-chain pointers or externally retained copies; no promise of complete deletion is supportable from cache purge alone. **CSP-PR-03:** They SHOULD minimize retention of per-user interaction data, limit analytics correlation and disclose unavoidable on-chain linkability. **CSP-PR-04:** A query to a third-party gateway or validation endpoint SHOULD be evaluated for disclosure of the user's interest in an agent or artifact.

## 12. Conformance evidence and falsification

### 12.1 Claim record

A claim of a CSP level SHOULD include: repository/ref, profile version, implementation commit, consumer-policy file/digest, independent chain/evidence resolver identity, evaluation block/time, supported functions, test-case IDs and results, missing/unimplemented features, and a statement of reviewer independence. A green CI run only establishes what that workflow actually executed. Synthetic Rego fixture success is **not** verified on-chain interoperability.

### 12.2 Minimum negative and boundary tests

| Test family | Failure deliberately exercised | Required observation | Requirement basis |
| --- | --- | --- | --- |
| T01–T06 | Unanchored/mismatched/unavailable/unsafe bytes | Correct integrity state; no unsafe execution | CSP-IN-01–07, CSP-SF-01–09 |
| T03, T10 | Control transfer, wallet reset, registration mismatch | New owner never inherits stale wallet or cross-registry trust | CSP-ID-01–11 |
| T07–T09 | Sybil flood, third-party responses, revocation | No manufactured reputation; recorded suppression | CSP-RP-01–08 |
| T11–T14 | Conflicting, progressive, expired and drifted validation | No false permanent badge | CSP-VL-01–12 |
| T15–T18 | Wrong chain, wrong digest algorithm, unverified indexer and reorg | No affirmative derived trust determination | CSP-EV-01–04, CSP-IN-01 |
| T19–T22 | Invalid trust-model claim, methodology mismatch, absent scope and approval substitution | No claim stronger than available evidence; no action authorization | CSP-AB-01, CSP-VL-01–14 |
| T23–T24 | Inactive economic-security mechanism; unqualified external coverage | No L4 assurance | CSP-EC-01–04 |

See [conformance test cases](../conformance/test-cases.md), [checklist](../conformance/checklist.md), and the source-derived [machine-readable requirement index](../conformance/requirements.json). The tests are written as executable acceptance propositions for implementers; only the Rego-specific fixtures currently have actual-engine CI execution in this repository. Do not infer implemented full-stack conformance from the presence of test descriptions.

### 12.3 Adversarial example: validity laundering

An indexer sees a registered ERC-721 token and valid `agentWallet` signature, then accepts a high numeric feedback summary from a colluding selected client set and a validator `response=100` for an unrelated task. A directory marks the agent “verified and authorized for payments.” Each upstream record may be correctly formed while the combined assertion is invalid. The correct output separates registry subject identity, wallet control, provenance-limited reputation, request-specific validator response and an **unevaluated authorization** proposition. Even a perfect upstream signature or hash cannot provide the missing mandate.

### 12.4 Adversarial example: temporal false success

A consumer caches an anchored registration file and a successful validation; the agent changes `agentURI`, the NFT transfers and the indexer misses a reorg. The old digest may still match its old bytes. The consumer MUST label the evidence as historical, MUST NOT show current wallet continuity, and MUST re-evaluate validation scope and source finality before any current positive display. Integrity is not freshness.

## 13. Compatibility, implementation contracts and migrations

The published `policy/policy.schema.json` remains fixed to `version: 0.9.1` with the established identity, safeFetch, reputation, validation and disclosure blocks. This revision does **not** modify that schema or its example. The optional `policy/rego/input.schema.json` and `output.schema.json` separately use contract version `1.0.0` and are not replacements for the comprehensive consumer-policy schema. A consumer cannot infer full CSP conformance from successful execution of the Rego sample.

**Compatibility-sensitive clarifications:** (i) full namespace-qualified `agentRegistry` identity must not be conflated with the Rego adapter's address-only field; (ii) embedded `data:` URI bytes require source-block validation and must not be mislabelled as independent digest verification; (iii) KECCAK-256 on-chain commitments are distinct from local SHA-256 evidence identifiers; (iv) unknown or stale source state cannot become PASS. These refinements may require migration for downstream systems relying on the broader v0.9.1 wording. This revision therefore merits an explicit **new versioned compatibility baseline if adopted**, not a silent replacement of the published v0.9.1 tag.

### 13.1 Consumer-policy schema mapping and its limits

The current [consumer-policy schema](../policy/policy.schema.json) expresses some, but not all, obligations in this working draft. The schema version remains `0.9.1`, and a syntactically valid policy still needs a real consumer implementation, independently verified source evidence and an assurance result. The mappings below identify relevant fields rather than claiming automatic enforcement:

| Existing v0.9.1 configuration | Consumer obligation | Evidence not established by schema validation |
| --- | --- | --- |
| `identity.requireCurrentRegistrationLink` | CSP-ID-08–09 | On-chain pair and independently resolved linked registrations |
| `identity.requireWalletReverificationAfterTransfer`, `showWalletBindingStatus`, `showWalletVerificationType` | CSP-ID-03–07 | Actual ownership, transfer sequence and cryptographic verification at an identified block |
| `identity.treatMissingSupportedTrustAsDiscoveryOnly` | CSP-ID-10 | Whether any advertised trust model has external supporting evidence |
| `safeFetch.allowedSchemes`, `timeoutMs`, `maxBytes`, `followRedirects`, `maxRedirects`, `dataUriPolicy` | CSP-SF-01–09 | Enforcement at each redirect, DNS/network destination, decompression and rendering boundary |
| `safeFetch.cache.separateUnanchoredCache` | CSP-IN-07 | Integrity algorithm, source snapshot and content classification correctness |
| `reputation.weighting`, `rateLimits`, `display` | CSP-RP-01–08 | Reviewer independence, numeric scaling, actual rate limits, revocation state and selection provenance |
| `validation.bindToRequestHash`, `requireScopeMethodFreshness`, `invalidateOnAgentUriChange` | CSP-VL-01–04, CSP-VL-08 | Verified KECCAK-256 linkage and independent artifact/scope binding |
| `validation.finalityRule`, `validatorPolicy`, `showSupersededResponses` | CSP-VL-05–12 | Historical event chronology, validator qualification, conflict governance and latest canonical state |
| `disclosures.*` | CSP-CF-01–04, CSP-VL-10–11 | Whether public claims match the actual evaluated evidence |
| **No existing field** for independent economic mechanism verification | CSP-EC-01–04 | L4 effective state, scope and enforceability |
| **No existing field** for runtime delegated authority | CSP-AB-01 | Action permission remains the responsibility of an external enforcement system |

This table intentionally avoids adding fields to `policy/policy.schema.json` in a documentation-driven PR. Consumers that cannot represent a required obligation in that configuration MUST implement or evidence it through a separately documented enforcement mechanism, and MUST NOT count absence of a schema field as proof that the requirement is inapplicable.

### 13.2 Claim outcomes

For a consequential proposition, **admitted** means the selected consumer policy and required evidence support *that bounded proposition*; **denied** means an established disqualifying condition applies; **indeterminate** means evidence is missing, unavailable, stale, contradictory or insufficient to decide. An `indeterminate` status MUST NOT be displayed or passed downstream as an affirmative claim. A consumer implementation SHOULD retain reason codes and source/policy identities for independent reproduction. The Rego prototype demonstrates this pattern for a single validation-display operation; it does not define a universal CSP API or action-authorization result.

No backward-incompatible change to existing JSON Schema field types is made here. An integration migration is needed only if the adopter previously collapsed the distinctions above, promoted unsupported trust assertions, or requires the expanded normative controls. Preserve historical claims under the version originally evaluated.

## 14. Traceability to upstream authority

The anchors below are intended to support independent source review. **“Local” means CSP derives a consumer protection decision; the upstream specification is not claimed to contain the CSP rule verbatim.**

| Local requirement family | Normative upstream basis | Consumer-specific derivation |
| --- | --- | --- |
| CSP-ID-01–03 | [ERC-8004 Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry); [ERC-721 Specification](https://eips.ethereum.org/EIPS/eip-721#specification) | Preserve full identity and operator/control distinctions. |
| CSP-ID-04–07 | [ERC-8004 On-chain metadata](https://eips.ethereum.org/EIPS/eip-8004#on-chain-metadata); [EIP-712 Specification](https://eips.ethereum.org/EIPS/eip-712#specification); [ERC-1271 Specification](https://eips.ethereum.org/EIPS/eip-1271#specification) | Invalidate stale bindings and preserve verification context. |
| CSP-ID-08–11 | [Agent Registration File](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file); [Endpoint Domain Verification](https://eips.ethereum.org/EIPS/eip-8004#endpoint-domain-verification-optional) | Cross-check claims without manufacturing recognition. |
| CSP-IN-01–07 | [Giving Feedback](https://eips.ethereum.org/EIPS/eip-8004#giving-feedback); [Validation Request](https://eips.ethereum.org/EIPS/eip-8004#validation-request); [Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response) | Compare exact bytes/algorithms; separate integrity from truth. |
| CSP-SF-01–09 | [Agent URI](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file); [RFC 3986 `7](https://www.rfc-editor.org/rfc/rfc3986#section-7) | Prevent attacker-controlled URI execution and fetch amplification. |
| CSP-RP-01–08 | [Reputation Registry](https://eips.ethereum.org/EIPS/eip-8004#reputation-registry); [Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions); [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations) | Bound selected-client population, Sybil assumptions and revocation. |
| CSP-VL-01–14 | [Validation Registry](https://eips.ethereum.org/EIPS/eip-8004#validation-registry); [Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response) | Request-/artifact-specific method, freshness and finality rules. |
| CSP-EC-01–04 | [ERC-8004 Validation Registry](https://eips.ethereum.org/EIPS/eip-8004#validation-registry); [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations) | Require external economic evidence rather than infer L4 from ERC. |
| CSP-EV, CSP-OP, CSP-PR, CSP-AB, CSP-CF | [ERC-8004 Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations); [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119); [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) | Local governance, evidence, presentation, privacy and assurance boundaries. |

### 14.1 Machine-readable requirement index

[conformance/requirements.json](../conformance/requirements.json) is generated from the unique normative CSP requirement IDs in this document and mapped to any corresponding descriptive T01–T24 scenarios. It records `descriptive-scenario-only` separately from `inspection-required`; neither represents an executed conformance test. [scripts/generate_spec_requirements.py](../scripts/generate_spec_requirements.py) is the deterministic generator, and CI fails when the generated index no longer matches the normative source. The prose text remains authoritative in cases of conflict.

## 15. References and change governance

**Primary normative upstream:**

1. [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004), **Draft**; particularly the [Identity](https://eips.ethereum.org/EIPS/eip-8004#identity-registry), [Reputation](https://eips.ethereum.org/EIPS/eip-8004#reputation-registry), [Validation](https://eips.ethereum.org/EIPS/eip-8004#validation-registry) and [Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations) sections.
2. [ERC-721: Non-Fungible Token Standard, Specification](https://eips.ethereum.org/EIPS/eip-721#specification).
3. [EIP-712: Typed Structured Data Hashing and Signing, Specification](https://eips.ethereum.org/EIPS/eip-712#specification), especially domain separation and replay-attack considerations.
4. [ERC-1271: Standard Signature Validation Method for Contracts, Specification](https://eips.ethereum.org/EIPS/eip-1271#specification).
5. [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels, `1](https://www.rfc-editor.org/rfc/rfc2119#section-1); [RFC 8174: Ambiguity of Uppercase vs Lowercase, `2](https://www.rfc-editor.org/rfc/rfc8174#section-2).

**Informative retrieval and security context:** [RFC 3986: URI Generic Syntax ``6–7](https://www.rfc-editor.org/rfc/rfc3986); [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110); [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

**Local companion material:** [Architecture](../docs/architecture.md), [Threat model](../docs/threat-model.md), [Upstream alignment](../docs/upstream-alignment-2026-11.md), [Rego implementation](../docs/executable-rego-policy.md), [Conformance checklist](../conformance/checklist.md), [Test scenarios](../conformance/test-cases.md).

This repository must treat ERC-8004 and adjacent upstream standards as external authorities, retain source/citation provenance for material requirements, and reassess local consumers when upstream registry semantics change. Changes to CSP requirement meaning, conformance levels, evidence interpretation or published schemas require a versioned release decision and explicit migration notes; simple editorial changes need not cause new releases.

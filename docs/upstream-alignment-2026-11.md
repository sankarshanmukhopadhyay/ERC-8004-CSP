# ERC-8004 Upstream Alignment and CSP Source Traceability

**Reviewed:** 2026-11-14. **Upstream status:** [ERC-8004 is Draft](https://eips.ethereum.org/EIPS/eip-8004).  
**Local scope:** consumer-security requirements only; the [revised CSP working draft](../spec/erc-8004-csp.md) is not an upstream ERC amendment or published new version.

## Traceability of source semantics to consumer obligations

| Upstream reference and exact section | Source-defined proposition | Local derivation and section | Interoperability caveat |
| --- | --- | --- | --- |
| [ERC-8004: Identity Registry](https://eips.ethereum.org/EIPS/eip-8004#identity-registry) | Subject is (`agentRegistry` namespace string, `agentId` token) and control follows ERC-721 | CSP `5 `CSP-ID-01–07` | Token ID alone and address-only lookup are not globally unique |
| [ERC-721: Specification](https://eips.ethereum.org/EIPS/eip-721#specification) | Transfer and operator approval are token-specific | CSP `5, `CSP-ID-03–05` | Approval does not establish third-party action mandates |
| [ERC-8004: Agent URI and Registration File](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file) | HTTPS/IPFS/data URI, service claims, registrations and optional supportedTrust | CSP ``5–7, `CSP-ID-08–11` | Registration and supportedTrust declarations are not independently verified assurances |
| [ERC-8004: Endpoint Domain Verification](https://eips.ethereum.org/EIPS/eip-8004#endpoint-domain-verification-optional) | Optional well-known registration proves endpoint-domain association | CSP `5.3 `CSP-ID-11` | Domain control is not endpoint safety or delegated authorization |
| [ERC-8004: On-chain metadata](https://eips.ethereum.org/EIPS/eip-8004#on-chain-metadata) | `agentWallet` is reserved, signature-bound, cleared on transfer | CSP `5.2 `CSP-ID-04–07` | Wallet-control evidence is not consent to any particular operation |
| [EIP-712: Specification](https://eips.ethereum.org/EIPS/eip-712#specification), [Security Considerations](https://eips.ethereum.org/EIPS/eip-712#security-considerations) | Typed data and domain binding; signing standard does not supply replay protection automatically | CSP `5.2 | Consumer must record exact domain, deadline and context |
| [ERC-1271: Specification](https://eips.ethereum.org/EIPS/eip-1271#specification) | Contract wallet can verify signature; result can depend on state/time | CSP `5.2 | Cannot treat an old signature result as permanent |
| [ERC-8004: Giving Feedback](https://eips.ethereum.org/EIPS/eip-8004#giving-feedback) | Signed fixed-point value and optional KECCAK-256 `feedbackHash` | CSP ``6, 8 `CSP-IN-01`, `CSP-RP-01` | Raw numeric values and local SHA-256 digests are not interchangeable |
| [ERC-8004: Revoking Feedback](https://eips.ethereum.org/EIPS/eip-8004#revoking-feedback), [Appending Responses](https://eips.ethereum.org/EIPS/eip-8004#appending-responses) | Clients revoke; anyone may append response | CSP `8 `CSP-RP-03,07` | An annotation is not authenticated adjudication |
| [ERC-8004: Read Functions](https://eips.ethereum.org/EIPS/eip-8004#read-functions) | `getSummary` selects nonempty `clientAddresses` | CSP `8 `CSP-RP-02–06` | Selection governs summary meaning and Sybil exposure |
| [ERC-8004: Validation Request](https://eips.ethereum.org/EIPS/eip-8004#validation-request) | Designated validator and KECCAK-256 `requestHash` | CSP `9 `CSP-VL-01–03` | Local methodology/scope bindings are additional, not upstream fields |
| [ERC-8004: Validation Response](https://eips.ethereum.org/EIPS/eip-8004#validation-response) | Value 0–100; repeated response on one request; optional evidence hash | CSP `9 `CSP-VL-04–12` | Neither universal threshold nor finality implied |
| [ERC-8004: Security Considerations](https://eips.ethereum.org/EIPS/eip-8004#security-considerations) | Sybil exposure and external validator economics | CSP ``8, 10–12 | Economic guarantees and authorization require separate evidence |

## Important semantic deltas from CSP v0.9.1

1. **Namespace fidelity:** upstream `agentRegistry` is the full namespace-qualified string. The experimental Rego input's `subject.agent_registry` is currently an address-only adapter field; `subject.chain_id` is separate and there is no explicit namespace field. A resolver/adapter must verify the mapping, not describe the Rego input as upstream wire shape.
2. **Digest algorithms:** `feedbackHash`, `requestHash` and `responseHash` use ERC-8004 KECCAK-256 commitments, while the Rego sample's `sha256:` digest is a local artifact reference. The two are not substitutes.
3. **Data URI integrity:** embedded content is bound to the verified observed URI and may be immutable within that snapshot; it is not automatically an independently established digest-authenticity proof. The revised CSP distinguishes embedded provenance from external content anchoring.
4. **Validation semantics:** `methodologyURI`, `scopeTags`, weight, finality and confidence are consumer or validator methodology concerns, not mandatory `validationResponse` ABI arguments.
5. **Evidence uncertainty:** reorganization, stale indexers, missing bytes, conflicting signals and absent delegation stay separately representable and cannot become an affirmative consumer or execution decision.

These are **local interpretive and compatibility decisions**, not changes to ERC-8004. See [CSP `13](../spec/erc-8004-csp.md) and [release assessment](release-assessment-2026-11.md).

## Authority and historical-state principle

An on-chain record establishes a bounded source observation. An indexer gives a derived view; a consumer policy supplies a separate interpretation; a runtime authorization engine needs a separate principal mandate. A historical observation, the state effective at a particular time and a present determination are distinct questions. Never infer one from another without source/time/lifecycle evidence.

## Related implementation and test evidence

- [Rego evaluator](executable-rego-policy.md) implements *normalized validation-display admission only*.
- [Architecture](architecture.md) identifies the resolver-to-policy boundary.
- [Conformance cases](../conformance/test-cases.md) provide 24 local falsification scenarios, but the full set is **not** currently executable in this repository.
- [Consumer policy schema](../policy/policy.schema.json) remains the released v0.9.1 policy configuration contract.

Reference authority remains with [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004), [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [EIP-712](https://eips.ethereum.org/EIPS/eip-712), and [ERC-1271](https://eips.ethereum.org/EIPS/eip-1271). An upstream draft revision needs a fresh applicability review rather than an automatic local normative update.


## Immutable upstream revision and applicability

This CSP candidate is based on **ethereum/ERCs commit [503591a6](https://github.com/ethereum/ERCs/blob/503591a6e80e6e1affdd6403341e25269141f046/ERCS/erc-8004.md)**, Git blob SHA \`7653a80922c0bf0243669f30e7a2d4aabfe006aa\`, reviewed on 2026-11-14 while ERC-8004 remained a Draft. The [upstream pin manifest](../spec/upstream-erc8004-pin.json) records its section anchors, which are checked in CI. Floating EIP URLs are informative convenience links; they do not silently replace the pinned version.

**Registry deployment conformance is not implied by a source pin.** An implementer must independently establish chain, Identity/Reputation/Validation Registry addresses, linked Identity Registry (where exposed), ABI revision, code/proxy implementation and source-block evidence. Earlier ERC drafts may use a different ABI; legacy records require an explicitly governed adapter and cannot be decoded as this revision by assumption.

**Specific protocol distinctions clarified by the red-team review:**
- The [pinned Giving Feedback section](https://github.com/ethereum/ERCs/blob/503591a6e80e6e1affdd6403341e25269141f046/ERCS/erc-8004.md#giving-feedback) prohibits owner/operator feedback at submission; consumer scoring also needs the relevant *current* owner/operator conflict view after transfers.
- The [pinned Feedback hash](https://github.com/ethereum/ERCs/blob/503591a6e80e6e1affdd6403341e25269141f046/ERCS/erc-8004.md#giving-feedback) supports optional zero commitment for content-addressed URIs; CSP locally requires verified CID/DAG integrity before evidence promotion. For non-content-addressed sources, an absent hash cannot establish byte integrity.
- The [pinned Validation Request](https://github.com/ethereum/ERCs/blob/503591a6e80e6e1affdd6403341e25269141f046/ERCS/erc-8004.md#validation-request) is created by an owner/operator choosing the validator, so independent validation quality cannot be inferred from contract success.
- The [pinned Validation Read Functions](https://github.com/ethereum/ERCs/blob/503591a6e80e6e1affdd6403341e25269141f046/ERCS/erc-8004.md#read-functions-1) report latest request status, not immutable historical independent evidence.
- A **consumer-local** \`sha256:\` artifact/policy digest and the source's \`keccak256\` request/content commitment are not interchangeable.

CSP's new §§16–22 requirements are consumer-derived obligations, not new upstream MUST clauses. See the [generated individual-requirement index](../conformance/requirements.json), which now carries the upstream source pin and descriptive/inspection evidence status.

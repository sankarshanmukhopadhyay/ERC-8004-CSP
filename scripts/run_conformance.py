#!/usr/bin/env python3
"""Bounded *synthetic normalized-evidence* CSP consumer-policy harness.

No blockchain/RPC, HTTP fetcher, KECCAK implementation, validator, or LLM is
executed here. This deliberately tests only the disposition of normalized
assertions supplied by a fixture author. It cannot certify a consumer.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "conformance/red-team-vectors.json"

def canonical_digest(data: dict) -> str:
    # Deterministic test-record digest only. Not RFC8785/JCS or a chain hash.
    return "sha256:" + hashlib.sha256(
        json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()

def evaluate(signal: dict) -> dict:
    """Return disposition of *asserted* normalized evidence; no source verification."""
    category = signal.get("kind")
    evidence = signal.get("evidence", {})
    if category not in {"identity", "integrity", "reputation", "validation"} or not isinstance(evidence, dict):
        return {"status": "indeterminate", "reason_codes": ["UNSUPPORTED_INPUT"], "authorization": "not-evaluated"}

    negative, unknown = set(), set()
    # Registry/ABI/chain assumptions affect every affirmative evaluation.
    for key, reason in (
        ("recognized_registry", "UNRECOGNIZED_REGISTRY"),
        ("supported_abi", "ABI_REVISION_UNRECOGNIZED"),
        ("code_unchanged", "REGISTRY_IMPLEMENTATION_CHANGED"),
    ):
        state = evidence.get(key)
        if state is False: negative.add(reason)
        elif state is not True: unknown.add("UNVERIFIED_" + key.upper())
    if evidence.get("source_finality") != "verified":
        unknown.add("SOURCE_FINALITY_UNVERIFIED")
    if evidence.get("injected_instruction") is True:
        # Prompt injection is never trusted instruction, even in an otherwise
        # admissible registration. The fixture is expected to show suppression.
        negative.add("UNTRUSTED_INSTRUCTION")

    if category == "identity":
        if evidence.get("canonical_subject") is False:
            negative.add("NONCANONICAL_IDENTITY")
        elif evidence.get("canonical_subject") is not True:
            unknown.add("CANONICAL_SUBJECT_UNVERIFIED")
        if evidence.get("owner_epoch_current") is False:
            negative.add("OWNER_EPOCH_CHANGED")
        elif evidence.get("owner_epoch_current") is not True:
            unknown.add("OWNER_EPOCH_UNVERIFIED")
        if evidence.get("cross_registration_verified") is False:
            negative.add("UNVERIFIED_LINKED_REGISTRATION")
        elif evidence.get("cross_registration_verified") is not True:
            unknown.add("LINKED_REGISTRATION_UNVERIFIED")

    elif category == "integrity":
        if evidence.get("json_valid") is False:
            negative.add("MALFORMED_OR_DISALLOWED")
        elif evidence.get("json_valid") is not True:
            unknown.add("JSON_VALIDITY_UNVERIFIED")
        if evidence.get("safe_endpoint") is False:
            negative.add("UNSAFE_FETCH_TARGET")
        elif evidence.get("safe_endpoint") is not True:
            unknown.add("SAFE_FETCH_UNVERIFIED")
        basis = evidence.get("integrity_basis")
        if basis == "keccak":
            if evidence.get("hash_nonzero") is not True:
                negative.add("MISSING_COMMITMENT")
            if evidence.get("exact_bytes_verified") is not True:
                unknown.add("EXACT_BYTES_UNVERIFIED")
        elif basis == "cid":
            if evidence.get("cid_method") != "verified-dag":
                negative.add("CID_NOT_VERIFIED")
        elif basis == "embedded":
            if evidence.get("uri_block_verified") is not True:
                unknown.add("EMBEDDED_URI_SOURCE_UNVERIFIED")
        else:
            negative.add("UNANCHORED_CONTENT")

    elif category == "reputation":
        count = evidence.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            unknown.add("SUMMARY_COUNT_UNVERIFIED")
        elif count == 0:
            negative.add("NO_DATA")
        if evidence.get("selection_basis") not in {"curated-allowlist", "graph-derived", "payment-evidenced-verified"}:
            negative.add("UNQUALIFIED_REVIEWER_SELECTION")
        if evidence.get("self_interested") is True:
            negative.add("SELF_INTERESTED_FEEDBACK")
        elif evidence.get("self_interested") is not False:
            unknown.add("REVIEWER_INDEPENDENCE_UNVERIFIED")
        if evidence.get("owner_epoch_current") is not True:
            negative.add("PRIOR_OWNER_EPOCH")
        if evidence.get("scale_and_tag_verified") is not True:
            unknown.add("SCALE_OR_TAG_UNVERIFIED")

    elif category == "validation":
        for key, reason in (
            ("registry_bound", "CROSS_REGISTRY_REQUEST"),
            ("request_verified", "REQUEST_COMMITMENT_UNVERIFIED"),
            ("scope_bound", "SCOPE_UNBOUND"),
            ("latest_state_consistent", "VALIDATION_STATE_CONFLICT"),
            ("validator_independent", "VALIDATOR_NOT_INDEPENDENT"),
        ):
            state = evidence.get(key)
            if state is False: negative.add(reason)
            elif state is not True: unknown.add("UNKNOWN_" + key.upper())
    # Demonstrate conservative policy precedence; observed reasons are retained.
    status = "negative" if negative else ("indeterminate" if unknown else "affirmative")
    return {"status": status, "reason_codes": sorted(negative | unknown), "authorization": "not-evaluated"}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vectors", type=Path, default=VECTORS)
    parser.add_argument("--output", type=Path, help="Write evidence report JSON")
    args = parser.parse_args()
    vectors = json.loads(args.vectors.read_text(encoding="utf-8"))
    if not isinstance(vectors, list) or not vectors:
        print("No vectors", file=sys.stderr)
        return 2
    records = []
    for v in vectors:
        observed = evaluate(v["input"])
        expected = v["expected"]
        satisfied = observed["status"] == expected["status"] and set(expected.get("reason_codes", [])) <= set(observed["reason_codes"])
        records.append({"id": v["id"], "expected": expected, "observed": observed, "test_verdict": "SATISFIED" if satisfied else "VIOLATED", "fixture_sha256": canonical_digest(v["input"])})
    report = {"execution_class": "author-supplied-normalized-fixture", "engine": "csp-reference-v1", "case_count": len(records), "satisfied": sum(v["test_verdict"]=="SATISFIED" for v in records), "violated": sum(v["test_verdict"]=="VIOLATED" for v in records), "results": records, "limitation": "Not live chain, network or independent consumer conformance evidence."}
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output: args.output.write_text(serialized, encoding="utf-8")
    else: print(serialized)
    return 0 if not report["violated"] else 1

if __name__ == "__main__":
    raise SystemExit(main())

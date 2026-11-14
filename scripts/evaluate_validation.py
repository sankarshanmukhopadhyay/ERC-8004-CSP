#!/usr/bin/env python3
"""Evaluate a normalized ERC-8004 validation signal using a real OPA process."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "policy/rego/validation.rego"
INPUT_SCHEMA = ROOT / "policy/rego/input.schema.json"
OUTPUT_SCHEMA = ROOT / "policy/rego/output.schema.json"


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def evaluate(opa: Path, policy: Path, request: dict, timeout: int = 15) -> dict:
    """Return decision + reproducibility record; never convert OPA failure to admit."""
    Draft202012Validator(json.loads(INPUT_SCHEMA.read_text())).validate(request)
    opa, policy = opa.resolve(strict=True), policy.resolve(strict=True)
    canonical = json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    version = subprocess.run(
        [str(opa), "version"], check=True, capture_output=True, timeout=timeout
    ).stdout.decode(errors="replace").strip()
    result = subprocess.run(
        [str(opa), "eval", "--format=json", "--data", str(policy),
         "--stdin-input", "data.csp.validation.decision"],
        input=canonical, check=True, capture_output=True, timeout=timeout,
    )
    document = json.loads(result.stdout)
    results = document.get("result") if isinstance(document, dict) else None
    if not isinstance(results, list) or len(results) != 1:
        raise ValueError("OPA must return exactly one expression result")
    expressions = results[0].get("expressions")
    if not isinstance(expressions, list) or len(expressions) != 1:
        raise ValueError("OPA must return exactly one expression")
    decision = expressions[0].get("value")
    Draft202012Validator(json.loads(OUTPUT_SCHEMA.read_text())).validate(decision)
    if decision["policy_version"] != request["policy_version"]:
        raise ValueError("Policy version mismatch")
    if decision["evidence_snapshot_id"] != request["evidence"]["snapshot_id"]:
        raise ValueError("Evidence snapshot mismatch")
    return {
        "decision": decision,
        "execution": {
            "engine": "OPA",
            "engine_version": version,
            "engine_sha256": sha256(opa.read_bytes()),
            "policy_sha256": sha256(policy.read_bytes()),
            "input_sha256": sha256(canonical),
            "output_sha256": sha256(result.stdout),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "execution_class": "locally-executed-unattested",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opa", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--policy", type=Path, default=POLICY)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        request = json.loads(args.input.read_text(encoding="utf-8"))
        record = evaluate(args.opa, args.policy, request)
        rendered = json.dumps(record, sort_keys=True, indent=2) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0  # DENY and INDETERMINATE are valid decisions, not process failures.
    except (OSError, ValueError, subprocess.SubprocessError, Exception) as exc:
        print(f"policy evaluation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

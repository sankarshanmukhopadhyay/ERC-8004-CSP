package csp.validation

import rego.v1

# Deliberately defective; for adversarial paired tests ONLY. Never deploy.
decision := {
    "contract_version": "1.0.0",
    "status": "admitted",
    "admit": true,
    "reason_codes": [],
    "policy_version": input.policy_version,
    "evidence_snapshot_id": input.evidence.snapshot_id,
}

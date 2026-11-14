package csp.validation

import rego.v1

# An admissible signal is a consumer display decision, never action authorization.
# Upstream evidence verification and input-schema validation are external prerequisites.

indeterminate_reasons contains "CHAIN_FINALITY_UNCERTAIN" if {
    input.evidence.chain_finality != "finalized"
}

indeterminate_reasons contains "EVIDENCE_UNVERIFIED" if {
    input.evidence.verification_status != "verified"
}

indeterminate_reasons contains "RESPONSE_CONFLICT" if {
    input.response.lifecycle == "conflicted"
}

indeterminate_reasons contains "EVIDENCE_TIMESTAMP_IN_FUTURE" if {
    input.evidence.verified_at > input.evaluation_time
}

indeterminate_reasons contains "INDEXER_SNAPSHOT_STALE" if {
    input.evaluation_time - input.evidence.verified_at > input.consumer_policy.max_index_lag_seconds
}

deny_reasons contains "REQUEST_HASH_MISMATCH" if {
    input.response.request_hash != input.request.request_hash
}

deny_reasons contains "ARTIFACT_MISMATCH" if {
    input.response.artifact_digest != input.request.artifact_digest
}

deny_reasons contains "SCOPE_MISMATCH" if {
    input.response.scope != input.request.scope
}

deny_reasons contains "VALIDATOR_NOT_ALLOWED" if {
    not allowed_validator
}

allowed_validator if {
    input.response.validator in input.consumer_policy.validators
}

deny_reasons contains "METHODOLOGY_MISMATCH" if {
    input.response.methodology_uri != input.consumer_policy.methodology_uri
}

deny_reasons contains "SCOPE_NOT_ALLOWED" if {
    not allowed_scope
}

allowed_scope if {
    input.request.scope in input.consumer_policy.allowed_scopes
}

deny_reasons contains "BELOW_THRESHOLD" if {
    input.response.value < input.consumer_policy.min_response_value
}

deny_reasons contains "VALIDATION_EXPIRED" if {
    input.evaluation_time - input.response.observed_at > input.consumer_policy.max_validation_age_seconds
}

deny_reasons contains "VALIDATION_TIMESTAMP_IN_FUTURE" if {
    input.response.observed_at > input.evaluation_time
}

deny_reasons contains "RESPONSE_SUPERSEDED" if {
    input.response.lifecycle == "superseded"
}

deny_reasons contains "REGISTRATION_CONTROL_CHANGED" if {
    input.control.state != "unchanged"
}

deny_reasons contains "CONTENT_NOT_ANCHORED" if {
    input.evidence.integrity != "anchored"
}

deny_reasons contains "EVIDENCE_SNAPSHOT_MISMATCH" if {
    input.evidence.agent_registry != input.subject.agent_registry
}

deny_reasons contains "EVIDENCE_AGENT_MISMATCH" if {
    input.evidence.agent_id != input.subject.agent_id
}

# Default indeterminate on missing input (also rejected by the schema-facing runner).
indeterminate_reasons contains "INCOMPLETE_INPUT" if {
    not input.policy_version == "1.0.0"
}

indeterminate_reasons contains "INCOMPLETE_INPUT" if {
    not input.evaluation_time
}

indeterminate_reasons contains "INCOMPLETE_INPUT" if {
    not input.evidence.snapshot_id
}

indeterminate_reasons contains "INCOMPLETE_INPUT" if {
    not input.subject.agent_registry
}

indeterminate_reasons contains "INCOMPLETE_INPUT" if {
    not input.response.validator
}

indeterminate_reasons contains "INCOMPLETE_INPUT" if {
    not input.consumer_policy.validators
}

status := "indeterminate" if {
    count(indeterminate_reasons) > 0
} else := "denied" if {
    count(deny_reasons) > 0
} else := "admitted"

reason_codes := sort(array.concat(
    [r | indeterminate_reasons[r]],
    [r | deny_reasons[r]]
))

decision := {
    "contract_version": "1.0.0",
    "status": status,
    "admit": status == "admitted",
    "reason_codes": reason_codes,
    "policy_version": input.policy_version,
    "evidence_snapshot_id": input.evidence.snapshot_id,
}

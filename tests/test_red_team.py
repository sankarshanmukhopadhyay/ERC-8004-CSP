"""Red-team regressions for local contracts and bounded evidence interpretation."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from scripts.csp_security_primitives import parse_evm_subject, strict_json_bytes, is_safe_https_literal
from scripts.run_conformance import evaluate, ROOT, VECTORS

class BoundaryTests(unittest.TestCase):
    def test_legacy_schema_and_example_still_valid(self):
        old=json.loads((ROOT/"policy/policy.schema.json").read_text())
        obj=json.loads((ROOT/"policy/example-policy.json").read_text())
        Draft202012Validator.check_schema(old)
        Draft202012Validator(old).validate(obj)
        self.assertEqual(obj["version"],"0.9.1")

    def test_synthetic_evidence_example_is_schema_valid(self):
        schema=json.loads((ROOT/"schemas/evidence-record.v0.10.0.schema.json").read_text())
        record=json.loads((ROOT/"examples/evidence-record.v0.10.0.json").read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(record)
        self.assertEqual(record["decision"]["authorization"],"not-evaluated")
        self.assertEqual(record["decision"]["status"],"indeterminate")
        self.assertEqual(record["executionClass"],"synthetic-illustration")

    def test_conformance_claim_cannot_promote_unrun_evidence(self):
        schema=json.loads((ROOT/"schemas/conformance-claim.v0.10.0.schema.json").read_text())
        obj=json.loads((ROOT/"examples/conformance-claim.v0.10.0.json").read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(obj)
        obj["claim_status"]="qualified"
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(obj)
        obj["evidence_class"]="implementation-executed"
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(obj)

    def test_v010_candidate_config_schema_and_example(self):
        schema=json.loads((ROOT/"policy/policy-v0.10.0.schema.json").read_text())
        obj=json.loads((ROOT/"policy/example-policy-v0.10.0.json").read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(obj)
        self.assertEqual(obj["version"],"0.10.0")
        obj["contentAdmission"]["reuseVerifiedBytes"]=False
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(obj)

    def test_canonical_subject_and_u256(self):
        addr="0x"+"a"*40
        self.assertEqual(parse_evm_subject(f"eip155:1:{addr}","42"),(1,addr,42))
        for registry,token in [(f"eip155:01:{addr}","42"),(f"eip155:1:{addr.upper()}","42"),
                               (f"eip155:1:{addr}","042"),(f"eip155:1:{addr}","-1"),
                               (f"eip155:1:{addr}",str(2**256))]:
            with self.subTest(registry=registry,token=token):
                with self.assertRaises(ValueError): parse_evm_subject(registry,token)

    def test_duplicate_key_nonfinite_depth_and_utf8_rejected(self):
        for value in [b'{"registrations":1,"registrations":2}',b'{"x":NaN}',b'{"x":1e309}',b'{"x":"\\ud800"}',b'\xff',
                      b'{"a":{"b":{"c":1}}}']:
            with self.subTest(value=value):
                with self.assertRaises((ValueError,UnicodeError)):
                    strict_json_bytes(value,max_depth=2)

    def test_ssrf_static_preflight(self):
        unsafe=["http://example.org","https://127.0.0.1","https://169.254.169.254",
                "https://[::ffff:169.254.169.254]","https://user:pass@example.org/",
                "https://example.org:8080/","https://10.0.0.1/","https://127.1/","https://0x7f.0x0.0x0.0x1/",
                "https://[2002:c0a8:101::]/","https://[64:ff9b::a9fe:a9fe]/"]
        for url in unsafe:
            with self.subTest(url=url): self.assertFalse(is_safe_https_literal(url))
        self.assertTrue(is_safe_https_literal("https://example.org/registration.json"))

    def test_keccak_is_not_sha3(self):
        # Actual Keccak implementation; this test does not prove correctness
        # of the full registry/RPC or URI byte-resolution path.
        import hashlib
        from Crypto.Hash import keccak
        examples=[(b"","c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
                  (b"abc","4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45")]
        for raw,want in examples:
            with self.subTest(raw=raw):
                actual=keccak.new(digest_bits=256,data=raw).hexdigest()
                self.assertEqual(actual,want)
                self.assertNotEqual(hashlib.sha3_256(raw).hexdigest(),want)

    def test_all_normalized_adversarial_cases(self):
        cases=json.loads(VECTORS.read_text())
        self.assertGreaterEqual(len(cases),20)
        seen=set()
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"],seen)
                seen.add(case["id"])
                observed=evaluate(case["input"])
                self.assertEqual(observed["status"],case["expected"]["status"])
                self.assertEqual(observed["authorization"],"not-evaluated")
                for code in case["expected"]["reason_codes"]:
                    self.assertIn(code,observed["reason_codes"])

    def test_missing_source_is_not_positive(self):
        case=json.loads(VECTORS.read_text())[0]
        data=copy.deepcopy(case["input"])
        del data["evidence"]["recognized_registry"]
        self.assertNotEqual(evaluate(data)["status"],"affirmative")

if __name__=="__main__":
    unittest.main()

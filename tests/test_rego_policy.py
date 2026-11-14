"""Exercise the OPA process through the same entry point used by consumers."""
import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from scripts.evaluate_validation import ROOT, INPUT_SCHEMA, POLICY, evaluate

FIXTURES = ROOT / "conformance/rego"
INPUT = json.loads((FIXTURES / "admissible.json").read_text())
CASES = json.loads((FIXTURES / "cases.json").read_text())


def alter(obj, path, value):
    target = obj
    for segment in path[:-1]:
        target = target[segment]
    target[path[-1]] = value


class ContractTests(unittest.TestCase):
    def test_example_validates(self):
        Draft202012Validator(json.loads(INPUT_SCHEMA.read_text())).validate(INPUT)

    def test_invalid_missing_and_out_of_range(self):
        schema = Draft202012Validator(json.loads(INPUT_SCHEMA.read_text()))
        for bad in ("missing_response", "out_of_range", "unsupported_lifecycle"):
            with self.subTest(bad=bad):
                item = copy.deepcopy(INPUT)
                if bad == "missing_response":
                    del item["response"]
                elif bad == "out_of_range":
                    item["response"]["value"] = 101
                else:
                    item["response"]["lifecycle"] = "invented"
                with self.assertRaises(ValidationError):
                    schema.validate(item)


@unittest.skipUnless(os.environ.get("CSP_OPA_BIN"), "Set CSP_OPA_BIN for real OPA integration")
class RealOpaTests(unittest.TestCase):
    def test_all_decisions(self):
        opa = Path(os.environ["CSP_OPA_BIN"])
        for case in CASES:
            with self.subTest(case=case["id"]):
                obj = copy.deepcopy(INPUT)
                for change in case["changes"]:
                    alter(obj, change["path"], change["value"])
                result = evaluate(opa, POLICY, obj)
                decision = result["decision"]
                self.assertEqual(decision["status"], case["status"])
                self.assertEqual(decision["admit"], case["status"] == "admitted")
                for code in case["reasons"]:
                    self.assertIn(code, decision["reason_codes"])
                self.assertNotIn("authorize_action", decision)
                self.assertEqual(len(result["execution"]["policy_sha256"]), 64)

    def test_paired_false_success_exposure(self):
        opa = Path(os.environ["CSP_OPA_BIN"])
        bad_input = copy.deepcopy(INPUT)
        bad_input["evidence"]["verification_status"] = "unavailable"
        safe = evaluate(opa, POLICY, bad_input)
        flawed = evaluate(opa, FIXTURES / "defective.rego", bad_input)
        self.assertEqual(safe["decision"]["status"], "indeterminate")
        self.assertFalse(safe["decision"]["admit"])
        self.assertTrue(flawed["decision"]["admit"])
        self.assertEqual(safe["execution"]["input_sha256"], flawed["execution"]["input_sha256"])
        self.assertEqual(safe["execution"]["engine_sha256"], flawed["execution"]["engine_sha256"])
        self.assertNotEqual(safe["execution"]["policy_sha256"], flawed["execution"]["policy_sha256"])

    def test_runner_cli_outputs_record(self):
        opa = Path(os.environ["CSP_OPA_BIN"])
        with tempfile.TemporaryDirectory() as path:
            output = Path(path) / "result.json"
            proc = subprocess.run(
                ["python", str(ROOT / "scripts/evaluate_validation.py"),
                 "--opa", str(opa), "--input", str(FIXTURES / "admissible.json"),
                 "--output", str(output)], capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            record = json.loads(output.read_text())
            self.assertTrue(record["decision"]["admit"])


if __name__ == "__main__":
    unittest.main()

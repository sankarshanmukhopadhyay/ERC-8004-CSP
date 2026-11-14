"""Static specification traceability guards; not normative conformance certification."""
from __future__ import annotations
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=(ROOT/"spec/erc-8004-csp.md").read_text(encoding="utf-8")
CASES=(ROOT/"conformance/test-cases.md").read_text(encoding="utf-8")
CHECKLIST=(ROOT/"conformance/checklist.md").read_text(encoding="utf-8")
README=(ROOT/"README.md").read_text(encoding="utf-8")
RELEASE=(ROOT/"docs/release-assessment-2026-11.md").read_text(encoding="utf-8")

from scripts.generate_spec_requirements import catalogue

class SpecificationTraceabilityTests(unittest.TestCase):
    def test_machine_readable_requirements_not_stale(self):
        stored=json.loads((ROOT/"conformance/requirements.json").read_text(encoding="utf-8"))
        self.assertEqual(stored,catalogue())
        self.assertEqual(len(stored["requirements"]),len({x["id"] for x in stored["requirements"]}))
        self.assertTrue(all(x["verification_status"] in (
            "descriptive-scenario-only","inspection-required") for x in stored["requirements"]))

    def test_requirement_ids_are_uniquely_declared(self):
        declared=re.findall(r"\*\*(CSP-[A-Z]{2}-[0-9]{2}):\*\*",SPEC)
        self.assertGreaterEqual(len(declared),100)
        self.assertEqual(len(declared),len(set(declared)),"Duplicate normative requirement ID")

    def test_required_families_and_levels(self):
        for family in ("CSP-AB-","CSP-UP-","CSP-EV-","CSP-CF-","CSP-ID-",
                       "CSP-IN-","CSP-SF-","CSP-RP-","CSP-VL-","CSP-EC-","CSP-OP-","CSP-PR-"):
            with self.subTest(family=family):
                self.assertIn(family,SPEC)
        for level in ("L0","L1","L2","L3","L4"):
            self.assertIn(level,SPEC)
            self.assertIn(level,CHECKLIST)

    def test_scenario_identifiers_are_complete_and_unique(self):
        ids=re.findall(r"\*\*T([0-9]{2})\*\*",CASES)
        self.assertEqual(sorted(ids),[f"{n:02d}" for n in range(1,48)])

    def test_all_upstream_registers_and_relevant_specs_cited(self):
        required=[
            "https://eips.ethereum.org/EIPS/eip-8004#identity-registry",
            "https://eips.ethereum.org/EIPS/eip-8004#reputation-registry",
            "https://eips.ethereum.org/EIPS/eip-8004#validation-registry",
            "https://eips.ethereum.org/EIPS/eip-8004#giving-feedback",
            "https://eips.ethereum.org/EIPS/eip-8004#validation-response",
            "https://eips.ethereum.org/EIPS/eip-721#specification",
            "https://eips.ethereum.org/EIPS/eip-712#specification",
            "https://eips.ethereum.org/EIPS/eip-1271#specification",
        ]
        for link in required:
            with self.subTest(link=link):
                self.assertIn(link,SPEC)

    def test_version_boundaries_remain_explicit(self):
        policy=json.loads((ROOT/"policy/policy.schema.json").read_text())
        self.assertEqual(policy["properties"]["version"]["pattern"],r"^0\.9\.1$")
        rego=json.loads((ROOT/"policy/rego/input.schema.json").read_text())
        self.assertEqual(rego["properties"]["policy_version"]["const"],"1.0.0")
        self.assertIn("published working-draft specification milestone", README)
        self.assertIn("release warranted as a published working-draft", RELEASE.lower())

    def test_false_success_guards_documented(self):
        for needle in ("KECCAK-256","indeterminate","agentRegistry","sha256:",
                       "MUST NOT treat ERC-8004 identity","reorganization"):
            with self.subTest(needle=needle):
                self.assertIn(needle,SPEC)

if __name__=="__main__":
    unittest.main()

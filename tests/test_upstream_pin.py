"""Offline upstream revision + Markdown anchor reconciliation.

These checks verify a recorded GitHub blob/heading inventory, not live HTTP,
registry code hashes, or implementation of an ABI.
"""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PIN=json.loads((ROOT/"spec/upstream-erc8004-pin.json").read_text(encoding="utf-8"))
SPEC=(ROOT/"spec/erc-8004-csp.md").read_text(encoding="utf-8")

class UpstreamTraceabilityTests(unittest.TestCase):
    def test_pinned_authority_and_blob_provenance(self):
        self.assertEqual(PIN["source"],"ethereum/ERCs")
        self.assertEqual(PIN["path"],"ERCS/erc-8004.md")
        self.assertRegex(PIN["commit"],r"^[a-f0-9]{40}$")
        self.assertRegex(PIN["blob_sha"],r"^[a-f0-9]{40}$")
        self.assertIn(PIN["commit"],SPEC)
        self.assertIn(PIN["blob_sha"],SPEC)
        self.assertIn("Draft",PIN["status"])

    def test_upstream_citations_use_valid_snapshot_anchors(self):
        pinned=set(PIN["heading_anchors"])
        refs=re.findall(
            r"https://github\.com/ethereum/ERCs/blob/([0-9a-f]{40})/ERCS/erc-8004\.md#([a-z0-9-]+)",
            SPEC,
        )
        self.assertGreaterEqual(len(refs),8)
        for sha,anchor in refs:
            with self.subTest(anchor=anchor):
                self.assertEqual(sha,PIN["commit"])
                self.assertIn(anchor,pinned)

    def test_index_entries_reference_pinned_upstream(self):
        index=json.loads((ROOT/"conformance/requirements.json").read_text(encoding="utf-8"))
        self.assertEqual(index["upstream_pin"],PIN["commit"])
        for item in index["requirements"]:
            with self.subTest(id=item["id"]):
                self.assertIn(PIN["commit"],item["upstream_ref"])
                self.assertIn(item["upstream_ref"].split("#")[-1], PIN["heading_anchors"])
                self.assertIn(item["min_level"],{"L0","L1","L2","L3","L4"})
                self.assertIn(item["derivation_class"],{"consumer-derived","restates-upstream","external-standard"})
                self.assertIn(item["verification_status"],{"inspection-required","descriptive-scenario-only"})

if __name__=="__main__":
    unittest.main()

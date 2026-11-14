"""Derive the non-normative requirement index from the canonical CSP Markdown.

The prose specification is authoritative; the generated JSON indexes stable IDs
and descriptive acceptance scenarios. Neither an index nor a scenario is a test run.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"spec/erc-8004-csp.md"
SCENARIOS=ROOT/"conformance/test-cases.md"
DEST=ROOT/"conformance/requirements.json"
ID_PATTERN=re.compile(r"\*\*(CSP-[A-Z]{2}-\d{2}):\*\*")
TEST_PATTERN=re.compile(r"^\|\s*\*\*(T\d{2})\*\*\s*\|.*$",re.M)
REF_PATTERN=re.compile(r"CSP-([A-Z]{2})-(\d{2})(?:[–-](\d{2}))?")

def expanded_refs(text: str) -> set[str]:
    output=set()
    for family,start,end in REF_PATTERN.findall(text):
        first=int(start)
        last=int(end) if end else first
        if last < first:
            raise ValueError(f"Descending requirement reference {family}-{start}–{end}")
        output.update(f"CSP-{family}-{num:02d}" for num in range(first,last+1))
    return output

def catalogue() -> dict:
    content=SOURCE.read_text(encoding="utf-8")
    scenarios=SCENARIOS.read_text(encoding="utf-8")
    heading="Document status"
    requirements=[]
    seen=set()
    for lineno,line in enumerate(content.splitlines(),start=1):
        if re.match(r"^#{2,4}\s",line):
            heading=line.lstrip("#").strip()
        for match in ID_PATTERN.finditer(line):
            req=match.group(1)
            if req in seen:
                raise ValueError(f"Duplicate requirement {req}")
            seen.add(req)
            requirements.append({"id":req,"section":heading,"source_line":lineno,
                                 "descriptive_scenarios":[],"verification_status":"inspection-required"})
    if not requirements:
        raise ValueError("No requirements found")
    scenario_refs={}
    for line in TEST_PATTERN.findall(scenarios):
        if line in scenario_refs:
            raise ValueError(f"Duplicate scenario {line}")
        scenario_refs[line]=set()
    for row in scenarios.splitlines():
        m=re.match(r"^\|\s*\*\*(T\d{2})\*\*\s*\|",row)
        if m:
            scenario_refs[m.group(1)].update(expanded_refs(row.split("|")[-2]))
    unmatched=sorted({ref for refs in scenario_refs.values() for ref in refs} - seen)
    if unmatched:
        raise ValueError(f"Scenario references unknown requirements: {unmatched}")
    for req in requirements:
        linked=sorted(case for case,refs in scenario_refs.items() if req["id"] in refs)
        req["descriptive_scenarios"]=linked
        if linked:
            req["verification_status"]="descriptive-scenario-only"
    return {
        "schema_version":"1.0.0",
        "profile_status":"unreleased-working-draft",
        "proposed_profile_version":"0.10.0",
        "canonical_specification":"spec/erc-8004-csp.md",
        "test_source":"conformance/test-cases.md",
        "assurance_statement":"Generated index; test descriptions are not executed conformance evidence.",
        "requirements":requirements
    }

def main() -> None:
    data=catalogue()
    DEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Indexed {len(data['requirements'])} source requirements")

if __name__=="__main__":
    main()

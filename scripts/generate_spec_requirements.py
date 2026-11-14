"""Derive the *non-authoritative* requirement catalogue from the canonical CSP spec.

Each row has explicit level, source pin, requirement strength and test evidence
classification. Descriptive tests and inspection procedures are NOT run evidence.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"spec/erc-8004-csp.md"
SCENARIOS=ROOT/"conformance/test-cases.md"
DEST=ROOT/"conformance/requirements.json"
PIN=json.loads((ROOT/"spec/upstream-erc8004-pin.json").read_text(encoding="utf-8"))
ID_PATTERN=re.compile(r"\*\*(CSP-[A-Z]{2}-\d{2}):\*\*")
TEST_PATTERN=re.compile(r"^\|\s*\*\*(T\d{2})\*\*\s*\|.*$",re.M)
REF_PATTERN=re.compile(r"CSP-([A-Z]{2})-(\d{2})(?:[–-](\d{2}))?")
LEVEL={"AB":"L0","UP":"L0","CF":"L0","EV":"L1","ID":"L1",
       "IN":"L1","SF":"L1","OP":"L1","PR":"L1","RP":"L2","VL":"L3","EC":"L4"}
ANCHOR={"AB":"security-considerations","UP":"specification","CF":"security-considerations",
        "EV":"specification","ID":"identity-registry","IN":"agent-uri-and-agent-registration-file",
        "SF":"agent-uri-and-agent-registration-file","OP":"security-considerations","PR":"security-considerations",
        "RP":"reputation-registry","VL":"validation-registry","EC":"validation-registry"}

def expanded_refs(text: str) -> set[str]:
    result=set()
    for family,start,end in REF_PATTERN.findall(text):
        first=int(start);last=int(end) if end else first
        if last < first: raise ValueError("Descending reference")
        result.update(f"CSP-{family}-{n:02d}" for n in range(first,last+1))
    return result

def catalogue() -> dict:
    source=SOURCE.read_text(encoding="utf-8")
    scenarios=SCENARIOS.read_text(encoding="utf-8")
    heading="Document status"
    requirements=[];seen=set()
    for lineno,line in enumerate(source.splitlines(),start=1):
        if re.match(r"^#{2,4}\s",line):
            heading=line.lstrip("#").strip()
        found=list(ID_PATTERN.finditer(line))
        for i,match in enumerate(found):
            ident=match.group(1);family=ident.split("-")[1]
            if ident in seen:raise ValueError(f"Duplicate normative ID: {ident}")
            seen.add(ident)
            clause=line[match.end():found[i+1].start() if i+1<len(found) else len(line)]
            strongest=("MUST" if re.search(r"\bMUST(?: NOT)?\b",clause)
                       else "SHOULD" if re.search(r"\bSHOULD(?: NOT)?\b",clause)
                       else "MAY" if re.search(r"\bMAY\b",clause) else "UNSPECIFIED")
            upstream="https://github.com/{}/blob/{}/{}/#{}".format(
                PIN["source"],PIN["commit"],PIN["path"],ANCHOR[family])
            # Path slash is intentionally normalized below; tests check hash-pin.
            upstream=upstream.replace(".md/#",".md#")
            requirements.append({
                "id":ident,"section":heading,"source_line":lineno,
                "min_level":LEVEL[family],"keyword":strongest,
                "derivation_class":"consumer-derived",
                "upstream_ref":upstream,
                "descriptive_scenarios":[],
                "verification_method":"inspection",
                "verification_status":"inspection-required",
            })
    if not requirements:raise ValueError("No requirements found")
    mapped={}
    for row in scenarios.splitlines():
        m=re.match(r"^\|\s*\*\*(T\d{2})\*\*\s*\|",row)
        if not m:continue
        test=m.group(1)
        if test in mapped:raise ValueError(f"Duplicate scenario {test}")
        mapped[test]=expanded_refs(row.split("|")[-2])
    missing=sorted({id for ids in mapped.values() for id in ids}-seen)
    if missing:raise ValueError(f"Unknown IDs: {missing}")
    for entry in requirements:
        cases=sorted(test for test,ids in mapped.items() if entry["id"] in ids)
        entry["descriptive_scenarios"]=cases
        if cases:
            entry["verification_method"]="descriptive-test-or-implementation-evidence"
            entry["verification_status"]="descriptive-scenario-only"
    return {
        "schema_version":"1.1.0",
        "profile_status":"published-working-draft",
        "proposed_profile_version":"0.10.0",
        "upstream_pin":PIN["commit"],
        "canonical_specification":"spec/erc-8004-csp.md",
        "test_source":"conformance/test-cases.md",
        "assurance_statement":"Generated index. Scenarios are descriptive, not executed production conformance.",
        "requirements":requirements,
    }

def main() -> None:
    output=catalogue()
    DEST.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    linked=sum(bool(row["descriptive_scenarios"]) for row in output["requirements"])
    print(f"requirements={len(output['requirements'])} descriptive={linked} inspection-only={len(output['requirements'])-linked}")

if __name__=="__main__":
    main()

import sys
import json
import requests

if len(sys.argv) < 2:
    print("Usage: python sca.py <requirements.txt>")
    sys.exit(1)

vulns = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line or '==' not in line:
            continue
        pkg, version = line.split("==")
        res = requests.post("https://api.osv.dev/v1/query", json={
            "package": {"name": pkg, "ecosystem": "PyPI"},
            "version": version
        })
        results = res.json().get("vulns", [])
        for v in results:
            vulns.append({
                "package": pkg,
                "version": version,
                "id": v["id"],
                "summary": v.get("summary", "")
            })

if vulns:
    with open("sca_results.json", "w") as out:
        json.dump(vulns, out, indent=2)
    print(json.dumps(vulns, indent=2))
    sys.exit(1)
else:
    print("No known vulnerabilities in dependencies.")
    sys.exit(0)

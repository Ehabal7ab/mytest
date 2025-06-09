import os
import re
import json
import sys

secret_patterns = [
    r'AKIA[0-9A-Z]{16}',  # AWS Access Key
    r'sk_live_[0-9a-zA-Z]{24}',  # Stripe Live Key
    r'sk_test_[0-9a-zA-Z]{16,}',  # Stripe Test Key
    r'(?i)secret[_-]?key\s*[:=]\s*["\'][A-Za-z0-9-_]{8,}["\']',
    r'(?i)password\s*[:=]\s*["\'][^"\']{6,}["\']',
    r'(?i)api[_-]?key\s*[:=]\s*["\'][A-Za-z0-9-_]{16,}["\']'
]

matches = []

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py") or file.endswith(".env"):
            with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    for pattern in secret_patterns:
                        if re.search(pattern, line):
                            matches.append({
                                "file": file,
                                "line": i,
                                "pattern": pattern,
                                "content": line.strip()
                            })

if matches:
    with open("secrets_found.json", "w") as out:
        json.dump(matches, out, indent=2)
    print("Secrets detected:")
    for match in matches:
        print(match)
    sys.exit(1)
else:
    print("No secrets found.")
    sys.exit(0)

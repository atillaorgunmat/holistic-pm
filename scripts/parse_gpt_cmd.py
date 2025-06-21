#!/usr/bin/env python3
import json, re, sys, pathlib

event_path, tasks_path = sys.argv[1], sys.argv[2]

# Load issue body from GitHub event payload
with open(event_path, "r", encoding="utf-8") as f:
    body = json.load(f)["issue"]["body"]

# Extract directive lines (UPDATE, CREATE, CLOSE, pattern:, replacement:)
lines = []
for ln in body.splitlines():
    if re.match(r"^[ \t]*(UPDATE|CREATE|CLOSE|pattern:|replacement:)", ln):
        lines.append(ln.rstrip())

# Append extracted lines to Tasks.md
if lines:
    with open(tasks_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("Appended the following lines to Tasks.md:")
    for line in lines:
        print(line)
else:
    print("No directive lines found.")
    sys.exit(0)

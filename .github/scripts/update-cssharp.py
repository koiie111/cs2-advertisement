#!/usr/bin/env python3
"""Pin the latest stable CSS API from NuGet; fail closed on lookup errors."""
import json
import os
from pathlib import Path
import re
import urllib.request

project = Path("Advertisement/Advertisement.csproj")
text = project.read_text(encoding="utf-8")
pattern = r'(<PackageReference Include="CounterStrikeSharp.API" Version=")([^"]+)(")'
match = re.search(pattern, text)
if match is None:
    raise RuntimeError("CounterStrikeSharp.API reference not found")
with urllib.request.urlopen(
    "https://api.nuget.org/v3-flatcontainer/counterstrikesharp.api/index.json", timeout=60
) as response:
    versions = json.load(response)["versions"]
stable = [v for v in versions if re.fullmatch(r"\d+\.\d+\.\d+", v)]
latest = max(stable, key=lambda v: tuple(map(int, v.split("."))))
current = match.group(2)
changed = tuple(map(int, latest.split("."))) > tuple(map(int, current.split(".")))
if changed:
    project.write_text(re.sub(pattern, lambda m: m.group(1) + latest + m.group(3), text), encoding="utf-8")
version = latest if changed else current
print(f"CounterStrikeSharp.API: {current} -> {version}")
if os.environ.get("GITHUB_OUTPUT"):
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"changed={str(changed).lower()}\nversion={version}\n")

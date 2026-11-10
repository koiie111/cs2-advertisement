"""Validate synthetic work counts and print medians; never infer native/full-tick gains."""
import json
import statistics
from pathlib import Path

root = Path(__file__).resolve().parents[2]
directory = root / "docs" / "measurements"
baseline = json.loads((directory / "offline-baseline.json").read_text(encoding="utf-8-sig"))
candidate = json.loads((directory / "offline-candidate.json").read_text(encoding="utf-8-sig"))
assert len(baseline) == len(candidate) == 33
print("| Path / online / active | Median ns baseline / candidate | Bytes/op baseline / candidate | Lookups/op baseline / candidate |")
print("|---|---:|---:|---:|")
for key in dict.fromkeys((r["path"], r["online"], r["active"]) for r in baseline):
    pairs = [[r for r in rows if (r["path"], r["online"], r["active"]) == key] for rows in (baseline, candidate)]
    for group in pairs:
        assert [r["repetition"] for r in group] == [0, 1, 2]
        for row in group:
            assert row["iterations"] == 100000
            assert row["sends"] == row["iterations"] * row["online"] * row["active"]
    times = [statistics.median(r["ns_per_operation"] for r in group) for group in pairs]
    left, right = pairs[0][0], pairs[1][0]
    print(f"| {key[0]} / {key[1]} / {key[2]} | {times[0]:.2f} / {times[1]:.2f} | "
          f"{left['bytes_per_operation']:g} / {right['bytes_per_operation']:g} | "
          f"{left['lookups_per_operation']:g} / {right['lookups_per_operation']:g} |")
print("PASS: identical send counts in all 33 baseline/candidate windows. Synthetic managed doubles only.")

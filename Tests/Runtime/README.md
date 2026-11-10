# Offline runtime checks

`dotnet run --project Tests/Runtime/Runtime.Tests.csproj -c Release`

Compiles the **production plugin sources** with deterministic managed CSS/Panorama doubles. Exercises registered tick/event/listener/command callbacks, including timer ownership and cancellation, controller replacement, map cleanup, hot reload, rejected/successful reload, language changes, bounded localization and personal Panorama state restoration. No production source conditionals or native dependencies are used. The original parser/layout suite remains separate.

The doubles model the relevant behavior of CounterStrikeSharp [Utilities](https://github.com/roflmuffin/CounterStrikeSharp/blob/v1.0.378/managed/CounterStrikeSharp.API/Utilities.cs), [BasePlugin](https://github.com/roflmuffin/CounterStrikeSharp/blob/v1.0.378/managed/CounterStrikeSharp.API/Core/BasePlugin.cs), [ConfigManager](https://github.com/roflmuffin/CounterStrikeSharp/blob/v1.0.378/managed/CounterStrikeSharp.API/Modules/Config/ConfigManager.cs) and [Timer](https://github.com/roflmuffin/CounterStrikeSharp/blob/v1.0.378/managed/CounterStrikeSharp.API/Modules/Timers/Timer.cs). They do not emulate native entity lifetime, callback ordering across plugins, TOML parsing, transport, client rendering or input arbitration. Config fixtures are created only below the test output directory. These tests cannot replace live acceptance.

Text evidence/source SHA256 values use canonical LF line endings to survive Git checkout on Windows and Linux; release binary SHA256 values always describe the exact bytes. `analyze.py` checks the evidence manifest before comparing counts.

## Same harness on baseline and candidate

From the repository root in PowerShell, with a clean baseline checkout outside the web root:

```powershell
git worktree add --detach ../advertisement-review-baseline-20261110 233c811c54144bb26c6588d2fa2781a6daed9edb
$env:DOTNET_TieredCompilation = '0'
$baselineSource = (Resolve-Path ../advertisement-review-baseline-20261110/Advertisement).Path
dotnet run --project Tests/Runtime/Runtime.Tests.csproj -c Release "-p:PluginSource=$baselineSource" -- --bench > docs/measurements/offline-baseline.json
dotnet run --project Tests/Runtime/Runtime.Tests.csproj -c Release -- --bench > docs/measurements/offline-candidate.json
python Tests/Runtime/analyze.py
```

`PluginSource` is relative to `Tests/Runtime`; an absolute path is also accepted. Baseline uses the identical driver/doubles and its unmodified plugin files. `--bench` runs tick and rotating-ad dispatch at 0/1/8/32 online, with inactive and active HTML. Each scenario gets 20,000 warm-up operations and three 100,000-operation windows. The driver verifies send counts separately from cost. `DOTNET_TieredCompilation=0` fixes JIT tier; environment details are in `docs/measurements/offline-scenario.json`.

Time and allocations include managed doubles. They omit native wrapper allocations, native call cost, timers outside the tested dispatch, background work and the engine tick. No synthetic percentage is a live gain. Read raw repetitions, not only medians; compare real-client output and full-path/full-tick percentiles on an authorized test instance before rollout.

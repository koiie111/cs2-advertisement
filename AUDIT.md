# Advertisement performance audit

Baseline: 233c811c54144bb26c6588d2fa2781a6daed9edb. Build: dotnet build Advertisement/Advertisement.csproj -c Release. Baseline builds without warnings. Existing Panorama tests fail: CSS is 24px, assertion expects 22px.

Findings: OnTick enumerates all slots even with no HTML. Message formatting unconditionally queries cvars and enumerates players per recipient. One-shot timers remain in BasePlugin.Timers. Welcome callbacks lack connection/map identity. Reload mutates live state before parsing. Rotation index can overflow. Preserve alive/dead paused HTML counter, per-tick sends and existing Panorama.

References: https://docs.cssharp.dev/api/CounterStrikeSharp.API.Core.Listeners.OnTick.html ; https://docs.cssharp.dev/docs/guides/referencing-players.html ; CounterStrikeSharp v1.0.378 Utilities.cs and BasePlugin.cs.

Installed #7 is a distinct v1.0.9 binary (SHA256 f59cb017603f6ff8cce28e97ae82071aec56972bcf0f39a096aa207923ef62bf), not the baseline of this diff.

# Install and rollback

Build with .NET SDK 10: `dotnet build Advertisement/Advertisement.csproj -c Release -o out`. Run `dotnet run --project Tests/PanoramaText.Tests.csproj -c Release -- .`.

Requires existing CSS API 1.0.378 / .NET 10. Package Advertisement.dll, Advertisement.deps.json, PanoramaManager.dll and lang files. Preserve existing configuration and custom translations. No CSS runtime upgrade, database change or new required configuration fields. Panorama remains opt-in and requires the existing Workshop resources; the layout itself is unchanged (24px).

Before maintenance record the instance/port, online count, current file/config hashes and save originals outside plugin autoload. On an empty authorized instance unload Advertisement, replace its DLL/deps and bundled dependency, then load it. Check css_plugins list and logs. Do not repeatedly retry assembly-loader failures: restore originals, use a scoped authorized instance restart only if required. Never restart the host.

Rollback: unload Advertisement, restore the original DLL/deps/dependencies and translation files, remove only newly introduced files, reload and verify the original version and hashes. Retain the existing config. Public fleet rollout and client visual acceptance remain pending.

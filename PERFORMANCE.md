# O5 — Advertisement

2026-11-10. Реализация и offline-ревью завершены; статус игровой приёмки — `awaiting_live`. [PR #1](https://github.com/koiie111/cs2-advertisement/pull/1). Массовой выкладки нет.

## Sources and changes

Baseline: upstream 233c811c54144bb26c6588d2fa2781a6daed9edb. Final code: eaedaba. Owner selected current upstream including Panorama. Older server7 v1.0.9 source mapping is unmapped; it depends on CSS API 1.0.361/GeoIP and is not our performance baseline. Original DLL SHA256 f59cb017603f6ff8cce28e97ae82071aec56972bcf0f39a096aa207923ef62bf.

Active HTML slots replace all-player scans; empty OnTick has no native calls/allocations. Identity/map cleanup isolates reconnects. Preserve tick frequency and alive/dead paused budgets. Localization cache is bounded to 4096 message/language entries, invalidated on config parse; placeholders are lazy/shared per dispatch. Preserve replacement order, unknown tags and pawn-based player count. Rotation wraps safely.

Timers are removed from BasePlugin.Timers on completion/cancellation; welcome timers are limited to one per slot and cancelled on reset/reload/unload. Config is read before live state changes; missing/malformed files retain current state. Reserve css_advert_reload and compare aliases case-insensitively. Panorama retains layout/capture=false, reuses identifiers/parsing and redraws personal text/phase on Restored. Actual 24px appearance retained, erroneous 22px test/docs corrected.

## Validation

.NET SDK 10.0.400, net10.0, CSS API 1.0.378, PanoramaManager 0.4.4. Zero-warning Release build. Commands:

```
dotnet build Advertisement/Advertisement.csproj -c Release -o ../candidate
dotnet run --project Tests/PanoramaText.Tests.csproj -c Release -- .
```

PASS: Panorama color/whitespace/reset/casing/overflow/label/CSS contracts; HTML 0/1/8/32 recipient budgets, zero/fractional durations, alive/dead pause/resume and replacement reset; repeated rotation and single-message groups. Local Panorama validator passes XML and 24 CSS properties. PR CI passes. Baseline builds but its 22px test fails before changes.

Первоначальные тесты не вызывали lifecycle/локализацию самого плагина. При повторном ревью добавлен `Tests/Runtime`: он компилирует production-исходники с управляемыми заменами CSS/Panorama и вызывает зарегистрированные callbacks. Native entities, реальный порядок событий и визуальный результат остаются интеграционными проверками.

## Server measurements

Public #7, CSS v378, zero players before/after every window. Baseline -> candidate -> baseline, three ~30s windows per series, 5s warmup. No game restart/map change. No profiler installed: identical temporary Stopwatch/allocation wrappers measure OnTick only. Probe patches in docs/measurements. Candidate probe is 2fcebdb; later changes concern Panorama/packaging/aliases/models, not idle OnTick. Aggregate counters cannot provide p95/p99, active timer/native costs or full-tick latency.

| Series | Window | Calls | ns/call with instrumentation | Bytes/call |
|---|---:|---:|---:|---:|
| baseline A | 1 | 2025 | 933.5 | 32.0 |
| baseline A | 2 | 2022 | 883.3 | 32.0 |
| baseline A | 3 | 2025 | 884.7 | 32.0 |
| candidate | 1 | 2022 | 825.1 | 0.0 |
| candidate | 2 | 2025 | 831.1 | 0.0 |
| candidate | 3 | 2025 | 924.0 | 0.0 |
| baseline B | 1 | 2024 | 1067.9 | 32.0 |
| baseline B | 2 | 2023 | 1003.8 | 32.0 |
| baseline B | 3 | 2024 | 1061.8 | 32.0 |

Result: 32 -> 0 bytes/call in idle HTML path. Timing difference is smaller than baseline-series drift: no measurable timing gain accepted. Do not claim -20% or a fix for 150ms spikes. Original v1.0.9 DLL/deps restored byte-for-byte after measurements; original Advertisement active among 61 loaded modules.

## Release and pending acceptance

Hashes: docs/measurements/release-SHA256.json. Installation/rollback: UPGRADE.md. Private artifacts/backups: C:/Users/koiie/.codex/tasks/advertisement-performance-20261110 (outside web root). Diagnostic DLLs are not release artifacts.

Pending: real-client Welcome/chat/center/HTML/Panorama and language switching; reconnect/slot reuse/map/round lifecycle; competing menus; timer/memory soak; 1/8/32 active recipients; paired full-path/full-tick percentiles. Это гейт серверного выпуска; merge исходников не означает live-приёмку.

Final release smoke: v1.0.10 loaded on empty #7; three css_advert_reload cycles completed, then original files restored byte-for-byte and v1.0.9 reloaded (61 modules). No restart. Probe raw source and measurement wrapper hashes are retained privately; patches and raw windows are committed.

## Повторное ревью по плану 10.11.2026

Прочитан весь `plans/cs2-plugin-optimization` текущего `koiie111/4ill.ru/main`, включая O/F-задания, lock-файлы, протокол приёмки и существующие отчёты. Сфера этого PR — Advertisement; Game Manager и WeaponPaints остаются отдельными задачами O5.

| Требование Advertisement | Результат |
|---|---|
| Разрешить различие 1.0.9 и HEAD | База PR закреплена на `233c811`, уже содержащем Panorama. По записанному выбору владельца оптимизируется эта база. Старый бинарник 1.0.9 остаётся `unmapped`; это не узкий backport к нему. В diff нет новой Panorama-функции/вёрстки. |
| Активные HTML-получатели и пустой fast return | Production OnTick проверен при 0/1/8/32 получателях; после expiry нет даже lookup игроков. |
| PrintTime, ShowHtmlWhenDead, частота отправки | Проверены нулевая/дробная/5-секундная длительности, alive/dead pause/resume и замена сообщения. Отправка остаётся каждый подходящий тик. |
| Welcome, интервалы, команды | Проверены три назначения Welcome, delay, ротация/интервал рекламы, регистр aliases и резерв reload. |
| Lifecycle и ограниченность | Реальные callbacks плагина прошли disconnect, controller replacement, slot reuse, map end, hot reload, 1000 завершений Welcome на каждое назначение, cancellation на reload/unload и bound локализации 4096. |
| Локализация/подготовка текста | Проверены смена языка, unknown tags, invalidation при config parse, pawn-based count и однократные общие placeholders на рассылку. |
| Panorama | Проверены персональный текст/phase на Restored, `CaptureInput=false`, cleanup анимационных timers. XML/CSS и существующий parser suite проходят; вёрстка не менялась. |

Команды дополнительной проверки:

```sh
dotnet run --project Tests/Runtime/Runtime.Tests.csproj -c Release
python Tests/Runtime/analyze.py
```

Baseline и candidate собраны SDK 10.0.400/net10.0 без предупреждений. Известное падение baseline parser-теста воспроизведено: он ожидал 22px при фактических 24px. Candidate suites проходят. Новая runtime-suite включена в PR CI. Существенных оставшихся пропусков кодовой реализации O5 Advertisement при ревью не найдено; закрыт пропуск воспроизводимых offline-проверок.

Одинаковый synthetic harness вызвал production OnTick и таймер рассылки на baseline/candidate. Для каждого сценария: 20 000 warm-up, 3 × 100 000 операций, одинаковые sends; tiered JIT выключен. Raw: `docs/measurements/offline-{baseline,candidate}.json`, условия: `offline-scenario.json`; воспроизведение/ограничения: `Tests/Runtime/README.md`. Для 32 активных HTML: 64 → 32 lookup и 608 → 0 **синтетических managed** байт/тик; для рассылки 32 игрокам: 2112 → 128 lookup и 88288 → 7896 байт/рассылку. Native wrapper allocations и native costs в doubles отсутствуют. Эти данные не являются полным тиком, live-процентом, p95/p99 или доказательством решения задержек 150 мс.

Решение ревью: исходники готовы к merge после CI по поручению владельца; `awaiting_live` остаётся для перечисленной игровой матрицы и полного профиля. В рамках этого ревью серверные действия не выполнялись. Исходный `release-SHA256.json` описывает прежнюю проверенную сборку; новая локальная сборка ревью имеет отдельный `review-release-SHA256.json`. При merge workflow `Build & Release` сам выбирает следующий tag от имеющихся тегов; версия CI-артефакта может отличаться от локальной v1.0.10.

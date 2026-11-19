# ARMSX2 driver source review — 2026-11-19

Inspected ARMSX2 source commit `5e61613fd9815b824d77d70c5165c3a83e5acb24`:

- [CustomDriver.kt](https://github.com/ARMSX2/ARMSX2/blob/5e61613fd9815b824d77d70c5165c3a83e5acb24/platforms/android/app/src/main/java/com/armsx2/CustomDriver.kt#L221-L280) defines nine GitHub Releases sources and filters them by GPU family. It fetches the default releases endpoint without paginating the entire history and lists ZIP assets.
- [GpuInfo.kt](https://github.com/ARMSX2/ARMSX2/blob/5e61613fd9815b824d77d70c5165c3a83e5acb24/platforms/android/app/src/main/java/com/armsx2/GpuInfo.kt#L83-L95) recommends sources rather than a fixed package: ARMSX2 Turnip for Adreno 6xx/7xx, StevenMXZ for 8xx, MaliSX2 for supported Mali GPUs, and KIMCHI as the remaining Adreno fallback. Xclipse/PowerVR have no custom-driver recommendation there.

Sources: `bmdhacks/malisx2`, `bmdhacks/armsx2-turnip`, `K11MCH1/AdrenoToolsDrivers`, `MrPurple666/purple-turnip`, `StevenMXZ/Adreno-Tools-Drivers`, `crueter/GameHub-8Elite-Drivers`, `PojavLauncherTeam/freedreno-builder`, `WearyConcern1165/ExynosTools`, `avavo/MdiEx`. The412Banner is not in this source list.

Compared the exact ZIP URLs from the same default API responses with our catalog, rather than enumerating all historical upstream releases. MaliSX2 and StevenMXZ had no missing ZIPs within these responses. Other feeds contain some absent historical, duplicate or previously excluded packages; absence from our catalog alone does not establish a useful addition.

## Selected addition

[ARMSX2 Turnip axfl3-003](https://github.com/bmdhacks/armsx2-turnip/releases/tag/axfl3-003): one missing Android package for Adreno 6xx/7xx. SHA-256, size, ZIP CRC, safe unique paths, extraction limits, metadata/library selection, AArch64 ELF, Android HAL marker, and upstream library SHA-256 verified. Linux assets excluded. No runtime device/game test was performed. The catalog recommendation boolean remains false; ARMSX2's source recommendation is described with its GPU scope.

## Deferred MdiEx

[avavo/MdiEx v3.6](https://github.com/avavo/MdiEx/releases/tag/v3.6) is another absent source. Downloaded all eight current ZIPs and verified their asset sizes and SHA-256. The seven chip-specific packages include Samsung Vulkan libraries with dependencies on private device libraries, including `libsbwchelper.so` and `android.hardware.graphics.mapper@4.0-impl-sgr.so`. Availability depends on matching Samsung firmware. They also declare Helix, NRAMV and Core metadata which the inspected EmuCoreX installer does not configure. The Nativo ZIP contains layers/helpers but no selectable Vulkan driver library. These packages were not added pending matching-device loading tests and explicit support for the declared auxiliary components. Their presence in ARMSX2's browser is not a runtime validation result for EmuCore apps.

## Banners selection policy

Keep one previously verified Banners-Turnip AIO package (`v27.0.0-20261109-r2`) and replace it selectively after future validation. Removed 4,174 other Banners-Turnip entries; all entries from other repositories remain unchanged. The separate Nightlies Rutabaga packages remain. Removed entries can be recovered from Git history.

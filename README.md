# EmuCoreV Drivers

This repository hosts the shared GPU driver catalog used by EmuCoreV, EmuCoreC, EmuCoreR, EmuCoreP, and EmuCoreX.

`drivers.json` is a catalog of Adreno, Mali, and Xclipse driver packages from upstream GitHub releases. Driver ZIP files are not committed to this repository; each entry links to the upstream release asset and keeps source/credits metadata. The top-level array and the existing object fields are kept backward-compatible for every app consuming this catalog.

Current catalog scope:

- MaliSX2 by ARMSX2 / bmdhacks for Mali Valhall v9/v11 and Bifrost v7 (G52)
- ARM Mali G57 vendor packages and ExynosTools Xclipse packages
- crueter GameHub and PojavLauncher Freedreno packages
- Turnip Mesa driver builds
- K11MCH1, StevenMXZ, MrPurple666, whitebelyash, s1mptom, and v3kt0r-87 builds
- The412Banner, WinNative-Emu, Vauzi-17, Balemuni, and Weab-chan community builds
- faux123, AlexSanz0902 Turnip-Z, sherft2607 Retroid Pocket Duo, DroidDeck, and GameHub Rutabaga packages
- nihui Mesa Turnip Android builds with compatible ZIP layout
- Auto, GMEM, SYSMEM, ADPKG, and A8xx variants when available
- Selected Qualcomm packages from StevenMXZ, K11MCH1, and zoerakk that use an AdrenoTools-compatible emulator ZIP layout

Archives must contain an ARM64 Vulkan shared library selectable by the existing app installers. Magisk-only modules and Linux container packages are excluded. Package validation does not establish runtime compatibility with every device, firmware, emulator, or game.

The 2026-10-21 refresh contains **217 packages**: verified local additions including MaliSX2 0.2.1, 0.1.5, and 0.1.4, seven newer upstream catalog entries retained, and one removed nihui Edge entry whose upstream asset returns HTTP 404. The 174 retained base entries remain unchanged. The existing JSON array, field names, field types, IDs of retained entries, and catalog URL are unchanged. New builds are not marked recommended automatically, and the existing recommendation flags are preserved.

The 2026-10-29 update adds MaliSX2 0.3.0 and keeps 0.2.3 and 0.2.2, which were published upstream after the refresh above; the catalog now lists **220 packages**. The 0.3.0 ZIP was downloaded and checked for release-asset size, SHA-256, ZIP layout, and the AArch64 ELF `libvulkan_malisx2.so`. The array shape, field names, field types, IDs of retained entries, and the catalog URL are unchanged, and the new entry is not marked recommended.

The 2026-11-07 update adds MaliSX2 0.4.0, 0.3.3, and 0.3.2 to the 0.3.1 entry added on 2026-11-02; the catalog now lists **224 packages**. All four ZIPs (0.4.0, 0.3.3, 0.3.2, and 0.3.1) were downloaded and checked for release-asset size, SHA-256, ZIP layout (two safe entries, no path traversal), `meta.json` (`schemaVersion` 1, `minApi` 29, `libraryName` `libvulkan_malisx2.so`), and the AArch64 ELF header of `libvulkan_malisx2.so` (16.7-16.9 MiB, within the 64 MiB per-file client limit). The array shape, field names, field types, IDs of retained entries, and the catalog URL are unchanged, and the new entries are not marked recommended.

The 2026-11-09 update adds **MaliSX2 0.4.1**, bringing the catalog to **225 packages**. The official release ZIP was downloaded and checked against the GitHub asset size and SHA-256, ZIP CRC and safe paths, client extraction limits, `meta.json` (`schemaVersion` 1, `minApi` 29, `libraryName` `libvulkan_malisx2.so`), and the AArch64 shared-library ELF header. Its two files include a 16,857,728-byte Vulkan library whose SHA-256 also matches the upstream release notes. Existing entries and recommendation flags are preserved; the new entry is not marked recommended.

The subsequent **2026-11-09 Adreno expansion adds 4,707 packages**, bringing the catalog to **4,932 packages from 23 download repositories**: 4,864 Turnip, 51 Qualcomm, 12 Mali, four Vortek/Xclipse, and one Adreno/GameHub entry. The 225 existing entries, including MaliSX2 0.4.1, remain unchanged. No PanVK or other new Mali packages are included in this expansion.

This expansion inventories all published releases returned by GitHub for the 19 Adreno build repositories below, plus the dedicated Rutabaga release in The412Banner/Nightlies. Banners-Turnip's 1,358 published releases were enumerated with GraphQL to avoid the REST API's first-1,000-results limit. Historic and automated builds are included, not just the latest release of each publisher. The scope is these verified sources as observed on 2026-11-09, not every driver repository on the internet.

Of 4,732 not-yet-listed ZIP candidates, 4,711 passed package validation, 21 were rejected, and four passing archives were omitted as exact SHA-256 duplicates of retained packages. A further 1,586 Linux, Wayland, Magisk, or KernelSU assets were excluded by package type. The checks cover release-asset size, GitHub SHA-256 when available, ZIP CRC, safe unique paths, 256-entry / 64 MiB per-file / 128 MiB extracted client limits, the main-library selection algorithm shared by the inspected EmuCoreX/EmuCoreV/EmuCoreC installers, AArch64 shared-library format, Android Vulkan HAL `HMI` exports, metadata/library agreement when metadata is readable, and bundled private dependency names. Every new entry records the downloaded archive's SHA-256. One candidate was excluded by its compressed asset size before download; all other candidate archives were downloaded. Standalone Linux ICDs are excluded; combined DroidDeck archives are included only when the existing selectors choose their Android library.

Some historical packs omit metadata or contain numeric strings or malformed metadata JSON. The current inspected installers select the Vulkan library without parsing `meta.json`, so those packages are assessed by the actual selected ELF rather than rejected only for metadata formatting. Android API requirements are copied when declared; otherwise the entry directs readers to the upstream release. Package validation is not a device or game test. GPU restrictions and firmware dependencies remain relevant, and no new entry is marked recommended.

Known client limitation: the inspected clients identify installed packages by the upstream ZIP filename. Different releases named `turnip.zip` therefore share one installation name, and the UI can show another version as already downloaded. Remove the installed package before downloading a different release with the same filename. This also applies to matching filenames from different publishers; the catalog preserves the upstream download URLs and cannot rename those archives.

| Source | Packages added in the Adreno expansion |
| --- | ---: |
| [The412Banner/Banners-Turnip](https://github.com/The412Banner/Banners-Turnip/releases) | 4,172 |
| [StevenMXZ/Adreno-Tools-Drivers](https://github.com/StevenMXZ/Adreno-Tools-Drivers/releases) | 103 |
| [Vauzi-17/710](https://github.com/Vauzi-17/710/releases) | 76 |
| [Weab-chan/freedreno_turnip-CI](https://github.com/Weab-chan/freedreno_turnip-CI/releases) | 72 |
| [MrPurple666/purple-turnip](https://github.com/MrPurple666/purple-turnip/releases) | 55 |
| [whitebelyash/AdrenoToolsDrivers](https://github.com/whitebelyash/AdrenoToolsDrivers/releases) | 51 |
| [K11MCH1/AdrenoToolsDrivers](https://github.com/K11MCH1/AdrenoToolsDrivers/releases) | 41 |
| [WinNative-Emu/Drivers](https://github.com/WinNative-Emu/Drivers/releases) | 38 |
| [v3kt0r-87/Mesa-Turnip-Builder](https://github.com/v3kt0r-87/Mesa-Turnip-Builder/releases) | 34 |
| [PojavLauncherTeam/freedreno-builder](https://github.com/PojavLauncherTeam/freedreno-builder/releases) | 21 |
| [faux123/turnip-faux123-driver](https://github.com/faux123/turnip-faux123-driver/releases) | 11 |
| [Droid-Deck/Drivers](https://github.com/Droid-Deck/Drivers/releases) | 11 |
| [sherft2607/turnip-adreno722-duo](https://github.com/sherft2607/turnip-adreno722-duo/releases) | 5 |
| [AlexSanz0902/turnip-sd865-z](https://github.com/AlexSanz0902/turnip-sd865-z/releases) | 4 |
| [The412Banner/Nightlies Rutabaga](https://github.com/The412Banner/Nightlies/releases/tag/rutabaga-drivers) | 4 |
| [nihui/mesa-turnip-android-driver](https://github.com/nihui/mesa-turnip-android-driver/releases) | 4 |
| [Balemuni/Balemunis-Aurora](https://github.com/Balemuni/Balemunis-Aurora/releases) | 2 |
| [s1mptom/freedreno_turnip-CI](https://github.com/s1mptom/freedreno_turnip-CI/releases) | 2 |
| [crueter/GameHub-8Elite-Drivers](https://github.com/crueter/GameHub-8Elite-Drivers/releases) | 1 |
| [zoerakk/qualcomm-adreno-driver](https://github.com/zoerakk/qualcomm-adreno-driver/releases) | 0; remaining candidates duplicate another package or have mismatched private dependency names |

The 2026-11-12 update adds **MaliSX2 0.5.0**, bringing the catalog to **4,933 packages**. The official release ZIP was downloaded and checked against the GitHub asset size (3,948,621 bytes) and SHA-256, ZIP CRC and safe paths, `meta.json` (`schemaVersion` 1, `minApi` 29, `libraryName` `libvulkan_malisx2.so`), and the AArch64 shared-library ELF header. Its 17,111,728-byte Vulkan library matches the SHA-256 in the upstream release notes. Existing entries and recommendation flags are preserved; the new entry is not marked recommended.

Rejected candidates include Qualcomm packages whose renamed private libraries do not match `DT_NEEDED`, K11MCH1 v676 with a missing `vkbgsl.so`, one StevenMXZ package missing `libc++_shared.so`, two packages without an Android HAL entry point, one Magisk module, and an oversized early Pojav archive. Archives are not repaired, repackaged, or rehosted by this catalog.

PanVK is a separate driver implementation from MaliSX2. The inspected Zenithblue 26.3.1 Android/AdrenoTools and FristOneRR 3.7.0 packages export the Android Vulkan HAL `HMI` and have standard Android library dependencies, so their packaging fits EmuCoreX's existing AdrenoTools loading path. The [FristOneRR wrapper](https://github.com/FristOneRR/FristOneRR-Panvk-Driver#emulators) is part of its Windows/Winlator setup; upstream also documents direct installation in emulators with a custom-driver option. These facts do not establish EmuCoreX rendering compatibility. Its MaliSX2-specific rendering policies do not automatically apply to PanVK, and Mali model/kernel compatibility is different. PanVK remains outside this catalog update pending actual emulator/device validation.

Selected additions:

| Publisher | Packages added |
| --- | --- |
| [StevenMXZ](https://github.com/StevenMXZ/Adreno-Tools-Drivers/releases) | 26.3.0 R2/R3/R4, their OneUI variants, Gen8 V34/V35 |
| [whitebelyash](https://github.com/whitebelyash/AdrenoToolsDrivers/releases) | Mainline V30/V31, Stable V1, their Sync variants, Gen8 V29 Sync |
| [MrPurple666](https://github.com/MrPurple666/purple-turnip/releases/tag/vturnip_mrpurple_T30-toasted.adpkg) | T30 Toasted |
| [v3kt0r-87](https://github.com/v3kt0r-87/Mesa-Turnip-Builder/releases/tag/14_aug_2026) | Mesa 26.2.0 emulator ZIP |
| [nihui](https://github.com/nihui/mesa-turnip-android-driver/releases) | Previously missing 26.1.2 and 26.1.3 |
| [K11MCH1](https://github.com/K11MCH1/AdrenoToolsDrivers/releases) | Qualcomm v837.6 and v840 |
| [The412Banner](https://github.com/The412Banner/Banners-Turnip/releases/tag/v26.3.0-20260830-r4) | 20260830 R4 Standard, A8xx, and A710/A720/A722 Test |
| [WinNative-Emu](https://github.com/WinNative-Emu/Drivers/releases/tag/v1.12) | 1.12 Balanced and Performance |
| [Vauzi-17](https://github.com/Vauzi-17/710/releases/tag/3.6) | A710/A720/A722 v3.6 |
| [Balemuni](https://github.com/Balemuni/Balemunis-Aurora/releases/tag/V2) | Apex V2 Universal and Ultimate SD8 Gen 2 |
| [Weab-chan](https://github.com/Weab-chan/freedreno_turnip-CI/releases/tag/25.3.0-devel_bbdd688) | October 2025 standard, patched sysmem, and SD8 Gen 2 UI-fix alternatives |
| [zoerakk](https://github.com/zoerakk/qualcomm-adreno-driver/releases/tag/842.8) | Qualcomm v842.8 for Snapdragon Elite / Adreno 8xx |

All 33 new ZIPs were downloaded and checked for release-asset size, ZIP CRC, safe paths, ARM64 ELF format, Vulkan ICD/HAL exports, metadata library selection, and the strictest current client limits (256 files, 64 MiB per file, 128 MiB extracted). GitHub SHA-256 asset digests were checked when supplied. The 174 retained download links were also checked for availability.

The prior 207-entry local update passed six compatibility tests with the catalog parsers from all five apps and their shared main-library selection algorithm. This refresh retains the same top-level array and field types. Archive checks do not establish runtime compatibility on every GPU.

Read each package's GPU and Android requirements before installing it; current clients display these requirements but do not automatically enforce every restriction. Qualcomm packages can depend on matching vendor firmware. Experimental A8xx and A710/A720/A722 packages may have rendering issues or require sysmem. WinNative Performance requests high GPU clocks and can increase power use and heat. Driver version numbers such as Qualcomm v840 are not GPU model numbers.

The older zoerakk 800.51 archive was not added because its required private library names do not match the bundled files. No archives are modified or rehosted by this catalog.


MaliSX2 0.5.0, 0.4.1, 0.4.0, 0.3.3, 0.3.2, 0.3.1, 0.3.0, 0.2.3, 0.2.2, 0.2.1, 0.1.5, and 0.1.4 link to the [official ARMSX2 / bmdhacks releases](https://github.com/bmdhacks/malisx2/releases), without modifying or rehosting their archives:
- **MaliSX2 0.5.0**: ZIP SHA-256 `71c1e3dc68ef1396d469f245019d42ab73980e48034095453b7be776195c3641`. Adds the Mali-G31, G51, G310, G510, G610 and G710 and a separate ARM Linux package (not listed here). Output and speed are unchanged from 0.4.1 on the Mali-G615, G57 and G52. On the G51 and G31 a few advanced shader features are unavailable, so shaders that need them fail to build instead of drawing wrongly.
- **MaliSX2 0.4.1**: ZIP SHA-256 `feb44fcb0c459894cbf1b4e9403fd756db74f54e9b889fd652fbdc4043689034`. Adds Vita3K-Plus support and its memory mapping modes, fixes broken God of War Collection geometry on the Mali-G52, and prevents an out-of-memory crash from stale shaders after changing Vita3K settings. Vita3K-Plus gameplay has only been tested upstream on the Mali-G52; required features passed driver tests on the G57 and G615, with gameplay there still untested. ARMSX2 output is unchanged on the G57/G615 accuracy corpus, with no slowdown found.
- **MaliSX2 0.4.0**: ZIP SHA-256 `835f980506ed46fa51925fd279b256d23b0ddf481ffd1ab39be2fee275cf8bf8`. Adds synchronization2 barriers and submits, more dynamic pipeline state, local read, descriptor indexing, 8- and 16-bit numbers in shaders, events, and indirect draws and dispatches on every supported GPU; brings parallel-RDP (mupen64plus-next) and BC compressed textures to the Mali-G52 and the G57 family; fixes Mali-G52 device loss in Persona 4, GPU hangs on Unisoc T618, and instanced draws that start part-way through a vertex buffer; and stops apps crashing on indirect draws and dispatches. `MALISX2_DEBUG` is replaced by `MALISX2_MEASURE=cpuprof`.
- **MaliSX2 0.3.3**: ZIP SHA-256 `10d4168ab80f47dbe4c7d2f28fd590acbd3e2ed72164bf0bff5c5842f2a57bc3`. Fixes Mali-G52 crashes at 1.5x internal resolution and above by letting the tiler memory grow with the scene, and removes thin vertical streaks at 2x and higher on the Mali-G615 and the G57 family (WRC 3, Katamari Damacy).
- **MaliSX2 0.3.2**: ZIP SHA-256 `8430ff49afc187f648b4d8a6338d3136f9f238ba0b80e69bdc40a32c0d07358d`. Mostly hakuX work on the Mali-G52: the tiler memory ring grows from 4 to as many as 16 regions only when a game needs it, Android graphics buffers can be imported as Vulkan buffers, descriptor pools use a bump allocator, `vkCmdSetIndexRangeMALISX2` skips the CPU index-range scan on the G52 and G76, and `MALISX2_DEBUG` adds CPU, GPU cycle, and shader statistics.
- **MaliSX2 0.3.1**: ZIP SHA-256 `34da06a52a0349c3e6ae07f7fb7d2dc5b76203c62b256b8d517e8df2509bb364`. Implements occlusion queries, so Dolphin now starts, and makes hakuX about 1.7x faster on the Mali-G615 at 3x and 4x internal resolution; VkEvent, query pools, and clip distances work on the G615, the Mali-G52 gains the same occlusion queries, the Mali-G76 is accepted on the Bifrost path, and the shader compiler is newer.
- **MaliSX2 0.3.0**: ZIP SHA-256 `e35b577f07ab4261ef7a08e17df2e1477910fed4e8e4b0e70268c57d0dde7c74`. Adds hakuX (Xbox) support on Mali-G57 (dynamic rendering, timeline semaphores, validated render passes), stops advertising BCn/DXT textures and 4x-16x multisampling (reported as 1x), and makes Linux display page flips wait for the GPU. ARMSX2 behaviour is unchanged, but the first launch after the update rebuilds the pipeline cache because the version is part of `driverInfo`. Dolphin does not start on 0.3.0; occlusion query pools arrive in 0.3.1.
- **MaliSX2 0.2.3**: ZIP SHA-256 `133c35a49c4197e9177969e69e4dba41ea2433598810277b4f37597c8751a78f`. Fixes swap chain creation on Rockchip RK3576 handhelds such as the Anbernic RG Vita Pro.
- **MaliSX2 0.2.2**: ZIP SHA-256 `f860040265427e55abe4515eed75c302870708b4cbb613fedb7133997e2b3b6d`. Accepts more Mali-G57-family kernel driver versions, fixes the RK3576 swap chain black screen, reduces shader size, and fixes a possible GPU fault when post-processing and normal drawing overlap.
- **MaliSX2 0.2.1**: ZIP SHA-256 `80166d8dc2f1051158966cafdf7d47e0866e13976fcc609e12c2e897695b3ae0`. Adds experimental preview support for Mali-G52 / G52 r1 (RK3566/RK3568, courtesy of @TheGammaSqueeze).
- **MaliSX2 0.1.5**: ZIP SHA-256 `a3061b5135ef7bbecbdfc25b0db0b8370da8259d53f9daf3b4df3c79437d5cd1`. Optimized 4x4 texels per thread texture transfers for faster uploads.
- **MaliSX2 0.1.4**: ZIP SHA-256 `35cec77da26ba9bc23531f423f34ba741f0fe82e212feb72ce0967023d6ee3d9`. Android 15 swapchain fix.

Archives contain `meta.json` and the AArch64 Vulkan HAL `libvulkan_malisx2.so`. The driver is MIT licensed. Supported GPUs are G52 (experimental), G76 (accepted since 0.3.1, untested upstream), G57/G68/G77/G78/G78AE (Valhall v9, requires Arm kbase r40p0 or newer, kernel interface 11.36+), and G615/G715 (Valhall v11). Other Mali generations are unsupported. 0.3.0 and newer declare `minApi` 29 in their `meta.json`, so they need Android 10 or newer; 0.3.1 and newer report MSAA as 1x, so an app that assumes 4x multisampling may not start. The entries remain unmarked as recommended. Apps must check GPU and kernel compatibility and report whether the custom driver actually loaded.

The Android app reads:

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

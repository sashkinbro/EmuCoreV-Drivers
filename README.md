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
- nihui Mesa Turnip Android builds with compatible ZIP layout
- Auto, GMEM, SYSMEM, ADPKG, and A8xx variants when available
- Selected Qualcomm packages from StevenMXZ, K11MCH1, and zoerakk that use an AdrenoTools-compatible emulator ZIP layout

Archives must contain an ARM64 Vulkan shared library selectable by the existing app installers. Magisk-only modules and Linux container packages are excluded. Package validation does not establish runtime compatibility with every device, firmware, emulator, or game.

The 2026-10-21 refresh contains **217 packages**: verified local additions including MaliSX2 0.2.1, 0.1.5, and 0.1.4, seven newer upstream catalog entries retained, and one removed nihui Edge entry whose upstream asset returns HTTP 404. The 174 retained base entries remain unchanged. The existing JSON array, field names, field types, IDs of retained entries, and catalog URL are unchanged. New builds are not marked recommended automatically, and the existing recommendation flags are preserved.

The 2026-10-29 update adds MaliSX2 0.3.0 and keeps 0.2.3 and 0.2.2, which were published upstream after the refresh above; the catalog now lists **220 packages**. The 0.3.0 ZIP was downloaded and checked for release-asset size, SHA-256, ZIP layout, and the AArch64 ELF `libvulkan_malisx2.so`. The array shape, field names, field types, IDs of retained entries, and the catalog URL are unchanged, and the new entry is not marked recommended.

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


MaliSX2 0.3.0, 0.2.3, 0.2.2, 0.2.1, 0.1.5, and 0.1.4 link to the [official ARMSX2 / bmdhacks releases](https://github.com/bmdhacks/malisx2/releases), without modifying or rehosting their archives:
- **MaliSX2 0.3.0**: ZIP SHA-256 `e35b577f07ab4261ef7a08e17df2e1477910fed4e8e4b0e70268c57d0dde7c74`. Adds hakuX (Xbox) support on Mali-G57 (dynamic rendering, timeline semaphores, validated render passes), stops advertising BCn/DXT textures and 4x-16x multisampling (reported as 1x), and makes Linux display page flips wait for the GPU. ARMSX2 behaviour is unchanged, but the first launch after the update rebuilds the pipeline cache because the version is part of `driverInfo`. Dolphin does not start on 0.3.0; occlusion query pools arrive in 0.3.1.
- **MaliSX2 0.2.3**: ZIP SHA-256 `133c35a49c4197e9177969e69e4dba41ea2433598810277b4f37597c8751a78f`. Fixes swap chain creation on Rockchip RK3576 handhelds such as the Anbernic RG Vita Pro.
- **MaliSX2 0.2.2**: ZIP SHA-256 `f860040265427e55abe4515eed75c302870708b4cbb613fedb7133997e2b3b6d`. Accepts more Mali-G57-family kernel driver versions, fixes the RK3576 swap chain black screen, reduces shader size, and fixes a possible GPU fault when post-processing and normal drawing overlap.
- **MaliSX2 0.2.1**: ZIP SHA-256 `80166d8dc2f1051158966cafdf7d47e0866e13976fcc609e12c2e897695b3ae0`. Adds experimental preview support for Mali-G52 / G52 r1 (RK3566/RK3568, courtesy of @TheGammaSqueeze).
- **MaliSX2 0.1.5**: ZIP SHA-256 `a3061b5135ef7bbecbdfc25b0db0b8370da8259d53f9daf3b4df3c79437d5cd1`. Optimized 4x4 texels per thread texture transfers for faster uploads.
- **MaliSX2 0.1.4**: ZIP SHA-256 `35cec77da26ba9bc23531f423f34ba741f0fe82e212feb72ce0967023d6ee3d9`. Android 15 swapchain fix.

Archives contain `meta.json` and the AArch64 Vulkan HAL `libvulkan_malisx2.so`. The driver is MIT licensed. Supported GPUs are G52 (experimental), G57/G68/G77/G78/G78AE (Valhall v9, requires Arm kbase r40p0 or newer, kernel interface 11.36+), and G615/G715 (Valhall v11). Other Mali generations are unsupported. 0.3.0 declares `minApi` 29 in its `meta.json`, so it needs Android 10 or newer. The entries remain unmarked as recommended. Apps must check GPU and kernel compatibility and report whether the custom driver actually loaded.

The Android app reads:

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

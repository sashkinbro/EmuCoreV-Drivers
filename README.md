# EmuCoreV Drivers

Shared GPU driver catalog used by EmuCoreV, EmuCoreC, EmuCoreR, EmuCoreP, and EmuCoreX.

## Current catalog

As of **2026-11-19**, `drivers.json` contains **761 packages** from **24 download repositories**:

| Catalog family | Packages |
| --- | ---: |
| Turnip | 691 |
| Qualcomm | 51 |
| Mali | 14 |
| Vortek / Xclipse | 4 |
| Adreno / GameHub | 1 |
| **Total** | **761** |

**The412Banner/Banners-Turnip: one selected package**, `Turnip-v27.0.0-20261109-r2-Banners-AIO.zip`. Future updates should replace this selection after validation, rather than import the automated release history or additional variants. The four Rutabaga packages from the separate `The412Banner/Nightlies` repository remain available.

The catalog includes **MaliSX2 0.5.1** and **ARMSX2 Turnip axfl3-003**. Removed packages and previous catalog counts can be found in Git history.

## Sources currently listed

Counts below are calculated from the current `drivers.json` and refer to download repositories.

| Source | Current packages |
| --- | ---: |
| [K11MCH1/AdrenoToolsDrivers](https://github.com/K11MCH1/AdrenoToolsDrivers/releases) | 196 |
| [StevenMXZ/Adreno-Tools-Drivers](https://github.com/StevenMXZ/Adreno-Tools-Drivers/releases) | 115 |
| [Vauzi-17/710](https://github.com/Vauzi-17/710/releases) | 77 |
| [Weab-chan/freedreno_turnip-CI](https://github.com/Weab-chan/freedreno_turnip-CI/releases) | 75 |
| [whitebelyash/AdrenoToolsDrivers](https://github.com/whitebelyash/AdrenoToolsDrivers/releases) | 59 |
| [MrPurple666/purple-turnip](https://github.com/MrPurple666/purple-turnip/releases) | 57 |
| [WinNative-Emu/Drivers](https://github.com/WinNative-Emu/Drivers/releases) | 40 |
| [v3kt0r-87/Mesa-Turnip-Builder](https://github.com/v3kt0r-87/Mesa-Turnip-Builder/releases) | 36 |
| [PojavLauncherTeam/freedreno-builder](https://github.com/PojavLauncherTeam/freedreno-builder/releases) | 22 |
| [nihui/mesa-turnip-android-driver](https://github.com/nihui/mesa-turnip-android-driver/releases) | 19 |
| [bmdhacks/malisx2](https://github.com/bmdhacks/malisx2/releases) | 13 |
| [Droid-Deck/Drivers](https://github.com/Droid-Deck/Drivers/releases) | 11 |
| [faux123/turnip-faux123-driver](https://github.com/faux123/turnip-faux123-driver/releases) | 11 |
| [sherft2607/turnip-adreno722-duo](https://github.com/sherft2607/turnip-adreno722-duo/releases) | 5 |
| [AlexSanz0902/turnip-sd865-z](https://github.com/AlexSanz0902/turnip-sd865-z/releases) | 4 |
| [Balemuni/Balemunis-Aurora](https://github.com/Balemuni/Balemunis-Aurora/releases) | 4 |
| [The412Banner/Nightlies](https://github.com/The412Banner/Nightlies/releases) | 4 |
| [WearyConcern1165/ExynosTools](https://github.com/WearyConcern1165/ExynosTools/releases) | 4 |
| [s1mptom/freedreno_turnip-CI](https://github.com/s1mptom/freedreno_turnip-CI/releases) | 3 |
| [crueter/GameHub-8Elite-Drivers](https://github.com/crueter/GameHub-8Elite-Drivers/releases) | 2 |
| [The412Banner/Banners-Turnip](https://github.com/The412Banner/Banners-Turnip/releases) | 1 |
| [bmdhacks/armsx2-turnip](https://github.com/bmdhacks/armsx2-turnip/releases) | 1 |
| [sashkinbro/EmuCoreV-Drivers](https://github.com/sashkinbro/EmuCoreV-Drivers/releases) | 1 |
| [zoerakk/qualcomm-adreno-driver](https://github.com/zoerakk/qualcomm-adreno-driver/releases) | 1 |
| **Total** | **761** |

## GPU requirements and recommendations

- **ARMSX2 Turnip axfl3-003** targets Adreno 6xx/7xx and requires Android 10 (API 29) or newer. It includes fixes for Adreno 610/613. It is not an Adreno 8xx package.
- **MaliSX2 0.5.1** supports Mali G31, G51, G52, G76, G57, G68, G77, G78, G78AE, G310, G510, G610, G710, G615 and G715, subject to device firmware and Arm Mali kernel driver compatibility. It requires Android 10 (API 29) or newer. Older MaliSX2 releases support fewer models; read each entry's requirements. MSAA is not implemented.
- Qualcomm and Xclipse packages can require matching vendor firmware and private device libraries. GPU model and driver version are different things.
- Experimental A8xx and device-specific variants are not universal upgrades. Read the package description and upstream release before installation.

ARMSX2 recommends sources by GPU: its own Turnip for Adreno 6xx/7xx, StevenMXZ for Adreno 8xx, and MaliSX2 for supported Mali devices. These are ARMSX2 recommendations, not runtime validation for every EmuCore app. New catalog entries are not automatically marked `recommended`; the shared boolean cannot express GPU-specific recommendations.

See [the ARMSX2 source review](docs/armsx2-source-review.md) for inspected code, source selection and deferred MdiEx packages. PanVK and MdiEx remain outside this catalog pending the relevant device and integration checks.

## Package validation

The catalog links to release assets and preserves source and credits metadata. Archives are not repaired or repackaged by this catalog. The JSON stays a top-level array; retained entry IDs, field names and types remain compatible with existing clients.

Package checks cover asset size and SHA-256 when available, ZIP CRC, safe unique paths, the selected AArch64 Vulkan shared library, Android HAL entry points, and metadata/library agreement when metadata is readable. Client extraction limits are **256 entries**, **64 MiB per file**, and **128 MiB extracted**. Linux-only archives and Magisk/KernelSU-only modules are excluded.

The selected Banners AIO, MaliSX2 0.5.1 and ARMSX2 Turnip axfl3-003 archives were downloaded and checked during the latest updates. Archive validation does not establish rendering correctness or performance on every device, emulator or game.

Known client limitation: upstream ZIP filenames identify installed packages. Releases with the same filename, such as `turnip.zip`, can appear as the same installed driver. Remove the installed package before downloading another release with that filename.

## Catalog URL

Apps read the same catalog URL:

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

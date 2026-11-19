# EmuCoreV Drivers

Shared GPU driver catalog for EmuCoreV, EmuCoreC, EmuCoreR, EmuCoreP, and EmuCoreX.

**761 packages · 24 sources · Updated November 19, 2026**

The catalog includes Turnip, Qualcomm, MaliSX2, and Xclipse packages. Each entry in [`drivers.json`](drivers.json) provides its download link, GPU requirements, description, and credits. Compatibility depends on the device, firmware, and emulator.

## Sources

| Source | Packages |
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

Banners-Turnip is limited to **one selected AIO package** (`v27.0.0-20261109-r2`). Future updates replace this selection instead of importing its automated build history. The separate Nightlies source contains four Rutabaga packages.

Recent additions: **MaliSX2 0.5.1** and **ARMSX2 Turnip axfl3-003** for Adreno 6xx/7xx. Package checks do not establish runtime compatibility; new entries are not automatically marked recommended.

## Catalog URL

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

Previous changes are available in [Git history](https://github.com/sashkinbro/EmuCoreV-Drivers/commits/main/). Technical findings from the ARMSX2 comparison are in the [source review](docs/armsx2-source-review.md).

# EmuCoreV Drivers

Shared GPU driver catalog for EmuCoreV, EmuCoreC, EmuCoreR, EmuCoreP, and EmuCoreX.

**785 packages · 24 sources · Updated November 26, 2026**

The catalog includes Turnip, Qualcomm, MaliSX2, and Xclipse packages. Each entry in [`drivers.json`](drivers.json) provides its download link, GPU requirements, description, and credits. Compatibility depends on the device, firmware, and emulator.

## Sources

| Source | Packages |
| --- | ---: |
| [K11MCH1/AdrenoToolsDrivers](https://github.com/K11MCH1/AdrenoToolsDrivers/releases) | 196 |
| [StevenMXZ/Adreno-Tools-Drivers](https://github.com/StevenMXZ/Adreno-Tools-Drivers/releases) | 117 |
| [Vauzi-17/710](https://github.com/Vauzi-17/710/releases) | 83 |
| [Weab-chan/freedreno_turnip-CI](https://github.com/Weab-chan/freedreno_turnip-CI/releases) | 75 |
| [whitebelyash/AdrenoToolsDrivers](https://github.com/whitebelyash/AdrenoToolsDrivers/releases) | 59 |
| [MrPurple666/purple-turnip](https://github.com/MrPurple666/purple-turnip/releases) | 57 |
| [WinNative-Emu/Drivers](https://github.com/WinNative-Emu/Drivers/releases) | 40 |
| [v3kt0r-87/Mesa-Turnip-Builder](https://github.com/v3kt0r-87/Mesa-Turnip-Builder/releases) | 37 |
| [PojavLauncherTeam/freedreno-builder](https://github.com/PojavLauncherTeam/freedreno-builder/releases) | 22 |
| [nihui/mesa-turnip-android-driver](https://github.com/nihui/mesa-turnip-android-driver/releases) | 21 |
| [bmdhacks/malisx2](https://github.com/bmdhacks/malisx2/releases) | 15 |
| [Droid-Deck/Drivers](https://github.com/Droid-Deck/Drivers/releases) | 17 |
| [faux123/turnip-faux123-driver](https://github.com/faux123/turnip-faux123-driver/releases) | 13 |
| [sherft2607/turnip-adreno722-duo](https://github.com/sherft2607/turnip-adreno722-duo/releases) | 5 |
| [AlexSanz0902/turnip-sd865-z](https://github.com/AlexSanz0902/turnip-sd865-z/releases) | 5 |
| [Balemuni/Balemunis-Aurora](https://github.com/Balemuni/Balemunis-Aurora/releases) | 4 |
| [The412Banner/Nightlies](https://github.com/The412Banner/Nightlies/releases) | 4 |
| [WearyConcern1165/ExynosTools](https://github.com/WearyConcern1165/ExynosTools/releases) | 4 |
| [s1mptom/freedreno_turnip-CI](https://github.com/s1mptom/freedreno_turnip-CI/releases) | 3 |
| [crueter/GameHub-8Elite-Drivers](https://github.com/crueter/GameHub-8Elite-Drivers/releases) | 2 |
| [The412Banner/Banners-Turnip](https://github.com/The412Banner/Banners-Turnip/releases) | 1 |
| [bmdhacks/armsx2-turnip](https://github.com/bmdhacks/armsx2-turnip/releases) | 3 |
| [sashkinbro/EmuCoreV-Drivers](https://github.com/sashkinbro/EmuCoreV-Drivers/releases) | 1 |
| [zoerakk/qualcomm-adreno-driver](https://github.com/zoerakk/qualcomm-adreno-driver/releases) | 1 |
| **Total** | **785** |

Banners-Turnip is limited to **one selected AIO package** (`v27.0.0-20261109-r2`). Future updates replace this selection instead of importing its automated build history. The separate Nightlies source contributes only its Rutabaga packages.

Recent additions: **DD-Turnip-Emu-v1.0.0 (Droid-Deck)**, **DD-Turnip-v1.0.0 (Droid-Deck)**, **Turnip-710-720-722-v4.7-sw (Vauzi-17)**, **Turnip-710-720-722-v4.7-unified (Vauzi-17)** and 3 more. Package checks do not establish runtime compatibility; new entries are not automatically marked recommended.

## Automatic updates

The catalog keeps itself current. Every six hours the [`Sync driver releases`](.github/workflows/sync-drivers.yml) workflow (also startable by hand from the Actions tab) runs [`scripts/sync_drivers.py`](scripts/sync_drivers.py) over the sources in [`scripts/sources.json`](scripts/sources.json):

- every new release ZIP is downloaded and checked: size and SHA-256 against GitHub, ZIP CRCs, safe unique paths, the client limits (256 files, 64 MiB per file, 128 MiB extracted), the Vulkan library the EmuCore installers would select, AArch64 shared-library format, the Android Vulkan HAL `HMI` export, `meta.json`/library agreement, and that every private library the driver links against is bundled;
- a package that passes is added as a new entry, newest first, never marked recommended; package checks are not a device or game test;
- a package that fails, a Linux/Wayland/Magisk/KernelSU asset, or an exact duplicate of a catalog package is recorded with its reason in [`scripts/sync-state.json`](scripts/sync-state.json) and not downloaded again;
- drafts are skipped, and pre-releases unless the catalog already holds one from the same source;
- MaliSX2 entries also get the supported Mali models, changes and contributors from the release notes.

Existing entries are never changed or removed, and the workflow commits only when something changed. **Banners-Turnip**, **ExynosTools** and this repository's own packages stay curated by hand; from The412Banner/Nightlies only the `rutabaga-drivers` release is followed. Network or API errors mark the run as failed and are retried on the next run.

Run `python scripts/sync_drivers.py --dry-run` to see what would be added, `--full` to scan every release page instead of the newest 100 per source.

## Catalog URL

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

Previous changes are available in [Git history](https://github.com/sashkinbro/EmuCoreV-Drivers/commits/main/). Technical findings from the ARMSX2 comparison are in the [source review](docs/armsx2-source-review.md).

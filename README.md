# EmuCoreV Drivers

This repository hosts the GPU driver catalog used by EmuCoreV.

`drivers.json` is a catalog of Adreno driver packages from upstream GitHub releases. Driver ZIP files are not committed to this repository; each entry links to the upstream release asset and keeps source/credits metadata. The top-level array and the existing object fields are kept backward-compatible for every app consuming this catalog.

Current catalog scope:

- Turnip Mesa driver builds
- K11MCH1, StevenMXZ, MrPurple666, whitebelyash, s1mptom, and v3kt0r-87 builds
- nihui Mesa Turnip Android builds with compatible ZIP layout
- Auto, GMEM, SYSMEM, ADPKG, and A8xx variants when available
- Selected Qualcomm packages that use an AdrenoTools-compatible emulator ZIP layout
- ARM Mali vendor (bionic) driver packages extracted from device firmware
- WearyConcern1165 ExynosTools (Vortek) packages for Samsung Xclipse GPUs
- crueter GameHub Adreno packages for Snapdragon 8 Elite
- PojavLauncherTeam freedreno builds for older Adreno 6xx devices

The `gpu` field names the package's target vendor ("Adreno ...", "Mali ...",
"Xclipse ..."). Apps should only offer and install packages whose vendor matches
the device GPU; packages must never be installable across vendors (an Adreno
driver on a Mali device, or the reverse).

Only archives verified to contain a directly loadable Vulkan shared library are listed. Magisk-only packages are excluded.

The Android app reads:

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

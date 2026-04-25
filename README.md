# EmuCoreV Drivers

This repository hosts the GPU driver catalog used by EmuCoreV.

`drivers.json` is a generated catalog of Adreno-compatible driver packages from upstream GitHub releases. Driver ZIP files are not committed to this repository; each entry links to the upstream release asset and keeps source/credits metadata.

Current catalog scope:

- Turnip Mesa driver builds
- Qualcomm/Adreno stock driver packages
- Auto, GMEM, SYSMEM, ADPKG, and A8xx variants when available

The Android app reads:

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

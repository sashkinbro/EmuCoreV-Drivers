# EmuCoreV Drivers

This repository hosts the GPU driver catalog used by EmuCoreV.

`drivers.json` is a generated catalog of Turnip/Mesa Adreno driver packages from upstream GitHub releases. Driver ZIP files are not committed to this repository; each entry links to the upstream release asset and keeps source/credits metadata.

Current catalog scope:

- Turnip Mesa driver builds
- K11MCH1 AdrenoTools-compatible Turnip packages
- nihui Mesa Turnip Android builds with compatible ZIP layout
- Auto, GMEM, SYSMEM, ADPKG, and A8xx variants when available

Qualcomm stock driver packages are intentionally excluded to keep the in-app catalog focused on custom Turnip drivers.

The Android app reads:

```text
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Drivers/main/drivers.json
```

"""Package checks shared by the catalog sync scripts.

These mirror what the EmuCore installers do with a driver ZIP (see
GpuDriverManager.selectMainDriverFile in EmuCoreX) plus the checks used for
manual catalog additions: CRC, safe unique paths, client extraction limits,
AArch64 shared library, Android Vulkan HAL ``HMI`` export, metadata/library
agreement and bundled private dependencies.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import struct
import zipfile
from dataclasses import dataclass, field

# Strictest limits of the current clients.
MAX_ENTRIES = 256
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_EXTRACTED_BYTES = 128 * 1024 * 1024
MAX_ARCHIVE_BYTES = 128 * 1024 * 1024

EM_AARCH64 = 183
ET_DYN = 3
DT_NEEDED = 1

# Libraries a driver may link against without bundling them: Android platform
# and VNDK libraries, plus Qualcomm vendor libraries present on Adreno devices.
SYSTEM_LIBRARIES = {
    "libc.so", "libm.so", "libdl.so", "liblog.so", "libz.so", "libsync.so",
    "libnativewindow.so", "libandroid.so", "libvndksupport.so", "libhardware.so",
    "libcutils.so", "libutils.so", "libbase.so", "libc++.so", "libEGL.so",
    "libGLESv1_CM.so", "libGLESv2.so", "libGLESv3.so", "libdrm.so", "libui.so",
    "libhidlbase.so", "libbinder.so", "libbinder_ndk.so", "libprocessgroup.so",
    "libion.so", "libdmabufheap.so", "libvulkan.so", "libmediandk.so",
    "libgsl.so", "libllvm-glnext.so", "libllvm-qgl.so", "libadreno_utils.so",
    "libadreno_app_profiles.so", "libgralloc.qti.so", "libgralloccore.so",
    "libgrallocutils.so", "libqdMetaData.so", "libqdutils.so", "libsdmcore.so",
    "libdisplayconfig.qti.so", "libCB.so", "libOpenCL.so", "libpdmapper.so",
    "libpdnotifier.so", "libqti-perfd-client.so", "libdl_android.so",
}
SYSTEM_LIBRARY_PATTERNS = (
    re.compile(r"^android\.hardware\..+\.so$"),
    re.compile(r"^vendor\.qti\..+\.so$"),
    re.compile(r"^libhidl.*\.so$"),
)


class PackageError(Exception):
    pass


@dataclass
class Package:
    sha256: str
    size: int
    library: str
    meta: dict | None
    needed: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


def select_main_library(names: list[str]) -> str | None:
    """Same order as the EmuCore installers."""
    libs = [n for n in names if n.lower().endswith(".so")]
    base = lambda n: n.rsplit("/", 1)[-1].lower()
    for pick in (
        lambda n: base(n) == "libvulkan.so",
        lambda n: base(n).startswith(("vulkan.", "libvulkan.")),
        lambda n: "vulkan" in n.lower(),
    ):
        for n in libs:
            if pick(n):
                return n
    return None


def _elf_info(data: bytes) -> tuple[list[str], set[str]]:
    """Return (DT_NEEDED names, exported dynamic symbol names) of an ELF64 LE file."""
    if len(data) < 64 or data[:4] != b"\x7fELF":
        raise PackageError("main library is not an ELF file")
    if data[4] != 2 or data[5] != 1:
        raise PackageError("main library is not a 64-bit little-endian ELF")
    e_type, e_machine = struct.unpack_from("<HH", data, 16)
    if e_type != ET_DYN:
        raise PackageError("main library is not a shared library")
    if e_machine != EM_AARCH64:
        raise PackageError("main library is not AArch64")
    e_shoff = struct.unpack_from("<Q", data, 40)[0]
    e_shentsize, e_shnum = struct.unpack_from("<HH", data, 58)
    if not e_shoff or e_shentsize != 64 or e_shoff + e_shnum * 64 > len(data):
        raise PackageError("main library has no readable section table")
    sections = [struct.unpack_from("<IIQQQQIIQQ", data, e_shoff + i * 64) for i in range(e_shnum)]

    def blob(sec):
        return data[sec[4]:sec[4] + sec[5]]

    needed, exports = [], set()
    for sec in sections:
        sh_type, sh_link = sec[1], sec[6]
        if sh_type == 6 and sh_link < len(sections):  # SHT_DYNAMIC
            strtab = blob(sections[sh_link])
            dyn = blob(sec)
            for off in range(0, len(dyn) - 15, 16):
                tag, val = struct.unpack_from("<qQ", dyn, off)
                if tag == 0:
                    break
                if tag == DT_NEEDED:
                    needed.append(strtab[val:strtab.index(b"\0", val)].decode("utf-8", "replace"))
        elif sh_type == 11 and sh_link < len(sections):  # SHT_DYNSYM
            strtab = blob(sections[sh_link])
            syms = blob(sec)
            for off in range(0, len(syms) - 23, 24):
                st_name, st_info, _o, st_shndx = struct.unpack_from("<IBBH", syms, off)
                if st_shndx != 0 and st_name and (st_info >> 4) in (1, 2):  # GLOBAL/WEAK, defined
                    exports.add(strtab[st_name:strtab.index(b"\0", st_name)].decode("utf-8", "replace"))
    return needed, exports


def is_system_library(name: str) -> bool:
    return name in SYSTEM_LIBRARIES or any(p.match(name) for p in SYSTEM_LIBRARY_PATTERNS)


def _android_meta(zf: zipfile.ZipFile, names: list[str]) -> dict | None:
    metas = []
    for n in names:
        if n.rsplit("/", 1)[-1].lower() == "meta.json":
            try:
                raw = zf.read(n).decode("utf-8-sig", "replace")
                m = json.loads(raw)
            except ValueError:
                continue
            if isinstance(m, dict):
                metas.append(m)
    android = [m for m in metas if str(m.get("platform", "android")).lower() == "android"]
    return android[0] if android else None


def check_package(data: bytes, expected_size: int | None = None, digest: str | None = None) -> Package:
    if expected_size is not None and len(data) != expected_size:
        raise PackageError(f"size {len(data)} != GitHub asset size {expected_size}")
    sha = hashlib.sha256(data).hexdigest()
    if digest and digest != f"sha256:{sha}":
        raise PackageError(f"SHA-256 does not match GitHub digest {digest}")
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise PackageError(f"not a ZIP: {exc}") from exc
    with zf:
        infos = [i for i in zf.infolist() if not i.is_dir()]
        if len(infos) > MAX_ENTRIES:
            raise PackageError(f"{len(infos)} files, client limit is {MAX_ENTRIES}")
        names = []
        for i in infos:
            n = i.filename.replace("\\", "/").lstrip("/")
            if not n or ".." in n or ":" in n:
                raise PackageError(f"unsafe path {i.filename!r}")
            if i.file_size > MAX_FILE_BYTES:
                raise PackageError(f"{n} is larger than the 64 MiB client limit")
            names.append(n)
        if len({n.lower() for n in names}) != len(names):
            raise PackageError("duplicate paths in ZIP")
        if sum(i.file_size for i in infos) > MAX_EXTRACTED_BYTES:
            raise PackageError("extracted size over the 128 MiB client limit")
        lower = [n.lower() for n in names]
        if any(n.endswith("module.prop") or "meta-inf/com/google" in n for n in lower):
            raise PackageError("Magisk/KernelSU module")
        try:
            bad = zf.testzip()
        except (zipfile.BadZipFile, NotImplementedError, OSError) as exc:
            raise PackageError(f"cannot read ZIP: {exc}") from exc
        if bad:
            raise PackageError(f"CRC error in {bad}")
        lib = select_main_library(names)
        if not lib:
            raise PackageError("no Vulkan library the installers would select")
        lib_info = infos[names.index(lib)]
        needed, exports = _elf_info(zf.read(lib_info))
        if "HMI" not in exports:
            raise PackageError(f"{lib} does not export the Android Vulkan HAL entry point HMI")
        meta = _android_meta(zf, names)
        if meta and isinstance(meta.get("libraryName"), str) and meta["libraryName"]:
            declared = meta["libraryName"].rsplit("/", 1)[-1]
            if declared.lower() != lib.rsplit("/", 1)[-1].lower():
                raise PackageError(f"meta.json libraryName {declared!r} is not the selected library {lib!r}")
        bundled = {n.rsplit("/", 1)[-1] for n in names}
        missing = [d for d in needed if d not in bundled and not is_system_library(d)]
        if missing:
            raise PackageError(f"{lib} needs private libraries that are not bundled: {', '.join(missing)}")
    return Package(sha256=sha, size=len(data), library=lib, meta=meta, needed=needed, files=names)

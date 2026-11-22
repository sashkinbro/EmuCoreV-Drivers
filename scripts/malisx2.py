"""MaliSX2 (bmdhacks/malisx2) entries for the driver catalog.

Used by sync_drivers.py. For each published release the Android ZIP
(``malisx2-<ver>-<commit>.zip``) is checked and a ``mali-sx2-<ver>`` entry is
built with the supported Mali models, changes and contributors from the
release notes. Entries go to the top of the MaliSX2 block (newest first).
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import struct
import zipfile
from pathlib import Path

ID_PREFIX = "mali-sx2-"
MAX_UNCOMPRESSED_BYTES = 256 * 1024 * 1024
ELF_MACHINE_AARCH64 = 183
LIBRARY_NAME = "libvulkan_malisx2.so"


class CheckError(Exception):
    pass


def version_of(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def plain(text: str) -> str:
    """Markdown bullet text -> plain sentence text."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def section(body: str, title_regex: str) -> str:
    # The heading is matched on its own line only; the body runs to the next "## ".
    m = re.search(rf"^##[ \t]+{title_regex}[^\n]*\n(.*?)(?=^##\s|\Z)", body, re.M | re.S | re.I)
    return m.group(1) if m else ""


def bullets(text: str) -> list[str]:
    return [plain(m) for m in re.findall(r"^\s*[-*]\s+(.+)$", text, re.M)]


def parse_models(body: str) -> list[str]:
    """Bold bullet lines like '- **Mali-G31, G51, G52, G76**' in the release intro."""
    models: list[str] = []
    intro = re.split(r"^##\s", body, maxsplit=1, flags=re.M)[0]
    for line in re.findall(r"^\s*[-*]\s+\*\*(.+?)\*\*\s*$", intro, re.M):
        line = re.sub(r"(?i)\b(?:mali|immortalis)-", "", line)
        tokens = [t.strip() for t in line.split(",")]
        if not tokens or not all(re.fullmatch(r"G\d{2,3}(?:AE)?", t) for t in tokens):
            continue
        models.extend(t for t in tokens if t not in models)
    return models


def parse_contributors(body: str) -> list[str]:
    names = []
    for item in re.findall(r"^\s*[-*]\s+@([A-Za-z0-9-]+)", section(body, r"Contributors"), re.M):
        if item.lower() != "bmdhacks" and item not in names:
            names.append(item)
    return names


def pick_asset(release: dict) -> dict:
    version = version_of(release["tag_name"])
    pattern = re.compile(rf"^malisx2-{re.escape(version)}-[0-9a-f]{{6,40}}\.zip$")
    named = re.search(r"Install on Android:.*?`([^`]+\.zip)`", release.get("body") or "", re.S)
    assets = [a for a in release.get("assets", []) if pattern.match(a["name"])]
    if named:
        preferred = [a for a in assets if a["name"] == named.group(1)]
        if preferred:
            return preferred[0]
    if len(assets) != 1:
        raise CheckError(f"{release['tag_name']}: expected one Android ZIP asset, found {len(assets)}")
    return assets[0]


def check_zip(data: bytes, asset: dict, body: str) -> dict:
    """Package checks used for manual additions. Returns meta.json."""
    if len(data) != asset["size"]:
        raise CheckError(f"size {len(data)} != GitHub asset size {asset['size']}")
    sha = hashlib.sha256(data).hexdigest()
    digest = asset.get("digest") or ""
    if digest and digest != f"sha256:{sha}":
        raise CheckError(f"SHA-256 {sha} does not match GitHub digest {digest}")
    if f"`{asset['name']}` sha256 `" in body and sha not in body:
        raise CheckError("SHA-256 does not match the release notes")
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise CheckError(f"not a ZIP: {exc}") from exc
    with zf:
        bad = zf.testzip()
        if bad:
            raise CheckError(f"CRC error in {bad}")
        names = [i.filename for i in zf.infolist()]
        if len(names) != len(set(names)):
            raise CheckError("duplicate paths in ZIP")
        for n in names:
            if n.startswith(("/", "\\")) or ".." in Path(n).parts or ":" in n:
                raise CheckError(f"unsafe path {n!r}")
        if sum(i.file_size for i in zf.infolist()) > MAX_UNCOMPRESSED_BYTES:
            raise CheckError("uncompressed size over the client limit")
        meta_names = [n for n in names if Path(n).name == "meta.json"]
        if len(meta_names) != 1:
            raise CheckError("meta.json missing or duplicated")
        meta = json.loads(zf.read(meta_names[0]))
        if meta.get("schemaVersion") != 1:
            raise CheckError(f"meta.json schemaVersion {meta.get('schemaVersion')!r} != 1")
        lib = meta.get("libraryName")
        if lib != LIBRARY_NAME:
            raise CheckError(f"meta.json libraryName {lib!r} != {LIBRARY_NAME}")
        lib_paths = [n for n in names if Path(n).name == lib]
        if len(lib_paths) != 1:
            raise CheckError(f"{lib} missing or duplicated")
        elf = zf.read(lib_paths[0])
        if elf[:4] != b"\x7fELF" or elf[4] != 2 or elf[5] != 1:
            raise CheckError(f"{lib} is not a 64-bit little-endian ELF")
        if struct.unpack_from("<H", elf, 16)[0] != 3:
            raise CheckError(f"{lib} is not a shared library (ET_DYN)")
        if struct.unpack_from("<H", elf, 18)[0] != ELF_MACHINE_AARCH64:
            raise CheckError(f"{lib} is not AArch64")
        lib_sha = hashlib.sha256(elf).hexdigest()
        m = re.search(r"Android `" + re.escape(lib) + r"` sha256 `([0-9a-f]{64})`", body)
        if m and m.group(1) != lib_sha:
            raise CheckError(f"{lib} SHA-256 does not match the release notes")
    meta["_sha256"] = sha
    return meta


def describe(version: str, prev: str | None, body: str, min_api: int) -> str:
    news = bullets(section(body, r"What.s new"))
    notes = " ".join(n if n.endswith((".", "!", "?")) else n + "." for n in news)
    parts = ["MaliSX2 Vulkan driver by ARMSX2 and bmdhacks for supported Mali GPUs."]
    if notes:
        since = f" since {prev}" if prev else ""
        parts.append(f"Changes in {version}{since}: {notes}")
    if "driverInfo" in body:
        parts.append("The pipeline cache is rebuilt once after the update because the version is part of driverInfo.")
    parts.append(
        "Requires Arm's own Mali kernel driver (kbase); systems using only the open-source "
        "Linux Panthor or Panfrost driver are not covered."
    )
    if re.search(r"MSAA is not implemented", body, re.I):
        parts.append("MSAA is not implemented, so an app that assumes 4x multisampling may not start.")
    parts.append("Other Mali generations are unsupported.")
    parts.append(f"Requires Android {android_name(min_api)} (API {min_api}) or newer.")
    parts.append("Device firmware and kernel compatibility still apply.")
    return " ".join(parts)


def android_name(api: int) -> str:
    return {26: "8.0", 27: "8.1", 28: "9", 29: "10", 30: "11", 31: "12", 32: "12L",
            33: "13", 34: "14", 35: "15", 36: "16"}.get(api, f"API {api}")


def gpu_label(models: list[str]) -> str:
    return f"Mali Bifrost/Valhall/5th gen ({', '.join(models)})"


def build_entry(release: dict, asset: dict, meta: dict, prev_entry: dict | None) -> tuple[dict, list[str]]:
    warnings = []
    version = version_of(release["tag_name"])
    body = release.get("body") or ""
    models = parse_models(body)
    if not models:
        if not prev_entry or not prev_entry.get("supportedGpuModels"):
            raise CheckError("no supported GPU models in release notes and no previous entry to inherit from")
        models = list(prev_entry["supportedGpuModels"])
        warnings.append(f"{version}: supported models not found in release notes; inherited from {prev_entry['version']}")
    contributors = parse_contributors(body)
    credits = " / ".join(["ARMSX2", "bmdhacks", *contributors, "MaliSX2 contributors"]) + " (MIT)"
    min_api = int(meta.get("minApi") or 29)
    entry = {
        "id": f"{ID_PREFIX}{version}",
        "name": f"MaliSX2 {version}",
        "version": version,
        "tag": release["tag_name"],
        "family": "Mali",
        "variant": "MaliSX2",
        "gpu": gpu_label(models),
        "description": describe(version, prev_entry["version"] if prev_entry else None, body, min_api),
        "recommended": False,
        "publishedAt": release["published_at"],
        "downloadUrl": asset["browser_download_url"],
        "sourceUrl": release["html_url"],
        "credits": credits,
        "sizeBytes": asset["size"],
        "sha256": meta["_sha256"],
        "supportedGpuModels": models,
    }
    return entry, warnings


def is_malisx2(entry: dict) -> bool:
    return entry.get("id", "").startswith(ID_PREFIX)


def insert_entry(catalog: list[dict], entry: dict) -> None:
    """Insert into the MaliSX2 block, which is ordered newest first."""
    idx = [i for i, e in enumerate(catalog) if is_malisx2(e)]
    if not idx:
        catalog.append(entry)
        return
    for i in idx:
        if catalog[i]["publishedAt"] < entry["publishedAt"]:
            catalog.insert(i, entry)
            return
    catalog.insert(idx[-1] + 1, entry)


def new_entries(catalog: list[dict], releases: list[dict], download, include_pre: bool = False):
    """Return (entries added to catalog, failures, warnings). Inserts in place."""
    known_tags = {e["tag"] for e in catalog if is_malisx2(e)}
    known_ids = {e["id"] for e in catalog}
    include_pre = include_pre or any(r["prerelease"] and r["tag_name"] in known_tags for r in releases)
    candidates = sorted(
        (r for r in releases
         if not r["draft"] and (include_pre or not r["prerelease"])
         and r["tag_name"] not in known_tags
         and f"{ID_PREFIX}{version_of(r['tag_name'])}" not in known_ids),
        key=lambda r: r["published_at"])
    added, failed, warnings = [], [], []
    for rel in candidates:
        try:
            asset = pick_asset(rel)
            data = download(asset["browser_download_url"])
            meta = check_zip(data, asset, rel.get("body") or "")
            prev = next((e for e in catalog if is_malisx2(e) and e["publishedAt"] < rel["published_at"]), None)
            entry, warns = build_entry(rel, asset, meta, prev)
        except (CheckError, OSError, ValueError, KeyError) as exc:
            failed.append(f"bmdhacks/malisx2 {rel['tag_name']}: {exc}")
            continue
        insert_entry(catalog, entry)
        added.append(entry)
        warnings.extend(warns)
    return added, failed, warnings

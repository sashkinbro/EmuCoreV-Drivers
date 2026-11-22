#!/usr/bin/env python3
"""Keep drivers.json in sync with the GitHub releases of every catalog source.

Sources and their rules are in scripts/sources.json. For each source the
script lists its GitHub releases, and every release ZIP that is not yet known
is downloaded and checked like the manual additions were (see driverpkg.py).
A package that passes becomes a new catalog entry; one that fails is recorded
in scripts/sync-state.json with the reason, so it is not downloaded again.

* Existing entries are never changed or removed.
* Drafts are skipped. Pre-releases are skipped unless the catalog already holds
  a pre-release from the same source.
* Linux, Wayland, Magisk/KernelSU and similar assets are skipped by name.
* Exact SHA-256 duplicates of a catalog package are not added again.
* Running it twice in a row changes nothing (idempotent).
* Network or API errors are reported, nothing is recorded for them, and the
  exit status is 1 so the workflow run shows as failed; they are retried on
  the next run.

Usage:
  python scripts/sync_drivers.py             # newest 100 releases per source
  python scripts/sync_drivers.py --full      # every release of every source
  python scripts/sync_drivers.py --dry-run   # report only, write nothing
  python scripts/sync_drivers.py --only bmdhacks/malisx2

Only the Python standard library is used. GITHUB_TOKEN is used for API calls
when set.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import driverpkg  # noqa: E402
import malisx2  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "drivers.json"
README = ROOT / "README.md"
SOURCES = ROOT / "scripts" / "sources.json"
STATE = ROOT / "scripts" / "sync-state.json"
USER_AGENT = "EmuCoreV-Drivers-sync"
TAIL = ("GPU model, kernel and emulator compatibility still depend on the upstream release; "
        "not a universal replacement for all Adreno devices.")
VARIANT_RULES = [
    (r"oneui", "OneUI"), (r"patched", "Patched"), (r"sysmem", "SYSMEM"), (r"gmem", "GMEM"),
    (r"-p_|performance", "Performance"), (r"-b_|balanced", "Balanced"), (r"sync", "Sync"),
    (r"rutabaga", "Rutabaga"), (r"aio|universal|alladreno", "Universal"),
    (r"-win\.zip$", "Winlator"), (r"-sw\.zip$", "Switch"),
]
VARIANT_NOTES = {
    "OneUI": "OneUI-specific workaround; use only for the device/UI issue described upstream.",
    "Performance": "This build may request high GPU clocks, increasing power use and heat.",
}


class NetworkError(OSError):
    pass


# ---------------------------------------------------------------- network

def _open(url: str, accept: str, api: bool):
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    token = os.environ.get("GITHUB_TOKEN")
    if api and token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120)
    except (urllib.error.URLError, OSError) as exc:
        raise NetworkError(f"{url}: {exc}") from exc


def api_get(url: str):
    with _open(url, "application/vnd.github+json", True) as resp:
        return json.loads(resp.read()), resp.headers.get("Link", "")


def list_releases(repo: str, full: bool) -> list[dict]:
    url = f"https://api.github.com/repos/{repo}/releases?per_page=100"
    out = []
    while url:
        page, link = api_get(url)
        out.extend(page)
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if (full and m) else None
    return out


def download(url: str) -> bytes:
    with _open(url, "application/octet-stream", False) as resp:
        data = resp.read(driverpkg.MAX_ARCHIVE_BYTES + 1)
    if len(data) > driverpkg.MAX_ARCHIVE_BYTES:
        raise driverpkg.PackageError("archive larger than 128 MiB")
    return data


# ---------------------------------------------------------------- helpers

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def asset_stem(name: str) -> str:
    stem = re.sub(r"(?i)\.zip$", "", urllib.parse.unquote(name))
    return re.sub(r"(?i)\.adpkg$", "", stem)


def repo_of(url: str) -> str:
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/", url)
    return m.group(1).lower() if m else ""


def canon(url: str, aliases: dict[str, str]) -> str:
    repo = repo_of(url)
    tail = url.split("/", 5)[5] if url.count("/") >= 5 else url
    return f"{aliases.get(repo, repo)}/{urllib.parse.unquote(tail)}".lower()


def clean(text) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text.replace("�", "-")).strip()


def sentence(text: str) -> str:
    text = clean(text)
    return text if not text or text.endswith((".", "!", "?")) else text + "."


def guess_version(stem: str, tag: str, meta: dict | None, from_meta: bool) -> str:
    if from_meta and meta:
        m = re.search(r"\d+\.\d+\.\d+(?:-devel)?", clean(meta.get("driverVersion")))
        if m:
            return m.group(0)
    m = re.search(r"(?:^|[^A-Za-z0-9.])[vV]?(\d+(?:\.\d+){1,2})(?![\d.]*\d)", stem)
    if m:
        return m.group(1)
    return tag[1:] if tag.startswith(("v", "V")) and len(tag) > 1 else tag


# ---------------------------------------------------------------- entries

def build_entry(src: dict, cfg: dict, rel: dict, asset: dict, pkg: driverpkg.Package) -> dict:
    repo, tag = src["repo"], rel["tag_name"]
    owner = repo.split("/")[0]
    name = urllib.parse.unquote(asset["name"])
    stem = asset_stem(name)
    if not re.search(r"\d", stem):  # generic names such as turnip.zip
        stem = f"{stem} {tag}"
    meta = pkg.meta or {}
    vendor = clean(meta.get("vendor")).lower()
    qualcomm = "qualcomm" in vendor or any("gsl" in n for n in pkg.needed)
    family = "Qualcomm" if qualcomm else "Turnip"

    variant = src.get("variant")
    if not variant:
        variant = next((v for rx, v in VARIANT_RULES if re.search(rx, name, re.I)), "Standard")
    gpu = src.get("gpu") or next(
        (g for rx, g in cfg["gpuRules"] if re.search(rx, f"{name} {tag}")), cfg["defaultGpu"])

    parts = [f"{family} Vulkan driver package from {repo}, upstream release {tag}."]
    if clean(meta.get("description")):
        parts.append(sentence(meta.get("description")))
    min_api = meta.get("minApi")
    if isinstance(min_api, int) and not isinstance(min_api, bool) and 14 <= min_api <= 40:
        parts.append(f"Package declares Android API {min_api} or newer.")
    else:
        parts.append("Android version requirements are not declared reliably in package metadata; "
                     "check the upstream release.")
    notes = list(src.get("notes", []))
    if variant in VARIANT_NOTES and VARIANT_NOTES[variant] not in notes:
        notes.insert(0, VARIANT_NOTES[variant])
    parts.extend(notes)
    if qualcomm:
        parts.append("Qualcomm vendor binaries require compatible device firmware and vendor libraries.")
    parts.append(TAIL)

    if "credits" in src:
        credits = list(src["credits"])
    else:
        author = clean(meta.get("author"))
        skip = {owner.lower(), "qualcomm"} if qualcomm else {owner.lower()}
        credits = [owner] + ([author] if author and author.lower() not in skip else [])
        credits += ["Qualcomm"] if qualcomm else ["Mesa", "Freedreno contributors"]
    credits += src.get("creditsSuffix", [])

    url = asset["browser_download_url"]
    entry_id = (src["idTemplate"].format(tag=slug(tag)) if "idTemplate" in src else
                f"{slug(owner)}-{slug(tag)}-{slug(stem)}-{hashlib.sha256(url.encode()).hexdigest()[:8]}")
    return {
        "id": entry_id,
        "name": src["nameTemplate"].format(tag=tag) if "nameTemplate" in src
        else f"{stem.replace('_', ' ')} ({owner})",
        "version": guess_version(asset_stem(name), tag, pkg.meta, src.get("versionFromMeta", False)),
        "tag": tag,
        "family": family,
        "variant": variant,
        "gpu": gpu,
        "description": " ".join(parts),
        "recommended": False,
        "publishedAt": rel["published_at"],
        "downloadUrl": url,
        "sourceUrl": rel["html_url"],
        "credits": " / ".join(credits),
        "sizeBytes": pkg.size,
        "sha256": pkg.sha256,
    }


def insert_general(catalog: list[dict], entry: dict) -> None:
    """Insert into the leading block, which is ordered newest first (MaliSX2 follows it)."""
    end = next((i for i, e in enumerate(catalog) if malisx2.is_malisx2(e)), len(catalog))
    for i in range(end):
        if catalog[i]["publishedAt"] < entry["publishedAt"]:
            catalog.insert(i, entry)
            return
    catalog.insert(end, entry)


# ---------------------------------------------------------------- README

def update_readme(text: str, catalog: list[dict], cfg: dict, added: list[dict], today: dt.date) -> str:
    aliases = {}
    for s in cfg["sources"]:
        for a in s.get("aliases", []):
            aliases[a.lower()] = s["repo"].lower()
    counts: dict[str, int] = {}
    for e in catalog:
        r = repo_of(e["downloadUrl"])
        r = aliases.get(r, r)
        counts[r] = counts.get(r, 0) + 1

    def row(m):
        return f"{m.group(1)}{counts.get(m.group(2).lower(), 0)} |"
    text = re.sub(r"(\| \[([^\]]+/[^\]]+)\]\(https://github\.com/[^)]*\) \| )[\d,]+ \|", row, text)
    total = len(catalog)
    text = re.sub(r"(\| \*\*Total\*\* \| \*\*)[\d,]+(\*\* \|)", rf"\g<1>{total}\g<2>", text, count=1)
    date = f"{today:%B} {today.day}, {today.year}"
    text = re.sub(r"\*\*[\d,]+ packages · (\d+) sources · Updated [^*]+\*\*",
                  lambda m: f"**{total} packages · {m.group(1)} sources · Updated {date}**", text, count=1)
    if added:
        newest = sorted(added, key=lambda e: e["publishedAt"], reverse=True)
        names = [f"**{e['name']}**" for e in newest[:4]]
        more = len(newest) - len(names)
        listed = ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1]
        if more:
            listed = ", ".join(names) + f" and {more} more"
        text = re.sub(r"^Recent additions: .*?(?= Package checks do not establish)",
                      f"Recent additions: {listed}.", text, count=1, flags=re.M)
    return text


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--full", action="store_true", help="scan every release page, not only the newest 100")
    ap.add_argument("--only", action="append", default=[], help="limit to these owner/repo sources")
    args = ap.parse_args()

    cfg = json.loads(SOURCES.read_text(encoding="utf-8"))
    raw = CATALOG.read_text(encoding="utf-8")
    catalog = json.loads(raw)
    if json.dumps(catalog, indent=2, ensure_ascii=False) + "\n" != raw:
        print("drivers.json is not in canonical format; refusing to rewrite", file=sys.stderr)
        return 2
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"excluded": {}}
    excluded: dict[str, str] = state["excluded"]
    state_before = json.dumps(state, sort_keys=True)

    aliases = {}
    for s in cfg["sources"]:
        for a in s.get("aliases", []):
            aliases[a.lower()] = s["repo"].lower()
    known = {canon(e["downloadUrl"], aliases) for e in catalog}
    known |= {canon(u, aliases) for u in excluded}
    by_sha = {e["sha256"]: e["id"] for e in catalog if e.get("sha256")}
    skip_name = re.compile(cfg["excludeAssets"])

    added: list[dict] = []
    rejected: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []

    for src in cfg["sources"]:
        repo, mode = src["repo"], src["mode"]
        if mode == "manual" or (args.only and repo not in args.only):
            continue
        try:
            if mode == "tag":
                rel, _ = api_get(f"https://api.github.com/repos/{repo}/releases/tags/{src['tag']}")
                releases = [rel]
            else:
                releases = list_releases(repo, args.full)
        except NetworkError as exc:
            errors.append(f"{repo}: {exc}")
            continue

        if mode == "malisx2":
            try:
                new, failed, warns = malisx2.new_entries(catalog, releases, download)
            except NetworkError as exc:
                errors.append(f"{repo}: {exc}")
                continue
            added.extend(new)
            errors.extend(failed)
            warnings.extend(warns)
            continue

        repos = {repo.lower(), *[a.lower() for a in src.get("aliases", [])]}
        own_tags = {e["tag"] for e in catalog if aliases.get(repo_of(e["downloadUrl"]), repo_of(e["downloadUrl"])) in repos}
        include_pre = any(r["prerelease"] and r["tag_name"] in own_tags for r in releases)
        include = re.compile(src["include"]) if "include" in src else None
        for rel in sorted(releases, key=lambda r: r["published_at"] or ""):
            if rel["draft"] or (rel["prerelease"] and not include_pre):
                continue
            for asset in rel.get("assets", []):
                url, name = asset["browser_download_url"], asset["name"]
                if not name.lower().endswith(".zip") or (include and not include.search(name)):
                    continue
                key = canon(url, aliases)
                if key in known:
                    continue
                known.add(key)
                if skip_name.search(name):
                    excluded[url] = "not an Android driver package (asset name)"
                    continue
                if asset["size"] > driverpkg.MAX_ARCHIVE_BYTES:
                    excluded[url] = f"archive is {asset['size']} bytes, over the 128 MiB limit"
                    rejected.append(f"{repo} {name}: {excluded[url]}")
                    continue
                try:
                    data = download(url)
                    pkg = driverpkg.check_package(data, asset["size"], asset.get("digest"))
                except NetworkError as exc:
                    known.discard(key)
                    errors.append(f"{repo} {name}: {exc}")
                    continue
                except driverpkg.PackageError as exc:
                    excluded[url] = str(exc)
                    rejected.append(f"{repo} {name}: {exc}")
                    continue
                if pkg.sha256 in by_sha:
                    excluded[url] = f"same SHA-256 as catalog entry {by_sha[pkg.sha256]}"
                    rejected.append(f"{repo} {name}: {excluded[url]}")
                    continue
                entry = build_entry(src, cfg, rel, asset, pkg)
                insert_general(catalog, entry)
                by_sha[pkg.sha256] = entry["id"]
                added.append(entry)

    for e in added:
        print(f"added {e['id']} ({e['sizeBytes']} bytes, sha256 {e['sha256']})")
    for r in rejected:
        print(f"rejected {r}")
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if not added and not rejected:
        print("catalog is up to date")

    state_changed = json.dumps(state, sort_keys=True) != state_before
    if not args.dry_run:
        if added:
            CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8", newline="\n")
            readme = README.read_text(encoding="utf-8")
            README.write_text(update_readme(readme, catalog, cfg, added, dt.datetime.now(dt.timezone.utc).date()),
                              encoding="utf-8", newline="\n")
        if state_changed:
            state["excluded"] = dict(sorted(excluded.items()))
            STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write("## Driver catalog sync\n\n")
            fh.write("".join(f"- added {e['name']}\n" for e in added) or "- no new packages\n")
            fh.write("".join(f"- rejected {r}\n" for r in rejected))
            fh.write("".join(f"- warning: {w}\n" for w in warnings))
            fh.write("".join(f"- error: {e}\n" for e in errors))
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"changed={'true' if (added or state_changed) else 'false'}\n")
            fh.write(f"count={len(added)}\n")
            title = ", ".join(e["name"] for e in added[:3]) + (f" and {len(added) - 3} more" if len(added) > 3 else "")
            fh.write(f"title={title}\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

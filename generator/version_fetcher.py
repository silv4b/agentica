import json
import logging
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

TIMEOUT = 5
CACHE_TTL = timedelta(hours=1)

PYPI_URL = "https://pypi.org/pypi/{pkg}/json"
NPM_URL = "https://registry.npmjs.org/{pkg}/latest"
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
CARGO_URL = "https://crates.io/api/v1/crates/{pkg}"
RUBYGEMS_URL = "https://rubygems.org/api/v1/gems/{pkg}.json"

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def _fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logger.warning("Failed to fetch %s: %s", url, e)
        return None


def _clean_version(raw):
    v = raw.lstrip("vV")
    m = SEMVER_RE.match(v)
    return m.group(0) if m else v.split("-")[0]


def _fetch_pypi(pkg):
    data = _fetch_json(PYPI_URL.format(pkg=pkg))
    if data:
        return _clean_version(data["info"]["version"])
    return None


def _fetch_npm(pkg):
    data = _fetch_json(NPM_URL.format(pkg=pkg))
    if data:
        return _clean_version(data.get("version", ""))
    return None


def _fetch_github(repo):
    data = _fetch_json(
        GITHUB_API.format(owner=repo.split("/")[0], repo=repo.split("/")[1]),
        headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Agentica/1.0"},
    )
    if data:
        return _clean_version(data.get("tag_name", ""))
    return None


def _fetch_cargo(pkg):
    data = _fetch_json(CARGO_URL.format(pkg=pkg))
    if data:
        return _clean_version(data.get("crate", {}).get("max_stable_version", ""))
    return None


def _fetch_rubygems(pkg):
    data = _fetch_json(RUBYGEMS_URL.format(pkg=pkg))
    if data:
        return _clean_version(data.get("version", ""))
    return None


FETCHERS = {
    "pypi": _fetch_pypi,
    "npm": _fetch_npm,
    "github": _fetch_github,
    "cargo": _fetch_cargo,
    "rubygems": _fetch_rubygems,
}


def fetch_latest_version(version_source):
    if not version_source:
        return None
    parts = version_source.split(":", 1)
    if len(parts) != 2:
        return None
    registry, identifier = parts
    fetcher = FETCHERS.get(registry)
    if not fetcher:
        return None
    return fetcher(identifier)


def needs_version_check(tech, now=None):
    if not tech.version_source:
        return False
    if not tech.latest_version:
        return True
    if not tech.version_checked_at:
        return True
    now = now or datetime.now(tz=tech.version_checked_at.tzinfo)
    return (now - tech.version_checked_at) > CACHE_TTL


def get_version_label(tech, include_latest=False):
    base = tech.display_name
    if tech.latest_version:
        base += f" {tech.latest_version}"
    if include_latest and tech.version_source and not tech.latest_version:
        base += " (version unknown)"
    return base

"""Bounded, read-only ProPresenter API preflight (standard library only)."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, build_opener

# Leave room for interpreter startup within the user's ten-second limit.
PROBE_TIMEOUT = 8
HELP = ("Open ProPresenter > Settings > Network, enable Network, and confirm "
        "the port. Then rerun the command. Do not fall back to computer use.")


class NetworkAccessError(RuntimeError):
    pass


def resolve_api_url(explicit_url: str | None = None) -> str:
    url = explicit_url or os.environ.get("PROPRESENTER_API_URL")
    if not url:
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise NetworkAccessError("Set --api-url http://127.0.0.1:PORT using the port in ProPresenter. " + HELP)
        preferences = Path(appdata) / "RenewedVision/ProPresenter/Preferences/NetworkPreferences.proPref"
        try:
            values = dict(line.strip().rstrip(";").split("=", 1)
                          for line in preferences.read_text(encoding="utf-8-sig").splitlines()
                          if "=" in line)
        except OSError as exc:
            raise NetworkAccessError("Cannot read ProPresenter's network settings. Use --api-url. " + HELP) from exc
        if values.get("EnableNetwork", "false").lower() != "true":
            raise NetworkAccessError("ProPresenter Network is turned off. " + HELP)
        port = values.get("NetworkPort", "")
        if not port.isdigit() or not 1 <= int(port) <= 65535:
            raise NetworkAccessError("ProPresenter's network port is missing or invalid. " + HELP)
        url = f"http://127.0.0.1:{port}"
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise NetworkAccessError("Invalid ProPresenter API URL. Use http://HOST:PORT.") from exc
    if (parsed.scheme not in ("http", "https") or not parsed.hostname or
            port is None or not 1 <= port <= 65535 or parsed.username or parsed.password or
            parsed.path not in ("", "/") or parsed.query or parsed.fragment):
        raise NetworkAccessError("Invalid ProPresenter API URL. Use http://HOST:PORT without credentials or a path.")
    return url.rstrip("/")


def _probe(url: str) -> dict:
    # Ignore system web proxies for the app's local API. The parent enforces a
    # total deadline even if a server trickles bytes or DNS/HTTP stalls.
    opener = build_opener(ProxyHandler({}))
    with opener.open(url + "/version", timeout=PROBE_TIMEOUT) as response:
        version = json.loads(response.read(65537))
    if (not isinstance(version, dict) or version.get("api_version") != "v1" or
            "ProPresenter" not in version.get("host_description", "")):
        raise ValueError("The configured endpoint is not a supported ProPresenter API")
    with opener.open(url + "/v1/libraries", timeout=PROBE_TIMEOUT) as response:
        libraries = json.loads(response.read(1048577))
    if not isinstance(libraries, list):
        raise ValueError("ProPresenter did not return an accessible library list")
    return {"url": url, "version": version["host_description"], "libraries": len(libraries)}


def require_network(api_url: str | None = None) -> dict:
    url = resolve_api_url(api_url)
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--probe-url", url],
            capture_output=True, text=True, timeout=PROBE_TIMEOUT, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise NetworkAccessError(f"ProPresenter API did not respond within {PROBE_TIMEOUT} seconds. " + HELP) from exc
    except OSError as exc:
        raise NetworkAccessError(f"Could not start the ProPresenter network check: {exc}") from exc
    if result.returncode:
        detail = result.stderr.strip()
        if any(token in detail.lower() for token in ("10013", "permission denied", "forbidden by its access permissions")):
            raise NetworkAccessError("Local API access was denied by the OS or sandbox; this does not prove Network is off. "
                                     "Resolve local network permissions, then rerun. Do not fall back to computer use.")
        raise NetworkAccessError(f"ProPresenter API is unavailable at {url}: {detail}. " + HELP)
    return json.loads(result.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", help="API base URL; otherwise use PROPRESENTER_API_URL or Windows preferences")
    parser.add_argument("--probe-url", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        print(json.dumps(_probe(args.probe_url) if args.probe_url else require_network(args.api_url)))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

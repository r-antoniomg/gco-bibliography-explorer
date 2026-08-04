#!/usr/bin/env python3
"""
Update Zotero cache files for the GCO bibliography explorer.

This script fetches raw Zotero Web API JSON data and saves it into:

  assets/data/zotero-items.json
  assets/data/zotero-collections.json
  assets/data/zotero-cache-metadata.json

Run from the repository root:

  python scripts/update-zotero-cache.py

The first version intentionally stores raw Zotero API records rather than a
normalized local schema. Normalization and display decisions remain in the
Jekyll/JavaScript layer so that future sites can make their own metadata
choices without losing access to Zotero's original fields.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

GROUP_ID = "6606998"
API_BASE = "https://api.zotero.org"
API_VERSION = "3"
LIMIT = 100
REQUEST_DELAY_SECONDS = 0.15

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "assets" / "data"

ITEMS_OUTPUT = OUTPUT_DIR / "zotero-items.json"
COLLECTIONS_OUTPUT = OUTPUT_DIR / "zotero-collections.json"
METADATA_OUTPUT = OUTPUT_DIR / "zotero-cache-metadata.json"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def fetch_json(path: str, params: dict[str, str | int] | None = None):
    """Fetch JSON from the Zotero API."""
    params = params or {}
    query = urlencode(params)
    url = f"{API_BASE}{path}"

    if query:
        url = f"{url}?{query}"

    request = Request(
        url,
        headers={
            "User-Agent": "gco-bibliography-explorer-cache-script/0.1",
            "Zotero-API-Version": API_VERSION,
        },
    )

    try:
        with urlopen(request, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset)
            return json.loads(body)
    except HTTPError as error:
        raise RuntimeError(f"HTTP error while fetching {url}: {error.code} {error.reason}") from error
    except URLError as error:
        raise RuntimeError(f"Network error while fetching {url}: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON returned from {url}: {error}") from error


def fetch_all_pages(path: str, extra_params: dict[str, str | int] | None = None) -> list[dict]:
    """Fetch all paginated Zotero API results for an endpoint."""
    extra_params = extra_params or {}
    start = 0
    all_records: list[dict] = []

    while True:
        params = {
            "format": "json",
            "limit": LIMIT,
            "start": start,
        }
        params.update(extra_params)

        batch = fetch_json(path, params)

        if not isinstance(batch, list):
            raise RuntimeError(f"Expected list response from {path}, got {type(batch).__name__}")

        all_records.extend(batch)
        print(f"Fetched {len(batch):>3} records from {path} starting at {start}")

        if len(batch) < LIMIT:
            break

        start += LIMIT
        time.sleep(REQUEST_DELAY_SECONDS)

    return all_records


def write_json(path: Path, data) -> None:
    """Write JSON with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# -----------------------------------------------------------------------------
# Main cache update
# -----------------------------------------------------------------------------

def main() -> int:
    print("Updating Zotero cache files...")
    print(f"Repository root: {REPO_ROOT}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Zotero group ID: {GROUP_ID}")

    items = fetch_all_pages(f"/groups/{GROUP_ID}/items/top")
    collections = fetch_all_pages(f"/groups/{GROUP_ID}/collections")

    generated_at_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    metadata = {
        "generated_at_utc": generated_at_utc,
        "source": f"{API_BASE}/groups/{GROUP_ID}",
        "group_id": GROUP_ID,
        "api_version": API_VERSION,
        "items_file": str(ITEMS_OUTPUT.relative_to(REPO_ROOT)).replace("\\", "/"),
        "collections_file": str(COLLECTIONS_OUTPUT.relative_to(REPO_ROOT)).replace("\\", "/"),
        "item_count": len(items),
        "collection_count": len(collections),
        "cache_type": "raw_zotero_api_json",
        "notes": [
            "This cache stores raw Zotero API response records.",
            "Display normalization is handled by the site renderer and page scripts.",
            "Regenerate this cache after updating the Zotero library if the public site should reflect new data.",
        ],
    }

    write_json(ITEMS_OUTPUT, items)
    write_json(COLLECTIONS_OUTPUT, collections)
    write_json(METADATA_OUTPUT, metadata)

    print("\nCache update complete.")
    print(f"Items:       {len(items)} -> {ITEMS_OUTPUT}")
    print(f"Collections: {len(collections)} -> {COLLECTIONS_OUTPUT}")
    print(f"Metadata:              -> {METADATA_OUTPUT}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

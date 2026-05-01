"""Upstream source version fetcher for xenbase-ingest.

Two logical sources: infores:xenbase (the GenePageReports downloads from
download.xenbase.org) and the manually-uploaded XPO/SPO mapping file
hosted in monarch-ingest's GCS bucket. Versions from HTTP Last-Modified.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kozahub_metadata_schema import (
    now_iso,
    urls_from_download_yaml,
    version_from_http_last_modified,
)


INGEST_DIR = Path(__file__).resolve().parents[1]
DOWNLOAD_YAML = INGEST_DIR / "download.yaml"


def get_source_versions() -> list[dict[str, Any]]:
    xb_urls = urls_from_download_yaml(DOWNLOAD_YAML, contains=["download.xenbase.org"])
    xpo_urls = urls_from_download_yaml(DOWNLOAD_YAML, contains=["monarch-ingest"])
    now = now_iso()

    sources: list[dict[str, Any]] = []

    if xb_urls:
        ver, method = version_from_http_last_modified(xb_urls[0])
        sources.append({
            "id": "infores:xenbase",
            "name": "Xenbase",
            "urls": xb_urls,
            "version": ver,
            "version_method": method,
            "retrieved_at": now,
        })

    if xpo_urls:
        ver, method = version_from_http_last_modified(xpo_urls[0])
        sources.append({
            "id": "infores:monarchinitiative-xpo-spo",
            "name": "Xenopus XPO/SPO mapping (Monarch-curated)",
            "urls": xpo_urls,
            "version": ver,
            "version_method": method,
            "retrieved_at": now,
        })

    return sources

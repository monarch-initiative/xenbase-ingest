#!/usr/bin/env python
"""Download data files specified in download.yaml."""

import urllib.request
from pathlib import Path

import yaml


def download_files(config_path: str = "download.yaml") -> None:
    """Download all files specified in the config."""
    with open(config_path) as f:
        config = yaml.safe_load(f)

    for item in config.get("downloads", []):
        url = item["url"]
        local_name = item["local_name"]
        local_path = Path(local_name)

        # Create directory if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Downloading {url} -> {local_name}")
        urllib.request.urlretrieve(url, local_path)
        print(f"  Done: {local_path.stat().st_size} bytes")


if __name__ == "__main__":
    download_files()

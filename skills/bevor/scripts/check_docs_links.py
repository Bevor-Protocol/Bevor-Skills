#!/usr/bin/env python3
"""Check the public Bevor documentation links indexed by this skill."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def check(url: str, timeout: float) -> tuple[str, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "bevor-skill-link-check/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status >= 400:
                return url, f"HTTP {response.status}"
    except (urllib.error.URLError, TimeoutError) as exc:
        return url, str(exc)
    return url, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    docs_map = Path(__file__).resolve().parents[1] / "references" / "docs-map.md"
    urls = sorted(set(re.findall(r"https://docs\.bevor\.io[^)`\s]+", docs_map.read_text())))

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda url: check(url, args.timeout), urls))

    failures = [(url, error) for url, error in results if error]
    if failures:
        for url, error in failures:
            print(f"FAILED {url}: {error}", file=sys.stderr)
        return 1

    print(f"Checked {len(urls)} public Bevor documentation links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the v2 SWE GTM video timeline manifest.

This catches structural issues before the Premiere Compositor agent starts
issuing MCP tool calls.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger("swe_gtm_video.manifest_validate")

REQUIRED_TOP_LEVEL = ["project", "version", "spec", "premiere", "tracks", "timeline_items", "quality_gates"]
REQUIRED_SPEC = ["sequence_name", "width", "height", "fps", "audio_sample_rate_hz", "export_targets"]
REQUIRED_TIMELINE_ITEM = ["id", "type", "track", "start", "end"]


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in manifest:
            issues.append(f"Manifest missing top-level key: {key}")

    spec = manifest.get("spec", {})
    for key in REQUIRED_SPEC:
        if key not in spec:
            issues.append(f"Manifest spec missing key: {key}")

    if str(manifest.get("version", "")).split(".")[0] != "2":
        issues.append("Manifest version should be 2.x for Premiere MCP compositing")

    tracks = manifest.get("tracks", {})
    known_tracks = {track.get("id") for track in tracks.get("video", []) + tracks.get("audio", [])}
    if not known_tracks:
        issues.append("Manifest has no declared video/audio tracks")

    seen_ids: set[str] = set()
    for index, item in enumerate(manifest.get("timeline_items", []), start=1):
        for key in REQUIRED_TIMELINE_ITEM:
            if not item.get(key):
                issues.append(f"timeline_items[{index}] missing {key}")
        item_id = item.get("id")
        if item_id in seen_ids:
            issues.append(f"Duplicate timeline item id: {item_id}")
        if item_id:
            seen_ids.add(item_id)
        track = item.get("track")
        if track and track not in known_tracks:
            issues.append(f"timeline item {item_id or index} uses undeclared track: {track}")
        if item.get("type") in {"video", "audio", "graphic", "generated_video"} and not item.get("path"):
            issues.append(f"timeline item {item_id or index} of type {item.get('type')} should include path")

    captions = manifest.get("captions", {})
    if captions and not captions.get("path"):
        issues.append("captions block exists but missing path")

    audio_mastering = manifest.get("audio_mastering", {})
    if audio_mastering and not audio_mastering.get("loudness_target"):
        issues.append("audio_mastering block exists but missing loudness_target")

    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate timeline_manifest.json schema and references.")
    parser.add_argument("manifest", help="Path to timeline_manifest.json")
    parser.add_argument("--verbose", action="store_true", help="Print more detailed logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="[%(levelname)s] %(message)s")
    path = Path(args.manifest)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    issues = validate_manifest(manifest)
    if issues:
        LOGGER.warning("Manifest validation found %d issue(s)", len(issues))
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)
    LOGGER.info("Manifest validation passed: %s", path)


if __name__ == "__main__":
    main()

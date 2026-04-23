#!/usr/bin/env python3
"""Validate a SWE GTM video project for missing production files and obvious gaps."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path


LOGGER = logging.getLogger("swe_gtm_video.validate")


REQUIRED_FILES = [
    "01_strategy/creative_brief.md",
    "01_strategy/personas.md",
    "01_strategy/feature_truth_map.md",
    "02_composition/MASTER_PLAN.md",
    "02_composition/timestamp_plan.csv",
    "02_composition/shot_list.csv",
    "03_script/voiceover_script.md",
    "04_design/motion_visual_design.md",
    "05_audio/music_sound_plan.md",
    "05_audio/audio_mastering_plan.md",
    "06_capture/capture_plan.md",
    "07_generated_assets/veo_prompts.md",
    "08_edit/asset_registry.csv",
    "08_edit/timeline_manifest.json",
    "08_edit/premiere_mcp_execution_plan.md",
    "08_edit/premiere_mcp_operations.json",
    "08_edit/export_targets.json",
    "08_edit/compositor_review.md",
    "10_review/qa_report.md",
]

REQUIRED_TIMESTAMP_COLUMNS = [
    "start_time",
    "end_time",
    "scene",
    "intent",
    "visual",
    "action",
    "voiceover",
    "on_screen_copy",
    "music",
    "sfx",
    "source_asset",
    "method",
    "track",
    "transition",
    "motion_notes",
    "owner",
    "status",
    "risk",
]


def check_required_files(project_dir: Path) -> list[str]:
    """Return missing required file paths."""
    missing: list[str] = []
    for rel_path in REQUIRED_FILES:
        path = project_dir / rel_path
        if not path.exists():
            missing.append(rel_path)
            LOGGER.warning("Missing required file: %s", rel_path)
        else:
            LOGGER.info("Found required file: %s", rel_path)
    return missing


def check_timestamp_plan(project_dir: Path) -> list[str]:
    """Validate the timestamp CSV schema and flag incomplete high-impact fields."""
    issues: list[str] = []
    path = project_dir / "02_composition" / "timestamp_plan.csv"
    if not path.exists():
        return ["timestamp_plan.csv is missing"]

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        for column in REQUIRED_TIMESTAMP_COLUMNS:
            if column not in headers:
                issues.append(f"timestamp_plan.csv missing column: {column}")
                LOGGER.warning("timestamp_plan.csv missing column: %s", column)

        for row_number, row in enumerate(reader, start=2):
            scene = row.get("scene", f"row {row_number}")
            for column in ["start_time", "end_time", "scene", "intent", "method", "owner", "status"]:
                if not (row.get(column) or "").strip():
                    issue = f"timestamp_plan.csv row {row_number} ({scene}) missing {column}"
                    issues.append(issue)
                    LOGGER.warning(issue)

    if not issues:
        LOGGER.info("timestamp_plan.csv schema looks good")
    return issues


def check_manifest(project_dir: Path) -> list[str]:
    """Check that the timeline manifest is a Premiere MCP v2 manifest."""
    issues: list[str] = []
    path = project_dir / "08_edit" / "timeline_manifest.json"
    if not path.exists():
        return ["timeline_manifest.json is missing"]
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"timeline_manifest.json is invalid JSON: {exc}"]

    if str(manifest.get("version", "")).split(".")[0] != "2":
        issues.append("timeline_manifest.json should use version 2.x for Premiere MCP compositing")
    if "timeline_items" not in manifest:
        issues.append("timeline_manifest.json missing timeline_items")
    if "premiere" not in manifest:
        issues.append("timeline_manifest.json missing premiere MCP configuration block")
    if "audio_mastering" not in manifest:
        issues.append("timeline_manifest.json missing audio_mastering block")
    return issues


def check_brand_safety(project_dir: Path) -> list[str]:
    """Flag missing brand asset inventory signals."""
    issues: list[str] = []
    asset_registry = project_dir / "08_edit" / "asset_registry.csv"
    brand_dir = project_dir / "00_inputs" / "brand-assets"

    if brand_dir.exists() and not any(brand_dir.iterdir()):
        LOGGER.warning("brand-assets folder is empty; confirm whether brand assets are required")

    if not asset_registry.exists():
        issues.append("asset_registry.csv is missing")
        LOGGER.warning("asset_registry.csv is missing")

    return issues


def validate(project_dir: Path) -> int:
    LOGGER.info("Validating project: %s", project_dir)
    if not project_dir.exists():
        LOGGER.error("Project directory does not exist: %s", project_dir)
        return 2

    issues: list[str] = []
    issues.extend(check_required_files(project_dir))
    issues.extend(check_timestamp_plan(project_dir))
    issues.extend(check_manifest(project_dir))
    issues.extend(check_brand_safety(project_dir))

    if issues:
        LOGGER.warning("Validation finished with %d issue(s)", len(issues))
        for issue in issues:
            print(f"- {issue}")
        return 1

    LOGGER.info("Validation passed. The production project has the required Premiere MCP planning files.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a SWE GTM video project folder.")
    parser.add_argument("project_dir", help="Path to gtm-video/<project-slug>")
    parser.add_argument("--verbose", action="store_true", help="Print more detailed logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    raise SystemExit(validate(Path(args.project_dir)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a manifest-driven multi-track timeline from timestamp_plan.csv and asset_registry.csv.

This script creates a structured plan for the Premiere Compositor agent. It does
not render video. The resulting timeline_manifest.json should be refined by the
Video Editor and Premiere Compositor agents before final assembly in Premiere.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import logging
from pathlib import Path
from typing import Any


LOGGER = logging.getLogger("swe_gtm_video.timeline")


VIDEO_TRACKS = [
    {"id": "V1", "name": "Primary software capture / product proof", "locked": False},
    {"id": "V2", "name": "Detail captures / picture-in-picture / B-roll", "locked": False},
    {"id": "V3", "name": "Generated plates / transitions / cinematic context", "locked": False},
    {"id": "V4", "name": "UI focus masks / magnification / cursor treatment", "locked": False},
    {"id": "V5", "name": "Text overlays / callouts / lower thirds", "locked": False},
    {"id": "V6", "name": "Locked brand marks / logo / intro-outro overlays", "locked": True},
    {"id": "V7", "name": "Captions / subtitles / legal", "locked": False},
]

AUDIO_TRACKS = [
    {"id": "A1", "name": "Voiceover", "role": "dialogue", "target_level": "primary"},
    {"id": "A2", "name": "Music", "role": "music", "duck_under": "A1"},
    {"id": "A3", "name": "SFX / UI sounds", "role": "effects"},
    {"id": "A4", "name": "Ambience / risers / room tone", "role": "ambience"},
    {"id": "A5", "name": "Reference audio muted", "role": "reference", "muted": True},
]

BINS = [
    {"name": "01_Captures", "description": "Real product proof footage and screenshots"},
    {"name": "02_Generated", "description": "Approved generated plates and transitional assets"},
    {"name": "03_Audio_VO", "description": "Voiceover"},
    {"name": "04_Audio_Music", "description": "Music beds and stems"},
    {"name": "05_Audio_SFX", "description": "Sound effects and UI sounds"},
    {"name": "06_Graphics", "description": "Overlays, titles, lower thirds"},
    {"name": "07_Brand_Locked", "description": "Approved logos, intro/outro, brand marks"},
    {"name": "08_MOGRT", "description": "Approved motion graphics templates"},
    {"name": "09_Exports", "description": "Rendered masters and cutdowns"},
]


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV into dictionaries, logging useful progress for agents."""
    if not path.exists():
        LOGGER.warning("CSV not found: %s", path)
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    LOGGER.info("Read %d row(s) from %s", len(rows), path)
    return rows


def normalize_timecode(value: str, default: str = "00:00:00.000") -> str:
    """Normalize common mm:ss or hh:mm:ss inputs into hh:mm:ss.mmm strings."""
    raw = (value or "").strip()
    if not raw:
        return default
    if raw.count(":") == 1:
        raw = f"00:{raw}"
    if "." not in raw:
        raw = f"{raw}.000"
    return raw


def asset_lookup(asset_rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Return assets by id and by scene."""
    by_id: dict[str, dict[str, str]] = {}
    by_scene: dict[str, list[dict[str, str]]] = {}
    for asset in asset_rows:
        asset_id = (asset.get("asset_id") or "").strip()
        if asset_id:
            by_id[asset_id] = asset
        scene = (asset.get("scene") or "").strip()
        if scene:
            by_scene.setdefault(scene, []).append(asset)
    return by_id, by_scene


def create_scene_item(row: dict[str, str], idx: int, assets_for_scene: list[dict[str, str]]) -> dict[str, Any]:
    """Create a scene record from the timestamp plan."""
    scene_name = row.get("scene") or f"Scene {idx}"
    scene_id = f"SC{idx:03d}"
    return {
        "scene_id": scene_id,
        "name": scene_name,
        "start": normalize_timecode(row.get("start_time", "")),
        "end": normalize_timecode(row.get("end_time", ""), default="00:00:05.000"),
        "intent": row.get("intent", ""),
        "visual": row.get("visual", ""),
        "action": row.get("action", ""),
        "voiceover": row.get("voiceover", ""),
        "on_screen_copy": row.get("on_screen_copy", ""),
        "music": row.get("music", ""),
        "sfx": row.get("sfx", ""),
        "method": row.get("method", ""),
        "owner": row.get("owner", ""),
        "status": row.get("status", ""),
        "risk": row.get("risk", ""),
        "assets": [asset.get("asset_id", "") for asset in assets_for_scene if asset.get("asset_id")],
    }


def create_timeline_items(timestamp_rows: list[dict[str, str]], assets_by_scene: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    """Create track-aware timeline items from scene rows and registered assets."""
    items: list[dict[str, Any]] = []
    for idx, row in enumerate(timestamp_rows, start=1):
        scene_name = row.get("scene") or f"Scene {idx}"
        scene_id = f"SC{idx:03d}"
        start = normalize_timecode(row.get("start_time", ""))
        end = normalize_timecode(row.get("end_time", ""), default="00:00:05.000")
        transition = (row.get("transition") or "").strip()
        motion_notes = (row.get("motion_notes") or "").strip()
        registered_assets = assets_by_scene.get(scene_name, [])

        for asset_number, asset in enumerate(registered_assets, start=1):
            asset_type = (asset.get("type") or "video").strip().lower()
            track = (asset.get("track") or row.get("track") or ("A1" if asset_type == "audio" else "V1")).strip()
            item: dict[str, Any] = {
                "id": f"{scene_id}_{track}_{asset.get('asset_id') or asset_number}",
                "scene_id": scene_id,
                "type": asset_type,
                "role": asset.get("role") or "supporting_asset",
                "track": track,
                "asset_id": asset.get("asset_id", ""),
                "path": asset.get("path", ""),
                "start": start,
                "end": end,
                "source_in": "00:00:00.000",
                "source_out": asset.get("duration") or "match_timeline_duration",
                "notes": asset.get("notes") or row.get("intent", ""),
            }
            if track.startswith("V"):
                item.update({
                    "fit": "contain",
                    "opacity": 100,
                    "motion": {
                        "notes": motion_notes,
                        "scale": [{"time": start, "value": 100}],
                        "position": [{"time": start, "value": [960, 540]}],
                        "easing": "easeInOut",
                    },
                    "transition_in": None,
                    "transition_out": {"type": transition, "duration": "00:00:00.333"} if transition else None,
                })
            else:
                item.update({
                    "volume_db": 0,
                    "audio_role": asset.get("role") or "audio",
                })
            items.append(item)

        overlay_text = (row.get("on_screen_copy") or "").strip()
        if overlay_text:
            items.append({
                "id": f"{scene_id}_V5_OVERLAY",
                "scene_id": scene_id,
                "type": "text_overlay",
                "role": "on_screen_copy",
                "track": "V5",
                "start": start,
                "end": end,
                "text": overlay_text,
                "style_ref": "04_design/overlay_spec.md",
                "motion": {"notes": motion_notes, "opacity": [{"time": start, "value": 100}]},
                "safe_area": "title_safe",
            })
    return items


def build_manifest(project_dir: Path, sequence_name: str | None = None) -> dict[str, Any]:
    """Build a v2 multi-track manifest for agent-driven Premiere compositing."""
    timestamp_rows = read_csv(project_dir / "02_composition" / "timestamp_plan.csv")
    asset_rows = read_csv(project_dir / "08_edit" / "asset_registry.csv")
    _assets_by_id, assets_by_scene = asset_lookup(asset_rows)

    scenes = [
        create_scene_item(row=row, idx=idx, assets_for_scene=assets_by_scene.get(row.get("scene") or f"Scene {idx}", []))
        for idx, row in enumerate(timestamp_rows, start=1)
    ]
    timeline_items = create_timeline_items(timestamp_rows, assets_by_scene)

    slug = project_dir.name
    sequence = sequence_name or f"{slug}_master"
    manifest: dict[str, Any] = {
        "project": slug,
        "version": "2.0",
        "created_at": _dt.date.today().isoformat(),
        "spec": {
            "duration_seconds": 60,
            "aspect_ratio": "16:9",
            "resolution": "1920x1080",
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "audio_sample_rate_hz": 48000,
            "sequence_name": sequence,
            "premiere_project_path": str(project_dir / "09_exports" / "premiere-project" / f"{slug}.prproj"),
            "safe_areas": {"title_safe_percent": 90, "action_safe_percent": 95},
            "export_targets": ["primary_full_length", "silent_captioned", "social_cutdown"],
        },
        "premiere": {
            "mcp_server_name": "premiere_pro",
            "read_instructions_resource": "premiere://config/get_instructions",
            "use_tool_introspection": True,
            "preferred_workflows": [
                "build_brand_spot_from_mogrt_and_assets",
                "assemble_product_spot",
                "atomic_timeline_operations",
            ],
            "bridge_temp_directory": "/tmp/premiere-mcp-bridge",
            "requires_human_review_before_export": True,
        },
        "bins": BINS,
        "tracks": {"video": VIDEO_TRACKS, "audio": AUDIO_TRACKS},
        "scenes": scenes,
        "timeline_items": timeline_items,
        "transitions": [],
        "effects": [],
        "captions": {
            "path": str(project_dir / "08_edit" / "captions.srt"),
            "track": "V7",
            "burn_in": False,
            "style_ref": "04_design/overlay_spec.md#captions",
            "required_for_silent_export": True,
        },
        "audio_mastering": {
            "plan_path": str(project_dir / "05_audio" / "audio_mastering_plan.md"),
            "dialogue_track": "A1",
            "music_track": "A2",
            "sfx_track": "A3",
            "ducking": {"music_under_vo_db": -10, "attack_ms": 150, "release_ms": 350},
            "loudness_target": {"integrated_lufs": -14, "true_peak_db_tp": -1.0},
            "must_check": ["no_clipping", "vo_intelligible", "music_not_masking_vo", "sfx_not_distracting"],
        },
        "markers": [
            {"time": scene["start"], "name": scene["name"], "color": "blue", "notes": scene.get("intent", "")}
            for scene in scenes
        ],
        "quality_gates": [
            "manifest_times_do_not_overlap_unintentionally",
            "product_claims_match_feature_truth_map",
            "all_brand_layers_use_source_assets_only",
            "ui_text_readable_at_export_resolution",
            "captions_present_for_silent_export",
            "audio_mastering_target_checked",
            "export_matches_platform_specs",
        ],
    }
    LOGGER.info("Built manifest with %d scene(s) and %d timeline item(s)", len(scenes), len(timeline_items))
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build timeline_manifest.json from project CSV files.")
    parser.add_argument("project_dir", help="Path to gtm-video/<project-slug>")
    parser.add_argument("--output", help="Output JSON path. Defaults to <project>/08_edit/timeline_manifest.json")
    parser.add_argument("--sequence-name", help="Premiere sequence name. Defaults to <slug>_master.")
    parser.add_argument("--verbose", action="store_true", help="Print more detailed logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    project_dir = Path(args.project_dir)
    output = Path(args.output) if args.output else project_dir / "08_edit" / "timeline_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(project_dir, sequence_name=args.sequence_name)
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    LOGGER.info("Wrote timeline manifest: %s", output)


if __name__ == "__main__":
    main()

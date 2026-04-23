#!/usr/bin/env python3
"""Generate a Premiere MCP execution plan from timeline_manifest.json.

This translator creates two artifacts for the Premiere Compositor agent:

- 08_edit/premiere_mcp_execution_plan.md
- 08_edit/premiere_mcp_operations.json

It does not call MCP tools. The agent must use MCP introspection to map these
intent-level operations to the exact tool schemas available in the local
Premiere Pro MCP installation.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger("swe_gtm_video.premiere_plan")


def load_manifest(project_dir: Path) -> dict[str, Any]:
    path = project_dir / "08_edit" / "timeline_manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing manifest: {path}")
    LOGGER.info("Reading manifest: %s", path)
    return json.loads(path.read_text(encoding="utf-8"))


def group_assets(manifest: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for item in manifest.get("timeline_items", []):
        path = item.get("path")
        if not path:
            continue
        role = item.get("role") or item.get("type") or "asset"
        groups.setdefault(role, []).append(item)
    return groups


def build_operations(manifest: dict[str, Any]) -> dict[str, Any]:
    spec = manifest.get("spec", {})
    timeline_items = manifest.get("timeline_items", [])
    transitions = manifest.get("transitions", [])
    effects = manifest.get("effects", [])
    export_targets = spec.get("export_targets", [])

    operations: list[dict[str, Any]] = [
        {
            "id": "OP001_READ_PREMIERE_INSTRUCTIONS",
            "phase": "readiness",
            "intent": "Read Premiere MCP operating guidance before making edits.",
            "preferred_tool_or_resource": manifest.get("premiere", {}).get("read_instructions_resource", "premiere://config/get_instructions"),
            "requires_introspection": False,
            "status": "pending",
        },
        {
            "id": "OP002_INTROSPECT_TOOLS",
            "phase": "readiness",
            "intent": "List available Premiere MCP tools and exact schemas; do not guess parameters.",
            "preferred_tool_or_resource": "mcp_tool_introspection",
            "requires_introspection": True,
            "status": "pending",
        },
        {
            "id": "OP003_CREATE_OR_OPEN_PROJECT",
            "phase": "setup",
            "intent": "Create or open the Premiere project for this production.",
            "inputs": {"premiere_project_path": spec.get("premiere_project_path")},
            "preferred_strategy": "project_operation_tool_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP004_CREATE_SEQUENCE",
            "phase": "setup",
            "intent": "Create or select the master sequence with the requested resolution, fps, and audio sample rate.",
            "inputs": {
                "sequence_name": spec.get("sequence_name"),
                "width": spec.get("width"),
                "height": spec.get("height"),
                "fps": spec.get("fps"),
                "audio_sample_rate_hz": spec.get("audio_sample_rate_hz"),
            },
            "preferred_strategy": "create_sequence_or_select_sequence_tool_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP005_CREATE_BINS",
            "phase": "ingest",
            "intent": "Create production bins so the project remains editor-readable.",
            "inputs": {"bins": manifest.get("bins", [])},
            "preferred_strategy": "create_bin_tool_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP006_IMPORT_MEDIA",
            "phase": "ingest",
            "intent": "Import every approved asset referenced by the timeline manifest.",
            "inputs": {"items": [item for item in timeline_items if item.get("path")]},
            "preferred_strategy": "import_media_tool_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP007_ASSEMBLE_TIMELINE",
            "phase": "timeline",
            "intent": "Place, trim, layer, and order every clip/overlay/audio item by exact timecode and track.",
            "inputs": {"timeline_items": timeline_items},
            "preferred_strategy": "use_high_level_clipPlan_if_available_else_atomic_placement_tools",
            "status": "pending",
        },
        {
            "id": "OP008_APPLY_TRANSITIONS",
            "phase": "polish",
            "intent": "Apply transitions from the manifest with durations and emotional intent preserved.",
            "inputs": {"transitions": transitions},
            "preferred_strategy": "transition_tool_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP009_APPLY_MOTION_AND_EFFECTS",
            "phase": "polish",
            "intent": "Apply motion keyframes, scale/position/opacity changes, color/effects, and UI focus treatments.",
            "inputs": {"items_with_motion": [item for item in timeline_items if item.get("motion")], "effects": effects},
            "preferred_strategy": "keyframe_effect_tool_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP010_ADD_CAPTIONS_AND_GRAPHICS",
            "phase": "graphics",
            "intent": "Add captions, approved MOGRTs, text overlays, and locked brand layers.",
            "inputs": {"captions": manifest.get("captions", {}), "brand_items": [item for item in timeline_items if str(item.get("track", "")).upper() == "V6"]},
            "preferred_strategy": "caption_mogrt_graphics_tools_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP011_AUDIO_MIX_AND_MASTER",
            "phase": "audio",
            "intent": "Mix VO/music/SFX, duck music, apply available cleanup/mastering effects, and check loudness/peaks.",
            "inputs": {"audio_mastering": manifest.get("audio_mastering", {})},
            "preferred_strategy": "premiere_audio_tools_if_available_else_human_finishing_note",
            "status": "pending",
        },
        {
            "id": "OP012_MARKERS_AND_REVIEW",
            "phase": "review",
            "intent": "Create timeline markers and inspect sequence against manifest before export.",
            "inputs": {"markers": manifest.get("markers", []), "quality_gates": manifest.get("quality_gates", [])},
            "preferred_strategy": "marker_inspection_tools_from_introspection",
            "status": "pending",
        },
        {
            "id": "OP013_EXPORT_TARGETS",
            "phase": "export",
            "intent": "Export all requested masters/cutdowns using Premiere/Media Encoder tools if available.",
            "inputs": {"export_targets": export_targets, "export_targets_file": "08_edit/export_targets.json"},
            "preferred_strategy": "export_sequence_or_media_encoder_tool_from_introspection",
            "status": "pending",
        },
    ]

    return {
        "project": manifest.get("project"),
        "version": "2.0",
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "mcp_server": manifest.get("premiere", {}).get("mcp_server_name", "premiere_pro"),
        "strategy": "Agent-driven Premiere compositing. Use MCP introspection first; prefer high-level clipPlan when expressive enough; fall back to atomic timeline operations.",
        "operations": operations,
    }


def render_markdown(project_dir: Path, manifest: dict[str, Any], operations: dict[str, Any]) -> str:
    spec = manifest.get("spec", {})
    groups = group_assets(manifest)
    timeline_items = manifest.get("timeline_items", [])
    transitions = manifest.get("transitions", [])
    effects = manifest.get("effects", [])
    tracks = manifest.get("tracks", {})
    export_targets = spec.get("export_targets", [])

    def rows(items: list[dict[str, Any]], limit: int = 30) -> str:
        if not items:
            return "| TBD | TBD | TBD | TBD | TBD | Pending |\n"
        out = []
        for item in items[:limit]:
            out.append(
                f"| {item.get('id','')} | {item.get('start','')}–{item.get('end','')} | {item.get('track','')} | {item.get('path') or item.get('text','')} | {item.get('role','')} | Pending |"
            )
        if len(items) > limit:
            out.append(f"| … | … | … | {len(items) - limit} more item(s) | … | Pending |")
        return "\n".join(out) + "\n"

    return f"""# Premiere MCP Execution Plan — {manifest.get('project', project_dir.name)}

Generated: {_dt.datetime.now().isoformat(timespec='seconds')}
Manifest: `08_edit/timeline_manifest.json`
Operations JSON: `08_edit/premiere_mcp_operations.json`

## 1. Readiness

- [ ] Premiere Pro is open with a project loaded or ready to create
- [ ] Premiere MCP bridge panel is open and running
- [ ] MCP server `{operations.get('mcp_server', 'premiere_pro')}` is visible to Codex
- [ ] Read/attach `{manifest.get('premiere', {}).get('read_instructions_resource', 'premiere://config/get_instructions')}` when available
- [ ] Use MCP introspection to confirm exact tool schemas before calling tools

## 2. Sequence spec

| Field | Value |
|---|---|
| Project | {manifest.get('project', project_dir.name)} |
| Premiere project path | {spec.get('premiere_project_path', '')} |
| Sequence | {spec.get('sequence_name', '')} |
| Resolution | {spec.get('resolution', '')} |
| FPS | {spec.get('fps', '')} |
| Audio sample rate | {spec.get('audio_sample_rate_hz', '')} |
| Export targets | {', '.join(export_targets) if export_targets else 'TBD'} |

## 3. Track layout

### Video

| Track | Purpose | Locked? |
|---|---|---|
""" + "".join(
        f"| {track.get('id')} | {track.get('name')} | {track.get('locked', False)} |\n" for track in tracks.get('video', [])
    ) + """
### Audio

| Track | Purpose | Role |
|---|---|---|
""" + "".join(
        f"| {track.get('id')} | {track.get('name')} | {track.get('role', '')} |\n" for track in tracks.get('audio', [])
    ) + f"""
## 4. Asset groups

""" + "".join(
        f"- **{role}**: {len(items)} item(s)\n" for role, items in sorted(groups.items())
    ) + f"""
## 5. Timeline placement checklist

| Item | Time | Track | Asset/Text | Role | Status |
|---|---:|---|---|---|---|
{rows(timeline_items)}
## 6. Transitions

| Transition | Target | Type | Duration | Intent | Status |
|---|---|---|---:|---|---|
""" + ("".join(
        f"| {tr.get('id','')} | {tr.get('target_item_id','')} | {tr.get('type','')} | {tr.get('duration','')} | {tr.get('emotional_intent','')} | Pending |\n" for tr in transitions
    ) if transitions else "| TBD | TBD | TBD | TBD | TBD | Pending |\n") + f"""
## 7. Motion and effects

| Effect | Target | Type | Notes | Status |
|---|---|---|---|---|
""" + ("".join(
        f"| {fx.get('id','')} | {fx.get('target_item_id','')} | {fx.get('type','')} | {fx.get('notes','')} | Pending |\n" for fx in effects
    ) if effects else "| TBD | TBD | TBD | TBD | Pending |\n") + f"""
## 8. Audio mix and mastering

Mastering plan: `{manifest.get('audio_mastering', {}).get('plan_path', '05_audio/audio_mastering_plan.md')}`

- Dialogue track: {manifest.get('audio_mastering', {}).get('dialogue_track', 'A1')}
- Music track: {manifest.get('audio_mastering', {}).get('music_track', 'A2')}
- SFX track: {manifest.get('audio_mastering', {}).get('sfx_track', 'A3')}
- Target: {manifest.get('audio_mastering', {}).get('loudness_target', {})}

## 9. Operation plan

| ID | Phase | Intent | Strategy | Status |
|---|---|---|---|---|
""" + "".join(
        f"| {op.get('id')} | {op.get('phase')} | {op.get('intent')} | {op.get('preferred_strategy') or op.get('preferred_tool_or_resource')} | {op.get('status')} |\n" for op in operations.get('operations', [])
    ) + f"""
## 10. Review gates before export

""" + "".join(f"- [ ] {gate}\n" for gate in manifest.get('quality_gates', [])) + """
## 11. Compositor notes

Document any MCP limitation or manual finishing requirement in `08_edit/compositor_review.md` before exporting.
"""


def write_outputs(project_dir: Path, manifest: dict[str, Any], operations: dict[str, Any]) -> None:
    edit_dir = project_dir / "08_edit"
    edit_dir.mkdir(parents=True, exist_ok=True)
    operations_path = edit_dir / "premiere_mcp_operations.json"
    plan_path = edit_dir / "premiere_mcp_execution_plan.md"
    operations_path.write_text(json.dumps(operations, indent=2), encoding="utf-8")
    plan_path.write_text(render_markdown(project_dir, manifest, operations), encoding="utf-8")
    LOGGER.info("Wrote operations: %s", operations_path)
    LOGGER.info("Wrote execution plan: %s", plan_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Premiere MCP execution plan from timeline_manifest.json.")
    parser.add_argument("project_dir", help="Path to gtm-video/<project-slug>")
    parser.add_argument("--verbose", action="store_true", help="Print more detailed logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="[%(levelname)s] %(message)s")
    project_dir = Path(args.project_dir)
    manifest = load_manifest(project_dir)
    operations = build_operations(manifest)
    write_outputs(project_dir, manifest, operations)


if __name__ == "__main__":
    main()

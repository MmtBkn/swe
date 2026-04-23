#!/usr/bin/env python3
"""Scaffold a SWE GTM video production folder.

This helper intentionally does not generate creative content or render video.
It creates the folder structure and copies production templates so Codex and
specialist agents can fill them in consistently. Final assembly is driven by
Premiere Pro MCP, not by this script.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
import re
import shutil
from pathlib import Path


LOGGER = logging.getLogger("swe_gtm_video.init")


TEMPLATE_MAP = {
    "01_strategy/creative_brief.md": "creative_brief.template.md",
    "01_strategy/personas.md": "personas.template.md",
    "01_strategy/persona_empathy_map.md": "persona_empathy_map.template.md",
    "01_strategy/feature_truth_map.md": "feature_truth_map.template.md",
    "01_strategy/assumptions.md": "assumptions.template.md",
    "02_composition/MASTER_PLAN.md": "MASTER_PLAN.template.md",
    "02_composition/timestamp_plan.csv": "timestamp_plan.template.csv",
    "02_composition/shot_list.csv": "shot_list.template.csv",
    "02_composition/storyboard.md": "storyboard.template.md",
    "03_script/voiceover_script.md": "voiceover_script.template.md",
    "03_script/on_screen_copy.md": "on_screen_copy.template.md",
    "03_script/revision_log.md": "revision_log.template.md",
    "04_design/motion_visual_design.md": "motion_visual_design.template.md",
    "04_design/styleframes.md": "styleframes.template.md",
    "04_design/overlay_spec.md": "overlay_spec.template.md",
    "05_audio/voice_casting.md": "voice_casting.template.md",
    "05_audio/music_sound_plan.md": "music_sound_plan.template.md",
    "05_audio/sound_cue_sheet.csv": "sound_cue_sheet.template.csv",
    "05_audio/audio_mastering_plan.md": "audio_mastering_plan.template.md",
    "06_capture/capture_plan.md": "capture_plan.template.md",
    "06_capture/browser_capture_checklist.md": "browser_capture_checklist.template.md",
    "07_generated_assets/veo_prompts.md": "veo_prompts.template.md",
    "07_generated_assets/generated_asset_review.md": "generated_asset_review.template.md",
    "08_edit/timeline_manifest.json": "timeline_manifest.template.json",
    "08_edit/edit_decisions.md": "edit_decisions.template.md",
    "08_edit/premiere_mcp_execution_plan.md": "premiere_mcp_execution_plan.template.md",
    "08_edit/premiere_mcp_operations.json": "premiere_mcp_operations.template.json",
    "08_edit/sequence_markers.csv": "sequence_markers.template.csv",
    "08_edit/captions.srt": "captions.template.srt",
    "08_edit/export_targets.json": "export_targets.template.json",
    "08_edit/compositor_review.md": "compositor_review.template.md",
    "10_review/qa_report.md": "qa_report.template.md",
    "10_review/final_delivery_report.md": "final_delivery_report.template.md",
}


EXTRA_DIRS = [
    "00_inputs/brand-assets",
    "00_inputs/raw-product-context",
    "00_inputs/premiere-project-template",
    "00_inputs/mogrts",
    "05_audio/generated",
    "05_audio/generated/sfx",
    "05_audio/generated/ambience",
    "06_capture/captures",
    "07_generated_assets/assets",
    "09_exports/masters",
    "09_exports/cutdowns",
    "09_exports/social",
    "09_exports/review-links",
    "09_exports/premiere-project",
]


def slugify(value: str) -> str:
    """Convert a user-provided project name into a safe folder slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "swe-gtm-video"


def replace_placeholders(text: str, project_name: str, slug: str) -> str:
    """Apply lightweight placeholder substitution used by the templates."""
    return (
        text.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{PROJECT_SLUG}}", slug)
        .replace("{{date}}", _dt.date.today().isoformat())
    )


def copy_template(template_dir: Path, template_name: str, destination: Path, project_name: str, slug: str, force: bool) -> None:
    """Copy a template to the destination, preserving existing work unless forced."""
    source = template_dir / template_name
    if not source.exists():
        raise FileNotFoundError(f"Template not found: {source}")

    if destination.exists() and not force:
        LOGGER.info("Keeping existing file: %s", destination)
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    content = source.read_text(encoding="utf-8")
    destination.write_text(replace_placeholders(content, project_name, slug), encoding="utf-8")
    LOGGER.info("Created template file: %s", destination)


def scaffold_project(slug: str, project_name: str, output_root: Path, force: bool) -> Path:
    """Create a project folder and populate it with templates."""
    skill_root = Path(__file__).resolve().parents[1]
    template_dir = skill_root / "assets" / "templates"
    project_dir = output_root / slug

    LOGGER.info("Scaffolding SWE GTM video project")
    LOGGER.info("Project name: %s", project_name)
    LOGGER.info("Project slug: %s", slug)
    LOGGER.info("Output directory: %s", project_dir)

    project_dir.mkdir(parents=True, exist_ok=True)

    for rel_dir in EXTRA_DIRS:
        directory = project_dir / rel_dir
        directory.mkdir(parents=True, exist_ok=True)
        LOGGER.info("Ensured directory exists: %s", directory)

    readme = project_dir / "00_inputs" / "README.md"
    if force or not readme.exists():
        readme.write_text(
            "# Inputs\n\n"
            "Place brand assets, product context, screenshots, PRDs, release notes, source material, "
            "Premiere project templates, and approved MOGRTs here.\n\n"
            "Never store secrets, real customer data, private production credentials, or confidential legal/client content "
            "in this folder.\n",
            encoding="utf-8",
        )
        LOGGER.info("Created input README: %s", readme)

    for destination_rel, template_name in TEMPLATE_MAP.items():
        copy_template(template_dir, template_name, project_dir / destination_rel, project_name, slug, force)

    asset_registry_template = template_dir / "asset_registry.template.csv"
    asset_registry = project_dir / "08_edit" / "asset_registry.csv"
    if force or not asset_registry.exists():
        shutil.copyfile(asset_registry_template, asset_registry)
        LOGGER.info("Created asset registry: %s", asset_registry)

    LOGGER.info("Project scaffold complete: %s", project_dir)
    return project_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a SWE GTM video production folder.")
    parser.add_argument("--slug", required=True, help="Project slug or name. Example: lito-agentic-demo")
    parser.add_argument("--project-name", help="Human-readable project name. Defaults to the slug.")
    parser.add_argument("--output-root", default="gtm-video", help="Root output directory. Defaults to ./gtm-video")
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files. Use carefully.")
    parser.add_argument("--verbose", action="store_true", help="Print more detailed logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    slug = slugify(args.slug)
    project_name = args.project_name or args.slug.strip()
    scaffold_project(slug=slug, project_name=project_name, output_root=Path(args.output_root), force=args.force)


if __name__ == "__main__":
    main()

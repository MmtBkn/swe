# Editing and Premiere MCP Guide

The final assembly path for this skill is agent-driven Premiere Pro compositing through the Premiere Pro MCP bridge.

## Editing principle

The manifest describes the cut, but the editing agent makes it land. Use the manifest to protect structure, timing, asset provenance, brand safety, and export specs. Use editorial judgment to protect feeling.

## Preferred assembly path

1. Write the master plan.
2. Capture and approve assets.
3. Build `08_edit/timeline_manifest.json` as a v2 multi-track manifest.
4. Generate `08_edit/premiere_mcp_execution_plan.md`.
5. Have `swe_gtm_premiere_compositor` read Premiere guidance, introspect MCP tools, and build the sequence.
6. Inspect the sequence after major operation batches.
7. Master audio.
8. Export final and variants.
9. QA against product truth, brand, accessibility, and platform specs.

## Use high-level tools when they fit

If Premiere MCP exposes a high-level product/brand spot tool and its schema supports the manifest's timing, track placement, transitions, motion, trims, effects, color adjustments, graphics, and audio plan, use it to reduce operational complexity.

## Use atomic operations when needed

If high-level workflows are not expressive enough, use atomic operations:

- create/open project
- create/select sequence
- create bins
- import media
- place clips on tracks
- trim source in/out
- set sequence start/end/work area
- add transitions
- apply effects and keyframes
- add captions and graphics/MOGRTs
- mix/master audio
- create markers
- export masters and variants

## What not to do

- Do not use FFmpeg concat as the primary stitcher.
- Do not flatten the video too early; keep layers editable in Premiere.
- Do not apply generative treatment to brand assets.
- Do not over-cut UI proof.
- Do not export before audio and captions are reviewed.

# Specialist agent spawn prompts

Use these prompts when Codex custom agents are installed.

## Persona strategist

Spawn `swe_gtm_persona_strategist` to review the product context and produce/critique `01_strategy/personas.md` and `01_strategy/persona_empathy_map.md`. Focus on deepest pain, strongest desire, adoption fear, misconception, proof needed, and language the persona would actually use.

## Scriptwriter

Spawn `swe_gtm_scriptwriter` to transform the feature into a felt story. Revise `03_script/voiceover_script.md` and `03_script/on_screen_copy.md`. Avoid feature-tour language and generic AI hype.

## Motion designer

Spawn `swe_gtm_motion_designer` to design `04_design/motion_visual_design.md`, `styleframes.md`, and `overlay_spec.md`. Include transition intent, UI focus moments, safe areas, and brand-safe motion.

## Sound designer

Spawn `swe_gtm_sound_designer` to design `05_audio/voice_casting.md`, `music_sound_plan.md`, `sound_cue_sheet.csv`, and `audio_mastering_plan.md`. Include VO, music arc, SFX, silence, ducking, and final mastering intent.

## Director / Producer

Spawn `swe_gtm_director_producer` to produce `06_capture/capture_plan.md`, `browser_capture_checklist.md`, `07_generated_assets/veo_prompts.md`, `generated_asset_review.md`, and `08_edit/asset_registry.csv`.

## Video Editor / Montage

Spawn `swe_gtm_video_editor` to create `08_edit/edit_decisions.md`, `captions.srt`, `sequence_markers.csv`, and a version 2.x `timeline_manifest.json` that expresses multi-track timing, transitions, overlays, motion, captions, and audio.

## Premiere Compositor / Finishing Editor

Spawn `swe_gtm_premiere_compositor` to read `timeline_manifest.json`, generate or revise `premiere_mcp_execution_plan.md` and `premiere_mcp_operations.json`, use Premiere MCP introspection, build the sequence, apply transitions/effects/keyframes/captions, execute or document audio mastering, export deliverables, and write `compositor_review.md`.

## Brand Guardian

Spawn `swe_gtm_brand_guardian` before asset generation and again before export. Confirm claims, UI truth, privacy, brand marks, generated assets, MOGRTs, Premiere layers, captions, and final export safety.

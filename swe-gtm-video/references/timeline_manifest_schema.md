# Timeline Manifest v2 Schema Guide

`08_edit/timeline_manifest.json` is the creative and technical contract between the Video Editor and the Premiere Compositor agent.

## Required top-level sections

- `project`: project name or slug
- `version`: `2.x`
- `spec`: sequence and export specs
- `premiere`: MCP server and operation preferences
- `bins`: intended Premiere bin organization
- `tracks`: video/audio track definitions
- `scenes`: narrative scene metadata
- `timeline_items`: exact media, graphics, captions, and audio placements
- `transitions`: transition intents and durations
- `effects`: effect instructions
- `captions`: caption path/style/export behavior
- `audio_mastering`: dialogue/music/SFX treatment and loudness/peak target
- `markers`: review/story markers
- `quality_gates`: checks before export

## Timeline item types

Common item types:

- `video`: real capture footage
- `generated_video`: approved generated plate or transition
- `graphic`: image/logo/brand asset
- `mogrt`: approved motion graphics template
- `text_overlay`: generated text layer or title
- `audio`: VO, music, SFX, ambience
- `caption`: subtitle/caption item
- `marker`: sequence marker

## Track defaults

V1 primary product proof, V2 detail/B-roll, V3 generated plates, V4 UI focus/masks, V5 overlays, V6 locked brand, V7 captions/legal. A1 VO, A2 music, A3 SFX, A4 ambience, A5 reference.

## Design rule

Each item should explain why it exists. If a layer does not support story, proof, clarity, or emotion, remove it.

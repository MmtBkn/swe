# Quality Gates

Complete these before final delivery.

## Strategy and story

- Persona feels specific and emotionally accurate.
- The opening creates pain, stakes, or transformation in the first 3–5 seconds.
- The video has a clear before/after transformation.
- CTA is specific and earned.

## Product truth

- Every claim maps to `feature_truth_map.md`.
- Real UI footage shows actual product behavior.
- Generated video does not invent UI, metrics, logos, customer behavior, or product states.

## Brand and legal

- Logos and brand assets come from source files only.
- Brand layers are locked/protected in Premiere where possible.
- No unauthorized customer logos, PII, secrets, private URLs, access tokens, confidential docs, or privileged matter/client content.
- Any legal/compliance/security claim has approval.

## Edit and Premiere sequence

- `timeline_manifest.json` is version 2.x and has timeline items, tracks, captions, and audio mastering blocks.
- Premiere sequence matches the manifest.
- UI is readable at export resolution.
- Transitions and motion support the story, not decoration.
- Captions are present and legible for silent/autoplay versions.

## Audio

- VO is intelligible.
- Music ducks under VO.
- SFX are restrained and purposeful.
- No clipping, harsh artifacts, or distracting generated-audio issues.
- Audio mastering target is checked or documented as a manual finishing task.

## Export

- Runtime, aspect ratio, resolution, fps, safe areas, and caption behavior match `export_targets.json`.
- Final delivery report includes export paths, known limitations, approvals, and next variants.

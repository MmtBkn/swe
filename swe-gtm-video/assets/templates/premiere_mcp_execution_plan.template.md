# Premiere MCP Execution Plan — {{PROJECT_NAME}}

Date: {{date}}
Sequence: `{{PROJECT_SLUG}}_master`
Manifest: `08_edit/timeline_manifest.json`
Operations JSON: `08_edit/premiere_mcp_operations.json`

## 1. MCP readiness

- [ ] Adobe Premiere Pro is open with a project loaded or ready to create
- [ ] Premiere MCP bridge panel is open and running
- [ ] MCP temp directory matches config
- [ ] Codex can see the `premiere_pro` MCP server
- [ ] Read/attach `premiere://config/get_instructions` when available
- [ ] Use MCP introspection to confirm available tools and schemas before calling tools

## 2. Project and sequence setup

- Project path:
- Sequence name:
- Resolution:
- FPS:
- Audio sample rate:
- Work area:

## 3. Bins

| Bin | Purpose | Status |
|---|---|---|
| 01_Captures | Real product proof footage | Pending |
| 02_Generated | Approved generated plates | Pending |
| 03_Audio_VO | Voiceover | Pending |
| 04_Audio_Music | Music | Pending |
| 05_Audio_SFX | SFX/UI sounds | Pending |
| 06_Graphics | Text overlays/callouts | Pending |
| 07_Brand_Locked | Approved logos and intro/outro | Pending |
| 08_MOGRT | Approved templates | Pending |

## 4. Asset import checklist

| Asset ID | Path | Bin | Approval | Brand locked? | Status |
|---|---|---|---|---|---|
| TBD | TBD | TBD | Pending | No | Pending |

## 5. Timeline assembly plan

| Operation | Time | Track | Asset/Item | Action | Tool strategy | Status |
|---|---:|---|---|---|---|---|
| 001 | 00:00:00.000 | V1 | TBD | Place primary capture | High-level clipPlan or atomic placement | Pending |

## 6. Transition and motion plan

| Item | Transition / Motion | Duration | Emotional intent | Status |
|---|---|---:|---|---|
| TBD | TBD | TBD | TBD | Pending |

## 7. Overlay, caption, and MOGRT plan

- Use approved MOGRTs or source graphics when available.
- Do not generate, recolor, or reinterpret brand marks.
- Keep captions readable and inside safe areas.

## 8. Audio mix and mastering plan

See `05_audio/audio_mastering_plan.md`.

- [ ] VO placed on A1
- [ ] Music placed on A2 and ducked under VO
- [ ] SFX placed on A3, restrained and meaningful
- [ ] Loudness/peak targets checked
- [ ] No clipping or masking

## 9. Export plan

See `08_edit/export_targets.json`.

| Export | Path | Format | Status |
|---|---|---|---|
| Primary master | `09_exports/masters/{{PROJECT_SLUG}}_master.mp4` | H.264 MP4 | Pending |
| Silent captioned | `09_exports/social/{{PROJECT_SLUG}}_silent_captioned.mp4` | H.264 MP4 | Pending |
| Cutdown | `09_exports/cutdowns/{{PROJECT_SLUG}}_cutdown.mp4` | H.264 MP4 | Pending |

## 10. Post-export review

- [ ] Runtime matches target
- [ ] UI readable
- [ ] Captions correct
- [ ] Audio intelligible and mastered
- [ ] Logos and brand marks intact
- [ ] Product claims verified
- [ ] Export targets created
- [ ] Known MCP limitations documented in `08_edit/compositor_review.md`

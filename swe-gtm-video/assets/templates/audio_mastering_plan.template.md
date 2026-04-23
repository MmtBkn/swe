# Audio Mastering Plan — {{PROJECT_NAME}}

Date: {{date}}

## Emotional intent

Describe what the viewer should feel through sound at each act: pressure, recognition, lift, confidence, resolve.

## Track layout

| Track | Role | Source | Notes |
|---|---|---|---|
| A1 | Voiceover | `05_audio/generated/main_voiceover.wav` | Anchor the mix around intelligibility |
| A2 | Music | `05_audio/generated/main_music.wav` | Duck under VO, bloom in non-VO moments |
| A3 | SFX / UI sounds | `05_audio/generated/sfx/` | Minimal, tactile, meaningful |
| A4 | Ambience / risers | `05_audio/generated/ambience/` | Use sparingly |

## Voiceover treatment

- Cleanup:
- EQ:
- Compression:
- De-essing:
- Target perceived loudness:
- Notes:

## Music treatment

- Arc:
- Ducking under VO:
- Moments where music should breathe:
- Notes:

## SFX treatment

- Palette:
- Moments:
- Avoid:

## Mastering target

| Target | Value | Status |
|---|---:|---|
| Integrated loudness | -14 LUFS default unless platform-specific target overrides | Pending |
| True peak ceiling | -1.0 dBTP default unless platform-specific target overrides | Pending |
| No clipping | Required | Pending |
| VO intelligibility | Required | Pending |
| Music masking VO | Must not happen | Pending |

## Premiere MCP execution notes

- Use Premiere audio tools/effects if exposed by the MCP bridge.
- If a mastering operation is not exposed, document it in `08_edit/compositor_review.md` and create a human finishing note.
- Do not export final until the mix is audited.

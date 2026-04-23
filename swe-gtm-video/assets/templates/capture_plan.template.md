# Capture Plan — {{PROJECT_NAME}}

## Capture objective

Show verified product truth with clean, readable, brand-safe software footage.

## Environment

- App URL/local command: {{url_or_command}}
- Browser/device: {{Chrome/Edge/iOS/Android/etc.}}
- Viewport: {{width x height}}
- Feature flags: {{flags}}
- Test account/tenant: {{safe account}}
- Demo data seed: {{seed}}

## Capture list

| Capture ID | Scene | State/action | Steps | Output type | Target path | Retake triggers |
|---|---|---|---|---|---|---|
| C001 | Hook | {{state}} | {{steps}} | video/screenshot | 06_capture/captures/C001.* | {{triggers}} |
| C002 | Proof | {{state}} | {{steps}} | video/screenshot | 06_capture/captures/C002.* | {{triggers}} |

## Interaction notes

- Slow interactions enough for comprehension.
- Avoid accidental hover states unless intentional.
- Keep cursor paths clean.
- Capture separate takes for UI proof and cinematic motion.
- Remove or mask private data before capture.

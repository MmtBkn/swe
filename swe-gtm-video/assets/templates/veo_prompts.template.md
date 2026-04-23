# Veo / Video Generation Prompts — {{PROJECT_NAME}}

## Global rules for generated video

- Generated assets must support the story; they must not invent product capabilities.
- Do not generate or reinterpret company logos, product icons, customer logos, or legal brand marks.
- For software-screen shots, use a real screenshot/frame as reference whenever possible and preserve UI exactly.
- Reject outputs that change UI text, move controls, distort logos, hallucinate data, or imply unsupported behavior.

## Prompt records

### Asset V001 — {{asset name}}

- Purpose: {{why this asset exists}}
- Scene/timecode: {{timecode}}
- Source/reference frame: {{path}}
- Model/tool: {{Veo/Gemini/Vertex/etc.}}
- Duration: {{seconds}}
- Aspect ratio/resolution/fps: {{spec}}
- Prompt:

```text
{{prompt}}
```

- Negative constraints:

```text
Do not alter any UI text, product layout, logos, brand colors, customer names, or data. Do not create new product screens. Do not add extra labels, buttons, panels, or menus. Avoid generic sci-fi visuals and fake holographic UI.
```

- Acceptance criteria:
  - {{criteria}}
- Rejection criteria:
  - {{criteria}}
- Output path:
  - {{path}}
- Review notes:
  - {{notes}}

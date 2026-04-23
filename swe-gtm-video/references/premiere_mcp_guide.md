# Premiere Pro MCP Integration Guide

This skill is designed to use `Adobe_Premiere_Pro_MCP` by `hetpatel-11` as the final assembly bridge when available.

Repository:
`https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP`

## Setup summary

The repo's manual Codex setup pattern is:

```bash
git clone https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP.git
cd Adobe_Premiere_Pro_MCP
npm install
npm run build
codex mcp add premiere_pro --env PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge -- node /absolute/path/to/Adobe_Premiere_Pro_MCP/dist/index.js
```

Inside Premiere:

1. Open Premiere Pro.
2. Enable UXP developer mode if required by your installed version/path.
3. Open `Window > Extensions > MCP Bridge (CEP)`.
4. Set Temp Directory to `/tmp/premiere-mcp-bridge`.
5. Click `Save Configuration`.
6. Click `Start Bridge`.
7. Confirm the MCP client can see the `premiere_pro` server.

## Operating rules for agents

1. Read/attach `premiere://config/get_instructions` when available.
2. Use MCP introspection to see exact tools and schemas.
3. Prefer high-level assembly tools with `clipPlan` when they can faithfully express the manifest.
4. Fall back to atomic Premiere operations when the cut needs precision.
5. Inspect the sequence after major batches.
6. Document every unsupported operation in `08_edit/compositor_review.md`.

## Expected capabilities to look for via introspection

- Project and sequence operations
- Media import and bin management
- Timeline placement and clip operations
- Transitions, effects, color, and keyframes
- MOGRT/graphics and captions helpers
- Markers and metadata
- Export / Adobe Media Encoder helpers
- High-level product/brand assembly workflows

## Safety

Premiere automation is powerful but not magic. Keep a human-review gate before export, especially for brand/legal/product truth, UI integrity, and final audio mastering.

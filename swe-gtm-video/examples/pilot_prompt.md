# Pilot prompt

Use the `swe-gtm-video` skill.

Create a 60-second go-to-market video production package for our agentic software development feature.

Target persona: senior engineering leaders and product leaders who need AI agents to move real work forward safely, not just chat about work.

Use real browser capture for product proof. Use generated video only for emotional opening plates, transitions, or grounded screenshot-to-video assets. Keep company logos, intro assets, and brand marks intact.

Final assembly must be agent-driven through Adobe Premiere Pro MCP, not FFmpeg. Build a version 2.x multi-track `timeline_manifest.json`, create `premiere_mcp_execution_plan.md`, and have the Premiere Compositor agent use MCP introspection before executing Premiere operations.

Spawn the specialist subagents:

- swe_gtm_persona_strategist
- swe_gtm_scriptwriter
- swe_gtm_motion_designer
- swe_gtm_sound_designer
- swe_gtm_director_producer
- swe_gtm_video_editor
- swe_gtm_premiere_compositor
- swe_gtm_brand_guardian

Run one refinement round. Create the full `gtm-video/<slug>/` project folder with `MASTER_PLAN.md`, script, motion plan, audio/mastering plan, capture plan, Veo prompts, asset registry, multi-track timeline manifest, Premiere MCP execution plan, compositor review, QA report, and final delivery report.

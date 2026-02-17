import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveSkillPaths } from "./skill-paths.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const distDir = path.join(repoRoot, "dist");
const skillPaths = resolveSkillPaths(repoRoot, process.argv.slice(2));

if (skillPaths.length === 0) {
  console.error("No skills found to build. Expected folders containing SKILL.md.");
  process.exit(1);
}

fs.mkdirSync(distDir, { recursive: true });

for (const skillPath of skillPaths) {
  const skillDir = path.join(repoRoot, skillPath);
  const outFile = path.join(distDir, `${skillPath}.skill`);

  if (!fs.existsSync(skillDir)) {
    console.error(`Missing skill folder: ${skillDir}`);
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(outFile), { recursive: true });
  if (fs.existsSync(outFile)) fs.rmSync(outFile);

  const result = spawnSync("zip", ["-r", outFile, skillPath], {
    cwd: repoRoot,
    stdio: "inherit"
  });

  if ((result.status ?? 1) !== 0) process.exit(result.status ?? 1);
}

process.exit(0);

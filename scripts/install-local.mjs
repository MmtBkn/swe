import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveSkillPaths } from "./skill-paths.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillPaths = resolveSkillPaths(repoRoot, process.argv.slice(2));

const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
const skillsDir = path.join(codexHome, "skills");
fs.mkdirSync(skillsDir, { recursive: true });

if (skillPaths.length === 0) {
  console.error("No skills found to install. Expected folders containing SKILL.md.");
  process.exit(1);
}

for (const skillPath of skillPaths) {
  const distFile = path.join(repoRoot, "dist", `${skillPath}.skill`);
  if (!fs.existsSync(distFile)) {
    console.error(`Missing dist file: ${distFile}`);
    console.error(`Run: npm run dist -- ${skillPath}`);
    process.exit(1);
  }

  const result = spawnSync("unzip", ["-o", distFile, "-d", skillsDir], {
    stdio: "inherit"
  });

  if ((result.status ?? 1) !== 0) process.exit(result.status ?? 1);
}

process.exit(0);

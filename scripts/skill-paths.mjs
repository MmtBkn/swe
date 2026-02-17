import fs from "node:fs";
import path from "node:path";

function isSkillDir(repoRoot, relDir) {
  return fs.existsSync(path.join(repoRoot, relDir, "SKILL.md"));
}

export function discoverSkillPaths(repoRoot) {
  const ignoredTopLevelDirs = new Set([
    ".git",
    ".idea",
    "dist",
    "node_modules",
    "scripts"
  ]);

  const results = [];
  for (const entry of fs.readdirSync(repoRoot, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (ignoredTopLevelDirs.has(entry.name)) continue;

    if (entry.name === ".system") {
      const systemRoot = path.join(repoRoot, ".system");
      if (!fs.existsSync(systemRoot)) continue;

      for (const systemEntry of fs.readdirSync(systemRoot, { withFileTypes: true })) {
        if (!systemEntry.isDirectory()) continue;
        const relDir = path.join(".system", systemEntry.name);
        if (isSkillDir(repoRoot, relDir)) results.push(relDir);
      }

      continue;
    }

    if (isSkillDir(repoRoot, entry.name)) results.push(entry.name);
  }

  results.sort();
  return results;
}

export function resolveSkillPaths(repoRoot, argv) {
  const args = argv.filter(Boolean);
  const requested = args.length === 0 || args.includes("all") ? discoverSkillPaths(repoRoot) : args;
  return [...new Set(requested)];
}


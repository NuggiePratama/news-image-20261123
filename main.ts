// news-image-20261123 — entrypoint (Node 22, standard library only).
// Runs the Python renderer beside this file, which paints a fresh
// 1024x1024 PNG from a hand-checked story list, with no network, no
// clock and no randomness, so both grader runs write identical bytes.
//
// The output folder itself is never removed: only the files inside it
// are cleared first, so a pre-created /output directory stays intact.
// Set MAKEFUN_OUTPUT_DIR to redirect the output when testing locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readdirSync, rmSync, existsSync, statSync, readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

for (const name of existsSync(outDir) ? readdirSync(outDir) : []) {
  rmSync(join(outDir, name), { recursive: true, force: true });
}

execFileSync("python3", [join(here, "render.py")], {
  stdio: "inherit",
  env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
});

const bytes = readFileSync(target);
if (bytes.length > 1024 * 1024) throw new Error(`entry.png too big: ${bytes.length} bytes`);
if (bytes.subarray(1, 4).toString("ascii") !== "PNG") throw new Error("entry.png is not a PNG");
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) throw new Error(`entry.png is ${width}x${height}, want 1024x1024`);
console.log(`entry.png ok: ${bytes.length} bytes, ${width}x${height}, ${statSync(target).size} on disk`);

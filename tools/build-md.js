#!/usr/bin/env node
/*
 * Wrap every article .md into a sibling .md.js so reader.html can load it with a
 * plain <script> tag. Browsers block fetch() of local files on file://, a script
 * tag is not blocked. Run after editing any .md: node tools/build-md.js
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SKIP = new Set(["tools", "_template", "assets", "node_modules", ".cursor"]);

let count = 0;
for (const dir of fs.readdirSync(ROOT, { withFileTypes: true })) {
  if (!dir.isDirectory() || SKIP.has(dir.name) || dir.name.startsWith(".")) continue;
  const folder = path.join(ROOT, dir.name);
  for (const f of fs.readdirSync(folder)) {
    if (!f.endsWith(".md")) continue;
    const src = path.join(folder, f);
    const out = src + ".js";
    const key = dir.name + "/" + f.slice(0, -3);
    const md = fs.readFileSync(src, "utf8");
    // JSON.stringify escapes quotes and newlines; also break "</script" sequences.
    const body = JSON.stringify(md).replace(/<\/(script)/gi, "<\\/$1");
    fs.writeFileSync(out,
      "window.MD_SOURCES=window.MD_SOURCES||{};\nwindow.MD_SOURCES[" +
      JSON.stringify(key) + "]=" + body + ";\n");
    count++;
  }
}
console.log("built " + count + " .md.js file(s)");

/**
 * KaTeX Pre-render Build Script
 *
 * Processes all HTML files:
 *  1. Replaces $$...$$ (display) and $...$ (inline) with pre-rendered KaTeX HTML
 *  2. Removes client-side KaTeX JS <script> tags (keeps CSS for styling)
 *  3. Removes katex-lazy.js reference
 *  4. Copies all assets (images, js, css) to dist/
 */

const fs = require('fs');
const path = require('path');
const katex = require('katex');

const SRC = __dirname;
const DIST = path.join(__dirname, 'dist');

// Files/dirs to skip
const SKIP = new Set(['node_modules', 'dist', '.git', 'build.js', 'package.json', 'package-lock.json', '.gitignore']);

// ── Helpers ──

function mkdirp(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    mkdirp(dest);
    for (const child of fs.readdirSync(src)) {
      if (SKIP.has(child)) continue;
      copyRecursive(path.join(src, child), path.join(dest, child));
    }
  } else {
    fs.copyFileSync(src, dest);
  }
}

/**
 * Render all $...$ and $$...$$ in an HTML string.
 * Skips content inside <code>, <pre>, <script>, <style>, HTML tags/attributes.
 */
function renderMath(html) {
  // Split HTML into segments: tags vs text
  // We only process text segments (outside of tags)
  const TAG_RE = /<(?:script|style|code|pre)[^>]*>[\s\S]*?<\/(?:script|style|code|pre)>|<[^>]+>/gi;

  let result = '';
  let lastIndex = 0;
  let match;

  // Find all HTML tags and protected blocks
  const segments = [];
  const tagRegex = new RegExp(TAG_RE.source, 'gi');

  while ((match = tagRegex.exec(html)) !== null) {
    if (match.index > lastIndex) {
      segments.push({ type: 'text', content: html.slice(lastIndex, match.index) });
    }
    segments.push({ type: 'tag', content: match[0] });
    lastIndex = tagRegex.lastIndex;
  }
  if (lastIndex < html.length) {
    segments.push({ type: 'text', content: html.slice(lastIndex) });
  }

  // Process only text segments
  for (const seg of segments) {
    if (seg.type === 'tag') {
      result += seg.content;
    } else {
      result += renderMathInText(seg.content);
    }
  }

  return result;
}

function renderMathInText(text) {
  // Process display math first ($$...$$), then inline ($...$)
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => {
    return renderKaTeX(tex.trim(), true);
  });

  // Inline math: $...$ but not \\$ (escaped) or standalone $
  // Match $...$ where content is non-empty and doesn't start/end with space
  text = text.replace(/(?<![\\])\$([^\$\n]+?)\$/g, (full, tex) => {
    // Skip if it looks like a currency amount
    if (/^\d+[.,]?\d*$/.test(tex.trim())) return full;
    return renderKaTeX(tex.trim(), false);
  });

  return text;
}

let renderCount = 0;
let errorCount = 0;

function renderKaTeX(tex, displayMode) {
  try {
    renderCount++;
    return katex.renderToString(tex, {
      displayMode: displayMode,
      throwOnError: false,
      strict: false,
      trust: true,
      output: 'html'  // lighter than htmlAndMathml
    });
  } catch (e) {
    errorCount++;
    // Return original with delimiters on error
    const delim = displayMode ? '$$' : '$';
    return delim + tex + delim;
  }
}

/**
 * Clean up script tags:
 * - Remove KaTeX JS (katex.min.js, auto-render.min.js, katex-lazy.js)
 * - Keep katex.min.css (needed for rendered HTML styling)
 */
function cleanScripts(html) {
  // Remove katex.min.js script
  html = html.replace(/<script[^>]*katex\.min\.js[^>]*><\/script>\s*/g, '');
  // Remove auto-render script
  html = html.replace(/<script[^>]*auto-render\.min\.js[^>]*><\/script>\s*/g, '');
  // Remove katex-lazy.js script
  html = html.replace(/<script[^>]*katex-lazy\.js[^>]*><\/script>\s*/g, '');
  return html;
}

// ── Main ──

console.log('🔨 Building analytical chemistry review site...');
console.log(`   Source: ${SRC}`);
console.log(`   Output: ${DIST}`);

// Clean dist
if (fs.existsSync(DIST)) {
  fs.rmSync(DIST, { recursive: true });
}
mkdirp(DIST);

// Copy everything to dist
copyRecursive(SRC, DIST);

// Process all HTML files in dist
const htmlFiles = fs.readdirSync(DIST).filter(f => f.endsWith('.html'));

console.log(`\n📄 Processing ${htmlFiles.length} HTML files...\n`);

for (const file of htmlFiles) {
  const filePath = path.join(DIST, file);
  let html = fs.readFileSync(filePath, 'utf8');

  const before = html.length;
  html = renderMath(html);
  html = cleanScripts(html);

  fs.writeFileSync(filePath, html, 'utf8');

  const after = html.length;
  const ratio = ((after / before) * 100).toFixed(0);
  console.log(`   ✅ ${file} (${before} → ${after} bytes, ${ratio}%)`);
}

console.log(`\n✨ Done! Rendered ${renderCount} formulas (${errorCount} errors)`);
console.log(`   Output directory: ${DIST}`);

#!/bin/bash
# Comprehensive validation script for Analytical Chemistry deploy
# Checks: HTML structure, image references, links, nav consistency, KaTeX

DEPLOY_DIR="$(cd "$(dirname "$0")" && pwd)"
ERRORS=0
WARNINGS=0

echo "========================================="
echo "  Analytical Chemistry Deploy Validator"
echo "========================================="
echo "Directory: $DEPLOY_DIR"
echo ""

# 1. Check all HTML files exist
echo "--- [1] HTML File Existence Check ---"
for f in index.html login.html ch1.html ch3.html ch5-1.html ch5-2.html ch6.html ch7.html ch9.html ch10.html formulas.html exam-review.html quiz1.html quiz2.html final2022.html; do
  if [ ! -f "$DEPLOY_DIR/$f" ]; then
    echo "ERROR: Missing file: $f"
    ERRORS=$((ERRORS+1))
  fi
done
echo "  HTML files check done."

# 2. Check all image references point to existing files
echo ""
echo "--- [2] Image Reference Check ---"
for html in "$DEPLOY_DIR"/*.html; do
  fname=$(basename "$html")
  # Extract src attributes from img tags
  grep -oP 'src="([^"]+\.(png|jpg|jpeg|gif|svg))"' "$html" 2>/dev/null | sed 's/src="//;s/"$//' | while read -r img; do
    if [ ! -f "$DEPLOY_DIR/$img" ]; then
      echo "ERROR: [$fname] Image not found: $img"
      ERRORS=$((ERRORS+1))
      # Write to temp error file since we're in a subshell
      echo "1" >> /tmp/achem_errors.tmp
    fi
  done
done
if [ -f /tmp/achem_errors.tmp ]; then
  IMG_ERRS=$(wc -l < /tmp/achem_errors.tmp)
  ERRORS=$((ERRORS+IMG_ERRS))
  rm -f /tmp/achem_errors.tmp
else
  echo "  All image references valid."
fi

# 3. Check internal links (href to .html files)
echo ""
echo "--- [3] Internal Link Check ---"
for html in "$DEPLOY_DIR"/*.html; do
  fname=$(basename "$html")
  grep -oP 'href="([^"#]+\.html)' "$html" 2>/dev/null | sed 's/href="//' | sort -u | while read -r link; do
    if [ ! -f "$DEPLOY_DIR/$link" ]; then
      echo "ERROR: [$fname] Broken link: $link"
      echo "1" >> /tmp/achem_link_errors.tmp
    fi
  done
done
if [ -f /tmp/achem_link_errors.tmp ]; then
  LINK_ERRS=$(wc -l < /tmp/achem_link_errors.tmp)
  ERRORS=$((ERRORS+LINK_ERRS))
  rm -f /tmp/achem_link_errors.tmp
else
  echo "  All internal links valid."
fi

# 4. Check navigation bar consistency
echo ""
echo "--- [4] Navigation Bar Consistency Check ---"
EXPECTED_NAV_LINKS="index.html ch1.html ch3.html ch5-1.html ch5-2.html ch6.html ch7.html ch9.html ch10.html formulas.html"
for html in "$DEPLOY_DIR"/ch*.html "$DEPLOY_DIR"/formulas.html "$DEPLOY_DIR"/exam-review.html "$DEPLOY_DIR"/quiz*.html "$DEPLOY_DIR"/final2022.html; do
  [ ! -f "$html" ] && continue
  fname=$(basename "$html")
  for nav_link in $EXPECTED_NAV_LINKS; do
    if ! grep -q "href=\"$nav_link\"" "$html" 2>/dev/null; then
      echo "ERROR: [$fname] Missing nav link to: $nav_link"
      echo "1" >> /tmp/achem_nav_errors.tmp
    fi
  done
done
if [ -f /tmp/achem_nav_errors.tmp ]; then
  NAV_ERRS=$(wc -l < /tmp/achem_nav_errors.tmp)
  ERRORS=$((ERRORS+NAV_ERRS))
  rm -f /tmp/achem_nav_errors.tmp
else
  echo "  Navigation bars consistent."
fi

# 5. Check HTML structure (basic)
echo ""
echo "--- [5] HTML Structure Check ---"
for html in "$DEPLOY_DIR"/*.html; do
  fname=$(basename "$html")
  # Check DOCTYPE
  if ! head -1 "$html" | grep -qi "doctype"; then
    echo "ERROR: [$fname] Missing DOCTYPE"
    ERRORS=$((ERRORS+1))
  fi
  # Check closing tags
  if ! grep -q "</html>" "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing </html>"
    ERRORS=$((ERRORS+1))
  fi
  if ! grep -q "</body>" "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing </body>"
    ERRORS=$((ERRORS+1))
  fi
  if ! grep -q "</head>" "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing </head>"
    ERRORS=$((ERRORS+1))
  fi
  # Check for unclosed tags (basic: count <div vs </div>)
  OPEN_DIV=$(grep -o '<div' "$html" 2>/dev/null | wc -l)
  CLOSE_DIV=$(grep -o '</div>' "$html" 2>/dev/null | wc -l)
  if [ "$OPEN_DIV" -ne "$CLOSE_DIV" ]; then
    echo "WARNING: [$fname] Unbalanced div tags: $OPEN_DIV open vs $CLOSE_DIV close"
    WARNINGS=$((WARNINGS+1))
  fi
  # Check table balance
  OPEN_TABLE=$(grep -o '<table' "$html" 2>/dev/null | wc -l)
  CLOSE_TABLE=$(grep -o '</table>' "$html" 2>/dev/null | wc -l)
  if [ "$OPEN_TABLE" -ne "$CLOSE_TABLE" ]; then
    echo "ERROR: [$fname] Unbalanced table tags: $OPEN_TABLE open vs $CLOSE_TABLE close"
    ERRORS=$((ERRORS+1))
  fi
  # Check tr balance
  OPEN_TR=$(grep -o '<tr' "$html" 2>/dev/null | wc -l)
  CLOSE_TR=$(grep -o '</tr>' "$html" 2>/dev/null | wc -l)
  if [ "$OPEN_TR" -ne "$CLOSE_TR" ]; then
    echo "ERROR: [$fname] Unbalanced tr tags: $OPEN_TR open vs $CLOSE_TR close"
    ERRORS=$((ERRORS+1))
  fi
done
echo "  HTML structure check done."

# 6. Check KaTeX delimiters balance
echo ""
echo "--- [6] KaTeX Delimiter Check ---"
for html in "$DEPLOY_DIR"/*.html; do
  fname=$(basename "$html")
  [ "$fname" = "login.html" ] && continue
  [ "$fname" = "index.html" ] && continue
  # Check $$ balance (display math)
  DD_COUNT=$(grep -o '\$\$' "$html" 2>/dev/null | wc -l)
  if [ $((DD_COUNT % 2)) -ne 0 ]; then
    echo "ERROR: [$fname] Unbalanced \$\$ delimiters (count: $DD_COUNT)"
    ERRORS=$((ERRORS+1))
  fi
done
echo "  KaTeX delimiter check done."

# 7. Check required JS/CSS references
echo ""
echo "--- [7] Script/CSS Reference Check ---"
for html in "$DEPLOY_DIR"/ch*.html "$DEPLOY_DIR"/formulas.html "$DEPLOY_DIR"/exam-review.html "$DEPLOY_DIR"/quiz*.html "$DEPLOY_DIR"/final2022.html; do
  [ ! -f "$html" ] && continue
  fname=$(basename "$html")
  # Check for toc.js
  if ! grep -q 'toc.js' "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing toc.js reference"
    ERRORS=$((ERRORS+1))
  fi
  # Check for auth.js
  if ! grep -q 'auth.js' "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing auth.js reference"
    ERRORS=$((ERRORS+1))
  fi
  # Check for progress.js
  if ! grep -q 'progress.js' "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing progress.js reference"
    ERRORS=$((ERRORS+1))
  fi
  # Check for KaTeX
  if ! grep -q 'katex' "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing KaTeX reference"
    ERRORS=$((ERRORS+1))
  fi
  # Check for toc.css
  if ! grep -q 'toc.css' "$html" 2>/dev/null; then
    echo "ERROR: [$fname] Missing toc.css reference"
    ERRORS=$((ERRORS+1))
  fi
done
echo "  Script/CSS reference check done."

# 8. Check image CSS class exists in files that reference images
echo ""
echo "--- [8] Image CSS Class Check ---"
for html in "$DEPLOY_DIR"/*.html; do
  fname=$(basename "$html")
  if grep -q 'class="ppt-img"' "$html" 2>/dev/null; then
    if ! grep -q '\.ppt-img' "$html" 2>/dev/null; then
      echo "ERROR: [$fname] Uses ppt-img class but CSS not defined"
      ERRORS=$((ERRORS+1))
    fi
  fi
done
echo "  Image CSS class check done."

# Summary
echo ""
echo "========================================="
echo "  VALIDATION SUMMARY"
echo "========================================="
echo "  Errors:   $ERRORS"
echo "  Warnings: $WARNINGS"
echo "========================================="
echo ""
if [ $ERRORS -eq 0 ]; then
  echo "  PASS - All checks passed!"
else
  echo "  FAIL - Fix $ERRORS error(s) and re-run"
fi
exit $ERRORS

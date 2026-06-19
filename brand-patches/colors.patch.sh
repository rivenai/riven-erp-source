#!/usr/bin/env bash
set -euo pipefail

ODOO_DIR="${ODOO_DIR:-/opt/odoo}"

echo "Applying Riven color patches to ${ODOO_DIR} ..."

# Replace Odoo's primary purple tones with Riven green.
find "$ODOO_DIR" -type f \( \
  -name "*.css" -o -name "*.scss" -o -name "*.less" -o -name "*.xml" -o \
  -name "*.html" -o -name "*.js" -o -name "*.mjs" -o -name "*.svg" \
\) -print0 | xargs -0 perl -pi -e '
  s/#71639e/#00a86b/g;
  s/#875a7b/#00a86b/g;
  s/#7c7bad/#00a86b/g;
'

echo "Color patches applied."

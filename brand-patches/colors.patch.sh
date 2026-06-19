#!/usr/bin/env bash
set -euo pipefail

ODOO_DIR=""
for candidate in /usr/lib/python3/dist-packages/odoo /usr/lib/python3/site-packages/odoo /opt/odoo; do
  if [ -d "$candidate" ]; then
    ODOO_DIR="$candidate"
    break
  fi
done

if [ -z "$ODOO_DIR" ]; then
  echo "WARNING: Could not find Odoo installation directory. Skipping color patches."
  exit 0
fi

echo "Applying Riven color patches to ${ODOO_DIR} ..."

# Canonical Riven brand tokens (see brand/v1/tokens.css).
# Primary: Riven Teal #008173
find "$ODOO_DIR" -type f \( \
  -name "*.css" -o -name "*.scss" -o -name "*.less" -o -name "*.xml" -o \
  -name "*.html" -o -name "*.js" -o -name "*.mjs" -o -name "*.svg" \
\) -print0 | xargs -0 perl -pi -e '
  s/#71639e/#008173/gi;
  s/#875a7b/#008173/gi;
  s/#7c7bad/#008173/gi;
  s/#68465f/#008173/gi;
  s/#65435c/#008173/gi;
  s/#3d2938/#008173/gi;
  s/#00a86b/#008173/gi;
' 2>/dev/null || true

echo "Color patches applied."

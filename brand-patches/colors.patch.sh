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

# Canonical Riven brand tokens (Brand Guide 0.0.3 Alpha).
# Primary: Riven Magenta #EC008C (D009 teal #008173 retired 2026-08-27, owner ruling)
find "$ODOO_DIR" -type f \( \
  -name "*.css" -o -name "*.scss" -o -name "*.less" -o -name "*.xml" -o \
  -name "*.html" -o -name "*.js" -o -name "*.mjs" -o -name "*.svg" \
\) -print0 | xargs -0 perl -pi -e '
  s/#71639e/#EC008C/gi;
  s/#875a7b/#EC008C/gi;
  s/#7c7bad/#EC008C/gi;
  s/#68465f/#EC008C/gi;
  s/#65435c/#EC008C/gi;
  s/#3d2938/#EC008C/gi;
  s/#00a86b/#EC008C/gi;
  s/#008173/#EC008C/gi;
' 2>/dev/null || true

echo "Color patches applied."

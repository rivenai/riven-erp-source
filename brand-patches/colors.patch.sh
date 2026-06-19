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

find "$ODOO_DIR" -type f \( \
  -name "*.css" -o -name "*.scss" -o -name "*.less" -o -name "*.xml" -o \
  -name "*.html" -o -name "*.js" -o -name "*.mjs" -o -name "*.svg" \
\) -print0 | xargs -0 perl -pi -e '
  s/#71639e/#00a86b/g;
  s/#875a7b/#00a86b/g;
  s/#7c7bad/#00a86b/g;
' 2>/dev/null || true

echo "Color patches applied."

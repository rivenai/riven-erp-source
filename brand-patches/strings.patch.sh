#!/usr/bin/env bash
set -euo pipefail

# Detect Odoo installation path across common layouts.
ODOO_DIR=""
for candidate in /usr/lib/python3/dist-packages/odoo /usr/lib/python3/site-packages/odoo /opt/odoo; do
  if [ -d "$candidate" ]; then
    ODOO_DIR="$candidate"
    break
  fi
done

if [ -z "$ODOO_DIR" ]; then
  echo "WARNING: Could not find Odoo installation directory. Skipping string patches."
  exit 0
fi

echo "Applying Riven string patches to ${ODOO_DIR} ..."

find "$ODOO_DIR" -type f \( \
  -name "*.xml" -o -name "*.html" -o -name "*.js" -o -name "*.mjs" -o \
  -name "*.css" -o -name "*.scss" -o -name "*.less" -o -name "*.json" -o \
  -name "*.po" -o -name "*.pot" -o -name "*.md" -o -name "*.txt" -o \
  -name "*.csv" \
\) -print0 | xargs -0 perl -pi -e '
  s/Odoo S\.A\./Riven AI/g;
  s/odoo\.com/rivenai.io/g;
  s/Powered by Odoo/Powered by Riven AI/g;
  s/© Odoo/© Riven AI/g;
  s/\bOdoo\b/Riven ERP/g;
' 2>/dev/null || true

echo "String patches applied."

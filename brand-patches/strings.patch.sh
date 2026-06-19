#!/usr/bin/env bash
set -euo pipefail

ODOO_DIR="${ODOO_DIR:-/opt/odoo}"

echo "Applying Riven string patches to ${ODOO_DIR} ..."

# Patch UI/string files only (avoid altering Python module names / imports).
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
'

echo "String patches applied."

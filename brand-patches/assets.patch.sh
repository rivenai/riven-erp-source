#!/usr/bin/env bash
set -euo pipefail

ODOO_DIR=""
for candidate in /usr/lib/python3/dist-packages/odoo /usr/lib/python3/site-packages/odoo /opt/odoo; do
  if [ -d "$candidate" ]; then
    ODOO_DIR="$candidate"
    break
  fi
done

BRAND_DIR="/opt/brand-patches/assets"

if [ -z "$ODOO_DIR" ]; then
  echo "WARNING: Could not find Odoo installation directory. Skipping asset patches."
  exit 0
fi

echo "Applying Riven asset patches to ${ODOO_DIR} ..."

if [ -f "$BRAND_DIR/favicon.ico" ]; then
  find "$ODOO_DIR" -name "favicon.ico" -exec cp "$BRAND_DIR/favicon.ico" {} \; 2>/dev/null || true
fi

if [ -f "$BRAND_DIR/logo.png" ]; then
  find "$ODOO_DIR" -path "*/web/static/img/*" -type f \( -name "logo*.png" -o -name "logo*.svg" -o -name "nologo*.png" \) | while read -r img; do
    cp "$BRAND_DIR/logo.png" "$img" 2>/dev/null || true
  done
fi

echo "Asset patches applied."

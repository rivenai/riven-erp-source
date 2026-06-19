#!/usr/bin/env bash
set -euo pipefail

ODOO_DIR="${ODOO_DIR:-/opt/odoo}"
ASSETS_DIR="${ASSETS_DIR:-/opt/brand-patches/assets}"

echo "Applying Riven asset patches from ${ASSETS_DIR} ..."

declare -A MAP=(
  ["favicon.ico"]="$ODOO_DIR/addons/web/static/img/favicon.ico"
  ["logo.png"]="$ODOO_DIR/addons/web/static/img/logo.png"
  ["logo-login.png"]="$ODOO_DIR/addons/web/static/img/logo-inverse.png"
  ["logo-email.png"]="$ODOO_DIR/addons/web/static/img/logo-email.png"
  ["og-image.png"]="$ODOO_DIR/addons/web/static/img/og_image.png"
)

for asset in "${!MAP[@]}"; do
  src="$ASSETS_DIR/$asset"
  dst="${MAP[$asset]}"
  if [ -f "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    if [ "$src" -ef "$dst" ]; then
      echo "Asset already in place: $dst"
    else
      cp -v "$src" "$dst"
    fi
  else
    echo "Skipping missing asset: $src"
  fi
done

echo "Asset patches applied."

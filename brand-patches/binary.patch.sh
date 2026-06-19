#!/usr/bin/env bash
set -euo pipefail

# Strip upstream Odoo branding down to the runtime binary and entrypoint.
# This renames the odoo wrapper script and updates the container entrypoint
# so the running process is named "riven-erp" instead of "odoo".

ODOO_BIN="/usr/bin/odoo"
RIVEN_BIN="/usr/bin/riven-erp"
ENTRYPOINT="/entrypoint.sh"

if [ -f "$ODOO_BIN" ]; then
  echo "Renaming ${ODOO_BIN} -> ${RIVEN_BIN} ..."
  mv "$ODOO_BIN" "$RIVEN_BIN"
  chmod +x "$RIVEN_BIN"
fi

# Ensure a stable "riven-erp" command exists even if the upstream wrapper moves.
if [ -f "$RIVEN_BIN" ] && [ ! -e "$ODOO_BIN" ]; then
  ln -s "$RIVEN_BIN" "$ODOO_BIN"
fi

# Update the official Odoo entrypoint to invoke the Riven-branded binary.
# Only rewrite the actual `exec odoo ...` invocations so the container's CMD
# (`odoo`) still matches the case statement and the default Postgres credentials
# in the entrypoint are left intact.
if [ -f "$ENTRYPOINT" ]; then
  echo "Patching ${ENTRYPOINT} to use riven-erp ..."
  sed -i \
    -e 's|\bexec odoo\b|exec riven-erp|g' \
    -e 's|ODOO_RC|RIVEN_ERP_RC|g' \
    "$ENTRYPOINT" || true
fi

# Rename the canonical config file if it still has the upstream name and
# point the environment at it.
if [ -f "/etc/odoo/odoo.conf" ] && [ ! -f "/etc/odoo/riven-erp.conf" ]; then
  cp "/etc/odoo/odoo.conf" "/etc/odoo/riven-erp.conf"
fi

# Normalize upstream file paths inside the config to Riven-branded paths.
if [ -f "/etc/odoo/riven-erp.conf" ]; then
  sed -i \
    -e 's|/var/log/odoo/|/var/log/riven-erp/|g' \
    -e 's|/var/lib/odoo|/var/lib/riven-erp|g' \
    "/etc/odoo/riven-erp.conf" || true
fi

# Ensure the Riven log and data directories exist and are writable by the
# `odoo` runtime user inherited from the upstream image.
mkdir -p /var/log/riven-erp /var/lib/riven-erp
chmod 755 /var/log/riven-erp /var/lib/riven-erp
chown -R odoo:odoo /var/log/riven-erp /var/lib/riven-erp /etc/odoo/riven-erp.conf 2>/dev/null || \
  chown -R odoo /var/log/riven-erp /var/lib/riven-erp /etc/odoo/riven-erp.conf || true

# Ensure the container environment prefers the Riven config path.  This is
# read by the official entrypoint to locate the config file.
if [ -f "/etc/odoo/riven-erp.conf" ]; then
  RIVEN_ENV="/etc/odoo/riven-erp-env.sh"
  cat > "$RIVEN_ENV" <<'EOF'
export RIVEN_ERP_RC=${RIVEN_ERP_RC:-/etc/odoo/riven-erp.conf}
export ODOO_RC=${RIVEN_ERP_RC:-/etc/odoo/riven-erp.conf}
EOF
  chmod +x "$RIVEN_ENV"

  # Inject the env helper into container-wide shell startup when present.
  if [ -d "/etc/profile.d" ]; then
    ln -sf "$RIVEN_ENV" "/etc/profile.d/riven-erp.sh" || true
  fi
fi

echo "Binary/entrypoint patches applied."

# Applies EXACTLY the same transformation rules as riven.reident.patch.sh
# (the v0.0.02 community reidentification) to the enterprise addons tree:
#
#   Python package  : odoo      -> riven_erp   (so 'from odoo.addons.X import Y'
#                                             becomes 'from riven_erp.addons.X import Y',
#                                             matching how the 0.0.02 rename handled imports)
#   JS namespace    : odoo      -> riven
#   XML root tag    : <odoo>    -> <riven_erp>  (matches convert.py DATA_ROOTS)
#   Display strings : Odoo      -> Riven ERP, OdooBot -> Riven Bot
#   Legacy          : openerp/OpenERP/OPENERP -> riven_erp / Riven ERP / RIVEN_ERP
#   All-caps (env)  : ODOO*     -> RIVEN_ERP*
#   Domains         : odoo.com  -> rivenai.io
#
# No package move / egg-info / bin / entrypoint / release-marker work here —
# those are core-image concerns already handled by the 0.0.02 layer; the
# release marker bump to 0.0.03 is done by Dockerfile.v6.
#
# Usage: riven.enterprise.patch.sh [tree-dir]
#   default tree-dir = /usr/lib/python3/dist-packages/riven_erp/enterprise-addons
set -euo pipefail

ENT=${1:-/usr/lib/python3/dist-packages/riven_erp/enterprise-addons}

[ -d "$ENT" ] || { echo "ERROR: $ENT not found" >&2; exit 1; }

echo "== reident python (.py) in $ENT =="
find "$ENT" -type f -name '*.py' -print0 | xargs -0 -n 200 sed -i \
  -e 's@odoo\.define@riven.define@g' \
  -e 's@odoo\.loader@riven.loader@g' \
  -e 's@odoo\.isReady@riven.isReady@g' \
  -e 's@odoo\.isTourReady@riven.isTourReady@g' \
  -e 's@odoo\.startTour@riven.startTour@g' \
  -e 's@odoo\.__session_info__@riven.__session_info__@g' \
  -e 's@odoo\.__DEBUG__@riven.__DEBUG__@g' \
  -e 's@odoo\.__WOWL_DEBUG__@riven.__WOWL_DEBUG__@g' \
  -e 's@odoo\.csrf_token@riven.csrf_token@g' \
  -e 's@odoo\.loadMenusPromise@riven.loadMenusPromise@g' \
  -e 's@odoo\.reloadMenus@riven.reloadMenus@g' \
  -e 's@odoo\.mobile@riven.mobile@g' \
  -e 's@odoo\.pro@riven.pro@g' \
  -e 's@odoo\.official@riven.official@g' \
  -e 's@odoo\.odoo@riven.riven@g' \
  -e 's@odoo\.foo@riven.foo@g' \
  -e 's@odoo-module@riven-module@g' \
  -e 's@__odooAssetError@__rivenAssetError@g' \
  -e 's@odooscript@rivenscript@g' \
  -e 's@odoo\.conf@riven-erp.conf@g' \
  -e 's@~/.odoorc@~/.riven-erp.conf@g' \
  -e 's@~/.openerp_serverrc@~/.riven-erp.conf@g' \
  -e 's@odoo\.com@rivenai.io@g' \
  -e 's@odoo\.be@rivenai.io@g' \
  -e 's@odoo\.eu@rivenai.io@g' \
  -e 's@odoo\.sh@rivenai.io@g' \
  -e 's@\bodoo\b@riven_erp@g' \
  -e 's@\bOdoo\b@Riven ERP@g' \
  -e 's@OdooBot@Riven Bot@g' \
  -e 's@odoobot@rivenbot@g' \
  -e 's@\bopenerp\b@riven_erp@g' \
  -e 's@\bOPENERP\b@RIVEN_ERP@g' \
  -e 's@OpenERP@Riven ERP@g' \
  -e 's@ODOO@RIVEN_ERP@g' \
  -e 's@odoo@riven@gI'

echo "== reident javascript (.js) =="
find "$ENT" -type f -name '*.js' -print0 | xargs -0 -n 200 sed -i \
  -e 's@odoo@riven@gI'

echo "== reident templates (.xml .html) =="
find "$ENT" -type f \( -name '*.xml' -o -name '*.html' \) -print0 | xargs -0 -n 200 sed -i \
  -e 's@<odoo\([ >]\)@<riven_erp\1@g' \
  -e 's@</odoo>@</riven_erp>@g' \
  -e 's@<openerp\([ >]\)@<riven_erp\1@g' \
  -e 's@</openerp>@</riven_erp>@g' \
  -e 's@OdooBot@Riven Bot@g' \
  -e 's@odoobot@rivenbot@g' \
  -e 's@o_odoobot_command@o_rivenbot_command@g' \
  -e 's@odoo\.com@rivenai.io@g' \
  -e 's@\bOdoo\b@Riven ERP@g' \
  -e 's@odoo@riven@gI'

echo "== reident styles (.scss .css) =="
find "$ENT" -type f \( -name '*.scss' -o -name '*.css' \) -print0 | xargs -0 -n 200 sed -i \
  -e 's@odoo@riven@gI'

echo "== rename filesystem entries (dirs + files) containing odoo =="
find "$ENT" -depth -iname '*odoo*' -print0 | while IFS= read -r -d '' p; do
  d=$(dirname "$p"); b=$(basename "$p")
  nb=$(printf '%s' "$b" | sed 's@odoo@riven@gI')
  [ "$b" = "$nb" ] || mv -n "$p" "$d/$nb"
done

echo "== purge stale bytecode + recompile =="
find "$ENT" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
python3 -m compileall -q -f "$ENT"

echo "== enterprise tree reidentification complete =="

[stderr]

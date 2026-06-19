ARG ODOO_VERSION=19.0
FROM odoo:${ODOO_VERSION}

USER root

# Copy and apply Riven brand patches to the upstream Odoo installation.
COPY brand-patches /opt/brand-patches
RUN bash /opt/brand-patches/strings.patch.sh \
 && bash /opt/brand-patches/colors.patch.sh \
 && bash /opt/brand-patches/assets.patch.sh

# Ensure brand assets directory exists for downstream images.
RUN mkdir -p /mnt/extra-addons/brand/assets

USER odoo

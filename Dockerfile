ARG ODOO_VERSION=19.0
FROM python:3.12-slim-bookworm

ARG ODOO_VERSION
ENV ODOO_VERSION=${ODOO_VERSION}

# Install build tools, system libraries, and runtime dependencies required by Odoo.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    libwebp-dev \
    libfontconfig1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/odoo

# Shallow-clone upstream Odoo at build time. No full upstream history is kept in this repo.
RUN git clone --depth 1 --branch ${ODOO_VERSION} https://github.com/odoo/odoo.git .

# Copy and apply Riven brand patches.
COPY brand-patches /opt/brand-patches
RUN bash /opt/brand-patches/strings.patch.sh \
 && bash /opt/brand-patches/colors.patch.sh \
 && bash /opt/brand-patches/assets.patch.sh

# Install Odoo Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8069

ENTRYPOINT ["./odoo-bin"]

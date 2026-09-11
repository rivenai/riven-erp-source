# rivenai/riven-erp-source

Source-build foundation for **Riven ERP** — a fully brand-stripped, Riven-branded distribution of [Odoo](https://github.com/odoo/odoo).

This repository does **not** contain the upstream Odoo history. Instead, it provides a lightweight build harness that:

1. Shallow-clones upstream Odoo at build time (`--depth 1`).
2. Applies Riven brand patches in `brand-patches/`.
3. Builds and pushes the container image to `rivencommerceacr.azurecr.io/riven-erp`.

## Build

### Enterprise (canonical, what production runs)

The full enterprise image is built with `Dockerfile.enterprise`:

```bash
# 1. Export the enterprise tree from rivenai/riven-erp-enterprise
#    (pin the commit in the release notes of the tag being built)
tar -czf enterprise-src.tar.gz -C <enterprise-clone> enterprise

# 2. Build
docker build -f Dockerfile.enterprise \
  --build-arg RIVEN_RELEASE=0.0.04 \
  -t rivenai/riven-erp:pes-bridge-0.0.04 .
```

This layers the reidentified 736-module enterprise tree, the import_xml.rng
schema fix, and the XML root-tag repair onto the shipped community base.
`brand-patches/riven.enterprise.patch.sh` holds the reidentification rules.

Known gap: the base community reidentification (`riven.reident.patch.sh`, the
package-level rename) is not in this repo — it only survives inside the
shipped base image. Reconstructing it for a fully-from-source build is the
0.1.0 workstream.

### Base (community brand layer)

```bash
docker build --build-arg ODOO_VERSION=19.0 -t riven-erp:latest .
```

### CI

Pushes to `main` trigger `.github/workflows/build-and-push.yml`, producing:

- `rivencommerceacr.azurecr.io/riven-erp-source:latest`
- `rivencommerceacr.azurecr.io/riven-erp:${GITHUB_SHA}`

## Brand Patches

- `brand-patches/strings.patch.sh` — replaces Odoo-branded strings.
- `brand-patches/colors.patch.sh` — replaces Odoo purple colors with Riven green.
- `brand-patches/assets.patch.sh` — copies Riven assets into Odoo static paths.

Place asset files in `brand-patches/assets/` (see `brand-patches/assets/README.md`).

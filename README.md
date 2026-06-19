# rivenai/riven-erp-source

Source-build foundation for **Riven ERP** — a fully brand-stripped, Riven-branded distribution of [Odoo](https://github.com/odoo/odoo).

This repository does **not** contain the upstream Odoo history. Instead, it provides a lightweight build harness that:

1. Shallow-clones upstream Odoo at build time (`--depth 1`).
2. Applies Riven brand patches in `brand-patches/`.
3. Builds and pushes the container image to `rivencommerceacr.azurecr.io/riven-erp`.

## Build

### Local

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

# Odoo Render Deployment + My Inventory Import module

This package contains a minimal Odoo project prepared to deploy on Render (or other Docker-enabled hosts).

Structure:
- Dockerfile — builds Odoo image and copies `addons/` into `/mnt/extra-addons`
- odoo.conf — configuration using Render environment variables for Postgres
- addons/my_inventory_import — minimal add-on that imports inventory JSON from an external API by API token


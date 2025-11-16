# Odoo Render Deployment + My Inventory Import module

This package contains a minimal Odoo project prepared to deploy on Render (or other Docker-enabled hosts).

Structure:
- Dockerfile — builds Odoo image and copies `addons/` into `/mnt/extra-addons`
- odoo.conf — configuration using Render environment variables for Postgres
- addons/my_inventory_import — minimal add-on that imports inventory JSON from an external API by API token

## How to deploy on Render (summary)
1. Push this repository to GitHub.
2. Create a managed PostgreSQL database on Render and note host/port/user/password/db.
3. Create a **Web Service** on Render that builds from this repository (Docker).
4. Set environment variables on the Web Service:
   - RENDER_DB_HOST, RENDER_DB_PORT, RENDER_DB_USER, RENDER_DB_PASSWORD, RENDER_DB_NAME
   - ODOO_MASTER_PASSWORD = <some_admin_password>
5. Deploy and open the public URL provided by Render.
6. Activate developer mode in Odoo, update apps list, install "My Inventory Import".
7. Use "Import From API" menu to paste API URL and API token and import data.

See module README inside `addons/my_inventory_import` for more details.

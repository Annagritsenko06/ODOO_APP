# Render deployment notes (manual)
1. Create a PostgreSQL instance on Render (Managed Database).
2. Create a Web Service on Render connecting to your GitHub repo with this project.
   - Build Command: `docker build .`
   - Start Command: `odoo -c /etc/odoo/odoo.conf`
3. Add Environment Variables to the Web Service using the values from the PostgreSQL instance:
   - RENDER_DB_HOST
   - RENDER_DB_PORT
   - RENDER_DB_USER
   - RENDER_DB_PASSWORD
   - RENDER_DB_NAME
   - ODOO_MASTER_PASSWORD (set to a password you will remember)
4. Deploy. When the app is live open the URL and create the initial database using the Render PostgreSQL DB.

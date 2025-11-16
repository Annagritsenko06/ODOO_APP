FROM odoo:16.0

USER root

# Create folder for extra addons
RUN mkdir -p /mnt/extra-addons
RUN chown -R odoo:odoo /mnt/extra-addons

# Copy config and addons
COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons/

USER odoo

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]

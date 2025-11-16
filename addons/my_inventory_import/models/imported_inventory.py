from odoo import models, fields

class ImportedInventory(models.Model):
    _name = 'imported.inventory'
    _description = 'Imported Inventory (read-only viewer)'

    name = fields.Char(string='Title', readonly=True)
    external_id = fields.Char(string='External ID', readonly=True)
    api_token = fields.Char(string='API Token', readonly=True)
    data_json = fields.Text(string='Raw JSON', readonly=True)
    imported_on = fields.Datetime(string='Imported On', readonly=True)

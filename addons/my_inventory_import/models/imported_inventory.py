from odoo import models, fields, api
import json

class ImportedInventory(models.Model):
    _name = 'imported.inventory'
    _description = 'Imported Inventory (read-only viewer)'

    name = fields.Char(string='Title', readonly=True)
    external_id = fields.Char(string='External ID', readonly=True)
    api_token = fields.Char(string='API Token', readonly=True)
    data_json = fields.Text(string='Raw JSON', readonly=True, invisible=True)
    imported_on = fields.Datetime(string='Imported On', readonly=True)

    # Новые вычисляемые поля
    field_count = fields.Integer(string='Number of Fields', compute='_compute_stats', store=True)
    item_count = fields.Integer(string='Number of Items', compute='_compute_stats', store=True)
    aggregates_numeric = fields.Text(string='Numeric Aggregates', compute='_compute_stats')
    aggregates_text = fields.Text(string='Text Aggregates', compute='_compute_stats')

    @api.depends('data_json')
    def _compute_stats(self):
        for record in self:
            if not record.data_json:
                record.field_count = 0
                record.item_count = 0
                record.aggregates_numeric = ''
                record.aggregates_text = ''
                continue

            try:
                data = json.loads(record.data_json)
            except Exception:
                record.field_count = 0
                record.item_count = 0
                record.aggregates_numeric = ''
                record.aggregates_text = ''
                continue

            record.field_count = len(data.get('fields', []))
            record.item_count = data.get('itemCount', 0)

            numeric = data.get('aggregates', {}).get('numeric', {})
            text = data.get('aggregates', {}).get('text', {})

            # Форматирование числовых агрегатов
            record.aggregates_numeric = '\n'.join(
                f"{k}: Min = {v['min']}, Max = {v['max']}, Avg = {v['avg']}"
                for k, v in numeric.items()
            )

            # Форматирование текстовых агрегатов
            txt_lines = []
            for k, vals in text.items():
                vals_str = ', '.join(f"{v['value']}({v['count']})" for v in vals)
                txt_lines.append(f"{k}: {vals_str}")
            record.aggregates_text = '\n'.join(txt_lines)

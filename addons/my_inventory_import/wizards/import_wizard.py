from odoo import models, fields, api, _
import requests
import json

class ImportInventoryWizard(models.TransientModel):
    _name = 'import.inventory.wizard'
    _description = 'Import inventory from external API'

    api_url = fields.Char(
        string='API URL',
        required=True,
        default='https://your-app.example.com/api/inventories/aggregates'
    )
    api_token = fields.Char(string='API Token', required=True)
    external_id = fields.Char(string='External Inventory ID', help='Optional')

    def _call_api(self, url, token, external_id=None):
        headers = {'Accept': 'application/json', 'X-Api-Token': token}
        params = {}
        if external_id:
            params['id'] = external_id
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
        except Exception as e:
            raise models.ValidationError(_("API request failed: %s") % e)

        # fallback: try Authorization Bearer if 401
        if resp.status_code == 401:
            headers2 = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
            resp = requests.get(url, headers=headers2, params=params, timeout=15)

        if resp.status_code != 200:
            raise models.ValidationError(_("External API returned %s: %s") % (resp.status_code, resp.text))

        try:
            return resp.json()
        except Exception as e:
            raise models.ValidationError(_("Failed to parse JSON: %s") % e)

    def action_import(self):
        self.ensure_one()
        data = self._call_api(self.api_url, self.api_token, self.external_id)

        # canonicalize fields
        ext_id = data.get('external_id') or data.get('id') or self.external_id or ''
        title = data.get('title') or data.get('name') or f'Inventory {ext_id or ""}'
        raw = json.dumps(data, indent=2, ensure_ascii=False)

        Inventory = self.env['imported.inventory']
        domain = [('external_id', '=', ext_id)] if ext_id else [('name', '=', title)]
        inv = Inventory.search(domain, limit=1)
        vals = {
            'name': title,
            'external_id': ext_id,
            'api_token': self.api_token,
            'data_json': raw,
            'imported_on': fields.Datetime.now(),
        }
        if inv:
            inv.write(vals)
        else:
            inv = Inventory.create(vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'imported.inventory',
            'view_mode': 'form,tree',
            'res_id': inv.id,
            'target': 'current',
        }

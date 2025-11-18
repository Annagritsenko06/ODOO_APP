{
    'name': 'My ODOO FOR INVENTORIES',
    'version': '1.0',
    'summary': 'Import inventories from external app by API token (read-only viewer)',
    'author': 'Generated',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/inventory_views.xml',
        'views/import_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
}

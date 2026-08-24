{
    'name': 'Elva Proje',
    'version': '16.0.1.0.1',
    'category': 'Customizations',
    'summary': 'Adds x_deneme field to x_project model',
    'description': """
        This module adds a new field (x_deneme) to the x_project model, 
        which was created via the Odoo UI customization.
        
        Using XML data instead of Python to prevent state corruption of the manual model.
    """,
    'author': 'Tugay Hatil',
    'depends': ['base'],
    'data': [
        'data/ir_model_fields.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

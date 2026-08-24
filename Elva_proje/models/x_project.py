from odoo import models, fields

class XProject(models.Model):
    _inherit = 'x_project'

    x_deneme = fields.Char(string='Deneme')

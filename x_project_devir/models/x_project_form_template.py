# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class XProjectFormTemplate(models.Model):
    _name = 'x.project.form.template'
    _description = 'Proje Form Şablonu'
    _order = 'version desc, id desc'
    
    name = fields.Char('Şablon Adı', required=True, translate=True)
    version = fields.Integer('Versiyon', required=True, default=1)
    active = fields.Boolean('Aktif', default=True)
    description = fields.Text('Açıklama')
    section_ids = fields.One2many('x.project.form.section', 'template_id', string='Bölümler')
    form_count = fields.Integer('Form Sayısı', compute='_compute_form_count')
    
    _sql_constraints = [
        ('name_version_unique', 'UNIQUE(name, version)', 'Aynı isim ve versiyon için şablon zaten mevcut!'),
    ]
    
    @api.depends('section_ids')
    def _compute_form_count(self):
        for template in self:
            template.form_count = self.env['x.project.form'].search_count([
                ('template_id', '=', template.id)
            ])
    
    def action_duplicate(self):
        """Şablonu yeni versiyon olarak kopyalar"""
        self.ensure_one()
        new_version = self.version + 1
        # Mevcut aktif şablonları pasif yap
        self.search([('name', '=', self.name)]).write({'active': False})
        
        new_template = self.copy({
            'version': new_version,
            'active': True,
        })
        
        # Bölümleri ve soruları kopyala
        for section in self.section_ids:
            new_section = section.copy({
                'template_id': new_template.id,
            })
            for question in section.question_ids:
                question.copy({
                    'section_id': new_section.id,
                })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'x.project.form.template',
            'res_id': new_template.id,
            'view_mode': 'form',
        }
    
    def get_latest_active_template(self):
        """Aktif olan en son versiyon şablonunu döndürür"""
        return self.search([('active', '=', True)], order='version desc', limit=1)

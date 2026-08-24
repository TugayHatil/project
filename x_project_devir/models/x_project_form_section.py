# -*- coding: utf-8 -*-

from odoo import models, fields, api


class XProjectFormSection(models.Model):
    _name = 'x.project.form.section'
    _description = 'Proje Form Bölümü'
    _order = 'sequence, id'
    
    name = fields.Char('Bölüm Adı', required=True, translate=True)
    sequence = fields.Integer('Sıra', default=10)
    template_id = fields.Many2one('x.project.form.template', string='Şablon', required=True, ondelete='cascade')
    description = fields.Text('Açıklama')
    question_ids = fields.One2many('x.project.form.question', 'section_id', string='Sorular')
    question_count = fields.Integer('Soru Sayısı', compute='_compute_question_count')
    
    @api.depends('question_ids')
    def _compute_question_count(self):
        for section in self:
            section.question_count = len(section.question_ids)

# -*- coding: utf-8 -*-

from odoo import models, fields, api


class XProject(models.Model):
    _inherit = 'x.project'
    
    # Proje Devir Formu ilişkisi - geçici olarak devre dışı
    # form_ids = fields.One2many('x.project.form', 'project_id', string='Proje Formları')
    # active_form_id = fields.Many2one('x.project.form', string='Aktif Form', compute='_compute_active_form', store=True)
    # form_state = fields.Selection(related='active_form_id.state', string='Form Durumu', readonly=True)
    # form_version = fields.Integer(related='active_form_id.template_version', string='Form Versiyonu', readonly=True)
    # form_completion = fields.Float(related='active_form_id.completion_percentage', string='Tamamlanma Yüzdesi', readonly=True)
    
    # Geçici bilgi alanları
    devir_form_enabled = fields.Boolean('Devir Formu Aktif', default=False)
    devir_form_info = fields.Text('Devir Formu Bilgisi', default='Proje Devir Formu özelliği yakında aktif edilecek.')
    
    # Proje Devir Formu ilişkisi
    form_ids = fields.One2many('x.project.form', 'project_id', string='Proje Formları')
    active_form_id = fields.Many2one('x.project.form', string='Aktif Form', compute='_compute_active_form', store=True)
    form_state = fields.Selection(related='active_form_id.state', string='Form Durumu', readonly=True)
    form_version = fields.Integer(related='active_form_id.template_version', string='Form Versiyonu', readonly=True)
    form_completion = fields.Float(related='active_form_id.completion_percentage', string='Tamamlanma Yüzdesi', readonly=True)
    
    @api.depends('form_ids', 'form_ids.state')
    def _compute_active_form(self):
        for project in self:
            # En son oluşturulan formu aktif form olarak belirle
            active_form = project.form_ids.sorted(lambda x: x.create_date, reverse=True)[:1]
            project.active_form_id = active_form.id if active_form else False
    
    def action_create_form(self):
        """Yeni proje formu oluştur"""
        self.ensure_one()
        # Zaten aktif form varsa uyarı ver
        if self.active_form_id and self.active_form_id.state not in ['approved']:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'x.project.form',
                'res_id': self.active_form_id.id,
                'view_mode': 'form',
                'context': {'default_project_id': self.id},
            }
        
        # Yeni form oluştur
        form = self.env['x.project.form'].create({
            'project_id': self.id,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'x.project.form',
            'res_id': form.id,
            'view_mode': 'form',
            'context': {'default_project_id': self.id},
        }
    
    def action_view_forms(self):
        """Tüm formları görüntüle"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'x.project.form',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

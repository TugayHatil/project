# -*- coding: utf-8 -*-

from odoo import models, fields, api


class XProject(models.Model):
    _name = 'x.project'
    _description = 'Proje'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('Proje Adı', required=True, tracking=True)
    
    # Durum
    x_state = fields.Selection([
        ('draft', 'Taslak'),
        ('in_progress', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal'),
    ], string='Durum', default='draft', required=True, tracking=True)
    
    # Temel bilgiler
    x_analytic = fields.Many2one('account.analytic.account', string='Analitik Hesap', required=True, tracking=True)
    x_partner = fields.Many2one('res.partner', string='Müşteri', tracking=True)
    x_kontak = fields.Many2one('res.partner', string='Kontak', tracking=True)
    
    # Kullanıcılar
    x_sales_support = fields.Many2many('res.users', 'x_project_sales_support_rel', 'project_id', 'user_id', 
                                      string='Satış Destek', domain="[('share', '=', False), ('active', '=', True)]")
    x_sales_employe = fields.Many2many('res.users', 'x_project_sales_employe_rel', 'project_id', 'user_id',
                                      string='Satışçı', domain="[('share', '=', False), ('active', '=', True)]")
    x_project_engineer = fields.Many2many('res.users', 'x_project_engineer_rel', 'project_id', 'user_id',
                                          string='Proje Mühendisi', domain="[('share', '=', False), ('active', '=', True)]")
    
    # Tarihler
    x_date1 = fields.Date('Satış Tarihi')
    x_date2 = fields.Date('Teslim Tarihi')
    x_date3 = fields.Date('Başlangıç Tarihi')
    x_date4 = fields.Date('Bitiş Tarihi')
    
    # Diğer bilgiler
    x_web_link = fields.Char('Web Link')
    x_tag_id = fields.Many2many('x.project.tag', 'x_project_tag_rel', 'project_id', 'tag_id', string='Etiketler')
    x_proje_type = fields.Many2many('x.project.type', 'x_project_type_rel', 'project_id', 'type_id', 
                                    string='Proje Tipi')
    x_subcontractor = fields.Many2one('res.partner', string='Taşeron')
    x_tedarikci = fields.Many2many('res.partner', 'x_project_tedarikci_rel', 'project_id', 'partner_id',
                                   string='Tedarikçiler')
    
    # Dosyalar
    x_attachment = fields.Many2many('ir.attachment', 'x_project_attachment_rel', 'project_id', 'attachment_id',
                                    string='Dosyalar')
    
    # Açıklama
    x_description = fields.Html('Açıklama')
    
    # Priority
    x_priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Yüksek'),
        ('2', 'Çok Yüksek'),
        ('3', 'Acil'),
    ], string='Öncelik', default='0')
    
    def action_start(self):
        """Projeyi başlat"""
        self.write({'x_state': 'in_progress'})
    
    def action_complete(self):
        """Projeyi tamamla"""
        self.write({'x_state': 'completed'})
    
    def action_cancel(self):
        """Projeyi iptal et"""
        self.write({'x_state': 'cancelled'})
    
    def action_draft(self):
        """Projeyi taslağa al"""
        self.write({'x_state': 'draft'})


class XProjectType(models.Model):
    _name = 'x.project.type'
    _description = 'Proje Tipi'
    
    name = fields.Char('Proje Tipi', required=True)
    x_colour = fields.Integer('Renk', default=0)
    description = fields.Text('Açıklama')


class XProjectTag(models.Model):
    _name = 'x.project.tag'
    _description = 'Proje Etiketi'
    
    name = fields.Char('Etiket', required=True)
    color = fields.Integer('Renk', default=0)
    description = fields.Text('Açıklama')

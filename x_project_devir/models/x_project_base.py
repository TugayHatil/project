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
    
    # Temel bilgiler - sadece string alanlar
    x_partner_name = fields.Char('Müşteri Adı', tracking=True)
    x_kontak_name = fields.Char('Kontak Adı', tracking=True)
    
    # Kullanıcılar - sadece string alanlar
    x_sales_support_names = fields.Char('Satış Destek')
    x_sales_employe_names = fields.Char('Satışçı')
    x_project_engineer_names = fields.Char('Proje Mühendisi')
    
    # Tarihler
    x_date1 = fields.Date('Satış Tarihi')
    x_date2 = fields.Date('Teslim Tarihi')
    x_date3 = fields.Date('Başlangıç Tarihi')
    x_date4 = fields.Date('Bitiş Tarihi')
    
    # Diğer bilgiler
    x_web_link = fields.Char('Web Link')
    x_tag_names = fields.Char('Etiketler')
    x_proje_type_name = fields.Char('Proje Tipi')
    x_subcontractor_name = fields.Char('Taşeron')
    x_tedarikci_names = fields.Char('Tedarikçiler')
    
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

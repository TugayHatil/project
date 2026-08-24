# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class XProjectForm(models.Model):
    _name = 'x.project.form'
    _description = 'Proje Formu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('Form Adı', compute='_compute_name', store=True)
    project_id = fields.Many2one('x.project', string='Proje', required=True, ondelete='cascade')
    template_id = fields.Many2one('x.project.form.template', string='Form Şablonu', required=True, ondelete='restrict')
    template_version = fields.Integer('Şablon Versiyonu', related='template_id.version', store=True, readonly=True)
    
    # Form durumu
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('in_progress', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
        ('approved', 'Onaylandı'),
    ], string='Durum', default='draft', tracking=True)
    
    # İlerleme
    completion_percentage = fields.Float('Tamamlanma Yüzdesi', compute='_compute_completion_percentage', store=True)
    total_questions = fields.Integer('Toplam Soru', compute='_compute_completion_percentage', store=True)
    answered_questions = fields.Integer('Cevaplanan Soru', compute='_compute_completion_percentage', store=True)
    missing_required_questions = fields.Text('Eksik Zorunlu Sorular', compute='_compute_missing_required')
    
    # Form bilgileri
    filled_by = fields.Many2one('res.users', string='Formu Dolduran', default=lambda self: self.env.user)
    filled_date = fields.Datetime('Doldurma Tarihi', default=fields.Datetime.now)
    completed_date = fields.Datetime('Tamamlanma Tarihi')
    approved_date = fields.Datetime('Onay Tarihi')
    approved_by = fields.Many2one('res.users', string='Onaylayan')
    
    # Cevaplar
    answer_ids = fields.One2many('x.project.form.answer', 'form_id', string='Cevaplar')
    
    # Dosyalar
    attachment_ids = fields.Many2many('ir.attachment', string='Ekli Dosyalar')
    
    @api.depends('project_id', 'template_id')
    def _compute_name(self):
        for form in self:
            if form.project_id and form.template_id:
                form.name = f"{form.project_id.name or 'Proje'} - {form.template_id.name} v{form.template_id.version}"
            else:
                form.name = 'Yeni Form'
    
    @api.depends('answer_ids', 'template_id')
    def _compute_completion_percentage(self):
        for form in self:
            if not form.template_id:
                form.completion_percentage = 0
                form.total_questions = 0
                form.answered_questions = 0
                continue
            
            # Tüm soruları al
            all_questions = form.template_id.mapped('section_ids.question_ids')
            form.total_questions = len(all_questions)
            
            # Cevaplanan soruları say
            answered_questions = form.answer_ids.filtered(lambda a: a.value_text or a.value_boolean or a.value_date or a.value_integer or a.value_float or a.value_user_id or a.value_partner_id or a.value_selection or a.attachment_ids)
            form.answered_questions = len(answered_questions)
            
            # Yüzde hesapla
            if form.total_questions > 0:
                form.completion_percentage = (form.answered_questions / form.total_questions) * 100
            else:
                form.completion_percentage = 0
    
    def _compute_missing_required(self):
        for form in self:
            if not form.template_id:
                form.missing_required_questions = ''
                continue
            
            # Zorunlu soruları bul
            required_questions = form.template_id.mapped('section_ids.question_ids').filtered(lambda q: q.required)
            
            # Cevaplanmamış zorunlu soruları bul
            answered_question_ids = form.answer_ids.mapped('question_id.id')
            missing_questions = required_questions.filtered(lambda q: q.id not in answered_question_ids)
            
            if missing_questions:
                form.missing_required_questions = ', '.join(missing_questions.mapped('name'))
            else:
                form.missing_required_questions = ''
    
    def action_start(self):
        """Formu başlat"""
        self.write({'state': 'in_progress'})
        # Şablondan soruları oluştur
        self._generate_answers()
    
    def _generate_answers(self):
        """Şablondan cevap kayıtlarını oluşturur"""
        self.ensure_one()
        # Mevcut cevapları sil
        self.answer_ids.unlink()
        
        # Şablondan soruları al ve cevap kayıtları oluştur
        for section in self.template_id.section_ids:
            for question in section.question_ids:
                self.env['x.project.form.answer'].create({
                    'form_id': self.id,
                    'question_id': question.id,
                })
    
    def action_complete(self):
        """Formu tamamla"""
        missing_required = self.missing_required_questions
        if missing_required:
            raise ValidationError(_('Formu tamamlamak için eksik zorunlu soruları doldurmalısınız: %s') % missing_required)
        
        self.write({
            'state': 'completed',
            'completed_date': fields.Datetime.now(),
        })
    
    def action_approve(self):
        """Formu onayla"""
        self.write({
            'state': 'approved',
            'approved_date': fields.Datetime.now(),
            'approved_by': self.env.user,
        })
    
    def action_draft(self):
        """Formu taslağa al"""
        self.write({'state': 'draft'})
    
    def action_edit_form(self):
        """Formu düzenle"""
        self.write({'state': 'in_progress'})
    
    def action_print_pdf(self):
        """PDF oluştur"""
        return self.env.ref('x_project_devir.action_report_x_project_form').report_action(self)
    
    @api.model
    def create(self, vals):
        # Yeni form oluşturulduğunda aktif şablonun son versiyonunu kullan
        if not vals.get('template_id'):
            latest_template = self.env['x.project.form.template'].get_latest_active_template()
            if latest_template:
                vals['template_id'] = latest_template.id
        
        return super(XProjectForm, self).create(vals)

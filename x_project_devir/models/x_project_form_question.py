# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class XProjectFormQuestion(models.Model):
    _name = 'x.project.form.question'
    _description = 'Proje Form Sorusu'
    _order = 'section_id, sequence, id'
    
    name = fields.Char('Soru', required=True, translate=True)
    sequence = fields.Integer('Sıra', default=10)
    section_id = fields.Many2one('x.project.form.section', string='Bölüm', required=True, ondelete='cascade')
    
    # Cevap tipi seçenekleri
    answer_type = fields.Selection([
        ('text', 'Metin'),
        ('long_text', 'Uzun Metin'),
        ('date', 'Tarih'),
        ('datetime', 'Tarih Saat'),
        ('integer', 'Tam Sayı'),
        ('float', 'Ondalıklı Sayı'),
        ('percentage', 'Yüzde'),
        ('boolean', 'Evet/Hayır'),
        ('many2one_user', 'Kullanıcı'),
        ('many2many_user', 'Kullanıcılar (Çoklu)'),
        ('partner', 'Partner'),
        ('selection', 'Seçim'),
        ('multi_selection', 'Çoklu Seçim'),
        ('attachment', 'Dosya Eki'),
    ], string='Cevap Tipi', required=True, default='text')
    
    required = fields.Boolean('Zorunlu', default=False)
    active = fields.Boolean('Aktif', default=True)
    description = fields.Text('Açıklama/Açıklama')
    
    # Koşullu soru ayarları
    condition_question_id = fields.Many2one('x.project.form.question', string='Koşul Sorusu',
                                            help='Bu sorunun görünürlüğü bu sorunun cevabına bağlıdır')
    condition_value = fields.Char('Koşul Değeri', 
                                   help='Koşul sorusunun hangi değeri olduğunda bu soru görünecek')
    
    # Seçim değerleri
    selection_options = fields.Text('Seçenekler', 
                                   help='Her satır bir seçenek: Değer|Etiket formatında')
    
    # İstatistik
    answer_count = fields.Integer('Cevap Sayısı', compute='_compute_answer_count')
    
    @api.depends('section_id.template_id')
    def _compute_answer_count(self):
        for question in self:
            question.answer_count = self.env['x.project.form.answer'].search_count([
                ('question_id', '=', question.id)
            ])
    
    @api.constrains('condition_question_id')
    def _check_condition_question(self):
        for question in self:
            if question.condition_question_id:
                if question.condition_question_id.id == question.id:
                    raise ValidationError(_('Bir soru kendisine koşul olamaz!'))
                if question.condition_question_id.section_id.template_id != question.section_id.template_id:
                    raise ValidationError(_('Koşul sorusu aynı şablonda olmalıdır!'))
    
    def get_selection_options(self):
        """Seçenekleri dictionary olarak döndürür"""
        self.ensure_one()
        if not self.selection_options:
            return {}
        options = {}
        for line in self.selection_options.split('\n'):
            if '|' in line:
                value, label = line.split('|', 1)
                options[value.strip()] = label.strip()
        return options
    
    def check_visibility(self, answers_dict):
        """Sorunun görünürlüğünü kontrol eder"""
        self.ensure_one()
        if not self.condition_question_id:
            return True
        
        # Koşul sorusunun cevabını kontrol et
        condition_answer = answers_dict.get(self.condition_question_id.id)
        if condition_answer is None:
            return False
        
        # Koşul değerini kontrol et
        if self.condition_value:
            return str(condition_answer) == str(self.condition_value)
        
        return bool(condition_answer)

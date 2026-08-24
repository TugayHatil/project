# -*- coding: utf-8 -*-

from odoo import models, fields, api


class XProjectFormAnswer(models.Model):
    _name = 'x.project.form.answer'
    _description = 'Proje Form Cevabı'
    _order = 'question_id.sequence, id'
    
    form_id = fields.Many2one('x.project.form', string='Form', required=True, ondelete='cascade')
    question_id = fields.Many2one('x.project.form.question', string='Soru', required=True, ondelete='restrict')
    
    # Farklı veri tipleri için alanlar
    value_text = fields.Char('Metin Değeri')
    value_long_text = fields.Text('Uzun Metin Değeri')
    value_date = fields.Date('Tarih Değeri')
    value_datetime = fields.Datetime('Tarih Saat Değeri')
    value_integer = fields.Integer('Tam Sayı Değeri')
    value_float = fields.Float('Ondalıklı Sayı Değeri')
    value_percentage = fields.Float('Yüzde Değeri')
    value_boolean = fields.Boolean('Boolean Değeri')
    value_user_id = fields.Many2one('res.users', string='Kullanıcı Değeri')
    value_user_ids = fields.Many2many('res.users', string='Kullanıcılar Değeri')
    value_partner_id = fields.Many2one('res.partner', string='Partner Değeri')
    value_selection = fields.Char('Seçim Değeri')
    value_multi_selection = fields.Char('Çoklu Seçim Değeri')
    
    # Dosya eki
    attachment_ids = fields.Many2many('ir.attachment', string='Dosya Ekleri')
    
    # Görünürlük kontrolü
    is_visible = fields.Boolean('Görünür', compute='_compute_is_visible', store=True)
    
    @api.depends('form_id.answer_ids', 'question_id.condition_question_id')
    def _compute_is_visible(self):
        for answer in self:
            # Mevcut tüm cevapları dictionary olarak al
            answers_dict = {}
            if answer.form_id:
                for ans in answer.form_id.answer_ids:
                    value = ans._get_computed_value()
                    if value is not None:
                        answers_dict[ans.question_id.id] = value
            
            answer.is_visible = answer.question_id.check_visibility(answers_dict)
    
    def _get_computed_value(self):
        """Sorunun tipine göre doğru değeri döndürür"""
        self.ensure_one()
        question = self.question_id
        
        if question.answer_type == 'text':
            return self.value_text
        elif question.answer_type == 'long_text':
            return self.value_long_text
        elif question.answer_type == 'date':
            return self.value_date
        elif question.answer_type == 'datetime':
            return self.value_datetime
        elif question.answer_type == 'integer':
            return self.value_integer
        elif question.answer_type == 'float':
            return self.value_float
        elif question.answer_type == 'percentage':
            return self.value_percentage
        elif question.answer_type == 'boolean':
            return self.value_boolean
        elif question.answer_type == 'many2one_user':
            return self.value_user_id.id if self.value_user_id else None
        elif question.answer_type == 'many2many_user':
            return self.value_user_ids.ids if self.value_user_ids else []
        elif question.answer_type == 'partner':
            return self.value_partner_id.id if self.value_partner_id else None
        elif question.answer_type == 'selection':
            return self.value_selection
        elif question.answer_type == 'multi_selection':
            return self.value_multi_selection
        elif question.answer_type == 'attachment':
            return self.attachment_ids.ids if self.attachment_ids else []
        
        return None
    
    def get_display_value(self):
        """Görüntüleme için formatlanmış değer döndürür"""
        self.ensure_one()
        question = self.question_id
        
        if question.answer_type == 'text':
            return self.value_text
        elif question.answer_type == 'long_text':
            return self.value_long_text
        elif question.answer_type == 'date':
            return fields.Date.to_string(self.value_date) if self.value_date else ''
        elif question.answer_type == 'datetime':
            return fields.Datetime.to_string(self.value_datetime) if self.value_datetime else ''
        elif question.answer_type == 'integer':
            return str(self.value_integer) if self.value_integer else ''
        elif question.answer_type == 'float':
            return str(self.value_float) if self.value_float else ''
        elif question.answer_type == 'percentage':
            return f"{self.value_percentage}%" if self.value_percentage else ''
        elif question.answer_type == 'boolean':
            return _('Evet') if self.value_boolean else _('Hayır')
        elif question.answer_type == 'many2one_user':
            return self.value_user_id.name if self.value_user_id else ''
        elif question.answer_type == 'many2many_user':
            return ', '.join(self.value_user_ids.mapped('name'))
        elif question.answer_type == 'partner':
            return self.value_partner_id.name if self.value_partner_id else ''
        elif question.answer_type == 'selection':
            options = question.get_selection_options()
            return options.get(self.value_selection, self.value_selection)
        elif question.answer_type == 'multi_selection':
            if self.value_multi_selection:
                options = question.get_selection_options()
                selected_values = self.value_multi_selection.split(',')
                return ', '.join([options.get(v.strip(), v.strip()) for v in selected_values])
            return ''
        elif question.answer_type == 'attachment':
            return ', '.join(self.attachment_ids.mapped('name'))
        
        return ''

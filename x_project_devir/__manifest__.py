# -*- coding: utf-8 -*-
{
    'name': 'Proje Devir Formu',
    'version': '16.0.1.0.0',
    'category': 'Project',
    'summary': 'Dinamik proje devir/başlangıç formu sistemi',
    'description': """
        Proje Devir Formu Modülü
        ========================
        
        Bu modül x_project modeli üzerine dinamik proje devir/başlangıç formu sistemi ekler.
        
        Özellikler:
        - Dinamik soru yönetimi
        - Koşullu sorular
        - Form versiyonlama
        - Dosya yönetimi
        - PDF çıktısı
        - Tamamlanma yüzdesi hesaplama
    """,
    'author': 'Elva Mühendislik',
    'website': 'https://www.elva.com.tr',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/x_project_devir_menu.xml',
        'views/x_project_base_views.xml',
        'views/x_project_tag_views.xml',
        'views/x_project_form_template_views.xml',
        'views/x_project_form_section_views.xml',
        'views/x_project_form_question_views.xml',
        'views/x_project_form_views.xml',
        'views/x_project_form_answer_views.xml',
        'views/x_project_views.xml',
        'views/x_project_form_report_views.xml',
        'report/x_project_form_report_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'x_project_devir/static/src/css/x_project_devir.css',
            'x_project_devir/static/src/js/x_project_devir.js',
        ],
    },
    'installable': True,
    'application': True,
}

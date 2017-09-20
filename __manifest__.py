# -*- coding: utf-8 -*-
{
    'name': "Library Book",
    'summary': "Esta é uma descrição simples do novo módulo que estou desenvolvendo",
    'description': """Este campo deve ser usado para fornecer uma descrição mais completa
                      sobre o módulo o qual estou desenvolvendo""",
    'author': "MeuNomeCompleto",
    'license': "AGPL-3",
    'website': "http://www.meuwebsite.com.br",
    'category': 'Uncategorized',
    'version': '10.0.1.0.0',
    'depends': [
        'base',
        'decimal_precision',
        'mail',
    ],
    'data': [
        'views/decimal_precision.xml',
        'views/library_views.xml',
        'views/library_menus.xml',
        'views/library_book_views.xml',
        'views/library_book_menus.xml',
        'views/res_partner_views.xml',
        'views/res_partner_menus.xml',
        'views/library_book_publicacao.xml',
        'wizard/library_book_publicacao_wizard.xml',
        'security/library_book_security.xml',
        'security/ir.model.access.csv',
    ],
    #'demo': ['demo.xml'],
}
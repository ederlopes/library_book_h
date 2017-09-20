# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from odoo import api, models, fields


class LibraryBookPublicacao(models.Model):

    _name = b'library.book.publicacao'

    name = fields.Char(
        string='Nome',
        compute='_compute_name'
    )

    data_publicacao = fields.Datetime(
        string=u'Data Publicação',
    )

    diretor = fields.Many2one(
        comodel_name='res.users',
        string='Diretor Autoritario',
        required=True,
        default=lambda self: self.env.user,
    )

    livros_id = fields.Many2one(
        comodel_name='library.book',
        required=True,
        string='Livros',
    )

    def _compute_name(self):
        for record in self:
            if record.data_publicacao and record.livros_id:
                record.name = record.livros_id.name + \
                              ' - ' + record.data_publicacao

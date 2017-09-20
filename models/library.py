# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from odoo import models, fields


class Biblioteca(models.Model):

    _name = b'library'

    name = fields.Char(
        string='Nome',
    )

    diretor = fields.Many2one(
        comodel_name='res.users',
        string='Diretor Autoritario',
        required=True,
    )

    livros_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='biblioteca_id',
        string='Livros',
    )

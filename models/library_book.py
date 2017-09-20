# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from datetime import timedelta

from odoo import api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class Livros(models.Model):

    _name = b'library.book'
    _description = 'Livros'
    _inherit = ['mail.thread']
    _order = 'date_release desc, name'
    # _rec_name = 'endereco'

    # _sql_constraints = [
    #     ('name_uniq', 'UNIQUE (endereco)',
    #      'Book title must be unique.')
    # ]

    name = fields.Char(string='Nome')

    active = fields.Boolean('Active', default=True)

    age_days = fields.Float(
        string='Dias até final Exposição',
        compute='_compute_age',
        inverse='_inverse_age',
        store=True,
        compute_sudo=False,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Autor',
        required=True,
        default=lambda self: self.env.user,
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Empresa',
        default=lambda self: self.env.user.company_id,
    )

    partner_ids = fields.Many2many(
        string='Editor',
        required=True,
        comodel_name='res.partner',
    )

    biblioteca_id = fields.Many2one(
        string='Biblioteca',
        comodel_name='library',
    )

    data_lancamento = fields.Datetime(
        string=u'Data Lançamento',
    )

    date_release = fields.Date(
        string='Data Final Exposição',
    )

    state = fields.Selection([
        ('novo', 'Novo'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('publicado', 'Publicado'),
        ('cancelado', 'cancelado')],
        string='State',
        default='novo',
    )

    # create_uid = fields.Many2one(
    #     comodel_name='res.users',
    #     string=u'Creation User',
    #     compute='_compute_create_uid',
    #     store=True,
    #     required=False
    # )
    #
    # @api.depends('titulo')
    # def _compute_create_uid(self):
    #     for record in self:
    #         if not record.create_uid:
    #             record.create_uid = self.env.user.id


    # telefone = fields.Char(
    #     string='Telfone',
    #     related=partner_id.phone,
    #     store=True,
    # )

    currency_id = fields.Many2one('res.currency', string='Moeda')

    cost_price = fields.Float(
        precision=dp.get_precision('Book Price'),
        string='Book Cost',
    )

    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='library_book_attachment_rel',
        column1='library_book_id',
        column2='attachment_id',
        string=u'Attachments',
    )

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.from_string(fields.Date.today())
        for book in self.filtered('date_release'):
            delta = fields.Date.from_string(book.date_release) - today
            book.age_days = delta.days

    @api.multi
    def _inverse_age(self):
        today = fields.Datetime.from_string(fields.Datetime.now())
        for book in self.filtered('date_release'):
            d = today + timedelta(days=book.age_days)
            book.date_release = fields.Date.to_string(d)

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise ValidationError(
                    'Release date must be in the past')

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('novo', 'confirmado'),
            ('confirmado', 'enviado'),
            ('confirmado', 'publicado'),
            ('enviado', 'cancelado'),
        ]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                # raise UserError("Transição de estados não permitida!")
                continue

    def action_available(self):
        for record in self:
            record.change_state('confirmado')

    def action_lost(self):
        for record in self:
            record.change_state('lost')

    def action_publicar(self):
        for record in self:
            record.change_state('publicado')

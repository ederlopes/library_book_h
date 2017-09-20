# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from odoo import api, models, fields


class ResPartner(models.Model):

    _name = b'res.partner'
    _inherit = b'res.partner'

    is_editor = fields.Boolean(
        string='Eh editor?'
    )

    is_depends = fields.Boolean(
        string='Eh Depends?',
        compute='_compute_is_depends',
    )

    is_onchange = fields.Boolean(
        string='Eh Onchange?',
    )

    @api.multi
    def open_commercial_entity(self):
        print ('=================================== Chamou a funcao')

    @api.onchange('is_onchange')
    def _onchange_is_onchange(self):
        print ('=================================== Chamou on change')

    @api.depends('is_editor')
    def _compute_is_depends(self):
        for record in self:
            record.is_depends = not record.is_editor
        print('=================================== Chamou depends')

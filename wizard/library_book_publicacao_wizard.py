# -*- coding: utf-8 -*-

# from __future__ import division, print_function, unicode_literals

from odoo import api, models, fields


class Publicacao(models.TransientModel):

    _name = 'library.book.publicacao.wizard'

    data_publicacao = fields.Datetime(
        string=u'Data Publicação',
    )

    diretor = fields.Many2one(
        comodel_name='res.users',
        string='Diretor Autoritario',
        required=True,
        default=lambda self: self.env.user,
    )

    livros_ids = fields.Many2many(
        comodel_name='library.book',
        string='Livros',
        domain="[('state', '!=', 'publicado')]",
    )

    @api.multi
    def publicar_livros(self):
        publicacoes = []
        for record in self:
            for livro in record.livros_ids:
                # Criar um dict para gerar nova publicacao
                publicacao = {
                    'data_publicacao': record.data_publicacao,
                    'diretor': record.diretor.id,
                    'livros_id': livro.id,
                }

                # Cria uma instancia da publicacao
                publicacoes.append(self.env['library.book.publicacao'].create(publicacao).id)

                # Seta o estado do livro como publicado
                livro.state = 'publicado'

                # return {'type': 'ir.actions.act_window_close'}

                action = {
                    'type': 'ir.action.act_window',
                    'name': 'Publicações',
                    'res_model': 'library.book.publicacao',
                    'domain': [(b'id', b'in', [1, 2]) ],
                    'view_mode': 'form,tree',
                }

                print (action)
                return action

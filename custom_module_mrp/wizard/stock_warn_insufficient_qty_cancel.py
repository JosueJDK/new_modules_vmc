# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockWarnInsufficientQtyCancelUnbuild(models.TransientModel):
    _name = 'stock.warn.insufficient.qty.cancel.unbuild'
    _inherit = 'stock.warn.insufficient.qty'
    _description = 'Cantidad Insuficiente de Descontruidos'

    cancel_unbuild_id = fields.Many2one('mrp.cancel.unbuild', 'Cancelar Descontruccion')

    def _get_reference_document_company_id(self):
        return self.cancel_unbuild_id.company_id

    def action_done(self):
        self.ensure_one()
        return self.cancel_unbuild_id.action_unbuild()

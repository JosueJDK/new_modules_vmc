# -*- coding: utf-8 -*-

from . import controllers
from . import models


def _create_warehouse_data(cr):
    self.env['ir.sequence'].create({
                'name': 'Cancel Unbuild',
                'code': 'mrp.cancel.unbuild',
                'company_id': self.company_id.id,
                'prefix': 'CUB/',
                'padding': 5,
                'number_next': 1,
                'number_increment': 1
            })
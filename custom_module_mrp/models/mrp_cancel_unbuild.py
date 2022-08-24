# -- coding: utf-8 --
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import float_compare, float_round, float_is_zero

class CancelMrpUnbuild(models.Model):
    _name = 'mrp.cancel.unbuild'
    _description = 'Cancelar orden de desconstruccion'
    _order = 'id desc'
    

    # Nombre de la referencia
    name = fields.Char('Referencia', copy=False, readonly=True, default=lambda x: _('New'))

    # Id del producto fabricado
    product_id = fields.Many2one(
        'product.product', 'Producto', check_company=True,
        domain="[('bom_ids', '!=', False), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=True, states={'done': [('readonly', True)]})
    
    # Cantidad de productos producidos
    product_qty = fields.Float(
        'Cantidad', default=1.0,
        required=True, states={'done':[('readonly', True)]})
    # Unidad de medida
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unidad de Medida',
        required=True, states={'done': [('readonly', True)]})
    # Lista de materiales del producto producido
    bom_id = fields.Many2one(
        'mrp.bom', 'Lista de Materiales',
        domain="""[
        '|',
            ('product_id', '=', product_id),
            '&',
                ('product_tmpl_id.product_variant_ids', '=', product_id),
                ('product_id','=',False),
        ('type', '=', 'normal'),
        '|',
            ('company_id', '=', company_id),
            ('company_id', '=', False)
        ]""",
        required=True, states={'done': [('readonly', True)]}, check_company=True)

    # Id de la compania
    company_id = fields.Many2one(
        'res.company', 'Compania',
        default=lambda s: s.env.company,
        required=True, index=True, states={'done': [('readonly', True)]})

    # Id de la orden de desconstruccion que tengas state 'done'
    uo_id = fields.Many2one(
        'mrp.unbuild', 'Orden de Desconstruccion',
        domain="[('state', 'in', ['done', 'cancel']), ('company_id', '=', company_id)]",
        states={'done': [('readonly', True)]}, check_company=True)
    
    has_tracking=fields.Selection(related='product_id.tracking', readonly=True)

    # Estado de anulacion de la orden de desconstruccion
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')], string='Status', default='draft', index=True)
    
    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)


    # Mostrar los productos relacionados con esa orden de desconstruccion
    @api.onchange('uo_id')
    def _onchange_uo_id(self):
        if self.uo_id:
            self.product_id = self.uo_id.product_id.id
            self.product_qty = self.uo_id.product_qty
            self.product_uom_id = self.uo_id.product_uom_id
            self.bom_id = self.uo_id.bom_id
    
    # Mostrar la lista de materiales correspondientes al producto seleccionado
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.bom_id = self.env['mrp.bom']._bom_find(product=self.product_id, company_id=self.company_id.id)
            self.product_uom_id = self.uo_id.product_id == self.product_id and self.uo_id.product_uom_id.id or self.product_id.uom_id.id
                
    @api.constrains('product_qty')
    def _check_qty(self):
        if self.product_qty <= 0:
            raise ValueError(_('Unbuild Order product quantity has to be strictly positive.'))

    @api.model
    def create(self, vals):
        self.create_sequence_cancel_unbuild()
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.cancel.unbuild') or _('New')
        print("Atributo vals",vals)
        return super(CancelMrpUnbuild, self).create(vals)
    
    # Evitar la eliminacion de un (Cancel Unbuild) en estado 'DONE'
    def unlink(self):
        if 'done' in self.mapped('state'):
            raise UserError(_("You cannot delete an unbuild order if the state is 'Done'."))
        return super(CancelMrpUnbuild, self).unlink()

    def create_sequence_cancel_unbuild(self):
        exist_cub =  self.env['ir.sequence'].search([('prefix','=','CUB/')])
        if len(exist_cub) == 0:
            self.env['ir.sequence'].create({
                'name': 'Cancel Unbuild',
                'code': 'mrp.cancel.unbuild',
                'company_id': self.company_id.id,
                'prefix': 'CUB/',
                'padding': 5,
                'number_next': 1,
                'number_increment': 1
            })

    def action_cancel_unbuild(self):
        id_cub = self.env['stock.move'].search([('name','=ilike','CUB/%')])
        list_ids = []
        for id_ in id_cub:
            list_ids.append(id_.unbuild_id.id)
        if self.uo_id.id in list_ids:
            self.write({'state': 'draft'})
            raise UserError(_("No puedes cancelar la misma orden de desconstruccion dos o mas veces!.")) 
        else:
            datas =  self.env['stock.move'].search([('name','=',self.uo_id.name)])
            for data in datas:
                self.env['stock.move'].create({
                    'name': self.name,
                    'date': self.create_date,
                    'product_id': data.product_id.id,
                    'product_uom_qty': data.product_uom_qty,
                    'product_uom': data.product_uom.id,
                    'procure_method': 'make_to_stock',
                    'location_dest_id': data.location_id.id,
                    'location_id': data.location_dest_id.id,
                    'warehouse_id': data.warehouse_id.id,
                    'unbuild_id': self.uo_id.id,
                    'cancel_unbuild_id' : self.id,
                    'company_id': self.company_id.id,
                    'state':'done'
                })

            moves =  self.env['stock.move'].search([('name','=',self.name)])
            for move in moves:
                self.env['stock.move.line'].create({
                    'move_id': move.id,
                    'qty_done': move.product_uom_qty,
                    'product_id': move.product_id.id,
                    'product_uom_id': move.product_uom.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'state':'done'
                })
            return self.write({'state': 'done'})


    # Validacion de la nueva orden 
    def action_validate(self):
        unbuild_qty = self.env['mrp.unbuild'].search([('name','=',self.uo_id.name)])
        if(int(self.product_qty) <= int(unbuild_qty.product_qty)):
            self.create_sequence_cancel_unbuild()
            return self.action_cancel_unbuild()
        else:
            return {
                'name': _('Insufficient Quantity'),
                'view_mode': 'form',
                'res_model': 'stock.warn.insufficient.qty.cancel.unbuild',
                'view_id': self.env.ref('custom_module_mrp.stock_warn_insufficient_qty_unbuild_form_view').id,
                'type': 'ir.actions.act_window',
                'target': 'new'}
            

class StockMove(models.Model):
    _inherit = 'stock.move'

    cancel_unbuild_id = fields.Many2one(
        'mrp.cancel.unbuild', 'Disassembly Order', check_company=True)
    cancel_consume_unbuild_id = fields.Many2one(
        'mrp.cancel.unbuild', 'Consumed Disassembly Order', check_company=True)
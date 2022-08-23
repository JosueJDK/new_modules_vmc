# -*- coding: utf-8 -*-
# from odoo import http


# class custom_module_mrp(http.Controller):
#     @http.route('/custom_module_mrp/custom_module_mrp/', auth='public')
#     def index(self, **kw):
#         return Hello, world

#     @http.route('/custom_module_mrp/custom_module_mrp/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_module_mrp.listing', {
#             'root': '/custom_module_mrp/custom_module_mrp/',
#             'objects': http.request.env['custom_module_mrp.custom_module_mrp'].search([]),
#         })

#     @http.route('/custom_module_mrp/custom_module_mrp/objects/<model(custom_module_mrp.custom_module_mrp):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_module_mrp.object', {
#             'object': obj
#         })


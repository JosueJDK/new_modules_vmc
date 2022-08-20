# -*- coding: utf-8 -*-
# from odoo import http


# class CustomWebsiteVmc(http.Controller):
#     @http.route('/custom_website_vmc/custom_website_vmc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_website_vmc/custom_website_vmc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_website_vmc.listing', {
#             'root': '/custom_website_vmc/custom_website_vmc',
#             'objects': http.request.env['custom_website_vmc.custom_website_vmc'].search([]),
#         })

#     @http.route('/custom_website_vmc/custom_website_vmc/objects/<model("custom_website_vmc.custom_website_vmc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_website_vmc.object', {
#             'object': obj
#         })

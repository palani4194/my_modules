# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteHideProductPrice(http.Controller):
#     @http.route('/website_hide_product_price/website_hide_product_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_hide_product_price/website_hide_product_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_hide_product_price.listing', {
#             'root': '/website_hide_product_price/website_hide_product_price',
#             'objects': http.request.env['website_hide_product_price.website_hide_product_price'].search([]),
#         })

#     @http.route('/website_hide_product_price/website_hide_product_price/objects/<model("website_hide_product_price.website_hide_product_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_hide_product_price.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteDeliveryTracking(http.Controller):
#     @http.route('/website_delivery_tracking/website_delivery_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_delivery_tracking/website_delivery_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_delivery_tracking.listing', {
#             'root': '/website_delivery_tracking/website_delivery_tracking',
#             'objects': http.request.env['website_delivery_tracking.website_delivery_tracking'].search([]),
#         })

#     @http.route('/website_delivery_tracking/website_delivery_tracking/objects/<model("website_delivery_tracking.website_delivery_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_delivery_tracking.object', {
#             'object': obj
#         })
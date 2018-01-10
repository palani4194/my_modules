# -*- coding: utf-8 -*-

import base64
from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import consteq
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class CustomerPortal(CustomerPortal):


# tree view method for delivery order
    @http.route(['/my/delieveryorders/', '/my/delieveryorders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_delivery_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        search_str = kw.get('delivery_search') or False
        

        values = self._prepare_portal_layout_values()
        domain = [('origin', 'like', 'SO0%')]
        delivery_orders = request.env["stock.picking"]

        searchbar_sortings = {
            'name': {'label': _('DO name'), 'order': 'name asc'},
            'date': {'label': _('Delivery date'), 'order': 'scheduled_date'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('stock.picking', domain)

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        do_count = delivery_orders.search_count(domain)



        pager = portal_pager(
            url="/my/delieveryorders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=do_count,
            page=page,
            step=self._items_per_page
        )
        if search_str:
            search_str = "%" + search_str + "%"
            domain += ['|',('origin', '=ilike', search_str),('name', '=ilike', search_str)]
            
        do_orders = delivery_orders.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_orders_history'] = do_orders.ids[:100]

        values.update({
            'date': date_begin,
            'orders': do_orders.sudo(),
            'page_name': 'DeliveryOrder',
            'pager': pager,
            'attrib_values': [],
            'archive_groups': archive_groups,
            'default_url': '/my/delieveryorders',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("website_delivery_tracking.portal_delivery_orders", values)


# tree view record count for delivery order
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        DeliveryOrder = request.env['stock.picking']
        do_count = DeliveryOrder.search_count([('origin', 'like', 'SO0%')])

        values.update({
            'DeliveryOrder': do_count,
        })
        return values



# form view open for delivery order

    @http.route(['/my/delieveryorders/<int:order>'], type='http', auth="public", website=True)
    def portal_delivery_page(self, order=None, access_token=None, **kw):
    
        try:
            order_sudo = self._order_check_access_do(order, access_token=access_token)
        except AccessError:
            return request.redirect('/my')

        values = self._order_get_page_view_values_do(order_sudo, access_token, **kw)
        return request.render("website_delivery_tracking.portal_delivery_page", values)


    def _order_get_page_view_values_do(self, order, access_token, **kwargs):
        order_invoice_lines = {il.product_id.id for il in order.move_lines.mapped('move_line_ids')}

        values = {
            'order': order,
            'order_invoice_lines': order_invoice_lines,
        }

        history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, order))

        return values


    def _order_check_access_do(self, order, access_token=None):
        order = request.env['stock.picking'].browse([order])
        order_sudo = order.sudo()
        try:
            order.check_access_rights('read')
            order.check_access_rule('read')
        except AccessError:
            if not access_token or not consteq(order_sudo.access_token, access_token):
                raise
        return order_sudo

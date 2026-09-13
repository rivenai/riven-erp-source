from riven_erp import _, http
from riven_erp.exceptions import AccessError, ValidationError
from riven_erp.http import request


class PesPortalController(http.Controller):

    # --------------------------------------------------
    # Support Tickets
    # --------------------------------------------------
    @http.route(['/my/support', '/my/support/page/<int:page>'], type='http',
                auth='user', website=True)
    def portal_my_support(self, page=1, **kw):
        partner = request.env.user.partner_id
        Ticket = request.env['pes.support.ticket'].sudo()
        # Portal users see their own company's tickets (partner + commercial partner)
        domain = ['|', ('partner_id', '=', partner.id),
                  ('partner_id', '=', partner.commercial_partner_id.id)]
        tickets = Ticket.search(domain, order='create_date desc, id desc')
        values = {
            'tickets': tickets,
            'page_name': 'support',
        }
        return request.render('riven_pes_portal.portal_my_support', values)

    @http.route('/my/support/new', type='http', auth='user', website=True)
    def portal_support_new(self, **kw):
        orders = request.env['sale.order'].sudo().search([
            ('partner_id', 'child_of', request.env.user.partner_id.commercial_partner_id.id),
            ('state', 'in', ['sale', 'done']),
        ], order='date_order desc', limit=20)
        values = {
            'orders': orders,
            'page_name': 'support',
        }
        return request.render('riven_pes_portal.portal_support_new', values)

    @http.route('/my/support/submit', type='http', auth='user', website=True)
    def portal_support_submit(self, **post):
        if not post.get('subject'):
            return request.redirect('/my/support/new')
        partner = request.env.user.partner_id
        Ticket = request.env['pes.support.ticket'].sudo()
        vals = {
            'partner_id': partner.commercial_partner_id.id or partner.id,
            'subject': post.get('subject'),
            'category': post.get('category', 'other'),
            'priority': post.get('priority', '1'),
            'description': post.get('description') or '',
        }
        if post.get('sale_order_id'):
            vals['sale_order_id'] = int(post['sale_order_id'])
        ticket = Ticket.create(vals)
        # Log portal activity
        request.env['pes.portal.activity'].sudo().create({
            'activity_type': 'support_ticket',
            'description': 'Support ticket submitted: %s' % ticket.name,
            'sale_order_id': ticket.sale_order_id.id,
            'page_url': '/my/support/submit',
        })
        return request.redirect('/my/support/%s' % ticket.id)

    @http.route('/my/support/<int:ticket_id>', type='http', auth='user', website=True)
    def portal_support_detail(self, ticket_id, **kw):
        ticket = request.env['pes.support.ticket'].sudo().browse(ticket_id)
        if not ticket.exists():
            return request.redirect('/my/support')
        partner = request.env.user.partner_id
        if ticket.partner_id.id not in (partner.id, partner.commercial_partner_id.id):
            raise AccessError(_('You do not have access to this ticket.'))
        values = {
            'ticket': ticket,
            'page_name': 'support',
        }
        return request.render('riven_pes_portal.portal_support_detail', values)

    # --------------------------------------------------
    # RMA
    # --------------------------------------------------
    @http.route('/my/returns', type='http', auth='user', website=True)
    def portal_my_returns(self, **kw):
        partner = request.env.user.partner_id
        Rma = request.env['pes.rma'].sudo()
        domain = ['|', ('partner_id', '=', partner.id),
                  ('partner_id', '=', partner.commercial_partner_id.id)]
        rmas = Rma.search(domain, order='create_date desc, id desc')
        values = {
            'rmas': rmas,
            'page_name': 'returns',
        }
        return request.render('riven_pes_portal.portal_my_returns', values)

    @http.route('/my/returns/new', type='http', auth='user', website=True)
    def portal_return_new(self, **kw):
        orders = request.env['sale.order'].sudo().search([
            ('partner_id', 'child_of', request.env.user.partner_id.commercial_partner_id.id),
            ('state', 'in', ['sale', 'done']),
        ], order='date_order desc', limit=20)
        values = {
            'orders': orders,
            'page_name': 'returns',
        }
        return request.render('riven_pes_portal.portal_return_new', values)

    @http.route('/my/returns/submit', type='http', auth='user', website=True)
    def portal_return_submit(self, **post):
        if not post.get('product_label'):
            return request.redirect('/my/returns/new')
        partner = request.env.user.partner_id
        Rma = request.env['pes.rma'].sudo()
        rma = Rma.create({
            'partner_id': partner.commercial_partner_id.id or partner.id,
            'sale_order_id': post.get('sale_order_id') and int(post['sale_order_id']) or False,
            'product_label': post.get('product_label'),
            'quantity': float(post.get('quantity') or 1),
            'reason': post.get('reason', 'defective'),
            'description': post.get('description') or '',
            'state': 'submitted',
        })
        return request.redirect('/my/returns')

    # --------------------------------------------------
    # Warranty
    # --------------------------------------------------
    @http.route('/my/warranty', type='http', auth='user', website=True)
    def portal_my_warranty(self, **kw):
        partner = request.env.user.partner_id
        Warranty = request.env['pes.warranty.registration'].sudo()
        domain = ['|', ('partner_id', '=', partner.id),
                  ('partner_id', '=', partner.commercial_partner_id.id)]
        warranties = Warranty.search(domain, order='create_date desc, id desc')
        values = {
            'warranties': warranties,
            'page_name': 'warranty',
        }
        return request.render('riven_pes_portal.portal_my_warranty', values)

    @http.route('/my/warranty/submit', type='http', auth='user', website=True)
    def portal_warranty_submit(self, **post):
        if not post.get('product_label'):
            return request.redirect('/my/warranty')
        partner = request.env.user.partner_id
        Warranty = request.env['pes.warranty.registration'].sudo()
        Warranty.create({
            'partner_id': partner.commercial_partner_id.id or partner.id,
            'product_label': post.get('product_label'),
            'serial_number': post.get('serial_number'),
            'install_date': post.get('install_date') or False,
            'warranty_years': int(post.get('warranty_years') or 10),
            'installer': post.get('installer'),
            'location': post.get('location'),
            'state': 'registered',
        })
        return request.redirect('/my/warranty')

    # --------------------------------------------------
    # Quote Requests (customer RFQ)
    # --------------------------------------------------
    @http.route(['/my/quotes', '/my/quotes/page/<int:page>'], type='http',
                auth='user', website=True)
    def portal_my_quotes(self, page=1, **kw):
        partner = request.env.user.partner_id
        Req = request.env['pes.quote.request'].sudo()
        domain = ['|', ('partner_id', '=', partner.id),
                  ('partner_id', '=', partner.commercial_partner_id.id)]
        quotes = Req.search(domain, order='create_date desc, id desc')
        values = {
            'quotes': quotes,
            'page_name': 'quote_requests',
        }
        return request.render('riven_pes_portal.portal_my_quotes', values)

    @http.route('/my/quotes/new', type='http', auth='user', website=True)
    def portal_quote_new(self, **kw):
        values = {
            'page_name': 'quote_requests',
        }
        return request.render('riven_pes_portal.portal_quote_new', values)

    @http.route('/my/quotes/submit', type='http', auth='user', website=True)
    def portal_quote_submit(self, **post):
        descriptions = post.get('descriptions', '').strip()
        if not descriptions:
            return request.redirect('/my/quotes/new')
        partner = request.env.user.partner_id
        Req = request.env['pes.quote.request'].sudo()
        qty_raw = post.get('quantities', '').strip()
        lines = []
        descs = [d.strip() for d in descriptions.splitlines() if d.strip()]
        qtys = [q.strip() for q in qty_raw.splitlines() if q.strip()] if qty_raw else []
        for i, d in enumerate(descs[:25]):
            try:
                qty = float(qtys[i]) if i < len(qtys) and qtys[i] else 1.0
            except ValueError:
                qty = 1.0
            lines.append((0, 0, {'description': d[:500], 'product_qty': qty}))
        req = Req.create({
            'partner_id': partner.commercial_partner_id.id or partner.id,
            'contact_name': post.get('contact_name') or partner.name,
            'contact_email': post.get('contact_email') or partner.email,
            'contact_phone': post.get('contact_phone') or partner.phone,
            'date_target': post.get('date_target') or False,
            'notes': post.get('notes') or '',
            'line_ids': lines,
        })
        request.env['pes.portal.activity'].sudo().create({
            'activity_type': 'quote_request',
            'description': 'Quote request submitted: %s' % req.name,
            'page_url': '/my/quotes/submit',
        })
        return request.redirect('/my/quotes/%s' % req.id)

    @http.route('/my/quotes/<int:req_id>', type='http', auth='user', website=True)
    def portal_quote_detail(self, req_id, **kw):
        req = request.env['pes.quote.request'].sudo().browse(req_id)
        if not req.exists():
            return request.redirect('/my/quotes')
        partner = request.env.user.partner_id
        if req.partner_id.id not in (partner.id, partner.commercial_partner_id.id):
            raise AccessError(_('You do not have access to this quote request.'))
        values = {
            'quote': req,
            'page_name': 'quote_requests',
        }
        return request.render('riven_pes_portal.portal_quote_detail', values)

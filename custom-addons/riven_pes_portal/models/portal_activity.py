from riven_erp import _, api, fields, models


class PesPortalActivity(models.Model):
    _name = 'pes.portal.activity'
    _description = 'PES Portal Activity Log'
    _order = 'activity_date desc, id desc'

    partner_id = fields.Many2one('res.partner', string='Customer',
                                 default=lambda self: self.env.user.partner_id)
    user_id = fields.Many2one('res.users', string='User',
                              default=lambda self: self.env.user)
    activity_type = fields.Selection([
        ('login', 'Login'),
        ('quote_request', 'Quote Request'),
        ('order_view', 'Order Viewed'),
        ('support_ticket', 'Support Ticket'),
        ('page_view', 'Page View'),
        ('download', 'Document Download'),
    ], default='page_view')
    description = fields.Char()
    sale_order_id = fields.Many2one('sale.order', string='Related Order')
    page_url = fields.Char()
    ip = fields.Char()
    activity_date = fields.Datetime(default=fields.Datetime.now)

    @api.model
    def log(self, activity_type, description=None, order=None, url=None):
        """Fire-and-forget activity logging from portal controllers."""
        try:
            self.sudo().create({
                'activity_type': activity_type,
                'description': description,
                'sale_order_id': order and order.id or False,
                'page_url': url,
                'ip': self.env['res.partner']._get_client_ip() if hasattr(
                    self.env['res.partner'], '_get_client_ip') else False,
            })
        except Exception:
            _logger = self.env['ir.logging']
            return False

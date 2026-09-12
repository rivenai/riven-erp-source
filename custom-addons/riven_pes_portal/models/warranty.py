from riven_erp import _, api, fields, models


class PesWarrantyRegistration(models.Model):
    _name = 'pes.warranty.registration'
    _description = 'PES Product Warranty Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Registration #', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True,
                                 default=lambda self: self.env.user.partner_id)
    product_id = fields.Many2one('product.product', string='Product (Catalog)', tracking=True)
    product_label = fields.Char(string='Product (as described by customer)', required=True, tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Related Order')
    serial_number = fields.Char(tracking=True)
    install_date = fields.Date()
    warranty_years = fields.Integer(default=10)
    warranty_start = fields.Date(tracking=True)
    warranty_end = fields.Date(compute='_compute_warranty_end', store=True)
    installer = fields.Char()
    location = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('registered', 'Registered'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], default='draft', tracking=True, copy=False)
    notes = fields.Html()

    @api.depends('warranty_start', 'warranty_years')
    def _compute_warranty_end(self):
        for reg in self:
            if reg.warranty_start and reg.warranty_years:
                try:
                    from datetime import relativedelta
                except ImportError:
                    from dateutil.relativedelta import relativedelta
                reg.warranty_end = reg.warranty_start + relativedelta(
                    years=reg.warranty_years)
            else:
                reg.warranty_end = False

    def action_register(self):
        for reg in self:
            if not reg.warranty_start:
                reg.warranty_start = reg.install_date or fields.Date.context_today(reg)
        self.write({'state': 'registered'})

    @api.model
    def _cron_check_expiry(self):
        """Move registrations to 'expiring' 30 days before warranty_end."""
        today = fields.Date.context_today(self)
        from datetime import timedelta
        limit = today + timedelta(days=30)
        expiring = self.search([
            ('state', '=', 'registered'),
            ('warranty_end', '!=', False),
            ('warranty_end', '<=', limit),
        ])
        expired = self.search([
            ('state', 'in', ['registered', 'expiring']),
            ('warranty_end', '!=', False),
            ('warranty_end', '<', today),
        ])
        expiring.write({'state': 'expiring'})
        expired.write({'state': 'expired'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'pes.warranty.registration') or _('New')
        return super().create(vals_list)

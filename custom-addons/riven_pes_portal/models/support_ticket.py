from riven_erp import _, api, fields, models


class PesSupportTicket(models.Model):
    _name = 'pes.support.ticket'
    _description = 'PES Support Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Ticket #', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, tracking=True,
                                 default=lambda self: self.env.user.partner_id)
    sale_order_id = fields.Many2one('sale.order', string='Related Order')
    subject = fields.Char(required=True, tracking=True)
    description = fields.Html()
    category = fields.Selection([
        ('order', 'Order Issue'),
        ('product', 'Product Question'),
        ('delivery', 'Delivery / Shipping'),
        ('invoice', 'Invoice / Billing'),
        ('warranty', 'Warranty Claim'),
        ('other', 'Other'),
    ], default='other', tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], default='1', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('waiting_customer', 'Waiting on Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], default='new', tracking=True, copy=False)
    assigned_to = fields.Many2one('res.users', string='Assigned To', tracking=True)
    resolution = fields.Html(readonly=True, copy=False)

    def action_assign(self):
        self.write({'assigned_to': self.env.user.id, 'state': 'in_progress'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_close(self):
        self.write({'state': 'closed'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('pes.support.ticket') or _('New')
        return super().create(vals_list)

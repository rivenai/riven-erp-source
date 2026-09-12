from riven_erp import _, api, fields, models


class PesRma(models.Model):
    _name = 'pes.rma'
    _description = 'PES Return Authorization (RMA)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='RMA #', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True,
                                 default=lambda self: self.env.user.partner_id)
    sale_order_id = fields.Many2one('sale.order', string='Related Order')
    product_id = fields.Many2one('product.product', string='Product', tracking=True)
    product_label = fields.Char(string='Product (as described by customer)', tracking=True)
    quantity = fields.Float(default=1.0, required=True)
    reason = fields.Selection([
        ('defective', 'Defective Product'),
        ('wrong_item', 'Wrong Item Shipped'),
        ('damaged', 'Damaged in Shipping'),
        ('unsuitable', 'Unsuitable for Application'),
        ('surplus', 'Surplus / Unused'),
        ('other', 'Other'),
    ], default='defective', required=True, tracking=True)
    description = fields.Html()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('received', 'Received'),
        ('processed', 'Processed / Refunded'),
        ('closed', 'Closed'),
    ], default='draft', tracking=True, copy=False)
    received_date = fields.Date(readonly=True, copy=False)
    resolution = fields.Html(readonly=True, copy=False)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_receive(self):
        self.write({'state': 'received', 'received_date': fields.Date.context_today(self)})

    def action_process(self):
        self.write({'state': 'processed'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('pes.rma') or _('New')
        return super().create(vals_list)

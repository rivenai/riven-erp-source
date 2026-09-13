from riven_erp import _, api, fields, models
from riven_erp.exceptions import UserError


class PesQuoteRequest(models.Model):
    _name = 'pes.quote.request'
    _description = 'PES Quote Request (customer RFQ from portal)'
    _order = 'create_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, index=True)
    contact_name = fields.Char(string='Contact Name')
    contact_email = fields.Char(string='Contact Email')
    contact_phone = fields.Char(string='Contact Phone')
    date_target = fields.Date(string='Needed By')
    notes = fields.Text(string='Customer Notes')
    state = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('quoted', 'Quoted'),
        ('converted', 'Converted to Order'),
        ('lost', 'Lost'),
    ], string='Status', default='new', tracking=True)
    line_ids = fields.One2many('pes.quote.request.line', 'request_id',
                               string='Requested Items')
    sale_order_id = fields.Many2one('sale.order', string='Quotation',
                                    readonly=True, copy=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, readonly=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('pes.quote.request') or _('New')
        return super().create(vals_list)

    def action_create_quotation(self):
        """Create a DRAFT sale.order (quotation) from this request.
        Does NOT confirm the order - confirmation stays a human action."""
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Add at least one requested item first.'))
        order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'client_order_ref': self.name,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'name': line.description or line.product_id.display_name,
                'product_uom_qty': line.product_qty,
            }) for line in self.line_ids],
        })
        self.write({'sale_order_id': order.id, 'state': 'quoted'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id,
            'view_mode': 'form',
            'target': 'current',
        }


class PesQuoteRequestLine(models.Model):
    _name = 'pes.quote.request.line'
    _description = 'PES Quote Request Line'
    _rec_name = 'description'

    request_id = fields.Many2one('pes.quote.request', string='Request',
                                 required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description', required=True)
    product_qty = fields.Float(string='Quantity', default=1.0, required=True)

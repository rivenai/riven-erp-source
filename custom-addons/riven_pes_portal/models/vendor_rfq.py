from riven_erp import _, api, fields, models
from riven_erp.exceptions import UserError


class PesVendorRfq(models.Model):
    _name = 'pes.vendor.rfq'
    _description = 'PES Vendor RFQ (request for quote to a supplier)'
    _order = 'create_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    supplier_id = fields.Many2one('res.partner', string='Supplier',
                                  required=True, index=True,
                                  domain=[('supplier_rank', '>', 0)])
    date_due = fields.Date(string='Response Due')
    notes = fields.Text(string='Notes to Supplier')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('responded', 'Responded'),
        ('awarded', 'Awarded'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('pes.vendor.rfq.line', 'rfq_id',
                               string='Requested Items')
    response_notes = fields.Text(string='Supplier Response Notes', copy=False)
    responded_date = fields.Datetime(string='Responded On', copy=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, readonly=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('pes.vendor.rfq') or _('New')
        return super().create(vals_list)

    def action_mark_sent(self):
        for rfq in self:
            if not rfq.line_ids:
                raise UserError(_('Add at least one item before sending RFQ %s.') % rfq.name)
        self.write({'state': 'sent'})
        return True

    def action_award(self):
        self.write({'state': 'awarded'})
        return True

    def action_close(self):
        self.write({'state': 'closed'})
        return True

    def submit_supplier_response(self, line_vals, response_notes=False):
        """Called from the portal (sudo) with sanitized supplier-entered data."""
        self.ensure_one()
        if self.state not in ('sent', 'responded'):
            raise UserError(_('This RFQ is not open for responses.'))
        self.write({'response_notes': response_notes or self.response_notes,
                    'state': 'responded',
                    'responded_date': fields.Datetime.now()})
        for line_id, price, lead, note in line_vals:
            if price is None and lead is None and not note:
                continue
            line = self.env['pes.vendor.rfq.line'].browse(line_id)
            if not line.exists() or line.rfq_id.id != self.id:
                continue
            vals = {}
            if price is not None:
                vals['unit_price'] = price
            if lead is not None:
                vals['lead_days'] = lead
            if note:
                vals['response_note'] = note[:500]
            if vals:
                line.write(vals)
        return True


class PesVendorRfqLine(models.Model):
    _name = 'pes.vendor.rfq.line'
    _description = 'PES Vendor RFQ Line'
    _rec_name = 'description'

    rfq_id = fields.Many2one('pes.vendor.rfq', string='RFQ',
                             required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description', required=True)
    product_qty = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Float(string='Quoted Unit Price', copy=False)
    lead_days = fields.Integer(string='Lead Time (days)', copy=False)
    response_note = fields.Char(string='Supplier Note', copy=False)

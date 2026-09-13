from riven_erp import api, fields, models, _

PORTAL_STATUS_SELECTION = [
    ('pricing', 'Pricing In Progress'),
    ('awaiting_signature', 'Awaiting Signature'),
    ('signed', 'Signed'),
    ('in_production', 'In Production'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('closed', 'Closed'),
]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    portal_status = fields.Selection(
        PORTAL_STATUS_SELECTION,
        string='Portal Status',
        default='pricing',
        copy=False,
        tracking=True,
        help='Client-visible status shown on the portal Deal Room and order list. '
             'Advances automatically to Signed when the client signs online.',
    )
    project_site = fields.Char(string='Project Site')
    project_type = fields.Char(string='Project Type')
    rfq_sent_date = fields.Date(string='RFQ Sent Date')
    pricing_expected_date = fields.Date(string='Pricing Expected Date')
    delivery_lead_weeks = fields.Integer(string='Delivery Lead Time (weeks)')

    def get_portal_display_status(self):
        """Status key to render: explicit portal_status wins, else derived from state."""
        self.ensure_one()
        if self.portal_status:
            return self.portal_status
        state_map = {
            'draft': 'pricing',
            'sent': 'awaiting_signature',
            'sale': 'in_production',
            'done': 'delivered',
            'cancel': 'closed',
        }
        return state_map.get(self.state, 'pricing')

    def write(self, vals):
        # Signature-driven status progression: when the core Accept & Sign flow
        # records the client signature, advance the portal status to Signed.
        if 'signed_by' in vals and vals.get('signed_by') and 'portal_status' not in vals:
            vals = dict(vals, portal_status='signed')
        res = super().write(vals)
        if 'portal_status' in vals:
            status_labels = dict(self._fields['portal_status']._description_selection(self.env))
            for order in self:
                if order.portal_status:
                    order.message_post(
                        body=_('Portal status updated to %s.', status_labels.get(order.portal_status, order.portal_status))
                    )
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricing_confidence = fields.Selection(
        [
            ('catalog', 'Catalog Price'),
            ('estimated', 'Estimated'),
            ('quoted', 'Supplier Quoted'),
            ('locked', 'Locked / PO-Ready'),
        ],
        string='Pricing Confidence',
        default='catalog',
        help='Client-facing pricing confidence indicator. Never exposes vendor cost.',
    )

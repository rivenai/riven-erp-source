import json

from riven_erp import api, fields, models
from riven_erp.exceptions import ValidationError


class RivenPortalConfig(models.Model):
    """Tenant configuration for the Riven Commerce Portal.

    Suite-native: no client-specific values live in code. Each tenant
    (e.g. PES Supply via riven_pes_portal) ships a config record.
    """
    _name = 'riven.portal.config'
    _description = 'Riven Commerce Portal Tenant Configuration'
    _rec_name = 'name'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', string='Company')
    portal_title = fields.Char(string='Portal Title')
    primary_color = fields.Char(string='Primary Color', default='#0C882A')
    secondary_color = fields.Char(string='Secondary Color', default='#0F213E')
    deal_room_enabled = fields.Boolean(string='Deal Room Enabled', default=True)
    show_pricing_confidence = fields.Boolean(string='Show Pricing Confidence', default=True)
    show_doc_vault = fields.Boolean(string='Show Document Vault', default=True)
    status_label_map = fields.Text(
        string='Status Label Overrides (JSON)',
        help='JSON dict mapping portal status keys to custom labels, '
             'e.g. {"pricing": "Sourcing Pricing"}. Leave empty for suite defaults.',
    )

    @api.constrains('status_label_map')
    def _check_status_label_map(self):
        for config in self:
            if config.status_label_map:
                try:
                    parsed = json.loads(config.status_label_map)
                    if not isinstance(parsed, dict):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValidationError('Status Label Overrides must be a JSON object like {"pricing": "Custom Label"}.')

    @api.model
    def get_active(self):
        """Return the tenant config record for rendering (sudo-safe, single tenant per DB)."""
        config = self.sudo().search([], limit=1)
        return config or self.sudo().new({})

    @api.model
    def portal_status_map(self):
        """Return {status_key: (label, bootstrap_badge_class)} with tenant label overrides applied."""
        labels = {
            'pricing': ('Pricing In Progress', 'text-bg-warning'),
            'awaiting_signature': ('Awaiting Signature', 'text-bg-info'),
            'signed': ('Signed', 'text-bg-success'),
            'in_production': ('In Production', 'text-bg-primary'),
            'shipped': ('Shipped', 'text-bg-secondary'),
            'delivered': ('Delivered', 'text-bg-success'),
            'closed': ('Closed', 'text-bg-dark'),
        }
        overrides = {}
        config = self.sudo().search([], limit=1)
        if config and config.status_label_map:
            try:
                parsed = json.loads(config.status_label_map)
                if isinstance(parsed, dict):
                    overrides = parsed
            except (ValueError, TypeError):
                overrides = {}
        return {key: (overrides.get(key, label), badge) for key, (label, badge) in labels.items()}

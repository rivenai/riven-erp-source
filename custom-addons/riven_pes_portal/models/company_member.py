from riven_erp import _, api, fields, models


class PesCompanyMember(models.Model):
    _name = 'pes.company.member'
    _description = 'PES Company Member (Multi-User Portal Access)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'partner_id, sequence, id'

    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one('res.partner', string='Company', required=True,
                                 tracking=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Portal User')
    name = fields.Char(string='Member Name', required=True, tracking=True)
    email = fields.Char(required=True, tracking=True)
    role = fields.Selection([
        ('admin', 'Company Admin'),
        ('buyer', 'Buyer'),
        ('approver', 'Approver'),
        ('viewer', 'Viewer'),
    ], default='viewer', required=True, tracking=True)
    active = fields.Boolean(default=True)
    invite_sent = fields.Boolean(readonly=True, copy=False)
    invite_date = fields.Datetime(readonly=True, copy=False)
    can_approve = fields.Boolean(compute='_compute_permissions', store=True)
    can_view_invoices = fields.Boolean(compute='_compute_permissions', store=True)
    can_request_quotes = fields.Boolean(compute='_compute_permissions', store=True)

    @api.depends('role')
    def _compute_permissions(self):
        perms = {
            'admin': (True, True, True),
            'buyer': (False, True, True),
            'approver': (True, True, False),
            'viewer': (False, False, False),
        }
        for member in self:
            member.can_approve, member.can_view_invoices, member.can_request_quotes = \
                perms.get(member.role, (False, False, False))

    def action_mark_invite_sent(self):
        self.write({'invite_sent': True, 'invite_date': fields.Datetime.now()})

from riven_erp import fields, models


class IrAttachment(models.Model):
    """Client-portal visibility gate on attachments (Document vault)."""
    _inherit = 'ir.attachment'

    portal_visible = fields.Boolean(
        string='Visible in Client Portal',
        default=True,
        help='Clear this to hide an internal-only attachment from the client order '
             'Document vault. Client-safe docs (signed PDF, proposal, BOL) stay visible.',
    )
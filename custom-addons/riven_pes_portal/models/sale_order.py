from riven_erp import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Sanitized supplier fulfillment status — vendor names and costs are
    # intentionally NOT exposed to the customer portal; only these fields.
    pes_supplier_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('backordered', 'Backordered'),
        ('cancelled', 'Cancelled'),
    ], string='Supplier Status', tracking=False, copy=False)
    pes_supplier_eta = fields.Date(string='Supplier ETA', copy=False)
    pes_tracking_numbers = fields.Char(string='Tracking #', copy=False)
    pes_supplier_confirmed_qty = fields.Float(
        string='Qty Confirmed by Supplier', copy=False)

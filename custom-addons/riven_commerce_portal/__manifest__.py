{
    'name': 'Riven Commerce Portal',
    'summary': 'Riven Business Suite buyer-commerce portal: order status badges, Deal Room, order timeline, document vault, signature-driven status flow. Tenant-config branding.',
    'description': """
Riven Commerce Portal (suite-native)
====================================
Buyer-commerce portal layer of the Riven Business Suite. Tenant-agnostic by
design: all branding and labels flow from riven.portal.config — a client
onboards by configuration, never by fork.

Capabilities (v0.0.09):
- Order list status badges (/my/orders)
- Deal Room on the order/quote detail page: project overview, portal status
  badge, RFQ/pricing/delivery timeline, pricing-confidence legend
- Per-line pricing confidence (catalog / estimated / supplier quoted / locked)
- Document vault section per order (client-safe attachment list)
- Signature-driven status progression: when the client signs via the core
  Accept & Sign flow, portal status auto-advances to Signed
- Chatter notifications on portal-status changes (no external email; email
  templates remain approval-gated per mail guardrail)

This module carries ZERO client-specific assets, strings, or colors.
    """,
    'version': '0.0.09',
    'category': 'Website/Portal',
    'author': 'Riven ERP',
    'license': 'LGPL-3',
    'depends': ['portal', 'sale_management', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/config_views.xml',
        'views/sale_order_views.xml',
        'views/portal_order_list.xml',
        'views/portal_deal_room.xml',
    ],
    'application': True,
    'installable': True,
}

{
    'name': 'PES Supply Portal',
    'summary': 'PES Supply customer portal: support tickets, RMA, warranty registration, company members, portal activity',
    'description': """
PES Supply Portal
=================
Rebuilt (2026-09) on the Riven ERP 19 stack from the pre-rebuild portal specification:
- Support ticket system (portal submit + track)
- Return authorization (RMA) workflow
- Product warranty registration
- Multi-user company accounts (roles)
- Portal activity tracking
- Warranty expiry monitoring cron

Replaces the pre-suspension portal customizations (former x_pes_* models and portal views).
    """,
    'version': '0.0.05',
    'category': 'Website/Portal',
    'author': 'Riven ERP',
    'license': 'LGPL-3',
    'depends': ['portal', 'sale_management', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/ir_cron.xml',
        'views/backend_views.xml',
        'views/sale_order_views.xml',
        'views/portal_templates.xml',
        'views/sale_order_portal.xml',
    ],
    'application': True,
    'installable': True,
}

# -*- coding: utf-8 -*-
{
    "name": "Sol luminiare Invoice Customization",
    "author": "HashMicro/ Kunal",
    "version": "1.0",
    "website": "www.hashmicro.com",
    "category": "luminiare",
    "depends": ['account','solum_sale','web_readonly_bypass'],
    "data": [
		'security/ir.model.access.csv',
		'views/invoice_view.xml',
		'views/report_menu.xml',
		'report/sol_invoice_report_view.xml',
		'report/idesign_invoice_report_view.xml',
        'report/report_trial_balance.xml',
		'report/sol_commission_invoice_report_view.xml',
		'data/data.xml',
		'data/invoice_action_data.xml',
    ],
    'description': '''Invoice Customization''',
    'demo': [],
    'installable': True,
    'auto_install': False,
}

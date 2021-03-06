# -*- coding: utf-8 -*-
{
    'name': "marketplaces",

    'summary': """
        * Make a module that can connect to major marketplaces""",

    'description': """
        * Make a module that can connect to major marketplaces
    """,

    'author': "HashMicro / Vu",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'HashMicro',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/data_update_views.xml',
        'views/data_product_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
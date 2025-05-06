{
    'name': 'Cash Payment Gateway',
    'version': '16.0',
    'summary': '',
    'description': 'Cash Payment Gateway',
    'category': 'Accounting/Payment',
    'author': 'Derly González',
    'website': '',
    'license': 'Other proprietary',
    'depends': [
       "account_payment",
        "payment",
    ],
    'data': [
        # views
        'views/templates.xml',
        'views/payment_provider_views.xml',
        #data
        'data/payment_provider_data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

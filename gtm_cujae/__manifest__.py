{
    'name': "gtm_cujae",
    'author': "Ernesto",
    'website': "http://www.yourcompany.com",

    'summary': """
        Modulo Trámites Migratorios Cujae
        """,
    'sequence': 13,

    'description': """
        Este módulo es para gestionar los trámites migratorios de la CUJAE
    """,

    'category': 'Uncategorized',
    'version': '1.0',

    'depends': [
        'base','helpdesk_mgmt','helpdesk_mgmt_project','helpdesk_mgmt_timesheet','helpdesk_type','config_cujae'
    ],

    'data':[
        'security/ir.model.access.csv',
        'data/gtm_sequence.xml',
        'data/gtm_data.xml',
        'views/gtm_menu.xml',
        'views/travel_form_views.xml',
        'views/travel_expense_views.xml',
        'views/gtm_form_views.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
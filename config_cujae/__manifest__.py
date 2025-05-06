{
    'name': "config_cujae",
    'author': "Ernesto",
    'website': "http://www.yourcompany.com",

    'summary': """
        Módulo de configuraciones generales
        """,
    'sequence': 11,

    'description': """
        Este módulo es para guardar los datos base de la CUJAE
    """,

    'category': 'Uncategorized',
    'version': '1.0',

    'depends': [
        'base','hr'
    ],

    'data':[
        'data/res_company_data.xml',
        'data/department_data.xml',
        'views/partner_extension_views.xml',
    ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
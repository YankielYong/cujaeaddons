{
    'name': 'event_cujae',
    'author': "Marlon Gonzalez Baro",
    "category": "Tools",
    "depends": ['base', 'event', 'website_event', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/event_views.xml',
        'views/reviewer_views.xml',
        'views/scientific_work_views.xml',
        'views/submission_page.xml',
        'views/submission_confirmation.xml',
        'views/event_website.xml',
        'data/faculty_data.xml',
        'data/responsible_data.xml',
    ],
    'license': 'AGPL-3',
    "installable": True,
    'application': True,
}

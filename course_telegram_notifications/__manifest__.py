{
    'name': "Notificaciones de eLearning por Telegram",
    'version': '16.0.1.0.0',
    'author': "Reinaldo y Keila",
    'category': 'eLearning',
    'summary': "Envía notificaciones a Telegram cuando se añade contenido a un curso.",
    'depends': ['website_slides'],
    'data': [
        'views/slide_channel_views.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
    'installable': True,
    'application': False,
}
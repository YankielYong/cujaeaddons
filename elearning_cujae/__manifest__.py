# -*- coding: utf-8 -*-
{
    'name': "eLearning CUJAE",

    'summary': """
        Modulo elearning Cujae
        """,
    'sequence': 1,

    'description': """
        Este módulo es para impartir cursos digitales
    """,

    'author': "Reinaldo y Keila",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/eLearning',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_slides','survey','website_slides_survey'],

    # always loaded
    # xd
    'data': [        
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/gamification_data.xml',
        'data/cron_jobs.xml',
        'data/mail_template_data.xml',
        'views/survey_question.xml',
        'views/survey_question_views.xml',
        #'static/description/icon.png',
        'views/slide_slide_views.xml',
        'views/survey_survey_views.xml',
        #'views/res_config_settings_views.xml',
        'views/slide_slide_partner_views.xml',
        'views/website_slides_menu_views.xml',
        'views/website_slide_templates_course.xml',
        'views/website_slides_templates_lesson.xml',
        'views/website_slides_templates_utils.xml',
        'views/website_slides_templates_lesson_fullscreen.xml',
        'views/website_slides_templates_homepage.xml',
        'views/slide_channel_views.xml',
        'views/website_profile.xml',
        'views/survey_templates.xml',
        'views/survey_template_form.xml',
        'views/gamification_menu.xml',
        'views/survey_user_views.xml',
        'views/survey_templates_print.xml',
       # 'views/survey_form.xml',
        'views/slide_channel_partner_views.xml',
        'wizard/question_wizard_views.xml',
        'views/action_open_question_wizard.xml'
        

        'security/security.xml',
        
    ],
    'images':[
        'static/description/icon.png',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/account_move_demo.xml',
    ],

     'assets': {
        'web.assets_frontend': [
          'elearning_cujae/static/src/scss/website_slides_survey.scss',
          'elearning_cujae/static/src/js/slides_upload.js',
          'elearning_cujae/static/src/js/slides_course_extend.js',
         # 'elearning_cujae/static/src/js/slides_upload_copy.js',
          'elearning_cujae/static/src/js/survey_submit.js',
         # 'elearning_cujae/static/src/js/slides_upload_copy.js',
          'elearning_cujae/static/src/js/slides_course_fullscreen_player.js',
          'elearning_cujae/static/src/xml/website_slides_fullscreen.xml',
          'elearning_cujae/static/src/xml/website_slide_upload.xml',
          'elearning_cujae/static/src/xml/website_slides_fullscreen.xml',


     ],
        'survey.survey_assets': [
          'elearning_cujae/static/src/js/survey_form.js',
          'elearning_cujae/static/src/js/survey_form_attachment.js',
          'elearning_cujae/static/src/scss/website_slides_survey_result.scss',
        ],
     },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

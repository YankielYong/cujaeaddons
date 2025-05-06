# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug
import werkzeug.utils
import werkzeug.exceptions

from odoo import _
from odoo import http
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_slides.controllers.main import WebsiteSlides
from odoo.addons.website_slides_survey.controllers.slides import WebsiteSlidesSurvey



class WebsiteSlidesSurveyExam(WebsiteSlides):

    @http.route(route='/slides_survey/slide/get_exam_url', type='http', auth='user', website=True,)
    def slide_get_exam_url_ex(self, slide_id, **kw):
        print("el controlador")

        fetch_res = self._fetch_slide(slide_id)
        print(fetch_res)
        if fetch_res.get('error'):
            raise werkzeug.exceptions.NotFound()
        slide = fetch_res['slide']
        print(slide.name)
        if slide.channel_id.is_member:
            slide.action_set_viewed()
            print(slide)

        exam_url = slide._generate_exam_url(slide).get(slide.id)
        print(slide.slide_category)
        if not exam_url:
            raise werkzeug.exceptions.NotFound()
            print("error3")
        return request.redirect(exam_url)

    @http.route(['/slides_survey/exam/search_read'], type='json', auth='user', methods=['POST'], website=True)
    def slides_exam_search_read_ex(self, fields):
        can_create = request.env['survey.survey'].check_access_rights('create', raise_exception=False)
        return {
            'read_results': request.env['survey.survey'].search_read([('exam', '=', True)], fields),
            'can_create': can_create,
        }

    # ------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------

    @http.route(['/slides/add_slide'], type='json', auth='user', methods=['POST'], website=True)
    def create_slide(self, *args, **post):
        if post['slide_category']=='certification':
            asd= WebsiteSlidesSurvey.create_slide(self,*args,**post)
            return asd
        elif post['slide_category']=='exam':
            create_new_survey = post['slide_category'] == "exam" and post.get('survey') and not post['survey']['id']
            linked_exam_id = int(post.get('survey', {}).get('id') or 0)
            if create_new_survey:
                # If user cannot create a new survey, no need to create the slide either.
                if not request.env['survey.survey'].check_access_rights('create', raise_exception=False):
                    return {'error': _('You are not allowed to create a survey.')}

                # Create survey first as exam slide needs a exam_id (constraint)
                post['exam_id'] = request.env['survey.survey'].create({
                    'title': post['survey']['title'],
                    'questions_layout': 'page_per_question',
                    'is_attempts_limited': True,
                    'attempts_limit': 1,
                    'is_time_limited': False,
                    'scoring_type': 'scoring_without_answers',
                    'exam': True,
                    'scoring_success_min': 80.0,
                    #'exam_mail_template_id': request.env.ref('survey.mail_template_exam').id,
                }).id
            elif linked_exam_id:
                try:
                    request.env['survey.survey'].browse([linked_exam_id]).read(['title'])
                except AccessError:
                    return {'error': _('You are not allowed to link a exam.')}
                post['exam_id'] = post['survey']['id']
                post['survey_id']= post['exam_id']

            # Then create the slide
            result = super(WebsiteSlidesSurveyExam, self).create_slide(*args, **post)
            if post['slide_category'] == "exam":
                # Set the url to redirect the user to the survey
                result['url'] = '/slides/slide/%s?fullscreen=1' % (slug(request.env['slide.slide'].browse(result['slide_id']))),
            return result
        else:
            result = super(WebsiteSlidesSurveyExam, self).create_slide(*args, **post)
            return result



    # Utils
    # ---------------------------------------------------
    def _slide_mark_completed(self, slide):
        if slide.slide_category == 'exam':
            raise werkzeug.exceptions.Forbidden(_("exam slides are completed when the survey is succeeded."))
        return super(WebsiteSlidesSurveyExam, self)._slide_mark_completed(slide)

    def _get_valid_slide_post_values(self):
        result = super(WebsiteSlidesSurveyExam, self)._get_valid_slide_post_values()
        result.append('exam_id')
        return result

    # Profile
    # ---------------------------------------------------
    def _prepare_user_slides_profile(self, user):
        values = super(WebsiteSlidesSurveyExam, self)._prepare_user_slides_profile(user)
        values.update({
            'completed_ex': self._get_users_completed_ex(user)[user.id]
        })
        return values

    # All Users Page
    # ---------------------------------------------------
    def _prepare_all_users_values(self, users):
        result = super(WebsiteSlidesSurveyExam, self)._prepare_all_users_values(users)
        completed_ex_per_user = self._get_users_completed_ex(users)
        for index, user in enumerate(users):
            result[index].update({
                'exam_count': len(completed_ex_per_user.get(user.id, []))
            })
        return result

    def _get_users_certificates(self, users):
        partner_ids = [user.partner_id.id for user in users]
        domain = [
            ('slide_partner_id.partner_id', 'in', partner_ids),
            ('scoring_success', '=', True),
            ('slide_partner_id.survey_scoring_success', '=', True),
            ('slide_id.slide_category', '=', 'certification')

        ]
        certificates = request.env['survey.user_input'].sudo().search(domain)
        users_certificates = {
            user.id: [
                certificate for certificate in certificates if certificate.partner_id == user.partner_id
            ] for user in users
        }
        return users_certificates

    def _get_users_completed_ex(self, users):
        partner_ids = [user.partner_id.id for user in users]
        
        domain = [
            ('slide_partner_id.partner_id', 'in', partner_ids),
            ('scoring_success', '=', True),
            ('slide_partner_id.survey_scoring_success', '=', True),
            ('slide_id.exam_id.exam', '=', True)

        ]
        completed_ex = request.env['survey.user_input'].sudo().search(domain)
        users_completed_ex = {
            user.id: [
                completed_ex for completed_ex in completed_ex if completed_ex.partner_id == user.partner_id
            ] for user in users
        }
        return users_completed_ex

    # Badges & Ranks Page
    # ---------------------------------------------------
    def _prepare_ranks_badges_values(self, **kwargs):
        """ Extract exam badges, to render them in ranks/badges page in another section.
        Order them by number of granted users desc and show only badges linked to opened exams."""
        values = super(WebsiteSlidesSurvey, self)._prepare_ranks_badges_values(**kwargs)

        # 1. Getting all exam badges, sorted by granted user desc
        domain = expression.AND([[('survey_id', '!=', False)], self._prepare_badges_domain(**kwargs)])
        exam_badges = request.env['gamification.badge'].sudo().search(domain)
        # keep only the badge with challenge category = slides (the rest will be displayed under 'normal badges' section
        exam_badges = exam_badges.filtered(
            lambda b: 'slides' in b.challenge_ids.mapped('challenge_category'))

        if not exam_badges:
            return values

        # 2. sort by granted users (done here, and not in search directly, because non stored field)
        exam_badges = exam_badges.sorted("granted_users_count", reverse=True)

        # 3. Remove exam badge from badges
        badges = values['badges'] - exam_badges

        # 4. Getting all course url for each badge
        exam_slides = request.env['slide.slide'].sudo().search([('exam_id', 'in', exam_badges.mapped('exam_id').ids)])
        exam_badge_urls = {slide.exam_id.exam_badge_id.id: slide.channel_id.website_url for slide in exam_slides}

        # 5. Applying changes
        values.update({
            'badges': badges,
            'exam_badges': exam_badges,
            'exam_badge_urls': exam_badge_urls
        })
        return values


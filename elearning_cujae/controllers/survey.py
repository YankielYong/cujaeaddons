# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.survey.controllers import main
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError


class SurveyExam(main.Survey):
    def _prepare_survey_finished_values_ex(self, survey, answer, token=False):
        result = super(SurveyExam, self)._prepare_survey_finished_values(survey, answer, token)
        if answer.slide_id:
            result['channel_id'] = answer.slide_id.channel_id

        return result

    def _prepare_retry_additional_values_ex(self, answer):
        result = super(SurveyExam, self)._prepare_retry_additional_values(answer)
        if answer.slide_id:
            result['slide_id'] = answer.slide_id.id
        if answer.slide_partner_id:
            result['slide_partner_id'] = answer.slide_partner_id.id

        return result
    
    @http.route(['/survey/<int:survey_id>/get_exam'], type='http', auth='user', methods=['GET'], website=True)
    def survey_get_exam(self, survey_id, **kwargs):
        survey = request.env['survey.survey'].sudo().search([
            ('id', '=', survey_id),
            ('exam', '=', True)
        ])

        if not survey:
            # no certification found
            return request.redirect("/")

        succeeded_attempt = request.env['survey.user_input'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('survey_id', '=', survey_id),
            ('scoring_success', '=', True)
        ], limit=1)

        if not succeeded_attempt:
            raise UserError(("The user has not succeeded the exam"))

        return self._generate_report(succeeded_attempt, download=True)
from odoo import api, fields, models


class GamificationBadge(models.Model):
    _inherit = 'gamification.badge'

    exam_ids = fields.One2many('survey.survey', 'exam_badge_id', 'Exam Ids')

    @api.depends('survey_ids.exam_badge_id')
    def _compute_survey_id(self):
        for badge in self:
            badge.survey_id = badge.exam_ids[0] if badge.exam_ids else None

  
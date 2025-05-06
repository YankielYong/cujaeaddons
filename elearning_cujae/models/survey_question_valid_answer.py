from odoo import models, fields, api
class SurveyQuestionValidAnswer(models.Model):
    _name = 'survey.question.valid.answer'
    _description = 'Respuesta Válida para Preguntas de Completar'

    question_id = fields.Many2one('survey.question', required=True, ondelete='cascade')
    value = fields.Char('Respuesta', required=True, translate=True)

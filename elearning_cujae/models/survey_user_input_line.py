from odoo import api, fields, models
from Tools.scripts.dutree import store
from odoo.exceptions import ValidationError

class SurveyUserInputLine(models.Model):
    _inherit = ['survey.user_input.line']

    max_score= fields.Float(related='question_id.max_score', string='Question score')

    answer_type = fields.Selection(
        selection_add=[
            ('upload_file', 'Subir archivo'),
            ('true_false', 'Verdadero o Falso'),
        ],
    )

    true_false_item_id = fields.Many2one(
        'survey.true_false_item',
        string="True/False Item"
    )

    value_file_data_ids = fields.Many2many('ir.attachment',
                                           help="The attachments "
                                                "corresponding to the user's "
                                                "file upload answer, if any.")

    @api.constrains('skipped', 'answer_type')
    def _check_answer_type_skipped(self):
        """ Check that a line's answer type is not set to 'upload_file' if
        the line is skipped."""
        for line in self:
            if line.answer_type != 'upload_file':
                super(SurveyUserInputLine, line)._check_answer_type_skipped()



    @api.constrains('answer_score', 'question_id')
    def _check_answer_score_limit(self):
        """Valida que el answer_score no sea mayor que el max_score de la pregunta."""
        for line in self:
            if line.answer_score > line.question_id.max_score:
                raise ValidationError(
                    ("El puntaje de la respuesta no puede ser mayor que la puntuación máxima de la pregunta (%s).")
                    % self.max_score
                )

    @api.model
    def _get_answer_score_values(self, vals, compute_speed_score=True):
        question_id=vals.get('question_id')
        question = self.env['survey.question'].browse(int(question_id))

        answer_is_correct = False
        answer_score = 0
        res=super(SurveyUserInputLine, self)._get_answer_score_values(vals, compute_speed_score)

        if question.question_type in ['char_box']:
            answer=vals['value_char_box']
            normalized_answer = answer.strip().lower() if answer else ""
            # Buscar coincidencia en respuestas válidas
            valid_answers = [ans.value.strip().lower() for ans in question.valid_answer_ids]
            if normalized_answer  in valid_answers:
                answer_is_correct=True
                answer_score = question.answer_score
            return {
            'answer_is_correct': answer_is_correct,
            'answer_score': answer_score
            }
        else:
            return res



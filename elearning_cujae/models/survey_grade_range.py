from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SurveyGradeRange(models.Model):
    _name = 'survey.grade.range'
    _description = 'Rango de Calificaciones para Encuestas'
    _order = 'min_percentage asc'

    survey_id = fields.Many2one('survey.survey', string="Encuesta", ondelete='cascade', required=True)
    min_percentage = fields.Float(string="Mínimo %", required=True, digits=(2, 2))
    max_percentage = fields.Float(string="Máximo %", required=True, digits=(2, 2))
    grade = fields.Integer(string="Nota", required=True)

    @api.constrains('min_percentage', 'max_percentage', 'grade', 'survey_id')
    def _check_all_validations(self):
        for record in self:
            # Validación básica de porcentajes
            if record.min_percentage >= record.max_percentage:
                raise ValidationError("El porcentaje mínimo debe ser menor que el máximo.")
            
            if record.min_percentage < 0 or record.max_percentage > 100:
                raise ValidationError("Los porcentajes deben estar entre 0% y 100%.")
            
            # Validación de grados
            if not 2 <= record.grade <= 5:
                raise ValidationError("La nota debe estar entre 2 y 5.")
            
            # Validación de unicidad de notas
            duplicate_grades = self.search([
                ('survey_id', '=', record.survey_id.id),
                ('grade', '=', record.grade),
                ('id', '!=', record.id)
            ])
            if duplicate_grades:
                raise ValidationError("¡Nota duplicada para esta encuesta!")
            
            # Validación de rangos especiales para notas 2 y 5
            if record.grade == 2:
                if record.min_percentage != 0:
                    raise ValidationError("La nota 2 debe comenzar en 0%.")
                if record.max_percentage != record.survey_id.scoring_success_min:
                    raise ValidationError("La nota 2 debe terminar en el porcentaje mínimo de aprobación de la encuesta.")
            elif record.grade == 5:
                if record.max_percentage != 100:
                    raise ValidationError("La nota 5 debe terminar en 100%.")
            
            # Validación de solapamiento
            overlapping = self.search([
                ('survey_id', '=', record.survey_id.id),
                ('id', '!=', record.id),
                ('min_percentage', '<', record.max_percentage),
                ('max_percentage', '>', record.min_percentage),
            ])
            if overlapping:
                raise ValidationError("¡Rangos solapados detectados!")
            
           
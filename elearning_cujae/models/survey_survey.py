from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Survey(models.Model):
    _inherit="survey.survey"
    grade_ranges = fields.One2many('survey.grade.range', 'survey_id', string="Grade Ranges")
    exam = fields.Boolean('¿Es un examen?', compute='_compute_exam',readonly=False, store=True, precompute=True)
    exam_give_badge = fields.Boolean('Dar insignia de examen', compute='_compute_exam_give_badge',readonly=False, store=True, copy=False)
    exam_badge_id = fields.Many2one('gamification.badge', 'Insignia de examen', copy=False)
    exam_badge_id_dummy = fields.Many2one(related='exam_badge_id', string='Insignia de examen ')
    professor_check= fields.Boolean('Revisado por profesor', compute='_compute_check_survey',store=True)
    user_input_ids = fields.One2many('survey.user_input', 'survey_id', string='User responses', readonly=False, groups='survey.group_survey_user')

    @api.depends('scoring_type')
    def _compute_exam(self):
        for survey in self:
            if not survey.exam or survey.scoring_type == 'no_scoring':
                survey.exam = False
    
    @api.depends('users_login_required', 'exam')
    def _compute_exam_give_badge(self):
        for survey in self:
            if not survey.exam_give_badge or \
               not survey.users_login_required or \
               not survey.exam:
                survey.exam_give_badge = False 

    @api.depends('question_ids')
    def _compute_check_survey(self):
        flag=False
        for survey in self:
            survey.professor_check = False
            for question in survey.question_ids:
                if question.question_type in ('text_box', 'upload_file') and question.is_scored_question and flag==False:
                    survey.professor_check = True
                    flag=True
                    

    def _create_default_grade_ranges(self):
        self.ensure_one()
        self.grade_ranges.unlink()  # Eliminar existentes
        
        scoring_min = self.scoring_success_min
        ranges = []
        
        # Nota 2 (obligatoria)
        ranges.append({
            'min_percentage': 0,
            'max_percentage': scoring_min,
            'grade': 2
        })
        
        # Calcular rangos para notas 3,4,5
        remaining = 100 - scoring_min
        if remaining > 0:
            step = remaining / 3
            ranges.extend([
                {
                    'min_percentage': scoring_min,
                    'max_percentage': scoring_min + step,
                    'grade': 3
                },
                {
                    'min_percentage': scoring_min + step,
                    'max_percentage': scoring_min + (2 * step),
                    'grade': 4
                },
                {
                    'min_percentage': scoring_min + (2 * step),
                    'max_percentage': 100,
                    'grade': 5
                }
            ])
        
        # Crear registros en orden
        for range_data in ranges:
            self.env['survey.grade.range'].create({
                **range_data,
                'survey_id': self.id
            })
    
    @api.model
    def create(self, vals):
        # Valor por defecto para scoring_success_min
        if 'scoring_success_min' not in vals:
            vals['scoring_success_min'] = 80.0
        
        survey = super().create(vals)
        survey._create_default_grade_ranges()
        return survey

    def write(self, vals):
        # Actualizar rangos si cambia scoring_success_min
        res = super().write(vals)
        if 'scoring_success_min' in vals:
            for survey in self:
                survey._create_default_grade_ranges()
        return res

    @api.constrains('scoring_success_min')
    def _check_scoring_min(self):
        for record in self:
            if record.scoring_success_min < 0 or record.scoring_success_min > 100:
                raise ValidationError("El porcentaje mínimo de aprobación debe estar entre 0 y 100")
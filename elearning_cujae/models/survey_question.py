from odoo import models, fields, api


class SurveyQuestion(models.Model):
    _inherit= 'survey.question'

    @api.depends('question_type', 'scoring_type', 'answer_date', 'answer_datetime', 'answer_numerical_box')
    def _compute_is_scored_question(self):
        """ Computes whether a question "is scored" or not. Handles following cases:
          - inconsistent Boolean=None edge case that breaks tests => False
          - survey is not scored => False
          - 'date'/'datetime'/'numerical_box' question types w/correct answer => True
            (implied without user having to activate, except for numerical whose correct value is 0.0)
          - 'simple_choice / multiple_choice': set to True even if logic is a bit different (coming from answers)
          - question_type isn't scoreable (note: choice questions scoring logic handled separately) => False
        """
        for question in self:
            print(question.question_type)
            if question.question_type=='text_box' or question.question_type=='upload_file':
                question.is_scored_question = True
                question.scoring_type= 'scoring_with_answers'
                print("hello")
            elif question.question_type == 'date':
                question.is_scored_question = bool(question.answer_date)
            elif question.question_type == 'datetime':
                question.is_scored_question = bool(question.answer_datetime)
            elif question.question_type == 'numerical_box' and question.answer_numerical_box:
                question.is_scored_question = True
            elif question.question_type in ['simple_choice', 'multiple_choice']:  # Add 'text_box' here
                question.is_scored_question = True
            else:
                question.is_scored_question = False
            
       


    
from odoo import models, fields

class Responsible(models.Model):
    _name = 'faculty.responsible'
    _description = 'Responsible for Faculty'

    name = fields.Char(string='Name', required=True)
    faculty_id = fields.Many2one('university.faculty', string='Faculty')
    organizer_id = fields.Many2one('res.users', string='Organizer')
from odoo import models, fields

class UniversityFaculty(models.Model):
    _name = 'university.faculty'
    _description = 'University Faculty'

    name = fields.Char(string='Faculty Name', required=True)
from odoo import models, fields, api

class ScientificWork(models.Model):
    _name = 'scientific.work'
    _description = 'Trabajo Científico'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Título del Trabajo', required=True)
    author_name=fields.Char(string='Nombre del autor', required=True)
    event_id = fields.Many2one('event.event', string='Evento', required=True)
    attachment = fields.Binary(string='Archivo del Trabajo', filename='attachment_filename')
    attachment_filename = fields.Char(string='Nombre del Archivo')
    state = fields.Selection([
        ('to_review', 'Por Revisar'),
        ('reviewed', 'Revisado'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    ], string='Estado', default='to_review', tracking=True)
    reviewer_ids = fields.One2many('work.reviewer', 'work_id', string='Revisores')

    def action_to_review(self):
        self.write({'state': 'to_review'})

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

class WorkReviewer(models.Model):
    _name = 'work.reviewer'
    _description = 'Revisor de Trabajo'

    name = fields.Char(string='Título del Trabajo', related = 'work_id.name')
    work_id = fields.Many2one('scientific.work', string='Trabajo', required=True)
    reviewer_id = fields.Many2one('res.users', string='Revisor', required=True)
    opinion = fields.Text(string='Opinión')
    rating = fields.Float(string='Calificación', digits=(2, 1))
    attachment = fields.Binary(
        string='Archivo del Trabajo',
        related='work_id.attachment',
        readonly=False
    )
    attachment_filename = fields.Char(
        string='Nombre del Archivo',
        related='work_id.attachment_filename'
    )
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cujae_user_type = fields.Selection(
        selection=[
            ('student', 'Estudiante'),
            ('teacher', 'Docente'),
            ('staff', 'No docente'),
            ('external', 'Contacto externo')
        ],
        string='Tipo de usuario CUJAE',
        default='student',
        help='Clasificación institucional del contacto',
        tracking=True  # Opcional: registra cambios en el chatter
    )
    gender = fields.Selection(
        selection=[('male', 'Masculino'), ('female', 'Femenino')],
        string="Sexo",
        default='male',
        tracking=True
    )
    address = fields.Char(string="Dirección personal")


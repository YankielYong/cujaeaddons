from odoo import api, fields, models
from odoo import _
class Ticket(models.Model):
    _inherit = 'helpdesk.ticket'
    _description = "Modificaciones al helpdesk ticket"

    travel_expense_id = fields.Many2one(
        "travel.expense",
        string="Planilla de costos de viaje",
        ondelete='cascade',
        context="{'default_ticket_id': id}",  # Autoasigna el ticket al crear
        copy=False
    )

    travel_form_id = fields.Many2one(
        'travel.form',
        string="Formulario de Viaje"
    )


    traveler_name = fields.Char(related='travel_form_id.traveler_name.name',
                                string="Nombre y apellidos", readonly=False)


    def action_open_expense(self):
        self.ensure_one()
        if not self.travel_expense_id:
            return {
                'name': _('Crear Planilla de Costos'),
                'type': 'ir.actions.act_window',
                'res_model': 'travel.expense',
                'view_mode': 'form',
                'target': 'current',
                'context': {
                    'default_ticket_id': self.id,
                    'form_view_initial_mode': 'edit'
                }
            }
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'travel.expense',
            'res_id': self.travel_expense_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
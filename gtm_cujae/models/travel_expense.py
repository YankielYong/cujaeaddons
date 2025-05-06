from odoo import api,models, fields
from odoo.exceptions import ValidationError

class TravelExpense(models.Model):
    _name = 'travel.expense'
    _description = "Registro de la información de los costos del viaje"

    name = fields.Char(
        string="Código",
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('travel.expense'),
        copy=False
    )

    ticket_id = fields.Many2one(
        "helpdesk.ticket",
        string="Solicitud de viaje",
        required=True
    )
    traveler_name = fields.Char(related="ticket_id.traveler_name", string="Nombre del solicitante", readonly=True)
    sponsor = fields.Char(string="Encargado de cubrir los gastos")
    ticket_cost = fields.Float(string="Costo del pasaje")
    taxes = fields.Float(string="Impuestos")
    diet_cost = fields.Float(string="Costos de dieta")
    accommodation_cost = fields.Float(string="Costos de alojamiento")
    medical_insurance_cost = fields.Float(string="Costos de seguro médico")
    pocket_money = fields.Float(string="Dinero de bolsillo (efectivo)")
    other_expenses = fields.Float(string="Otros gastos")
    other_expenses_specification = fields.Text(string="Especificación de otros gastos")
    total_travel_cost = fields.Float(
        string="Costo Total",
        compute='_compute_total_travel_cost',
        store=True,
        help="Suma de todos los gastos asociados al viaje"
    )

    @api.constrains(
        'ticket_cost', 'taxes', 'diet_cost', 'accommodation_cost',
        'medical_insurance_cost', 'pocket_money', 'other_expenses'
    )
    def _check_positive_values(self):
        for expense in self:
            error_fields = []

            if expense.ticket_cost and expense.ticket_cost < 0:
                error_fields.append('Costo del pasaje')
            if expense.taxes and expense.taxes < 0:
                error_fields.append('Impuestos')
            if expense.diet_cost and expense.diet_cost < 0:
                error_fields.append('Costos de dieta')
            if expense.accommodation_cost and expense.accommodation_cost < 0:
                error_fields.append('Costos de alojamiento')
            if expense.medical_insurance_cost and expense.medical_insurance_cost < 0:
                error_fields.append('Costos de seguro médico')
            if expense.pocket_money and expense.pocket_money < 0:
                error_fields.append('Dinero de bolsillo')
            if expense.other_expenses and expense.other_expenses < 0:
                error_fields.append('Otros gastos')

            if error_fields:
                raise ValidationError(
                    "Los siguientes campos no pueden tener valores negativos:\n- " +
                    "\n- ".join(error_fields) +
                    "\n\nPor favor ingrese valores mayores o iguales a cero."
                )

    @api.depends('ticket_cost','taxes','diet_cost','accommodation_cost','medical_insurance_cost','pocket_money','other_expenses')
    def _compute_total_travel_cost(self):
        for expense in self:
            expense.total_travel_cost = sum([
                expense.ticket_cost or 0,
                expense.taxes or 0,
                expense.diet_cost or 0,
                expense.accommodation_cost or 0,
                expense.medical_insurance_cost or 0,
                expense.pocket_money or 0,
                expense.other_expenses or 0
            ])

    @api.model
    def create(self, vals):
        # Generación automática de secuencia si no se proporciona
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('travel.expense')

        # Creación normal del registro
        expense = super(TravelExpense, self).create(vals)

        # Si se crea desde ticket (contexto) o tiene ticket_id asignado
        if expense.ticket_id:
            # Actualizar la referencia en el ticket
            expense.ticket_id.travel_expense_id = expense.id
        elif self._context.get('default_ticket_id'):
            # Asignar ticket desde contexto si no venía en vals
            expense.ticket_id = self._context['default_ticket_id']
            expense.ticket_id.travel_expense_id = expense.id

        return expense

    @api.constrains('ticket_id')
    def _check_unique_expense_per_ticket(self):
        for record in self:
            if record.ticket_id and self.search_count([
                ('ticket_id', '=', record.ticket_id.id),
                ('id', '!=', record.id)
            ]) > 0:
                raise ValidationError("Ya existe una planilla de costos para este ticket.")
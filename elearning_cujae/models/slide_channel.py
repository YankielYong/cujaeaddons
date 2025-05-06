from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.tools import is_html_empty


class Channel(models.Model):
    _inherit = 'slide.channel'

    nbr_exam = fields.Integer("Número de exámenes", compute='_compute_slides_statistics', store=True)
    company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
    availability_start_date = fields.Datetime(string="Fecha de Inicio de Disponibilidad", default=fields.Datetime.now)  # Cambio a Datetime
    availability_end_date = fields.Datetime(string="Fecha de Fin de Disponibilidad")  # Cambio a Datetime
    user_ids = fields.Many2many('res.users', string='Responsibles',  default=lambda self: [(4, self.env.user.id)] )

    @api.model
    def _cron_check_course_availability(self):
        """
        Función que se ejecuta diariamente mediante un cron job para verificar la disponibilidad de los cursos.
        Actualiza el campo 'is_published' basándose en las fechas de disponibilidad.
        """
        now = datetime.now()  # Usamos datetime.now() para incluir la hora actual
        courses = self.search([])  # Busca todos los cursos (slide.channel)
        for course in courses:
            if course.availability_start_date and course.availability_end_date:
                if course.availability_start_date <= now <= course.availability_end_date:
                    if not course.is_published:
                        course.write({'is_published': True})
                else:
                    if course.is_published:
                        course.write({'is_published': False})
            elif course.availability_start_date: #Solo fecha de inicio
                if course.availability_start_date <= now:
                    if not course.is_published:
                        course.write({'is_published': True})
                else:
                    if course.is_published:
                        course.write({'is_published': False})
            elif course.availability_end_date: #Solo fecha de fin
                if now <= course.availability_end_date:
                    if not course.is_published:
                        course.write({'is_published': True})
                else:
                    if course.is_published:
                        course.write({'is_published': False})


    @api.constrains('availability_start_date', 'availability_end_date')
    def _check_availability_dates(self):
        """
        Validación para asegurar que la fecha de inicio no sea posterior a la fecha de fin.
        """
        for record in self:
            if record.availability_start_date and record.availability_end_date and record.availability_start_date > record.availability_end_date:
                raise UserError("La fecha de inicio de disponibilidad no puede ser posterior a la fecha de fin.")


    @api.onchange('availability_start_date', 'availability_end_date')
    def _onchange_availability_dates(self):
        """
        Actualiza el estado de 'is_published' cuando cambian las fechas de disponibilidad directamente en el formulario.
        """
        now = datetime.now() # Usamos datetime.now() para incluir la hora actual
        if self.availability_start_date and self.availability_end_date:
            if self.availability_start_date <= now <= self.availability_end_date:
                self.is_published = True
            else:
                self.is_published = False
        elif self.availability_start_date: #Solo fecha de inicio
            if self.availability_start_date <= now:
                self.is_published = True
            else:
                self.is_published = False
        elif self.availability_end_date: #Solo fecha de fin
            if now <= self.availability_end_date:
                self.is_published = True
            else:
                self.is_published = False
        else:
            # Si no hay fechas, no cambiar el estado actual
            pass


    #cambios a user id
    
    @api.depends('upload_group_ids', 'user_ids')  # Cambiar user_id -> user_ids
    @api.depends_context('uid')
    def _compute_can_upload(self):
        for record in self:
            # Verificar si el usuario actual está en user_ids o es superuser
            if self.env.user in record.user_ids or self.env.is_superuser():
                record.can_upload = True
            elif record.upload_group_ids:
                record.can_upload = bool(record.upload_group_ids & self.env.user.groups_id)
            else:
                record.can_upload = self.env.user.has_group('website_slides.group_website_slides_manager')
    
    @api.depends('channel_type', 'user_ids', 'can_upload')  # Cambiar user_id -> user_ids
    @api.depends_context('uid')
    def _compute_can_publish(self):
        for record in self:
            if not record.can_upload:
                record.can_publish = False
            # Verificar si el usuario actual está en user_ids o es superuser
            elif self.env.user in record.user_ids or self.env.is_superuser():
                record.can_publish = True
            else:
                record.can_publish = self.env.user.has_group('website_slides.group_website_slides_manager')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('channel_partner_ids') and not self.env.is_superuser():
                vals['channel_partner_ids'] = [(0, 0, {'partner_id': self.env.user.partner_id.id})]
            if not is_html_empty(vals.get('description')) and is_html_empty(vals.get('description_short')):
                vals['description_short'] = vals['description']

        channels = super().create(vals_list)

        for channel in channels:
            # Agregar todos los usuarios en user_ids como miembros
            if channel.user_ids:  # <--- Cambiar user_id -> user_ids
                partners = channel.user_ids.mapped('partner_id')
                channel._action_add_members(partners)
            if channel.enroll_group_ids:
                channel._add_groups_members()

        return channels
    
    def write(self, vals):
        if 'description' in vals and not is_html_empty(vals['description']) and self.description == self.description_short:
            vals['description_short'] = vals['description']

        res = super().write(vals)

        # Manejar cambios en user_ids (Many2many)
        if 'user_ids' in vals:
            # Obtener todos los partners de los nuevos usuarios
            new_users = self.user_ids - self._origin.user_ids  # Usuarios agregados
            partners = new_users.mapped('partner_id')
            self._action_add_members(partners)
            
            # Reagendar actividades para todos los user_ids
            for user in self.user_ids:
                self.activity_reschedule(
                    ['website_slides.mail_activity_data_access_request'], 
                    new_user_id=user.id
                )

        if 'enroll_group_ids' in vals:
            self._add_groups_members()

        return res
    
    def action_grant_access(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id).exists()
        if partner and self._action_add_members(partner):
            # Buscar actividades para todos los user_ids
            activities = self.activity_search(
                ['website_slides.mail_activity_data_access_request'],
                additional_domain=[
                    ('request_partner_id', '=', partner.id),
                    ('user_id', 'in', self.user_ids.ids)  # <--- Filtrar por todos los responsables
                ]
            )
            activities.action_feedback(feedback=_('Access Granted'))
    
    def action_refuse_access(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id).exists()
        if partner:
            # Buscar actividades para todos los responsables (user_ids)
            activities = self.activity_search(
                ['website_slides.mail_activity_data_access_request'],
                additional_domain=[
                    ('request_partner_id', '=', partner.id),
                    ('user_id', 'in', self.user_ids.ids)  # <--- Filtrar por todos los responsables
            ]
        )
        activities.action_feedback(feedback=_('Access Refused'))
    
    def _action_request_access(self, partner):
        activities = self.env['mail.activity']
        requested_cids = self.sudo().activity_search(
            ['website_slides.mail_activity_data_access_request'],
            additional_domain=[('request_partner_id', '=', partner.id)]
        ).mapped('res_id')
        
        for channel in self:
            if channel.id not in requested_cids and channel.user_ids:  # <--- Cambiar user_id -> user_ids
                # Crear una actividad para cada responsable
                for user in channel.user_ids:
                    activities += channel.activity_schedule(
                        'website_slides.mail_activity_data_access_request',
                        note=_('<b>%s</b> is requesting access to this course. Responsible: %s') % (  # Nota mejorada
                            partner.name, 
                            ", ".join(channel.user_ids.mapped('name'))
                        ),
                        user_id=user.id,  # <--- Asignar a cada responsable
                        request_partner_id=partner.id
                    )
        return activities
        
class ChannelUsersRelation(models.Model):
        _inherit = 'slide.channel.partner'

        channel_user_ids = fields.Many2many('res.users', string='Responsibles', related='channel_id.user_ids')

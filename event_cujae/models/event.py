
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import requests
from html import unescape
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)

class Event(models.Model):
    _inherit = 'event.event'

    organizer_faculty = fields.Many2one(
        'university.faculty',
        string='Facultad Organizadora',
        required=True,
        help='Seleccione la facultad organizadora del evento.'
    )
    responsible_faculty = fields.Many2one(
        'faculty.responsible',
        string="Responsable",
        required=True,
        help='Seleccione el responsable del evento.'
    )
    descripcion = fields.Text(
        string="Descripción",
        help="Proporcione una descripción detallada del evento."
    )
    event_type_name = fields.Char(
        string='Nombre del Tipo de Evento',
        compute='_compute_event_type_name',
        store=True,
    )

    speaker_ids = fields.Many2many('res.partner', string='Ponentes')
    submission_page_url = fields.Char(string='URL para subir trabajos')

    @api.depends('event_type_id.name')
    def _compute_event_type_name(self):
        for record in self:
            record.event_type_name = record.event_type_id.name

    @api.onchange('event_type_id')
    def _onchange_event_type_id(self):
        for record in self:
            if record.event_type_id.name == 'Conferencia':
                record.submission_page_url = False
                return {
                    'domain': {},
                    'warning': {},
                    'value': {
                        'speaker_ids': [(6, 0, [])],
                    },
                }
            elif record.event_type_id.name == 'Científico':
                record.speaker_ids = [(6, 0, [])]
                return {
                    'domain': {},
                    'warning': {},
                    'value': {
                        'submission_page_url': '',
                    },
                }

    @api.model
    def create(self, vals):
        event = super(Event, self).create(vals)
        if event.event_type_id.name == 'Científico':
            self._create_submission_page()
        self._post_to_telegram(event)
        return event

    @staticmethod
    def _clean_html(html_content):
        if not html_content:
            return "Sin descripción"
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator="\n")
        return unescape(text.strip())



    def _post_to_telegram(self, event):
        telegram_bot_token = "7396987561:AAGMjZ-fvWcOFCtk_YILIWAxVLLWdumWHKY"
        telegram_chat_id = "@OdooEvent"

        descripcion = self._clean_html(event.descripcion)
        message = f'📢 ¡Nuevo evento publicado!\n\n' \
                  f'🎉 {event.name}\n' \
                  f'📅 Fecha: {event.date_begin.strftime("%d/%m/%Y %H:%M")}\n' \
                  f'📝 Descripción:\n\n{descripcion}'

        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code != 200:
                raise ValueError(f"Error al publicar en Telegram: {response.text}")
        except requests.ConnectionError:
            raise ValidationError("No se pudo publicar en Telegram porque no hay conexión a internet.")
            event = super(Event, self).create(vals)
            if event.event_type_id.name == 'Científico':
                self._create_submission_page()

    def _create_submission_page(self):
        website = self.env['website'].get_current_website()
        page = self.env['website.page'].create({
            'name': f'Subida de Trabajos - {self.name}',
            'url': f'/event/{self.id}',
            'website_id': website.id,
            'view_id': self.env.ref('event_cujae.view_submission_page').id,
        })
        self.submission_page_url = f"{website.domain}{page.url}"
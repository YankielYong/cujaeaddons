from odoo import models, fields, api, exceptions
import requests
import logging

from odoo.tools.convert import _

_logger = logging.getLogger(__name__)

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    telegram_bot_token = fields.Char(
        string="Token del Bot",
        help="Token obtenido de @BotFather. Ej: '1234567890:ABCdefGhIJKLMNopqrstUVWXYZ'"
    )
    telegram_channel_id = fields.Char(
        string="ID del Grupo/Canal",
        help="ID del grupo/canal"
    )
    enable_telegram = fields.Boolean(string="Activar Telegram")


    # Borrar campos en la base de datos al guardar
    def write(self, vals):
        if 'enable_telegram' in vals and not vals['enable_telegram']:
            vals.update({
                'telegram_bot_token': False,
                'telegram_channel_id': False,
            })
        return super().write(vals)

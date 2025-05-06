from odoo import http
from odoo.http import request

class TelegramController(http.Controller):
    @http.route('/event/telegram', type='http', auth='public')
    def send_telegram_message(self, event_id):
        event = request.env['event.event'].browse(int(event_id))
        event._post_to_telegram()
        return "Mensaje enviado a Telegram"
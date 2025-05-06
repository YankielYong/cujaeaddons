from odoo import models, api, _
import requests
import logging
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError
import time

_logger = logging.getLogger(__name__)

class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    def _send_telegram_notification(self, channel):
        """
        Envía notificación a Telegram con manejo de timeout y reintentos.
        """
        content_type = dict(self._fields['slide_type'].selection).get(self.slide_type, _("Sin tipo"))
    
        # Mensaje con tipo de contenido
        message = _("""
            📢 Nueva publicación en el curso <b>%s</b>:
            🏷️ <b>Título:</b> %s
            📄 <b>Tipo de Contenido:</b> %s
            🔗 <b>Enlace:</b> %s
            """) % (
        channel.name,
        self.name,
        content_type, 
        self.website_url
        )
        
        url = f"https://api.telegram.org/bot{channel.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": channel.telegram_channel_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        max_retries = 3  # Número máximo de reintentos
        timeout = 20  # Aumentar timeout a 20 segundos
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=timeout 
                )
                
                if response.status_code == 200:
                    return  
                else:
                    _logger.error("Error en Telegram (Intento %s): %s - %s", 
                                attempt + 1, 
                                response.status_code, 
                                response.text)
                    
            except (ConnectTimeout, ReadTimeout, ConnectionError) as e:
                _logger.warning("Timeout/Conectividad (Intento %s): %s", attempt + 1, str(e))
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    _logger.error("Fallo después de %s intentos: %s", max_retries, str(e))
            except Exception as e:
                _logger.error("Error inesperado: %s", str(e))
                break

    @api.model
    def _post_publication(self):
        """
        Heredamos la función original y añadimos notificación a Telegram
        """
        # Ejecutar funcionalidad original
        super_result = super(SlideSlide, self)._post_publication()
        
        # Nueva funcionalidad para Telegram
        for slide in self.filtered(lambda s: s.website_published):
            channel = slide.channel_id
            
            if (channel.enable_telegram and 
                channel.telegram_bot_token and 
                channel.telegram_channel_id):
                
                self._send_telegram_notification(channel)
                
        return super_result
import base64
from odoo import http
from odoo.http import request

class SubmissionController(http.Controller):

    @http.route('/event/submit_work', type='http', auth='public', website=True, methods=['POST'])
    def submit_work(self, **post):
        # Obtener los datos del formulario
        event_id = int(post.get('event_id', 0))  # Asegurar que sea un número
        author_name = post.get('author_name', '')
        work_title = post.get('work_title', '')
        attachment = post.get('attachment')  # Archivo subido

        file_base64 = False  # Inicializar la variable

        if attachment:
            file_data = attachment.read()  # Leer el contenido del archivo
            file_base64 = base64.b64encode(file_data).decode('utf-8')  # Convertir a base64

        # Crear el registro en Odoo
        work = request.env['scientific.work'].create({
            'name': work_title,  # Usar el título del trabajo
            'author_name': author_name,
            'event_id': event_id,
            'attachment': file_base64,  # Si no se subió archivo, queda como False
        })

        # Redirigir a una página de confirmación
        return request.redirect('/event/submission_confirmation')

    @http.route('/event/submission_confirmation', type='http', auth='public', website=True)
    def submission_confirmation(self, **kwargs):
        return request.render('event_cujae.submission_confirmation')

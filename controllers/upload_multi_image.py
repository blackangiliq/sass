from odoo import http
from odoo.http import request

class TaskAttachmentController(http.Controller):

    @http.route('/upload', type='http', auth="user", website=True)
    def upload_images_form(self, **post):
        return request.render('sass.upload_images_form_template')

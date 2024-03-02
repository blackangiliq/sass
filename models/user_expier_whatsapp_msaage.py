from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'WhatsApp Message'

    message = fields.Text(string='Message', required=True)

    @api.model
    def create(self, vals):
        existing_record = self.env['whatsapp.message'].search([])
        if existing_record:
            raise ValidationError("Only one WhatsApp message record is allowed.")
        return super(WhatsAppMessage, self).create(vals)

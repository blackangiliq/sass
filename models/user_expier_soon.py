import requests
from odoo import models, fields, api
from datetime import timedelta
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ExpireSoon(models.Model):
    _name = 'expire_soon'
    _description = 'SASS users who will expire soon'

    name = fields.Char(string="User")
    phone = fields.Char(string="Phone")
    expiration = fields.Datetime(string="expiration")
    message = fields.Text(string="Message")
    user_message_status = fields.Boolean(string="Message Status", default=False)

    def get_expired_users(self):
        current_datetime = datetime.now().date()
        expiration_threshold = current_datetime + timedelta(days=3)

        # Delete all existing records in the model
        self.search([]).unlink()

        self.env['sass.users'].search([]).get_and_update_record()

        sass_users = self.env['sass.users'].search(
            [('expiration', '>=', current_datetime), ('expiration', '<=', expiration_threshold)])
        for user in sass_users:
            print(user.name, "is about to expire soon.")
            self.create({
                "name": user.name,
                "phone": user.phone,
                'expiration': user.expiration
            })

    def send_whatsapp_message(self):
        whatsapp_message = self.env['whatsapp.message'].search([], limit=1)
        if not whatsapp_message:
            print("no shit in whatsapp.message model  ")
            return {
                'type': 'ir.actions.act_window',
                'name': 'Create WhatsApp Message',
                'res_model': 'whatsapp.message',
                'view_mode': 'form',
                'target': 'current',
                'context': self.env.context,
            }
        # print(whatsapp_message.message)
        soon_expire_users = self.search([])

        for user in soon_expire_users:
            message_template = whatsapp_message.message
            modified_message1 = message_template.replace('@', f"\n {user.name}\n", 1)
            print(modified_message1)

            phone_number = user.phone
            if phone_number.startswith('0'):
                phone_number = '964' + phone_number[1:]
            whatsapp_server = "http://localhost:3000/api/sendText"
            payload = {
                'phone': phone_number,
                'text': modified_message1 + f" \n I  {user.expiration} I \n ",  # You can customize the message here
                'session': 'default'
            }
            try:
                response = requests.get(whatsapp_server, params=payload)
                response.raise_for_status()  # Raise exception for bad status codes
                data = response.json()
                # print(data)
                print("Message sent successfully to", user.name)
                self.user_message_status = True
            except requests.exceptions.RequestException as e:
                print("Failed to send message to", user.name, "Error:", e)
                self.user_message_status = False

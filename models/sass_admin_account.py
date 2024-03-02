import json

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import models, fields
from odoo import models, fields
import json

class sass_admin_account(models.Model):
    _name = 'setting'
    _description = 'sass setting '

    sendWhatsupMsg = fields.Boolean(
        string='ارسال رسائل الى المستخدمين بعد التفعيل ؟',
    )
    name = fields.Char(string="sass admin user name", required=True)
    sass_password = fields.Char(string="sass admin password", required=True)
    sass_ip = fields.Char(string="sass server ip", required=True)

    ont_admin_user = fields.Char(string="telnet Ont User")
    ont_admin_pass = fields.Char(string="telnet Ont pass")

    area = fields.Many2one('area', string='Area')


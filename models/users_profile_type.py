
from odoo import models, fields, api


class sass(models.Model):
    _name = 'sass.profile'
    _description = 'sass.profile'
    name = fields.Char(string="profile name",required=True)
    price = fields.Float(string="price",required=True)
    priceWithServess = fields.Float(string="with service price ?", required=True)

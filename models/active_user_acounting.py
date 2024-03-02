
from odoo import models, fields, api


class activeUsersThisMonth(models.Model):

    _name = 'active.users'
    _description = 'active users this months'
    name = fields.Char(string="username", required=True)
    price = fields.Float(string="price", required=True)
    priceWithServess = fields.Float(string="with service price ?", required=True)

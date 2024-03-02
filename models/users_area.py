from odoo import models, fields, api

class Area(models.Model):
    _name = 'area'
    _description = 'Area'
    name = fields.Char(string='Area')

class Dist(models.Model):
    _name = 'dist'
    _description = 'dist'
    name = fields.Char(string='dist')

class Street(models.Model):
    _name = 'street'
    _description = 'street'
    name = fields.Char(string='street')
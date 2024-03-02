from odoo import models, fields, api , exceptions

class problem_type(models.Model):
    _name = 'problem.type'
    _description = 'problem type'
    name = fields.Char(string='problem type')
    color = fields.Integer(string='Problem Color')


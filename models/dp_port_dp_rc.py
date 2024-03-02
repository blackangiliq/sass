from odoo import models, fields

class rc(models.Model):
    _name = 'rc'
    _description = 'RC'
    name = fields.Char(string='RC')
    dp_ids = fields.One2many('dp', 'rc_id', string='DB List')


class dp(models.Model):
    _name = 'dp'
    _description = 'DP'
    rc_id = fields.Many2one('rc', string='From RC')
    name = fields.Char(string='DP')


class dp_port(models.Model):
    _name = 'dp_port'
    _description = 'DP Port'
    name = fields.Char(string='DP Port')

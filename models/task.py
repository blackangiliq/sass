from odoo import models, fields, api , exceptions
from odoo.exceptions import ValidationError

class Task(models.Model):
    _name = 'my_module.task'
    _description = 'Task'
    _inherit = 'sass.users'

    name = fields.Many2one('problem.type', required=True,string='Problem Type')
    call_number = fields.Char(string='Call number')
    username = fields.Many2one('sass.users', required=True)
    description = fields.Text(string='وصف المشكلة ')
    description_after_fix = fields.Text(string='تعليق الفني على المشكلة ')
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    color = fields.Integer(string='Color', compute='_compute_color', store=True)
    status = fields.Selection([
        ('new', 'New'),
        ('urgent', 'Urgent'),
        ('on_boarding', 'On-Boarding'),
        ('rescheduled', 'Rescheduled'),
        ('installation_ongoing', 'Installation On-Going'),
        ('task_failed', 'Task Failed'),
        ('task_done', 'Task Done'),
        ('activation_done', 'Activation Done'),
        ('close', 'Close')
    ], string='Status', default='new', required=True, group_expand='read_group_stage_ids')

    attachments = fields.One2many('task.attachment', 'task_id', string='Attachments')

    change_request = fields.One2many('task.change_request', 'task_id', string='change_request')




    firstname = fields.Char(string="firstname",related='username.firstname')
    lastname = fields.Char(string="lastname",related='username.lastname')
    ppoe = fields.Char(string="PPOE",related='username.ppoe')
    Customer_type = fields.Char(string="Customer Type",related='username.Customer_type')
    Whatsup_number = fields.Char(string="whatsup number",related='username.Whatsup_number')
    ont_model = fields.Char(string="Ont Model",related='username.ont_model')
    router_model = fields.Char(string="Router Model",related='username.router_model')
    area = fields.Many2one('area', string='Area',related='username.area',readonly=True)
    dist = fields.Many2one(string="dist",related='username.dist')
    street = fields.Many2one(string="street",related='username.street')
    home = fields.Char(string="home",related='username.home', )

    rc = fields.Many2one(string="rc",related='username.rc')
    dp = fields.Many2one(string="dp",related='username.dp')
    dp_port = fields.Many2one(string="DP Port",related='username.dp_port')

    expiration = fields.Datetime(related='username.expiration',string="expiration")
    profile_type = fields.Many2one(related='username.profile_type', string='نوع الاشتراك',readonly=True)
    phone = fields.Char(string='Phone',related='username.phone')
    location = fields.Char(string='Location', related='username.location')
    lng = fields.Char(string='Lng', related='username.lng', )
    lat = fields.Char(string='Lat', related='username.lat', )

    def read_group_stage_ids(self, states, domain, order):
        return [key for key, _ in self._fields['status'].selection]
    @api.model
    def create(self, values):
        task = super(Task, self).create(values)
        if 'username' in values:
            self.env['sass.users'].search([('id', '=', values['username'])]).write({'task': [(4, task.id)]})
        return task

    @api.depends('name.color')
    def _compute_color(self):
        for task in self:
            task.color = task.name.color


    def upload_image_action(self):
        # Open a file selection dialog in the browser
        return {
            'type': 'ir.actions.act_url',
            'url': 'javascript:document.getElementById("file_input").click();',
            'target': 'self',
        }


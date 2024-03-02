from odoo import models, fields, api, exceptions

class ChangeRequest(models.Model):
    _name = 'task.change_request'
    _description = 'task Change Request'

    task_id = fields.Many2one('my_module.task')
    name = fields.Many2one('sass.users', related='task_id.username', string="Username")


    firstname = fields.Char(string="firstname",related='name.firstname')
    firstname_edite = fields.Char(string="firstname")

    lastname = fields.Char(string="lastname",related='name.lastname')
    lastname_edite = fields.Char(string="lastname")

    ppoe = fields.Char(string="PPOE",related='name.ppoe')
    ppoe_edite = fields.Char(string="PPOE")

    Customer_type = fields.Char(string="Customer Type",related='name.Customer_type')
    Customer_type_edite = fields.Char(string="Customer Type")

    Whatsup_number = fields.Char(string="whatsup number",related='name.Whatsup_number')
    Whatsup_number_edite = fields.Char(string="whatsup number")

    ont_model = fields.Char(string="Ont Model",related='name.ont_model')
    ont_model_edite = fields.Char(string="Ont Model")

    router_model = fields.Char(string="Router Model",related='name.router_model')
    router_model_edite = fields.Char(string="Router Model")

    area = fields.Many2one(string='Area',related='name.area',readonly=True)
    area_edite = fields.Many2one( string='Area',related='name.area')

    dist = fields.Many2one(string="dist",related='name.dist')
    dist_edite = fields.Many2one(string="dist",related='name.dist')

    street = fields.Many2one(string="street",related='name.street')
    street_edite = fields.Many2one(related='name.street',string="street")

    home = fields.Char(string="home",related='name.home', )
    home_edite = fields.Char(string="home")

    rc = fields.Many2one(string="rc",related='name.rc')
    rc_edite = fields.Char(string="rc")

    dp = fields.Many2one(string="dp",related='name.dp')
    dp_edite = fields.Char(string="dp")

    dp_port = fields.Many2one(string="DP Port",related='name.dp_port')
    dp_port_edite = fields.Char(string="DP Port")


    phone = fields.Char(string='Phone',related='name.phone')
    phone_edite = fields.Char(string='Phone')

    location = fields.Char(string='Location', related='name.location')
    location_edite = fields.Char(string='Location', )

    lng = fields.Char(string='Lng', related='name.lng', )
    lng_edite = fields.Char(string='Lng')

    lat = fields.Char(string='Lat', related='name.lat', )
    lat_edite = fields.Char(string='Lat')

    status = fields.Selection([
        ('new', 'New'),
        ('approve', 'approve'),
        ('reject', 'reject')
    ], string='Status', default='new', required=True)

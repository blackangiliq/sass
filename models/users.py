from datetime import datetime, timedelta
from odoo import models, fields, api
import requests
from odoo.exceptions import UserError ,ValidationError
from mac_vendor_lookup import MacLookup

class sass(models.Model):
    _name = 'sass.users'
    _description = 'sass.users'

    name = fields.Char(string='Username')
    userid = fields.Char()
    profile_id = fields.Char()
    firstname = fields.Char(string="firstname")
    lastname = fields.Char(string="lastname")
    ppoe = fields.Char(string="ppoe")
    Customer_type = fields.Char(string="Customer Type")
    SSID = fields.Char(string="SSID")
    Subscription_Place = fields.Char(string="Subscription Place")
    No_Devices = fields.Char(string="No. Devices")
    Whatsup_number = fields.Char(string="whatsup number")
    ont_model = fields.Char(string="Ont Model")
    ont_sn = fields.Char(string="Ont SN")
    router_model = fields.Char(string="Router Model")

    area = fields.Many2one('area', string='Area')
    dist = fields.Many2one('dist',string="Dist")
    street = fields.Many2one('street',string="Street")
    home = fields.Char(string="Home")

    rc = fields.Many2one(comodel_name='rc',string="RC")
    dp = fields.Many2one(comodel_name='dp', string="DP", domain="[('rc_id', '=', rc)]")
    dp_port = fields.Many2one(comodel_name='dp_port',string="DP Port")

    users_in_same_dp = fields.Many2many('sass.users', compute='_get_users_in_same_dp',
                                        string='Users in Same Department')

    expiration_status = fields.Html(string="Status", compute='_compute_status_display')

    fat_location = fields.Char(string="fat_location")
    created_at = fields.Datetime(string="created_at")
    expiration = fields.Datetime(string="expiration")
    profile_type = fields.Many2one(comodel_name='sass.profile', required=True,string='نوع الاشتراك')
    phone = fields.Char(string='Phone')
    location = fields.Char(string='location')
    lng = fields.Char(string='lng')
    lat = fields.Char(string='lat')
    traffic = fields.Char(string="traffic")
    online_status = fields.Boolean(string="Online Status")
    online_ip = fields.Char(string="Online IP")
    online_MAC = fields.Char(string="Online MAC")
    MAC_vendor = fields.Char(string="Vendor MAC", compute='_compute_mac_vendor')

    @api.depends('online_MAC')
    def _compute_mac_vendor(self):
        mac_lookup = MacLookup()
        for record in self:
            if record.online_MAC:
                vendor = mac_lookup.lookup(record.online_MAC)
                record.MAC_vendor = vendor if vendor else ''
            else:
                record.MAC_vendor = ''

    note = fields.Text(string='ملاحضة')
    cal_num = fields.Many2many('user.calnum', string='another call number')
    active_history = fields.Many2many('active.history', string='تاريخ التفعيلات')
    task = fields.One2many('my_module.task', 'username', string='tasks')


    rating = fields.Selection([
        ('1', '1 star'),
        ('2', '2 stars'),
        ('3', '3 stars'),
        ('4', '4 stars'),
        ('5', '5 stars')
    ], string='تقييم اسلوب المشترك')

    pay_rating = fields.Selection([
        ('1', '1 star'),
        ('2', '2 stars'),
        ('3', '3 stars'),
        ('4', '4 stars'),
        ('5', '5 stars')
    ], string='التزام العميل بالدفع')


    def refresh_DP_users(self):
        for user in self:
            if user.dp:
                users_in_same_dp = self.search([('dp', '=', user.dp.id)])
                user.users_in_same_dp = users_in_same_dp.ids
                for user_in_same_dp in users_in_same_dp:
                     print(user_in_same_dp.name)
                     self.refresh_record(user_in_same_dp.name)

    def get_and_update_record(self):
        setting_records = self.env['setting'].search([])
        all_users = []


        if not setting_records:
            raise ValidationError("Please configure settings first.")

        base_url = "http://127.0.0.1:8080/sas/get_user_detels.php"

        for setting_record in setting_records:
            payload = {
                "ip": setting_record.sass_ip,
                "username": setting_record.name,
                "password": setting_record.sass_password,
                "count": 1000,  # Number of records per page
                "page": 1  # Start from page 1
            }
            try:

                while True:
                    response = requests.get(base_url, params=payload)
                    response.raise_for_status()  # Raise exception for bad status codes
                    data = response.json()
                    # Append users from the current page to the list
                    all_users.extend(data.get('data', []))
                    if data.get('next_page_url'):
                        # Update payload for the next page
                        payload['page'] += 1
                    else:
                        break
                for record_data in all_users:

                    # Check if the record already exists in the Odoo model
                    existing_record = self.search([('name', '=', record_data['username'])])

                    # Get the profile type name from the data
                    profile_type_name = record_data.get('profile_details', {}).get('name')

                    # Search for the profile type in Odoo based on its name
                    profile_type = self.env['sass.profile'].search([('name', '=', profile_type_name)], limit=1)


                    if not profile_type:
                        # Handle the case when the profile type is not found
                        # You may want to log a warning or take other actions here
                        continue

                    # Prepare the data for creating or updating the record
                    record_vals = {
                        'profile_id': record_data['profile_id'],
                        'userid': record_data['id'],
                        'name': record_data['username'],
                        'firstname': record_data['firstname'],
                        'lastname': record_data['lastname'],
                        'phone': record_data['phone'],
                        'profile_type': profile_type.id,
                        'area': setting_record.area.id,
                        'online_status': record_data['online_status'],

                        'location': record_data['address'],
                        'expiration': record_data['expiration'],
                        'created_at': record_data['created_at'],
                    }

                    if existing_record:

                        existing_record.write({
                            'profile_id': record_data['profile_id'],
                            'userid': record_data['id'],
                            'phone': record_data['phone'],
                            'profile_type': profile_type.id,
                            'location': record_data['address'],
                            'area': setting_record.area.id,
                            'online_status': record_data['online_status'],

                            'expiration': record_data['expiration'],
                            'created_at': record_data['created_at'],
                        })
                    else:
                        # Create new record
                        self.create(record_vals)


            except requests.exceptions.RequestException as e:
                # Handle any errors that occurred during the request
                print("Error:", e)



    def update_100_last_record(self):
        setting_record = self.env['setting'].search([], limit=1)

        if not setting_record:
            raise ValidationError("Please configure settings first.")

        base_url = "http://127.0.0.1:8080/sas/get_user_detels.php"
        payload = {
            "ip": setting_record.sass_ip,
            "name": setting_record.name,
            "password": setting_record.sass_password,
            "count": 100,  # Number of records per page
            "page": 1  # Start from page 1
        }

        all_users = []

        try:
            response = requests.get(base_url, params=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            data = response.json()

            # Append users from the current page to the list
            all_users.extend(data.get('data', []))

            # Check if there's a next page
            if data.get('next_page_url'):
                # Update payload for the next page
                payload['page'] += 1
            # No more pages, exit the loop

        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the request
            print("Error:", e)
        print(data)

        # Now you have all users in the all_users list, you can process them as needed
        for record_data in all_users:

            # Check if the record already exists in the Odoo model
            existing_record = self.search([('name', '=', record_data['username'])])

            # Get the profile type name from the data
            profile_type_name = record_data.get('profile_details', {}).get('name')

            # Search for the profile type in Odoo based on its name
            profile_type = self.env['sass.profile'].search([('name', '=', profile_type_name)], limit=1)

            if not profile_type:
                # Handle the case when the profile type is not found
                # You may want to log a warning or take other actions here
                continue

            # Prepare the data for creating or updating the record
            record_vals = {
                'profile_id': record_data['profile_id'],
                'userid': record_data['id'],
                'name': record_data['username'],
                'firstname': record_data['firstname'],
                'lastname': record_data['lastname'],
                'phone': record_data['phone'],
                'profile_type': profile_type.id,
                'location': record_data['address'],
                'expiration': record_data['expiration'],
                'created_at': record_data['created_at'],
            }

            if existing_record:
                # Update existing record
                existing_record.write({
                'profile_id': record_data['profile_id'],
                'userid': record_data['id'],
                'phone': record_data['phone'],
                'profile_type': profile_type.id,
                'location': record_data['address'],
                'expiration': record_data['expiration'],
                'created_at': record_data['created_at'],

            })
            else:
                # Create new record
                self.create(record_vals)

    def refresh_record(self, username=None):
        if username is None or username.strip() == '':
            username = self.name

        print(username)
        setting_record = self.env['setting'].search([], limit=1)
        sass_user = self.env['sass.users'].search([('name', '=', username)], limit=1)


        if not setting_record:
            raise ValidationError("Please configure settings first.")

        base_url = "http://127.0.0.1:8080/sas/get_user_detels.php"
        online_base_url = "http://127.0.0.1:8080/sas/get_online_user_deteils.php"
        payload = {
            "ip": setting_record.sass_ip,
            "username": setting_record.name,
            "password": setting_record.sass_password,
            "count": 100,  # Number of records per page
            "search": username,  # Number of records per page
            "page": 1  # Start from page 1
        }
        try:

            onlineIp=''
            response = requests.get(base_url, params=payload)
            online_response = requests.get(online_base_url, params=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            online_response.raise_for_status()  # Raise exception for bad status codes
            data = response.json()
            online_data = online_response.json()
            print(data['data'])
            record_data = data['data'][0]

            online_record_data = online_data.get("data")

            if online_record_data and isinstance(online_record_data, list):
                for record in online_record_data:
                    onlineIp = record.get("framedipaddress")
                    if onlineIp:
                        print("Online IP:", onlineIp)
                    else:
                        print("No Online IP available")
            else:
                # Handle the case when 'data' is empty or not available, or online_record_data is not a list
                print("No online record data available or it's not a list")

            profile_type = self.env['sass.profile'].search([('name', '=', record_data['profile_details']['name'])], limit=1)

            if online_record_data:  # Check if online_record_data is not empty
                if online_record_data[0] is not None:
                    daily_traffic_details = online_record_data[0].get('acctoutputoctets')
                    print(daily_traffic_details)

                    if daily_traffic_details is not None:
                        traffic = daily_traffic_details
                        if traffic >= 1024 ** 3:  # Check if traffic is in gigabytes
                            traffic_str = f"{traffic / (1024 ** 3):.2f} GB"
                        elif traffic >= 1024 ** 2:  # Check if traffic is in megabytes
                            traffic_str = f"{traffic / (1024 ** 2):.2f} MB"
                        elif traffic >= 1024:  # Check if traffic is in kilobytes
                            traffic_str = f"{traffic / 1024:.2f} KB"
                        else:
                            traffic_str = f"{traffic} Bytes"  # Or any appropriate default value
                    else:
                        traffic_str = "None"  # Handle the case when daily_traffic_details is None

                    # Update the 'traffic' field of the `sass_user` record
                    sass_user.write({
                        'traffic': traffic_str,
                        'online_MAC':online_record_data[0].get('callingstationid')
                    })
                else:
                    print("online_record_data[0] is None")
            else:
                print("Online record data is empty or does not contain any elements")

            sass_user.write({
                'profile_id': record_data['profile_id'],
                'userid': record_data['id'],
                'phone': record_data['phone'],
                'profile_type': profile_type.id,
                'location': record_data['address'],
                'expiration': record_data['expiration'],
                'created_at': record_data['created_at'],
                'online_ip': onlineIp,
                'online_status': record_data['online_status']
            })
        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the request
            print("Error:", e)

        pass


    def open_map_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.fat_location,
            'target': 'new'
        }
    def open_online_ip(self):
        print(self.online_ip)
        base_url = 'http://' +self.online_ip
        return {
            'type': 'ir.actions.act_url',
            'url': base_url,
            'target': 'new'
        }

    def _compute_status_display(self):
        current_datetime = fields.Datetime.now()
        for record in self:
            if record.expiration and record.online_status:
                expiration_datetime = fields.Datetime.from_string(record.expiration)
                if expiration_datetime <= current_datetime:
                    record.expiration_status = f'<span style="color: red;">Expired</span> | <span style="color: blue;">Online</span>'
                else:
                    record.expiration_status = '<span style="color: blue;">Active</span> | <span style="color: green;">Online</span>'



            elif record.expiration and not record.online_status:
                expiration_datetime = fields.Datetime.from_string(record.expiration)
                if expiration_datetime <= current_datetime:
                    record.expiration_status = '<span style="color: red;">Expired | Offline</span>'
                else:
                    record.expiration_status = ' <span style="color: blue;">Active</span> | <span style="color: red;">Offline</span>'
            else:
                if record.online_status:
                    record.expiration_status = '<span style="color: orange;">Online</span>'
                else:
                    record.expiration_status = '<span style="color: black;">Offline</span>'

    @api.depends('dp')
    def _get_users_in_same_dp(self):
        for user in self:
            if user.dp:
                users_in_same_dp = self.search([('dp', '=', user.dp.id)])
                user.users_in_same_dp = [(6, 0, users_in_same_dp.ids)]
            else:
                user.users_in_same_dp = False

class UserCalNum(models.Model):
    _name = 'user.calnum'
    _description = 'User CalNUM'
    name = fields.Char(string='Number')

class ActiveHistory(models.Model):
    _name = 'active.history'
    _description = 'active history record'
    name = fields.Datetime(
        string='اخر وقت تفعيل الاشتراك',
        default=lambda self: datetime.now(),
    )

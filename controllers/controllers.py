from odoo.http import request
from odoo import http
import json
from odoo.http import Response

class GetAllSassUser(http.Controller):
    @http.route('/get_cal_num', auth='public', type='http', methods=['GET'])
    def get_cal_num(self, **kw):
        cal_num = kw.get("cal_num")
        print(cal_num)
        response_data = []
        usersphone = request.env['sass.users'].sudo().search([('phone', '=', cal_num)])
        if usersphone:
            for user in usersphone:
                print(user.name)
                for userphone in user:
                    response_data.append({
                        'name': userphone.name,
                        'phone': userphone.phone,
                        'id': userphone.userid,
                        'cal_num': cal_num,
                    })
                response_message = {'message': 'Users found for the specified cal_num.', 'data': response_data}
        else:
            users = request.env['sass.users'].sudo().search([('cal_num', '=', cal_num)])
            print(users)

            if users:
                for user in users:
                    response_data.append({
                        'name': user.name,
                        'phone': user.phone,
                        'id': user.userid,
                        'cal_num': cal_num,
                    })
                response_message = {'message': 'Users found for the specified cal_num.', 'data': response_data}
            else:
                response_message = {'message': 'No users found for the specified cal_num.'}

        return Response(json.dumps(response_message), content_type='application/json')


    @http.route('/add_call_number_to_record', auth='public')
    def add_call_number_to_record(self, **kw):
        # Query all records of the 'sass.users' model
        Sassuser = request.env['sass.users'].sudo().search([])
        file_path = 'C:/Users/Lenovo/Desktop/sas_database/updated_data_users.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Iterate through each user record
            for user in Sassuser:
                if user.phone:
                    matching_data = next((entry for entry in data if entry.get('phone') == user.phone), None)
                    if matching_data:
                        call_numbers = matching_data.get('callNmum')
                        if call_numbers :
                            for number in call_numbers:
                                print("Username:", user.phone)
                                print("Username:", user.name)
                                print("Username:", number)
                                created_calnum = request.env['user.calnum'].sudo().create({'name': number})
                                user.write({'cal_num': [(4, created_calnum.id)]})

        return "done"



    @http.route('/get_fdt', auth='public')
    def get_fdt(self, **kw):
        Sassuser = request.env['sass.users'].sudo().search([])
        file_path = 'C:/Users/Lenovo/Desktop/sas_database/output.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
            for user in Sassuser:
                if user.name:
                    matching_data = next((entry for entry in data if entry.get('username') == user.name), None)
                    if matching_data:
                        jsonfileusername = matching_data.get('username')
                        if jsonfileusername:
                            print(jsonfileusername)
                            print(matching_data['fdt'])
                            print(matching_data['FAT'])
                            print(matching_data['Port'])
                            print(matching_data['fat_location'])
                            # Create or get the RC record
                            rc = request.env['rc'].sudo().search([('name', '=', matching_data['fdt'])])
                            if not rc:
                                rc = request.env['rc'].sudo().create({'name': matching_data['fdt']})
                            # Create or get the DP record
                            dp = request.env['dp'].sudo().search([('name', '=', matching_data['FAT']), ('rc_id', '=', rc.id)])
                            if not dp:
                                dp = request.env['dp'].sudo().create({'name': matching_data['FAT'], 'rc_id': rc.id})
                            # Create or get the DP Port record
                            dp_port = request.env['dp_port'].sudo().search([('name', '=', matching_data['Port'])])
                            if not dp_port:
                                dp_port = request.env['dp_port'].sudo().create({'name': matching_data['Port']})
                            # Update the user record
                            user.write({
                                'rc': rc.id,
                                'dp': dp.id,
                                'dp_port': dp_port.id,
                                'fat_location': matching_data['fat_location'],
                            })
        return "done"



    @http.route('/add_user_calnum', type='http', auth='user', methods=['GET'])
    def add_user_calnum(self, **kwargs):
        username = kwargs.get('username')
        calnums = kwargs.get('calnums')
        print(calnums)
        if not username or not calnums:
            return http.Response('Missing parameters', status=400)
        calnums_list = calnums.split(',')
        user = request.env['sass.users'].sudo().search([('name', '=', username)], limit=1)
        if user:
            created_calnums = []
            for calnum in calnums_list:
                created_calnum = request.env['user.calnum'].sudo().create({'name': calnum})
                created_calnums.append(created_calnum)
            user.write({'cal_num': [(4, calnum.id) for calnum in created_calnums]})
            return http.Response('CalNUMs added and linked successfully', status=200)
        else:
            return http.Response('User not found', status=404)






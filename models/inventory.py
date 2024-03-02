from odoo import models, fields,api

class EmployeeInventory(models.Model):
    _name = 'employee.inventory'
    _description = 'Employee Inventory'

    employee_id = fields.Many2one('res.users', string='Employee')
    item_id = fields.Many2one('inventory', string='Item')
    quantity = fields.Integer(string='Quantity')

    def unlink(self):
        for record in self:
            record.item_id.count += record.quantity
        return super(EmployeeInventory, self).unlink()

    @api.model
    def create(self, vals):
        # Decrease count in inventory when item is added to employee inventory
        item_id = vals.get('item_id')
        quantity = vals.get('quantity', 0)
        if item_id and quantity:
            inventory_item = self.env['inventory'].browse(item_id)
            inventory_item.count -= quantity
        return super(EmployeeInventory, self).create(vals)



class Inventory(models.Model):
    _name = 'inventory'
    _description = 'Inventory'

    name = fields.Char(string='Item Name', required=True)
    count = fields.Integer(string='Item Count')
    price = fields.Float(string='Item Price')
    model = fields.Char(string='Item Model')

from odoo import models, fields, api , exceptions
class TaskAttachment(models.Model):
    _name = 'task.attachment'
    _description = 'Task Attachment'
    task_id = fields.Many2one('my_module.task')
    id_type = fields.Text(string='نوع الصورة')
    image = fields.Image(string='صورة', attachment=True)
    image_preview = fields.Binary(string='Image Preview', compute='_compute_image_preview')

    @api.depends('image')
    def _compute_image_preview(self):
        for attachment in self:
            attachment.image_preview = attachment.image


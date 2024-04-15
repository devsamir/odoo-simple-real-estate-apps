from odoo import models, fields, api
from odoo.exceptions import ValidationError 

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    
    sales_id = fields.Many2one('res.users', required=True)
    
    @api.model_create_multi
    def create(self, val_list):
        for val in val_list:
            sales_person_properties = self.search_count([('sales_id', '=', val.get('sales_id'))])
            if sales_person_properties >= 2:
                raise ValidationError("User already has enough properties assigned to him")
        return super(EstateProperty, self).create(val_list)

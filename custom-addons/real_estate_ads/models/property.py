from odoo import fields, models, api, _

class Property(models.Model):
    _name = 'estate.property'
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'website.published.mixin', 'website.seo.metadata']
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Estate Properties"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancelled')], default='new', string="Status", group_expand='_expand_state')
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    # date_availability = fields.Date(string="Available From", readonly=True)
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Monetary(string="Expected Price", tracking=True)
    best_offer = fields.Monetary(string="Best Offer", compute='_compute_best_price')
    selling_price = fields.Monetary(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facade = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string="Garden Orientation", default="north")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string='Salesman')
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[
        ('is_company', '=', True)
    ])
    buyer_phone = fields.Char(string='Buyer Phone', related='buyer_id.phone')

    total_area = fields.Integer(string="Total Area", compute='_compute_total_area')

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    currency_id = fields.Many2one('res.currency', string="Currency", \
        default=lambda self: self.env.user.company_id.currency_id)

    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
    
    @api.onchange('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0
            
            
    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer'
        }
    
    def action_client_action(self):
        return {
            'type': 'ir.actions.client',
            # 'tag': 'reload',
            # 'tag': 'apps',
            'tag': 'display_notification',
            'params': {
                'title': _('Testing Client'),
                'type': 'success',
                'sticky': False
            }
            
        }
    
    def action_url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://odoo.com',
            'target': 'new'
        }
    
    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'
    
    def _get_report_base_filename(self):
        self.ensure_one()
        return f'Estate Property - {self.name}'
    
    # Override Website URL Function Compute
    def _compute_website_url(self):
        for rec in self:
            rec.website_url = '/properties/%s' % self.name
            
    def _expand_state(self, states, domain, order):
        return [
            key for key, dummy in type(self).state.selection
        ]

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of the property'
    name = fields.Char(string="Name", required=True)


class PropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag of the property'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
    
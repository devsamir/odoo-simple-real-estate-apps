from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class AbstractOffer(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'Abstract Offers'
    
    partner_email = fields.Char(string="Email")
    partner_phone = fields.Char(string="Phone Number")

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _inherit = ['abstract.model.offer']
    _description = 'Estate Property Offers'
    
    @api.depends('partner_id', 'property_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string="Description", compute='_compute_name')
    price = fields.Monetary(string="Price")
    status = fields.Selection(
         [('accepted', 'Accepted'), ('refused', 'Refused')],
         string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string='Validity')
    deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    currency_id = fields.Many2one('res.currency', string="Currency", \
        default=lambda self: self.env.user.company_id.currency_id)
    
    
    def action_accept_offer(self):
        self.status = 'accepted'
        if self.property_id:
            self.property_id.write({
             "selling_price": self.price,
             "state": 'accepted'
            })

            # Refused All Other Offer
            self.search([
                ['property_id', '=', self.property_id.id],
                ['id', '!=', self.id],
            ]).write({
                'status': 'refused'
            })
        
    def action_refused_offer(self):
        self.status = 'refused'

    def extend_offer_deadline(self):
        active_ids = self._context.get('active_ids', [])
        if active_ids:
            offer_ids = self.browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10
    
    def _extend_offer_deadline(self):
        offer_ids = self.search([])
        for offer in offer_ids:
            offer.validity = offer.validity + 1
    
    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string='Create Date', default=_set_create_date)

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False
    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.autovacuum
    def _clean_offers(self):
        self.search([
            ('status', '=', 'refused')
        ]).unlink()

    # @api.model_create_multi
    # def create(self, vals):
    #     for rec in vals:
    #         if not rec.get('creation_date'):
    #             rec['creation_date'] = fields.Date.today()
    #     return super(PropertyOffer, self).create(vals)

    # _sql_constraints = [
    #     ('check_validity', 'check(validity > 0)', 'Deadline cannot be before creation date')
    # ]

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline cannot be before creation date"))    

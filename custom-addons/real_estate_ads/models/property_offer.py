from odoo import fields,models,api
from datetime import timedelta
from odoo.exceptions import ValidationError
class PropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Real Estate Property Offer"

    price=fields.Float(string="price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    validity=fields.Integer(string="Validity")
    creation_date=fields.Date(string="Creation Date")#default=lambda self: fields.Date.today()
    deadline=fields.Date(string="DeadLine",compute="_compute_dedline",inverse="_inverse_dedline")
    partner_id=fields.Many2one("res.partner",string="Customer",required=True)
    property_id=fields.Many2one("estate.property",string="Property",required=True)

    @api.depends("validity","creation_date")
    def _compute_dedline(self):
        for rec in self:
            if rec.creation_date:
                    rec.deadline=rec.creation_date + timedelta(days=rec.validity or 0)
            else:
                rec.deadline=False
    def _inverse_dedline(self):
        for rec in self:
            if rec.creation_date and rec.deadline:
                    rec.validity=(rec.deadline - rec.creation_date).days
            else:
                rec.validity=0
    
    @api.constrains("validity")
    def _constrains_validity(self):
        for rec in self :
         if rec.validity<=0:
          raise ValidationError("The validity of an offer must be a positive number (at least 1 day).")


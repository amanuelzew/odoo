from odoo import fields,models,api
from datetime import timedelta
from odoo.exceptions import ValidationError
class PropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Real Estate Property Offer"
    
    @api.depends("property_id")
    def _computed_name(self):
         for rec in self:
              if rec.partner_id and rec.property_id:
                   rec.name=f"{rec.property_id.name} - {rec.partner_id._name}"
              else:
                   rec.name=False

    name=fields.Char(string="Name",compute=_computed_name)
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
            
    def action_accept_offer(self):
         self._validate_accepted_offer()
         if self.property_id:
              self.property_id.selling_price=self.price
              self.property_id.state="offer_accepted"
         self.status="accepted"
    
    def action_decline_offer(self):
         if all(self.property_id.offer_ids.mapped("status")):
              self.property_id.selling_price=0
              self.property_id.state="cancelled"
         self.status="refused"
    
    def _validate_accepted_offer(self):
         offer_ids=self.env["estate.property.offer"].search([
              ("property_id","=",self.property_id.id),
              ("status","=","accepted")
         ])
         if offer_ids:
              raise ValidationError("You have an accepted offer already")
     #server action    
    def extend_offer_deadline(self):
         for record in self:
             record.validity += 10
          
         """ return {
               "type": "ir.actions.client",
               "tag": "display_notification",
               "params": {
                    "title": "Success",
                    "message": "Deadlines extended by 10 days.",
                    "type": "success",
                    "sticky": False,
               }
          } """

    #cron action
    def _cron_extend_deadline(self):
          # 1. Find all offers that are still 'pending' or 'received'
          # We don't want to extend deadlines for sold or cancelled properties
          offers = self.search([
               ('validity', '>', 0)
          ])
          
          # 2. Call your existing logic on those found records
          for offer in offers:
               offer.validity += 1
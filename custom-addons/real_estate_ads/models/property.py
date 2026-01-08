from odoo import fields,models,api

class Property(models.Model):
    _name="estate.property"
    _description="Real Estate"

    name=fields.Char(string="Name")
    description=fields.Text(string="Description")
    state = fields.Selection([ 
         ("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), 
         ("sold", "Sold"), ("cancelled", "Cancelled"), ], string="Status", default="new")
    postcode=fields.Char(string="PostCode")
    date_availability=fields.Date(string="Available From")
    expected_price=fields.Float(string="Expected price")
    best_offer=fields.Float(string="Best offer")
    selling_price=fields.Float(string="Selling Price")
    bedrooms=fields.Integer(string="BedRooms")
    living_area=fields.Integer(string="Living Area(sqm)")
    facades=fields.Integer(string="Facades")
    garage=fields.Boolean(string="garage",default=False)
    garden=fields.Boolean(string="garden",default=False)
    garden_area=fields.Integer(string="Garden Area")
    garden_orientation=fields.Selection([
        ("north", "North"), ("south", "South"), ("east", "East"), ("west", "West"),
    ],string="Garden Orientation")
    offer_count=fields.Integer(string="Offers",compute="_compute_offer_count")
    type_id=fields.Many2one("estate.property.type",string="Property Type")
    tag_ids=fields.Many2many("estate.property.tag",string="Property Tag")
    offer_ids=fields.One2many("estate.property.offer","property_id",string="offers")
    sales_id=fields.Many2one("res.users",string="Salesman")
    buyer_id=fields.Many2one("res.partner",string="Buyer",domain=[("is_company","=",True)])
    buyer_phone = fields.Char(related="buyer_id.phone", string="Buyer Phone")

    total_area=fields.Integer(string="Total Area")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area=rec.living_area + rec.garden_area

    @api.onchange("living_area","garden_area")
    def _onchange_total_area(self):
            self.total_area=self.living_area + self.garden_area

    @api.depends("offer_ids")
    def _compute_offer_count(self):
         for rec in self:
              rec.offer_count=len(rec.offer_ids)
    
    def action_sold(self):
        self.state="offer_accepted"
    def action_cancel(self):
        self.state="cancelled"
    
    def action_property_view_offers(self):
         return{
              "type":"ir.actions.act_window",
              "name":f"{self.name} - offers",
              "domain":[("property_id","=",self.id)],
              "view_mode":"list,form",
              "res_model": "estate.property.offer",
         }



class PropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"

    name=fields.Char(string="Name",required=True)

class PropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Real Estate Property Tag"

    name=fields.Char(string="Name",required=True)
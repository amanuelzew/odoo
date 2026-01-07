from odoo import fields,models,api

class Property(models.Model):
    _name="estate.property"
    _description="Real Estate"

    name=fields.Char(string="Name")
    description=fields.Text(string="Description")
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
    type_id=fields.Many2one("estate.property.type",string="Property Type")
    tag_ids=fields.Many2many("estate.property.tag",string="Property Tag")
    offer_ids=fields.One2many("estate.property.offer","property_id",string="offers")
    sales_id=fields.Many2one("res.users",string="Salesman")
    buyer_id=fields.Many2one("res.partner",string="Buyer")

    total_area=fields.Integer(string="Total Area")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area=rec.living_area + rec.garden_area

    @api.onchange("living_area","garden_area")
    def _onchange_total_area(self):
            self.total_area=self.living_area + self.garden_area



class PropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"

    name=fields.Char(string="Name",required=True)

class PropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Real Estate Property Tag"

    name=fields.Char(string="Name",required=True)
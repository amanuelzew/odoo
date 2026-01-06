from odoo import fields,models

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
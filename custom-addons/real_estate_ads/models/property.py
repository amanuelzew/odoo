import io
import xlwt
import base64
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
    best_offer=fields.Float(string="Best offer",compute="_compute_best_price")
    selling_price=fields.Float(string="Selling Price",readonly=True)
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
    #smart button
    def action_property_view_offers(self):
         return{
              "type":"ir.actions.act_window",
              "name":f"{self.name} - offers",
              "domain":[("property_id","=",self.id)],
              "view_mode":"list,form",
              "res_model": "estate.property.offer",
          }
      #custom client action 
    def action_client_action(self):
          return {
               "type": "ir.actions.client",
               "tag": "display_notification",#apps,reload
               "params": {
                    "title": "Success!",
                    "message": "The notification has been sent to the client.",
                    "type": "success",  # Options: 'success', 'warning', 'danger', 'info'
                    "sticky": False,    # False means it disappears after a few seconds
                    #'next': {'type': 'ir.actions.client', 'tag': 'reload'}, # Optional: reload
               }
          }
    #url actions
    def action_url_action(self):
          return {
               "type": "ir.actions.act_url",
               "url": "https://www.google.com/search?q=property+in+{}".format(self.postcode or "London"),
               "target": "new"#self
          }
    @api.depends("offer_ids")
    def _compute_best_price(self):
         for rec in self:
              if rec.offer_ids:
                   rec.best_offer=max(rec.offer_ids.mapped("price"))
              else:
                   rec.best_offer=0
     #import export logic              
    def action_import_offers(self):
        """ Opens the import wizard for this property """
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'import',
            'params': {
                'model': 'estate.property.offer',
                'context': {
                    'default_property_id': self.id,
                },
            }
        }

    def action_download_offer_template(self):
        """ Generates Excel Template specifically for this property """
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Offers Template')
        
        # Headers matching your model fields
        # Note: 'property_id/id' allows importing via External ID
        headers = ['property_id/id', 'partner_id/id', 'price', 'validity', 'status']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)
        
        # Row 1: Sample Data
        # Get the external ID of the current property
        prop_ext_id = self.get_external_id().get(self.id) or f"__export__.estate_property_{self.id}"
        
        sheet.write(1, 0, prop_ext_id)
        sheet.write(1, 1, 'base.res_partner_1') # Sample External ID for a partner
        sheet.write(1, 2, self.expected_price)
        sheet.write(1, 3, 7) # Default 7 days validity
        sheet.write(1, 4, 'accepted') # Status options: accepted, refused
        
        workbook.save(output)
        
        attachment = self.env['ir.attachment'].create({
            'name': f'Template_Offers_{self.name}.xls',
            'type': 'binary',
            'datas': base64.b64encode(output.getvalue()),
            'res_model': 'estate.property',
            'res_id': self.id,
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }  


class PropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"

    name=fields.Char(string="Name",required=True)

class PropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Real Estate Property Tag"

    name=fields.Char(string="Name",required=True)
    color=fields.Integer(string="Color")
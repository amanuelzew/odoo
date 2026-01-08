{
    "name":"Real Estate",
    "description":"""Real Estate module""",
    "data":[
        "security/ir.model.access.csv",
        "views/property_view.xml",
        "views/property_type_view.xml",
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        "views/menu_items.xml",
        #data
        "data/estate_property_type_data.xml",
        "data/estate.property.type.csv",
    ],
    'demo': [
        'demo/estate.property.tag.csv',
        'demo/estate_property_demo.xml',
    ],
    "depends":['base'],
    "installable":True,
    'application': True,
    "licence":"LGPL-3",
    "category":"Sales",
    "website":"https://www.hello.com",
    "author":"aman",
    "version":"1.0"
}
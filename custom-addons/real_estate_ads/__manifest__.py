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
        #report
        "report/property_report.xml",
        "report/report_template.xml",
    ],
    'demo': [
        'demo/estate.property.tag.csv',
        'demo/estate_property_demo.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'real_estate_ads/static/src/js/my_custom_action.js',
        'real_estate_ads/static/src/xml/my_custom_action.xml',
        'real_estate_ads/static/src/scss/chatter_custom.scss',
    ],
    },
    "depends":['base','mail'],
    "installable":True,
    'application': True,
    "license":"LGPL-3",
    "category":"Sales",
    "website":"https://www.hello.com",
    "author":"aman",
    "version":"1.0"
}
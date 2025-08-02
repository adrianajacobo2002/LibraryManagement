{
    "name": "Library Management",
    "version": "1.0",
    "summary": "Gestión de socios de biblioteca",
    "category": "Library",
    "author": "Adriana Jacobo",
    "depends": ["base", "mail", "website", "portal", "product", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "security/library_security.xml",
        "views/member_views.xml",
        "views/book_views.xml",
        "views/portal_templates.xml",
        "views/pos_views.xml"
        "data/mail_templates.xml",
    ],
    "controllers":[
        "controllers/portal.py",
        "controllers/pos.py",
    ],
    "installable": True,
    "application": True,
    "assets": {
        "point_of_sale.assets": [
            "library_management/static/src/js/pos_loan.js",
            "library_management/static/src/xml/pos_loan_templates.xml"
        ],
        "web.assets_frontend": [
            "library_management/static/src/js/portal_loan.js",
        ],
    },
}

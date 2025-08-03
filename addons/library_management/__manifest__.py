{
    "name": "Library Management",
    "version": "1.0",
    "summary": "Gestión de socios de biblioteca",
    "category": "Library",
    "author": "Adriana Jacobo",
    "depends": ["base", "mail", "website", "portal", "product", "point_of_sale"],
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/member_views.xml",
        "views/book_views.xml",
        "views/portal_templates.xml",
        "views/portal_books_templates.xml",
        "views/loan_views.xml",
        "data/ir_cron.xml",
        "data/mail_templates.xml",
    ],
    "installable": True,
    "application": True,
    "assets": {
        "point_of_sale.assets": [
            "library_management/static/src/js/pos_loan.js",
            "library_management/static/src/xml/pos_loan_templates.xml"
        ],
    },
}

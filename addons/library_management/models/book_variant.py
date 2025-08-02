from odoo import models, fields

class LibraryBookVariant(models.Model):
    _inherit = 'product.product'

    is_library_book = fields.Boolean(related='product_tmpl_id.is_library_book', store=True)
    is_available = fields.Boolean(related='product_tmpl_id.is_available', store=True)

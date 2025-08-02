from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class LibraryBook(models.Model):
    _inherit = 'product.template'
    _description = 'Libro de la Biblioteca'
    _order = 'publication_date desc, name asc'
    
    name = fields.Char(string='Titulo', required=True, tracking=True)
    author = fields.Char(string='Autor', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', size=13, tracking=True, help="ISBN en formato de 10 o 13 dígitos")
    publication_date = fields.Integer(string='Año de publicación', required=True)
    is_library_book = fields.Boolean(string="¿Es libro de biblioteca?", default=False)
    is_available = fields.Boolean(string='Disponible para préstamo', default=True)
    years_since_publication = fields.Integer(string='Años desde publicación', compute='_compute_years_since_publication', store=True, help="Años transcurridos desde la fecha de publicación")

    list_price = fields.Float(default=0.0)
    sale_ok = fields.Boolean(default=False)
    purchase_ok = fields.Boolean(default=False)
    available_in_pos = fields.Boolean(string="Visible en POS", default=True)
    type = fields.Selection(selection_add=[('product', 'Almacenable')], default='product')
    
    @api.constrains('isbn')
    def _check_isbn(self):
        for book in self:
            if book.isbn:
                isbn = re.sub(r'[-\s]', '', book.isbn)
                if len(isbn) not in (10, 13) or not isbn.isdigit():
                    raise ValidationError("El ISBN debe contener 10 o 13 dígitos numéricos" "Puede incluir guiones, pero estos serán ignorados")
                
    @api.depends('publication_date')
    def _compute_years_since_publication(self):
        current_year = fields.Date.today().year
        for book in self:
            if book.publication_date:
                book.years_since_publication = current_year - book.publication_date
            else:
                book.years_since_publication = 0
                
    @api.onchange('isbn')
    def _onchange_isbn(self):
        self.default_code = self.isbn
        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_library_book'):
                vals['type'] = 'product'
                vals.setdefault('available_in_pos', True)
                vals.setdefault('sale_ok', False)
                vals.setdefault('purchase_ok', False)
                vals.setdefault('list_price', 0.0)
        return super().create(vals_list)


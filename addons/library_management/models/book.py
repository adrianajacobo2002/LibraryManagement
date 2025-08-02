from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Libro de la Biblioteca'
    _order = 'publication_date desc, title asc'
    
    title = fields.Char(string='Titulo', required=True, tracking=True)
    author = fields.Char(string='Autor', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', size=13, tracking=True, help="ISBN en formato de 10 o 13 dígitos")
    publication_date = fields.Integer(string='Año de publicación', required=True)
    active = fields.Boolean(string='Disponible', default=True)
    years_since_publication = fields.Integer(string='Años desde publicación', compute='_compute_years_since_publication', store=True, help="Años transcurridos desde la fecha de publicación")
    
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
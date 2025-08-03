from odoo import http
from odoo.http import request
import json


class LibraryAPI(http.Controller):

    @http.route('/api/book/<string:isbn>', type='json', auth='public', csrf=False)
    def check_book_availability(self, isbn):
        Book = request.env['product.template'].sudo()
        book = Book.search([('isbn', '=', isbn), ('is_library_book', '=', True)], limit=1)

        if not book:
            return {
                'error': 'Libro no encontrado',
                'isbn': isbn
            }

        return {
            'book_id': book.id,
            'isbn': book.isbn,
            'name': book.name,
            'available': book.is_available
        }

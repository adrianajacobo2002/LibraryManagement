from odoo import http
from odoo.http import request

class PosLoanController(http.Controller):
    @http.route('/library/pos/check_member', type='json', auth='user')
    def check_member(self, partner_id):
        member = request.env['library.member'].search([
            ('partner_id', '=', partner_id)
        ], limit=1)
        
        if not member:
            return {'is_member': False}
        
        return {
            'is_member': True,
            'active_loans': len(member.active_loan_ids),
            'member_name': member.name,
            'member_code': member.code
        }
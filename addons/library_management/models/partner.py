from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_library_member = fields.Boolean(string="Es socio de biblioteca")
    library_member_ids = fields.One2many('library.member', 'partner_id')
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class LibraryMember(models.Model):
    _name = 'library.member'
    _inherit = ['mail.thread', 'portal.mixin']
    _description = 'Miembro de Biblioteca'
    _order = 'id asc'
    
    partner_id = fields.Many2one(
        'res.partner',
        string = "Contacto Asociado",
        required = True,
        ondelete = 'restrict',
        domain = [('is_library_member', '=', False)]
    )
    
    loan_ids = fields.One2many(
        'library.loan', 
        'member_id', 
        string='Préstamos'
    )
    
    active_loan_ids = fields.One2many(
        'library.loan',
        'member_id',
        string='Préstamos activos',
        domain=[('state', 'in', ['borrowed', 'overdue'])]
    )
    
    active_loan_count = fields.Integer(compute='_compute_active_loans', string='Préstamos Activos')
    
    first_name = fields.Char(string="Nombre", required=True, tracking=True)
    last_name = fields.Char(string="Apellido", required=True, tracking=True)
    email = fields.Char(string="Email", required=True, tracking=True)
    join_date = fields.Date(string="Fecha de Alta", default=fields.Date.today)
    code = fields.Char(string="Código de socio", readonly=True, copy=False, index=True)
    active = fields.Boolean(default=True)
    
    _sql_constraints = [
        ('unique_member_code', 'UNIQUE(code)', 'Código irrepetible')
    ]
    
    @api.depends('active_loan_ids')
    def _compute_active_loans(self):
        for member in self:
            member.active_loan_count = len(member.active_loan_ids)
    
    def _get_portal_return_action(self):
        return self.env.ref('library_management.portal_my_loans').id
    
    
    @api.model
    def create(self, vals):
        vals['code'] = self._generate_code(vals)
        
        partner_vals = {
            'name': f"{vals.get('first_name', '')} {vals.get('last_name', '')}".strip(),
            'email': vals.get('email'),
            'is_library_member': True,
        }
        
        partner = self.env['res.partner'].create(partner_vals)
        vals['partner_id'] = partner.id
        
        member = super().create(vals)
        member._create_portal_user()
        return member
    
    def write(self, vals):
        if any(field in vals for field in ['first_name', 'last_name', 'email']):
            partner_vals = {}
            if 'first_name' in vals or 'last_name' in vals:
                first = vals.get('first_name', self.first_name)
                last = vals.get('last_name', self.last_name)
                partner_vals['name'] = f"{first} {last}".strip()
            if 'email' in vals:
                partner_vals['email'] = vals['email']
            self.partner_id.write(partner_vals)
        return super().write(vals)
        
    def _generate_code(self, vals):
        year = str(date.today().year)
        initials=(vals.get('first_name', 'X')[0] + vals.get('last_name', 'X')[0]).upper()
        
        existing = self.search_count([
            ('code', 'like', f"{year}-{initials}-%")
        ])
        
        return f"{year}-{initials}-{str(existing + 1).zfill(4)}"
    
    def _create_portal_user(self):
        if not self.partner_id.user_ids and self.active:
            portal_group = self.env.ref('base.group_portal')
            
            user = self.env['res.users'].with_context(
                no_reset_password=False,
                create_user=True
            ).create({
                'name': f"{self.first_name} {self.last_name}",
                'login': self.email,
                'partner_id': self.partner_id.id,
                'groups_id': [(4, portal_group.id)],
                'sel_groups_%s_%s' % (portal_group.id, self.env.ref('base.group_user').id):portal_group.id,
            })
            user.action_reset_password()
            
    def unlink(self):
        raise UserError(_("No se permite borrar registros"))
    
    

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Prestamo de libro"
    _order = "loan_date desc"

    book_id = fields.Many2one(
        "library.book",
        string="Libro",
        required=True,
        domain="[('available', '=', True)]",
    )
    member_id = fields.Many2one(
        "library.member", 
        string="Socio", 
        required=True
    )
    
    pos_order_id = fields.Many2one(
        "pos.order",
        string="Orden POS",
        readonly=True
    )
    
    loan_date = fields.Date(string="Fecha de préstamo", default=fields.Date.today, readonly=True)
    return_date = fields.Date(string="Fecha de devolución")
    due_date = fields.Date(string="Fecha límite", compute="_compute_due_date", store=True)
    state = fields.Selection(
        [("borrowed", "Prestado"), ("returned", "Devuelto"), ("overdue", "Vencido")],
        string="Estado",
        default="borrowed",
        tracking=True,
    )
    
    @api.depends('loan_date')
    def _compute_due_date(self):
        for loan in self:
            if loan.loan_date:
                loan.due_date = loan.loan_date + timedelta(days=30)
    
    @api.model
    def create(self, vals):
        member = self.env['library.member'].browse(vals.get('member_id'))
        if member and len(member.active_loan_ids) >= 5:
            raise ValidationError(_("El socio ya tiene cinco préstamos activos, el límite ha sido alcanzado."))
        
        book = self.env['library.book'].browse(vals.get('book_id'))
        if book and not book.available:
            raise ValidationError(_("El libro seleccionado no está disponible"))
        
        loan = super().create(vals)
        
        if book:
            book.write({'available': False})

        return loan
 
    def action_return_book(self):
        self.ensure_one()
        self.write({
            'return_date':fields.Date.today(),
            'state': 'returned'
        })
        self.book_id.write({'available': True})
        
    def action_renew_loan(self):
        self.ensure_one()
        if self.state != 'borrowed':
            raise ValidationError(_("Solo se pueden renovar prestamos activos"))
        self.write({
            'due_date': self.due_date + timedelta(days=30)
        })
        
    def _cron_check_overdue_loans(self):
        today = fields.Date.today()
        overdue_loans = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '<', today)
        ])
        overdue_loans.write({'state': 'overdue'})
        overdue_loans._send_overdue_notification()

    def _send_overdue_notification(self):
        template = self.env.ref('library_management.email_template_loan_overdue')
        for loan in self:
            template.with_context(
                email_to = loan.member_id.email,
                member_name = loan.member_id.name,
                book_title = loan.book_id.title,
                due_date = loan.due_date
            ).send_mail(loan.id, force_send=True)
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Prestamo de libro"
    _order = "loan_date desc"

    book_id = fields.Many2one(
        "product.template",
        string="Libro",
        required=True,
        domain="[('is_library_book', '=', True), ('is_available', '=', True)]",
    )
    member_id = fields.Many2one("library.member", string="Socio", required=True)

    partner_id = fields.Many2one(
        related="member_id.partner_id", string="Contacto", store=True, readonly=True
    )

    pos_order_id = fields.Many2one("pos.order", string="Orden POS", readonly=True)

    loan_date = fields.Date(
        string="Fecha de préstamo", default=fields.Date.today, readonly=True
    )
    return_date = fields.Date(string="Fecha de devolución")
    due_date = fields.Date(
        string="Fecha límite", compute="_compute_due_date", store=True
    )
    state = fields.Selection(
        [("borrowed", "Prestado"), ("returned", "Devuelto"), ("overdue", "Vencido")],
        string="Estado",
        default="borrowed",
        tracking=True,
    )

    @api.depends("loan_date")
    def _compute_due_date(self):
        for loan in self:
            if loan.loan_date:
                loan.due_date = loan.loan_date + timedelta(days=30)

    @api.model
    def create(self, vals):
        member = self.env["library.member"].browse(vals.get("member_id"))
        if member and len(member.active_loan_ids) >= 5:
            raise ValidationError(
                _(
                    "El socio ya tiene cinco préstamos activos, el límite ha sido alcanzado."
                )
            )

        book = self.env["product.template"].browse(vals.get("book_id"))
        if book and not book.is_available:
            raise ValidationError(_("El libro seleccionado no está disponible"))

        loan = super().create(vals)

        if book:
            book.write({"is_available": False})

        return loan

    def action_return_book(self):
        self.ensure_one()
        if self.state == "returned":
            raise ValidationError("Este préstamo ya ha sido devuelto.")
        self.write({"return_date": fields.Date.today(), "state": "returned"})
        self.book_id.write({"is_available": True})

    def action_renew_loan(self):
        self.ensure_one()
        if self.state != "borrowed":
            raise ValidationError(_("Solo se pueden renovar prestamos activos"))
        self.write({"due_date": self.due_date + timedelta(days=30)})

    def _cron_check_overdue_loans(self):
        today = fields.Date.today()
        overdue_loans = self.search(
            [
                ("state", "=", "borrowed"),
                ("due_date", "<", today),
            ]
        )

        for loan in overdue_loans:
            loan.state = "overdue"
            loan._send_direct_overdue_email()

    def _send_direct_overdue_email(self):
        self.ensure_one()

        if not self.partner_id or not self.partner_id.email:
            _logger.warning(f"Socio sin correo válido para préstamo ID {self.id}")
            return

        subject = f"Préstamo vencido - {self.book_id.name}"
        body = f"""
        <p>Hola {self.partner_id.name},</p>
        <p>El préstamo del libro <strong>{self.book_id.name}</strong> ha vencido desde el {self.due_date}.</p>
        <p>Por favor devuelve el libro lo antes posible.</p>
        <p>Gracias,<br/>Biblioteca</p>
        """

        self.env["mail.mail"].create(
            {
                "subject": subject,
                "body_html": body,
                "email_to": self.partner_id.email,
                "email_from": self.env.user.email or "biblioteca@example.com",
            }
        ).send()

    def action_send_overdue_email(self):
        for loan in self:
            loan._send_direct_overdue_email()

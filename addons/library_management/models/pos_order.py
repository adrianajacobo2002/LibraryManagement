from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = "pos.config"

    module_library_loan = fields.Boolean(
        string="Habilitar préstamos de biblioteca",
        help="Activa la funcionalidad de préstamos en este POS",
    )
    
    def open_ui(self):
        if self.module_library_loan:
            return super(PosConfig, self.with_context(skip_account_check=True)).open_ui()
        return super().open_ui()


class PosOrder(models.Model):
    _inherit = "pos.order"

    loan_ids = fields.One2many(
        "library.loan", "pos_order_id", string="Préstamos asociados"
    )

    def _export_for_ui(self, order):
        result = super()._export_for_ui(order)
        result["loan_ids"] = [
            {
                "id": loan.id,
                "book_id": (loan.book_id.id, loan.book_id.name),
                "loan_date": loan.loan_date,
                "due_date": loan.due_date,
                "return_date": loan.return_date,
                "state": loan.state,
            }
            for loan in order.loan_ids
        ]
        return result

    @api.model
    def create_from_ui(self, orders):
        order_ids = super().create_from_ui(orders)
        for order in self.browse(order_ids):
            if order.config_id.module_library_loan:
                self._create_loans_from_pos(order)
        return order_ids

    def _create_loans_from_pos(self, order):
        member = order.partner_id.library_member_ids[:1]
        if not member:
            return False

        Loan = self.env["library.loan"]
        for line in order.lines.filtered(lambda l: l.product_id.is_book):
            Loan.create(
                {
                    "book_id": line.product_id.book_id.id,
                    "member_id": member.id,
                    "pos_order_id": order.id,
                }
            )
        return True

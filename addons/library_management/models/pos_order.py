from odoo import models, api, fields
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _process_order(self, order, draft, existing_order):
        pos_order = super()._process_order(order, draft, existing_order)
        if isinstance(pos_order, int):
            pos_order = self.browse(pos_order)

        for line in pos_order.lines:
            if line.product_id.is_library_book:
                partner = pos_order.partner_id
                member = partner.library_member_id

                if not member:
                    raise ValidationError("Este cliente no tiene un socio de biblioteca asociado.")

                self.env["library.loan"].create({
                    "book_id": line.product_id.id,
                    "member_id": member.id,
                    "loan_date": fields.Date.today(),
                    "state": "borrowed",
                    "pos_order_id": pos_order.id,
                })

        return pos_order.id

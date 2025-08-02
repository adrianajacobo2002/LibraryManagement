from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_library_member = fields.Boolean(string="Es socio de biblioteca")
    library_member_ids = fields.One2many("library.member", "partner_id")

    library_member_id = fields.Many2one(
        "library.member",
        string="Socio de Biblioteca",
        compute="_compute_library_member",
        store=True,
    )

    @api.depends("library_member_ids")
    def _compute_library_member(self):
        for partner in self:
            partner.library_member_id = (
                partner.library_member_ids[:1].id
                if partner.library_member_ids
                else False
            )

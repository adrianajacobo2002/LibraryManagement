from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
import secrets
import base64

class LibraryMember(models.Model):
    _name = "library.member"
    _inherit = ["mail.thread", "portal.mixin"]
    _description = "Miembro de Biblioteca"
    _order = "id asc"

    partner_id = fields.Many2one(
        "res.partner",
        string="Contacto Asociado",
        required=True,
        ondelete="restrict",
        domain=[("is_library_member", "=", False)],
    )

    loan_ids = fields.One2many("library.loan", "member_id", string="Préstamos")

    active_loan_ids = fields.One2many(
        "library.loan",
        "member_id",
        string="Préstamos activos",
        domain=[("state", "in", ["borrowed", "overdue"])],
    )

    active_loan_count = fields.Integer(
        compute="_compute_active_loans", string="Préstamos Activos"
    )

    first_name = fields.Char(string="Nombre", required=True, tracking=True)
    last_name = fields.Char(string="Apellido", required=True, tracking=True)
    email = fields.Char(string="Email", required=True, tracking=True)
    join_date = fields.Date(string="Fecha de Alta", default=fields.Date.today)
    code = fields.Char(string="Código de socio", readonly=True, copy=False, index=True)
    active = fields.Boolean(default=True)

    access_token = fields.Char(string="Token de acceso al portal", readonly=True)
    portal_url = fields.Char(string="Enlace al Portal", compute="_compute_portal_url")

    _sql_constraints = [("unique_member_code", "UNIQUE(code)", "Código irrepetible")]

    @api.depends("active_loan_ids")
    def _compute_active_loans(self):
        for member in self:
            member.active_loan_count = len(member.active_loan_ids)

    @api.depends("access_token")
    def _compute_portal_url(self):
        for member in self:
            if member.access_token:
                member.portal_url = f"/my/loans?access_token={member.access_token}"
            else:
                member.portal_url = ""

    def _get_portal_return_action(self):
        return self.env.ref("library_management.portal_my_loans").id

    @api.model
    def create(self, vals):
        vals["code"] = self._generate_code(vals)

        if not vals.get("partner_id"):
            partner_vals = {
                "name": f"{vals.get('first_name', '')} {vals.get('last_name', '')}".strip(),
                "email": vals.get("email"),
                "is_library_member": True,
            }
            partner = self.env["res.partner"].create(partner_vals)
            vals["partner_id"] = partner.id
        else:
            partner = self.env["res.partner"].browse(vals["partner_id"])
            partner.write({"is_library_member": True})

        member = super().create(vals)
        member._compute_access_url()
        member._create_portal_user()
        return member

    def write(self, vals):
        if any(field in vals for field in ["first_name", "last_name", "email"]):
            partner_vals = {}
            if "first_name" in vals or "last_name" in vals:
                first = vals.get("first_name", self.first_name)
                last = vals.get("last_name", self.last_name)
                partner_vals["name"] = f"{first} {last}".strip()
            if "email" in vals:
                partner_vals["email"] = vals["email"]
            self.partner_id.write(partner_vals)
        return super().write(vals)

    def _generate_code(self, vals):
        year = str(date.today().year)
        initials = (
            vals.get("first_name", "X")[0] + vals.get("last_name", "X")[0]
        ).upper()

        existing = self.search_count([("code", "like", f"{year}-{initials}-%")])

        return f"{year}-{initials}-{str(existing + 1).zfill(4)}"

    def _create_portal_user(self):
        if not self.partner_id.user_ids and self.active:
            portal_group = self.env.ref("base.group_portal")

            user = (
                self.env["res.users"]
                .with_context(no_reset_password=False, create_user=True)
                .create(
                    {
                        "name": f"{self.first_name} {self.last_name}",
                        "login": self.email,
                        "partner_id": self.partner_id.id,
                        "groups_id": [(4, portal_group.id)],
                        "sel_groups_%s_%s"
                        % (
                            portal_group.id,
                            self.env.ref("base.group_user").id,
                        ): portal_group.id,
                    }
                )
            )
            user.action_reset_password()

    def unlink(self):
        raise UserError(_("No se permite borrar registros"))

    def action_generate_access_token(self):
        for member in self:
            if member.access_token:
                raise UserError("El token ya ha sido generado.")
            token = secrets.token_urlsafe(16)
            member.access_token = base64.urlsafe_b64encode(token.encode()).decode()

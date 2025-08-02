from odoo import http
from odoo.http import request
from datetime import date


class LibraryPortal(http.Controller):

    @http.route("/my/loans", type="http", auth="user", website=True)
    def portal_my_loans(self, **kw):
        if not request.env.user or not request.env.user.partner_id:
            return request.redirect("/my")

        partner = request.env.user.partner_id

        member = (
            request.env["library.member"]
            .sudo()
            .search([("partner_id", "=", partner.id), ("active", "=", True)], limit=1)
        )

        if not member:
            return request.redirect("/my")

        Loan = request.env["library.loan"].sudo()
        loans = Loan.search(
            [
                ("member_id", "=", member.id),
                ("state", "in", ["borrowed", "overdue", "returned"]),
            ],
            order="loan_date desc",
        )

        values = {
            "loans": loans,
            "member": member,
            "today": date.today(),
            "page_name": "my_loans",
            "user": request.env.user,
            "partner": partner,
        }

        values.update(
            request.env["ir.http"]
            .with_context(no_breadcrumbs=False)
            ._prepare_portal_layout_values()
        )

        if kw.get("renewed"):
            values["renew_success"] = True
        if kw.get("error"):
            values["renew_error"] = True

        return request.render("library_management.portal_my_loans", values)

    @http.route("/my/loans/<int:loan_id>/renew", type="http", auth="user", website=True)
    def renew_loan(self, loan_id, **kw):
        if not request.env.user or not request.env.user.partner_id:
            return request.redirect("/my/loans")

        loan = request.env["library.loan"].sudo().browse(loan_id)
        if not loan.exists():
            return request.redirect("/my/loans")

        member = (
            request.env["library.member"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", request.env.user.partner_id.id),
                    ("active", "=", True),
                ],
                limit=1,
            )
        )

        if not member or loan.member_id != member:
            return request.redirect("/my/loans")

        try:
            loan.action_renew_loan()
            return request.redirect("/my/loans?renewed=1")
        except Exception as e:
            return request.redirect("/my/loans?error=1")

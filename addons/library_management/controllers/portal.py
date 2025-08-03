from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date


class LibraryPortal(CustomerPortal):

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

        values.update(self._prepare_portal_layout_values())

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
            loans = request.env["library.loan"].sudo().search([
                ("member_id", "=", member.id),
                ("state", "in", ["borrowed", "overdue", "returned"]),
            ], order="loan_date desc")

            values = {
                "loans": loans,
                "member": member,
                "loan": loan,
                "today": date.today(),
                "renew_success": True,
                "page_name": "my_loans",
            }

            values.update(self._prepare_portal_layout_values())

            return request.render("library_management.portal_my_loans", values)

        except Exception as e:
            return request.redirect("/my/loans?error=1")
        
    @http.route("/my/loans/<int:loan_id>/receipt", type="http", auth="user", website=True)
    def view_receipt(self, loan_id, **kw):
        loan = request.env["library.loan"].sudo().browse(loan_id)

        member = request.env["library.member"].sudo().search([
            ("partner_id", "=", request.env.user.partner_id.id)
        ], limit=1)

        if not loan.exists() or loan.member_id != member:
            return request.redirect("/my/loans")

        return request.render("library_management.portal_loan_receipt", {
            "loan": loan,
            "member": member
        })

    @http.route('/my/books', type='http', auth='user', website=True)
    def portal_available_books(self, **kw):
        if not request.env.user or not request.env.user.partner_id:
            return request.redirect('/my')

        books = request.env['product.template'].sudo().search([
            ('is_library_book', '=', True),
            ('is_available', '=', True)
        ])

        values = {
            'books': books,
            'page_name': 'available_books'
        }
        values.update(self._prepare_portal_layout_values())

        return request.render('library_management.portal_available_books', values)


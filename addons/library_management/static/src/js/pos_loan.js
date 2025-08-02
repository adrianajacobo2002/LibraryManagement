odoo.define('library_management.pos_loan', function(require) {
    "use strict";

    const models = require('point_of_sale.models');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    models.load_fields('pos.order', ['loan_ids']);
    
    class LoanReceipt extends PosComponent {
        constructor() {
            super(...arguments);
            this.loans = this.props.order.get_loans();
        }
        
        get fines() {
            return this.loans.reduce((sum, loan) => sum + (loan.fine || 0), 0);
        }
    }
    LoanReceipt.template = 'LoanReceipt';
    Registries.Component.add(LoanReceipt);

    models.Order = models.Order.extend({
        initialize: function(attributes, options) {
            this._super.apply(this, arguments);
            this.loans = [];
        },
        
        get_loans: function() {
            return this.loan_ids ? this.loan_ids : [];
        },
        
        set_loans: function(loans) {
            this.loan_ids = loans;
        },
        
        add_loan: function(loan) {
            if (!this.loan_ids) this.loan_ids = [];
            this.loan_ids.push(loan);
        }
    });

    const { OrderReceipt } = require('point_of_sale.models');
    Registries.Component.extend(OrderReceipt, {
        template: 'OrderReceipt',
        renderElement: function() {
            this._super.apply(this, arguments);
            if (this.env.pos.config.module_library_loan && this.props.order.get_loans().length > 0) {
                const loanReceipt = new LoanReceipt({
                    order: this.props.order,
                    env: this.env
                });
                loanReceipt.render();
                this.el.querySelector('.receipt-order').before(loanReceipt.el);
            }
        }
    });
});
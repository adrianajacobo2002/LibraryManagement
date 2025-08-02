/** @odoo-module **/

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { OrderWidget } from "@point_of_sale/app/screens/product_screen/order_widget/order_widget";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.env.pos.db.product_by_id = new Proxy(this.env.pos.db.product_by_id, {
            get: (target, id) => {
                const product = target[id];
                return product && product.is_library_book ? product : undefined;
            },
        });
    },
});

patch(OrderWidget.prototype, {
    setup() {
        super.setup();
        this.env.pos.config.iface_tipproduct = false;
        this.env.pos.config.iface_discount = false;
    },
});

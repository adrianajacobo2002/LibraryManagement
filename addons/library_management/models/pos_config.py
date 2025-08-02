from odoo import models


class PosConfig(models.Model):
    _inherit = "pos.config"

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append("product.template")
        return result

    def _loader_params_product_template(self):
        result = super()._loader_params_product_template()
        result["domain"] = [
            ("available_in_pos", "=", True),
            ("is_library_book", "=", True),
            ("is_available", "=", True),
        ]
        result["fields"].extend(["is_library_book", "is_available"])
        return result

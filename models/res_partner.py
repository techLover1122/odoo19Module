from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    client_number = fields.Char(string="Client Number", readonly=True, copy=False)

    # Correct One2many
    product_line_ids = fields.One2many(
        "customer.product.line",
        "partner_id",
        string="Installed Products",
    )

    @api.model
    def create(self, vals):
        # Multiple partner creation
        if isinstance(vals, list):
            for record_vals in vals:
                if not record_vals.get("client_number"):
                    record_vals["client_number"] = (
                        self.env["ir.sequence"].next_by_code("res.partner.client")
                        or "NEW"
                    )
            return super().create(vals)

        # Single partner creation
        if not vals.get("client_number"):
            vals["client_number"] = (
                self.env["ir.sequence"].next_by_code("res.partner.client") or "NEW"
            )

        return super().create(vals)


class CustomerProductLine(models.Model):
    _name = "customer.product.line"
    _description = "Products installed per customer"

    partner_id = fields.Many2one(
        "res.partner", string="Customer", required=True, ondelete="cascade"
    )

    # Basic fields
    product_name = fields.Char(string="Product Name", required=True)
    place = fields.Char(string="Place")
    zone_number = fields.Integer(string="Zone Number")

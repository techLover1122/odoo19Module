# from odoo import models, fields, api


# class ResPartner(models.Model):
#     _inherit = "res.partner"

#     client_number = fields.Char(string="Client Number", readonly=True, copy=False)

#     # Correct One2many
#     product_line_ids = fields.One2many(
#         "customer.product.line",
#         "partner_id",
#         string="Installed Products",
#     )

#     @api.model
#     def create(self, vals):
#         # Multiple partner creation
#         if isinstance(vals, list):
#             for record_vals in vals:
#                 if not record_vals.get("client_number"):
#                     record_vals["client_number"] = (
#                         self.env["ir.sequence"].next_by_code("res.partner.client")
#                         or "NEW"
#                     )
#             return super().create(vals)

#         # Single partner creation
#         if not vals.get("client_number"):
#             vals["client_number"] = (
#                 self.env["ir.sequence"].next_by_code("res.partner.client") or "NEW"
#             )

#         return super().create(vals)


# class CustomerProductLine(models.Model):
#     _name = "customer.product.line"
#     _description = "Products installed per customer"

#     partner_id = fields.Many2one(
#         "res.partner", string="Customer", required=True, ondelete="cascade"
#     )

#     # Basic fields
#     product_name = fields.Char(string="Product Name", required=True)
#     place = fields.Char(string="Place")
#     zone_number = fields.Integer(string="Zone Number")


from odoo import models, fields, api
import io
import xlsxwriter


class ResPartner(models.Model):
    _inherit = "res.partner"

    client_number = fields.Char(string="Client Number", readonly=True, copy=False)

    # One2many to installed products
    product_line_ids = fields.One2many(
        "customer.product.line",
        "partner_id",
        string="Installed Products",
    )

    # Dummy binary field to serve XLSX
    dummy_xlsx = fields.Binary("XLSX", readonly=True)

    @api.model
    def create(self, vals):
        # Handle multiple records
        if isinstance(vals, list):
            for record_vals in vals:
                if not record_vals.get("client_number"):
                    record_vals["client_number"] = (
                        self.env["ir.sequence"].next_by_code("res.partner.client")
                        or "NEW"
                    )
            return super().create(vals)

        # Single record
        if not vals.get("client_number"):
            vals["client_number"] = (
                self.env["ir.sequence"].next_by_code("res.partner.client") or "NEW"
            )
        return super().create(vals)

    def download_installed_products_xlsx(self):
        """Generate XLSX file of installed products for this customer"""
        import base64

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet("Installed Products")

        # Headers
        headers = ["Product Name", "Place", "Zone Number"]
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header)

        # Product lines
        for row_num, line in enumerate(self.product_line_ids, start=1):
            sheet.write(row_num, 0, line.product_name)
            sheet.write(row_num, 1, line.place)
            sheet.write(row_num, 2, line.zone_number)

        workbook.close()
        output.seek(0)
        data = output.read()
        self.dummy_xlsx = base64.b64encode(data)  # <-- FIXED

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/?model=res.partner&id={self.id}&filename=installed_products.xlsx&field=dummy_xlsx&download=true",
            "target": "new",
        }


class CustomerProductLine(models.Model):
    _name = "customer.product.line"
    _description = "Products installed per customer"

    partner_id = fields.Many2one(
        "res.partner", string="Customer", required=True, ondelete="cascade"
    )
    product_name = fields.Char(string="Product Name", required=True)
    place = fields.Char(string="Place (Kitchen, Lobby, etc.)")
    zone_number = fields.Integer(string="Zone Number")

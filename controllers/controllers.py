# from odoo import http


# class CustomerProductManagement(http.Controller):
#     @http.route('/customer_product_management/customer_product_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_product_management/customer_product_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_product_management.listing', {
#             'root': '/customer_product_management/customer_product_management',
#             'objects': http.request.env['customer_product_management.customer_product_management'].search([]),
#         })

#     @http.route('/customer_product_management/customer_product_management/objects/<model("customer_product_management.customer_product_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_product_management.object', {
#             'object': obj
#         })


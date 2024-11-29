from flask_restx import Namespace, Resource, fields
from flask import request, abort
from .service import ProductService
from .schema import product_schema, products_schema
from .error_handler import ApiException

# Inisialisasi Namespace untuk Produk
product_ns = Namespace('Products', description="Manajemen Produk")

# Model untuk dokumentasi Swagger
product_model = product_ns.model(
    'Product',
    {
        'id': fields.Integer(readOnly=True, description="ID Produk"),
        'name': fields.String(required=True, description="Nama Produk"),
        'price': fields.Float(required=True, description="Harga Produk"),
        'description': fields.String(required=True, description="Deskripsi Produk"),
    }
)

# Endpoint untuk mendapatkan semua produk
@product_ns.route('/')
class ProductListResource(Resource):
    @product_ns.doc('get_products')
    @product_ns.marshal_list_with(product_model)
    def get(self):
        """Dapatkan daftar semua produk"""
        products = ProductService.get_all_products()
        return products_schema.dump(products)

    @product_ns.doc('create_product')
    @product_ns.expect(product_model, validate=True)
    @product_ns.marshal_with(product_model, code=201)
    def post(self):
        """Tambahkan produk baru"""
        data = request.get_json()
        if not data.get('name') or not data.get('price') or not data.get('description'):
            raise ApiException("Missing required fields", 400)
        new_product = ProductService.create_product(data)
        return product_schema.dump(new_product), 201


# Endpoint untuk operasi berdasarkan ID produk
@product_ns.route('/<int:product_id>')
@product_ns.param('product_id', 'ID produk')
class ProductResource(Resource):
    @product_ns.doc('get_product')
    @product_ns.marshal_with(product_model)
    def get(self, product_id):
        """Dapatkan produk berdasarkan ID"""
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ApiException("Product not found", 404)
        return product_schema.dump(product)

    @product_ns.doc('update_product')
    @product_ns.expect(product_model, validate=True)
    @product_ns.marshal_with(product_model)
    def put(self, product_id):
        """Perbarui produk berdasarkan ID"""
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ApiException("Product not found", 404)
        data = request.get_json()
        updated_product = ProductService.update_product(product_id, data)
        return product_schema.dump(updated_product)

    @product_ns.doc('delete_product')
    def delete(self, product_id):
        """Hapus produk berdasarkan ID"""
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ApiException("Product not found", 404)
        ProductService.delete_product(product_id)
        return {'message': 'Product deleted successfully'}, 200

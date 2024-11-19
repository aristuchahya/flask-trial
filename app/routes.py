from flask import Blueprint, request, jsonify, abort
from .service import ProductService
from .schema import product_schema, products_schema

product_bp = Blueprint('products', __name__, url_prefix="/api/v1/products")

@product_bp.route('/', methods=['GET'])
def get_products():
    products = ProductService.get_all_products()
    return products_schema.jsonify(products)

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        abort(404, description="Product not found")
    return product_schema.jsonify(product)
    
@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = ProductService.create_product(data)
    return product_schema.jsonify(new_product), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        abort(404, description="Product not found")
    data = request.get_json()
    update_product = ProductService.update_product(product_id, data)
    return product_schema.jsonify(update_product), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        abort(404, description="Product not found")
    ProductService.delete_product(product_id)
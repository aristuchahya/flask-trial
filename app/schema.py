from . import ma
from .models import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
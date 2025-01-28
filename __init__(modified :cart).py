import json
from typing import List

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    # Use list comprehension and `json.loads` for better performance and safety
    items = [
        product_id
        for cart_detail in cart_details
        for product_id in json.loads(cart_detail['contents'])
    ]
    
    # Fetch products in a single operation if possible
    return [products.get_product(product_id) for product_id in items]


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)

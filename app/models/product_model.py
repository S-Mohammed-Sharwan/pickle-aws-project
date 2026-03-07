"""
Product Model
Manages the product catalog using local Python dictionaries.
Includes comments showing how to switch to DynamoDB.
"""

import copy

# ══════════════════════════════════════════════════════════════════════════
# LOCAL DICTIONARY STORAGE (Development)
# Replace with DynamoDB calls when deploying to AWS (see comments below).
# ══════════════════════════════════════════════════════════════════════════

PRODUCTS = {
    "p001": {
        "id": "p001",
        "name": "Mango Pickle (Aam ka Achar)",
        "description": "Traditional homemade mango pickle made with raw mangoes, mustard oil, and aromatic spices. Aged for 30 days for authentic taste.",
        "price": 249.00,
        "category": "Pickles",
        "image": "images/mango_pickle.jpg",
        "stock": 50,
        "featured": True,
    },
    "p002": {
        "id": "p002",
        "name": "Lemon Pickle (Nimbu ka Achar)",
        "description": "Tangy and spicy lemon pickle prepared with fresh lemons, turmeric, red chili powder, and mustard seeds.",
        "price": 199.00,
        "category": "Pickles",
        "image": "images/lemon_pickle.jpg",
        "stock": 40,
        "featured": True,
    },
    "p003": {
        "id": "p003",
        "name": "Mixed Vegetable Pickle",
        "description": "A delightful medley of carrots, cauliflower, green chilies, and turnips pickled in mustard oil with traditional spices.",
        "price": 279.00,
        "category": "Pickles",
        "image": "images/mixed_vegetable_pickle.jpg",
        "stock": 35,
        "featured": False,
    },
    "p004": {
        "id": "p004",
        "name": "Garlic Pickle (Lahsun ka Achar)",
        "description": "Bold and fiery garlic pickle made with whole garlic cloves, red chili, and vinegar. Perfect with parathas.",
        "price": 229.00,
        "category": "Pickles",
        "image": "images/garlic_pickle.jpg",
        "stock": 30,
        "featured": True,
    },
    "p005": {
        "id": "p005",
        "name": "Spicy Banana Chips",
        "description": "Crispy thin-sliced banana chips fried in coconut oil and seasoned with chili and salt. A Kerala specialty.",
        "price": 149.00,
        "category": "Snacks",
        "image": "images/banana_chips.jpg",
        "stock": 60,
        "featured": True,
    },
    "p006": {
        "id": "p006",
        "name": "Masala Peanuts",
        "description": "Crunchy roasted peanuts coated with a spicy chickpea flour batter, seasoned with curry leaves and chili.",
        "price": 129.00,
        "category": "Snacks",
        "image": "images/masala_peanuts.jpg",
        "stock": 75,
        "featured": False,
    },
    "p007": {
        "id": "p007",
        "name": "Murukku (Chakli)",
        "description": "Traditional spiral-shaped crispy snack made from rice flour and urad dal flour, deep fried to perfection.",
        "price": 179.00,
        "category": "Snacks",
        "image": "images/murukku.jpg",
        "stock": 45,
        "featured": True,
    },
    "p008": {
        "id": "p008",
        "name": "Green Chili Pickle (Hari Mirch)",
        "description": "Fiery green chili pickle stuffed with tangy spice mix. For those who love it extra hot!",
        "price": 189.00,
        "category": "Pickles",
        "image": "images/green_chili_pickle.jpg",
        "stock": 25,
        "featured": False,
    },
    "p009": {
        "id": "p009",
        "name": "Sweet Mango Chutney",
        "description": "Sweet and tangy mango chutney made with ripe mangoes, jaggery, and mild spices. Great with snacks.",
        "price": 219.00,
        "category": "Chutneys",
        "image": "images/mango_chutney.jpg",
        "stock": 30,
        "featured": True,
    },
    "p010": {
        "id": "p010",
        "name": "Mixture Namkeen",
        "description": "Classic Indian savory mix with sev, peanuts, lentils, and crispy noodles tossed in chaat masala.",
        "price": 159.00,
        "category": "Snacks",
        "image": "images/mixture_namkeen.jpg",
        "stock": 55,
        "featured": False,
    },
}


def get_all_products():
    """
    Retrieve all products from the catalog.
    Returns a list of product dictionaries.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['products'].scan()
    # return response.get('Items', [])
    """
    return list(copy.deepcopy(PRODUCTS).values())


def get_product(product_id):
    """
    Retrieve a single product by its ID.
    Returns the product dict or None if not found.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['products'].get_item(Key={'id': product_id})
    # return response.get('Item')
    """
    product = PRODUCTS.get(product_id)
    return copy.deepcopy(product) if product else None


def update_inventory(product_id, quantity):
    """
    Reduce the stock of a product by the given quantity.
    Returns True if successful, False if insufficient stock.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['products'].update_item(
    #     Key={'id': product_id},
    #     UpdateExpression='SET stock = stock - :qty',
    #     ConditionExpression='stock >= :qty',
    #     ExpressionAttributeValues={':qty': quantity},
    #     ReturnValues='UPDATED_NEW'
    # )
    """
    product = PRODUCTS.get(product_id)
    if not product:
        return False
    if product["stock"] < quantity:
        return False
    product["stock"] -= quantity
    return True


def get_products_by_category(category):
    """
    Retrieve all products in a specific category.
    Returns a list of product dictionaries.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['products'].scan(
    #     FilterExpression=Attr('category').eq(category)
    # )
    # return response.get('Items', [])
    """
    return [
        copy.deepcopy(p)
        for p in PRODUCTS.values()
        if p["category"].lower() == category.lower()
    ]


def get_featured_products():
    """Retrieve all featured products."""
    return [copy.deepcopy(p) for p in PRODUCTS.values() if p.get("featured")]


def get_categories():
    """Get a list of unique product categories."""
    return list(set(p["category"] for p in PRODUCTS.values()))


def set_stock(product_id, new_stock):
    """
    Admin function: Set the stock of a product to a specific value.
    Returns True if the product exists, False otherwise.
    """
    product = PRODUCTS.get(product_id)
    if not product:
        return False
    product["stock"] = max(0, new_stock)
    return True

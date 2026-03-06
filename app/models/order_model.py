"""
Order Model
Manages customer orders using local Python dictionaries.
Includes comments showing how to switch to DynamoDB.
"""

import uuid
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════
# LOCAL DICTIONARY STORAGE (Development)
# Replace with DynamoDB calls when deploying to AWS (see comments below).
# ══════════════════════════════════════════════════════════════════════════

ORDERS = {}


def create_order(username, items, total_amount):
    """
    Create a new order for a user.
    - items: list of dicts with product_id, name, quantity, price
    - total_amount: total cost of the order
    Returns the order dict.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # order = { ... }
    # dynamodb_tables['orders'].put_item(Item=order)
    # return order
    """
    order_id = "ORD-" + str(uuid.uuid4())[:8].upper()
    order = {
        "order_id": order_id,
        "username": username,
        "items": items,
        "total_amount": total_amount,
        "status": "Confirmed",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Store order indexed by order_id
    ORDERS[order_id] = order
    return order


def get_user_orders(username):
    """
    Retrieve all orders for a specific user, most recent first.
    Returns a list of order dicts.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['orders'].query(
    #     IndexName='username-index',
    #     KeyConditionExpression=Key('username').eq(username)
    # )
    # return sorted(response.get('Items', []),
    #               key=lambda x: x['created_at'], reverse=True)
    """
    user_orders = [
        order for order in ORDERS.values() if order["username"] == username
    ]
    return sorted(user_orders, key=lambda x: x["created_at"], reverse=True)


def get_order(order_id):
    """
    Retrieve a single order by its ID.
    Returns the order dict or None.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['orders'].get_item(Key={'order_id': order_id})
    # return response.get('Item')
    """
    return ORDERS.get(order_id)


def get_all_orders():
    """
    Admin function: Retrieve all orders in the system.
    Returns a list of all order dicts, most recent first.
    """
    return sorted(ORDERS.values(), key=lambda x: x["created_at"], reverse=True)

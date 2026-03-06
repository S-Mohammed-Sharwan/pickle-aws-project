"""
Cart Routes
Manages the shopping cart using Flask sessions.
Supports add, remove, update quantity, and view cart.
"""

from flask import Blueprint, session, redirect, url_for, flash, render_template, request
from app.models.product_model import get_product

cart_bp = Blueprint("cart", __name__)


def _get_cart():
    """Retrieve the cart from the session (dict of product_id -> quantity)."""
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


@cart_bp.route("/cart")
def view_cart():
    """Display the shopping cart with item details and totals."""
    cart = _get_cart()
    cart_items = []
    total = 0.0

    for product_id, quantity in cart.items():
        product = get_product(product_id)
        if product:
            subtotal = product["price"] * quantity
            total += subtotal
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    return render_template("cart.html", cart_items=cart_items, total=total)


@cart_bp.route("/add_to_cart/<product_id>")
def add_to_cart(product_id):
    """Add a product to the cart (or increase quantity by 1)."""
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products.product_list"))

    cart = _get_cart()
    current_qty = cart.get(product_id, 0)

    # ── Check stock availability ───────────────────────────────────────
    if current_qty + 1 > product["stock"]:
        flash(f"Sorry, only {product['stock']} units of {product['name']} available.", "error")
        return redirect(url_for("products.product_list"))

    cart[product_id] = current_qty + 1
    session["cart"] = cart
    session.modified = True

    flash(f"Added {product['name']} to your cart!", "success")
    return redirect(url_for("products.product_list"))


@cart_bp.route("/remove_from_cart/<product_id>")
def remove_from_cart(product_id):
    """Remove a product entirely from the cart."""
    cart = _get_cart()
    if product_id in cart:
        del cart[product_id]
        session["cart"] = cart
        session.modified = True
        flash("Item removed from cart.", "info")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/update_cart/<product_id>", methods=["POST"])
def update_cart(product_id):
    """Update the quantity of a product in the cart."""
    cart = _get_cart()
    try:
        new_qty = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        new_qty = 1

    if new_qty <= 0:
        # Remove item if quantity is zero or negative
        if product_id in cart:
            del cart[product_id]
            flash("Item removed from cart.", "info")
    else:
        product = get_product(product_id)
        if product and new_qty > product["stock"]:
            flash(f"Only {product['stock']} units available.", "error")
            new_qty = product["stock"]
        cart[product_id] = new_qty

    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart.view_cart"))

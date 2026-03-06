"""
Order Routes
Handles checkout, placing orders, order confirmation, and order history.
Also includes an admin inventory dashboard.
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.models.product_model import get_product, update_inventory, get_all_products, set_stock
from app.models.order_model import create_order, get_user_orders, get_all_orders
from app.models.user_model import is_admin

order_bp = Blueprint("orders", __name__)


def _login_required(f):
    """Simple decorator to check if user is logged in."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


@order_bp.route("/checkout")
@_login_required
def checkout():
    """Display checkout summary before placing the order."""
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart.view_cart"))

    cart_items = []
    total = 0.0
    errors = []

    for product_id, quantity in cart.items():
        product = get_product(product_id)
        if product:
            # Check stock availability
            if quantity > product["stock"]:
                errors.append(
                    f"{product['name']} only has {product['stock']} units left (you requested {quantity})."
                )
            subtotal = product["price"] * quantity
            total += subtotal
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    if errors:
        for err in errors:
            flash(err, "error")
        return redirect(url_for("cart.view_cart"))

    return render_template("checkout.html", cart_items=cart_items, total=total)


@order_bp.route("/place_order", methods=["POST"])
@_login_required
def place_order():
    """Process the order: validate stock, reduce inventory, create order, clear cart."""
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart.view_cart"))

    user = session.get("user", {})
    username = user.get("username", "guest")

    order_items = []
    total = 0.0

    # ── Validate and prepare order items ───────────────────────────────
    for product_id, quantity in cart.items():
        product = get_product(product_id)
        if not product:
            flash(f"Product {product_id} not found.", "error")
            return redirect(url_for("cart.view_cart"))

        if quantity > product["stock"]:
            flash(
                f"Insufficient stock for {product['name']}. Only {product['stock']} available.",
                "error",
            )
            return redirect(url_for("cart.view_cart"))

        subtotal = product["price"] * quantity
        total += subtotal
        order_items.append({
            "product_id": product_id,
            "name": product["name"],
            "quantity": quantity,
            "price": product["price"],
            "subtotal": subtotal,
        })

    # ── Reduce inventory for each item ─────────────────────────────────
    for item in order_items:
        success = update_inventory(item["product_id"], item["quantity"])
        if not success:
            flash(f"Failed to process {item['name']}. Please try again.", "error")
            return redirect(url_for("cart.view_cart"))

    # ── Create the order ───────────────────────────────────────────────
    order = create_order(username, order_items, total)

    # ── Clear the cart ─────────────────────────────────────────────────
    session.pop("cart", None)
    session.modified = True

    return redirect(url_for("orders.order_success", order_id=order["order_id"]))


@order_bp.route("/order_success/<order_id>")
@_login_required
def order_success(order_id):
    """Display the order confirmation page."""
    from app.models.order_model import get_order

    order = get_order(order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("products.index"))
    return render_template("order_success.html", order=order)


@order_bp.route("/order_history")
@_login_required
def order_history():
    """Display the user's order history."""
    user = session.get("user", {})
    username = user.get("username", "")
    orders = get_user_orders(username)
    return render_template("order_history.html", orders=orders)


# ══════════════════════════════════════════════════════════════════════════
# ADMIN ROUTES (Bonus Feature)
# ══════════════════════════════════════════════════════════════════════════


@order_bp.route("/admin/dashboard")
@_login_required
def admin_dashboard():
    """Admin inventory dashboard — view products and all orders."""
    user = session.get("user", {})
    if not is_admin(user.get("username", "")):
        flash("Access denied. Admin privileges required.", "error")
        return redirect(url_for("products.index"))

    products = get_all_products()
    orders = get_all_orders()
    return render_template("admin_dashboard.html", products=products, orders=orders)


@order_bp.route("/admin/update_stock/<product_id>", methods=["POST"])
@_login_required
def admin_update_stock(product_id):
    """Admin route: Update stock for a product."""
    user = session.get("user", {})
    if not is_admin(user.get("username", "")):
        flash("Access denied.", "error")
        return redirect(url_for("products.index"))

    try:
        new_stock = int(request.form.get("stock", 0))
    except (ValueError, TypeError):
        new_stock = 0

    success = set_stock(product_id, new_stock)
    if success:
        flash("Stock updated successfully.", "success")
    else:
        flash("Product not found.", "error")

    return redirect(url_for("orders.admin_dashboard"))

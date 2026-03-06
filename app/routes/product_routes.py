"""
Product Routes
Handles the homepage, product catalog, and product detail pages.
"""

from flask import Blueprint, render_template, request
from app.models.product_model import (
    get_all_products,
    get_product,
    get_featured_products,
    get_products_by_category,
    get_categories,
)

product_bp = Blueprint("products", __name__)


@product_bp.route("/")
def index():
    """Homepage — shows featured products and welcome content."""
    featured = get_featured_products()
    return render_template("index.html", featured_products=featured)


@product_bp.route("/products")
def product_list():
    """Product catalog page with optional category filtering."""
    category = request.args.get("category", "").strip()
    categories = get_categories()

    if category:
        products = get_products_by_category(category)
    else:
        products = get_all_products()

    return render_template(
        "products.html",
        products=products,
        categories=categories,
        selected_category=category,
    )


@product_bp.route("/product/<product_id>")
def product_detail(product_id):
    """Single product detail page."""
    product = get_product(product_id)
    if not product:
        return render_template("404.html", message="Product not found."), 404
    return render_template("product_detail.html", product=product)

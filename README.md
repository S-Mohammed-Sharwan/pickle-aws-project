# 🫙 HomeMade Pickles & Snacks

A full-stack Flask e-commerce web application for selling homemade pickles, chutneys, and snacks online. Built with modular architecture, session-based cart, and optional AWS DynamoDB integration.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![AWS](https://img.shields.io/badge/AWS-DynamoDB_Ready-orange?logo=amazon-aws)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **User Auth** | Register, login, logout with session management |
| 🛍️ **Product Catalog** | 10 products across 3 categories with filtering |
| 🛒 **Shopping Cart** | Session-based cart with add/remove/update + stock validation |
| 📦 **Order Processing** | Checkout → inventory reduction → order confirmation |
| 📋 **Order History** | Per-user order history sorted by date |
| ⚙️ **Admin Dashboard** | Inventory management + view all orders |
| ☁️ **DynamoDB Ready** | Commented migration code in every model |

---

## 🗂️ Project Structure

```
homemade-pickles-app/
├── app/
│   ├── __init__.py              # App factory + blueprint registration
│   ├── config.py                # Config (SECRET_KEY, sessions, AWS)
│   ├── extensions.py            # Session init + optional DynamoDB
│   ├── models/
│   │   ├── product_model.py     # Product CRUD + 10 sample products
│   │   ├── user_model.py        # User auth with hashed passwords
│   │   └── order_model.py       # Order management
│   ├── routes/
│   │   ├── auth_routes.py       # /login, /register, /logout
│   │   ├── product_routes.py    # /, /products, /product/<id>
│   │   ├── cart_routes.py       # /cart, /add_to_cart, /remove, /update
│   │   └── order_routes.py      # /checkout, /place_order, /order_success
│   ├── templates/               # 12 Jinja2 HTML templates
│   └── static/
│       └── style.css            # Warm food-themed responsive CSS
├── run.py                       # Dev entry point
├── wsgi.py                      # Production WSGI entry point
├── requirements.txt             # Dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/S-Mohammed-Sharwan/pickle-aws-project.git
cd pickle-aws-project

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open **http://127.0.0.1:5000** in your browser.

### Admin Access

| Username | Password |
|----------|----------|
| `admin`  | `admin123` |

---

## 🛣️ Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with featured products |
| `/products` | GET | Product catalog with category filter |
| `/product/<id>` | GET | Product detail page |
| `/register` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/logout` | GET | Logout |
| `/cart` | GET | View cart |
| `/add_to_cart/<id>` | GET | Add item to cart |
| `/remove_from_cart/<id>` | GET | Remove item from cart |
| `/update_cart/<id>` | POST | Update item quantity |
| `/checkout` | GET | Checkout summary |
| `/place_order` | POST | Place order |
| `/order_success/<id>` | GET | Order confirmation |
| `/order_history` | GET | User's order history |
| `/admin/dashboard` | GET | Admin inventory & orders |
| `/admin/update_stock/<id>` | POST | Update product stock |

---

## ☁️ AWS Deployment

For full step-by-step deployment instructions, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**.

Quick summary:

1. **Create DynamoDB tables** (Products, Users, Orders)
2. **Create IAM Role** with DynamoDB access
3. **Launch EC2** (Ubuntu, t2.micro)
4. **Clone repo and install** dependencies
5. **Set `USE_DYNAMODB=true`** in environment
6. **Configure Gunicorn** as systemd service
7. **Configure Nginx** as reverse proxy
8. **Seed data** into DynamoDB
9. **Access** at `http://<EC2-Public-IP>`

### Run with Gunicorn (EC2)

```bash
gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4
```

### Enable DynamoDB

Set the following environment variables:

```bash
export USE_DYNAMODB=true
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=ap-south-1
```

Every model file contains commented DynamoDB equivalents using `boto3` — simply uncomment to switch from local dictionaries to DynamoDB.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask Blueprints, Flask-Session
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Database:** Python Dictionaries (dev) / AWS DynamoDB (prod)
- **Deployment:** Gunicorn, AWS EC2 compatible

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

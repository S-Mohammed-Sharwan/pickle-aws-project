# 📊 ER Diagram — HomeMade Pickles & Snacks

## ER Diagram Image

![ER Diagram](app/static/images/er_diagram.jpg)

## Entity Relationship Diagram (Mermaid)

```mermaid
erDiagram
    USERS {
        string id PK
        string username UK
        string email
        string password
        string full_name
        boolean is_admin
    }

    PRODUCTS {
        string id PK
        string name
        string description
        float price
        string category
        string image
        int stock
        boolean featured
    }

    ORDERS {
        string order_id PK
        string username FK
        list items
        float total_amount
        string status
        string created_at
    }

    ORDER_ITEMS {
        string product_id FK
        string name
        int quantity
        float price
        float subtotal
    }

    CART_SESSION {
        string session_id PK
        string product_id FK
        int quantity
    }

    USERS ||--o{ ORDERS : "places"
    ORDERS ||--|{ ORDER_ITEMS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "referenced in"
    PRODUCTS ||--o{ CART_SESSION : "added to"
    USERS ||--o| CART_SESSION : "owns"
```

## Data Flow

```mermaid
flowchart LR
    A["👤 User"] -->|Register/Login| B["🔐 Auth"]
    A -->|Browse| C["🛍️ Products"]
    C -->|Add to Cart| D["🛒 Cart (Session)"]
    D -->|Checkout| E["📋 Order"]
    E -->|Reduce Stock| C
    E -->|Save| F["📦 Orders DB"]
    G["⚙️ Admin"] -->|Manage Stock| C
    G -->|View| F
```

## Table Descriptions

| Entity | Storage | Key Fields |
|--------|---------|------------|
| **Users** | `USERS` dict / DynamoDB `HomemadePickles_Users` | `username` (PK), `password` (hashed), `is_admin` |
| **Products** | `PRODUCTS` dict / DynamoDB `HomemadePickles_Products` | `id` (PK), `name`, `price`, `stock`, `category` |
| **Orders** | `ORDERS` dict / DynamoDB `HomemadePickles_Orders` | `order_id` (PK), `username` (GSI), `items[]`, `total_amount` |
| **Cart** | Flask Session (filesystem) | `session_id`, `product_id → quantity` mapping |

## Relationships

| Relationship | Type | Description |
|-------------|------|-------------|
| User → Orders | One-to-Many | A user can place multiple orders |
| Order → Order Items | One-to-Many | Each order contains multiple items |
| Product → Order Items | One-to-Many | A product can appear in many orders |
| User → Cart | One-to-One | Each user session has one cart |
| Product → Cart | Many-to-Many | Multiple products can be in a cart |

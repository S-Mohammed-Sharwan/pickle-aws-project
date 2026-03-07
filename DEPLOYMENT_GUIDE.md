# 🚀 AWS Deployment Guide — HomeMade Pickles & Snacks

Complete step-by-step guide to deploy the application on **AWS EC2** with **DynamoDB** as the database.

---

## 📋 Architecture Overview

```
User → Internet → EC2 (Flask + Gunicorn) → DynamoDB
                    ↓
              Static Files (S3 optional)
```

| Component | AWS Service |
|-----------|-------------|
| Web Server | EC2 (Ubuntu) |
| App Server | Gunicorn + Flask |
| Database | DynamoDB |
| Reverse Proxy | Nginx |

---

## Step 1: Create DynamoDB Tables

Go to **AWS Console → DynamoDB → Create Table** and create these 3 tables:

### Table 1: `HomemadePickles_Products`
| Setting | Value |
|---------|-------|
| Table name | `HomemadePickles_Products` |
| Partition key | `id` (String) |

### Table 2: `HomemadePickles_Users`
| Setting | Value |
|---------|-------|
| Table name | `HomemadePickles_Users` |
| Partition key | `username` (String) |

### Table 3: `HomemadePickles_Orders`
| Setting | Value |
|---------|-------|
| Table name | `HomemadePickles_Orders` |
| Partition key | `order_id` (String) |
| GSI (Global Secondary Index) | Index name: `username-index`, Partition key: `username` (String) |

> **Capacity Mode:** Select **On-Demand** for all tables (no capacity planning needed).

---

## Step 2: Create IAM Role for EC2

1. Go to **AWS Console → IAM → Roles → Create Role**
2. Select **AWS Service → EC2**
3. Attach policy: **AmazonDynamoDBFullAccess**
4. Name: `HomemadePickles-EC2-Role`
5. Create role

---

## Step 3: Launch EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**

| Setting | Recommended Value |
|---------|-------------------|
| Name | `HomemadePickles-Server` |
| AMI | Ubuntu Server 22.04 LTS |
| Instance type | `t2.micro` (Free Tier) |
| Key pair | Create or select existing |
| Security Group | Allow **SSH (22)**, **HTTP (80)**, **HTTPS (443)** |
| IAM Instance Profile | `HomemadePickles-EC2-Role` |

2. Click **Launch Instance**

---

## Step 4: Connect to EC2 & Install Dependencies

```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@<EC2-Public-IP>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv nginx git -y
```

---

## Step 5: Deploy the Application

```bash
# Clone the repository
cd /home/ubuntu
git clone https://github.com/S-Mohammed-Sharwan/pickle-aws-project.git
cd pickle-aws-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 6: Set Environment Variables

Create an environment file:

```bash
sudo nano /home/ubuntu/pickle-aws-project/.env
```

Add the following:

```env
SECRET_KEY=your-strong-secret-key-here-change-this
USE_DYNAMODB=true
AWS_REGION=ap-south-1
FLASK_DEBUG=false

# If NOT using IAM Role (not recommended), add credentials:
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
```

> **Note:** If you attached the IAM Role in Step 3, you do NOT need AWS credentials — boto3 picks them up automatically from the instance metadata.

Create a systemd service to load the env file (covered in Step 7).

---

## Step 7: Configure Gunicorn as a Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/homemadepickles.service
```

Paste this:

```ini
[Unit]
Description=HomeMade Pickles Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/pickle-aws-project
EnvironmentFile=/home/ubuntu/pickle-aws-project/.env
ExecStart=/home/ubuntu/pickle-aws-project/venv/bin/gunicorn wsgi:app --bind 127.0.0.1:8000 --workers 3 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable homemadepickles
sudo systemctl start homemadepickles
sudo systemctl status homemadepickles
```

---

## Step 8: Configure Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/homemadepickles
```

Paste this:

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/pickle-aws-project/app/static/;
        expires 30d;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/homemadepickles /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 9: Seed Initial Data (Optional)

Create a seed script to populate DynamoDB with products:

```bash
cd /home/ubuntu/pickle-aws-project
source venv/bin/activate
python3 -c "
import boto3, os
os.environ['USE_DYNAMODB'] = 'true'

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('HomemadePickles_Products')

products = [
    {'id': 'p001', 'name': 'Mango Pickle (Aam ka Achar)', 'description': 'Traditional homemade mango pickle.', 'price': '249.00', 'category': 'Pickles', 'image': 'images/mango_pickle.jpg', 'stock': 50, 'featured': True},
    {'id': 'p002', 'name': 'Lemon Pickle', 'description': 'Tangy and spicy lemon pickle.', 'price': '199.00', 'category': 'Pickles', 'image': 'images/lemon_pickle.jpg', 'stock': 40, 'featured': True},
    {'id': 'p003', 'name': 'Mixed Vegetable Pickle', 'description': 'Medley of carrots, cauliflower, green chilies.', 'price': '279.00', 'category': 'Pickles', 'image': 'images/mixed_vegetable_pickle.jpg', 'stock': 35, 'featured': False},
    {'id': 'p004', 'name': 'Garlic Pickle', 'description': 'Bold and fiery garlic pickle.', 'price': '229.00', 'category': 'Pickles', 'image': 'images/garlic_pickle.jpg', 'stock': 30, 'featured': True},
    {'id': 'p005', 'name': 'Spicy Banana Chips', 'description': 'Crispy banana chips, Kerala style.', 'price': '149.00', 'category': 'Snacks', 'image': 'images/banana_chips.jpg', 'stock': 60, 'featured': True},
    {'id': 'p006', 'name': 'Masala Peanuts', 'description': 'Crunchy roasted masala peanuts.', 'price': '129.00', 'category': 'Snacks', 'image': 'images/masala_peanuts.jpg', 'stock': 75, 'featured': False},
    {'id': 'p007', 'name': 'Murukku (Chakli)', 'description': 'Traditional spiral crispy snack.', 'price': '179.00', 'category': 'Snacks', 'image': 'images/murukku.jpg', 'stock': 45, 'featured': True},
    {'id': 'p008', 'name': 'Green Chili Pickle', 'description': 'Fiery stuffed green chili pickle.', 'price': '189.00', 'category': 'Pickles', 'image': 'images/green_chili_pickle.jpg', 'stock': 25, 'featured': False},
    {'id': 'p009', 'name': 'Sweet Mango Chutney', 'description': 'Sweet and tangy mango chutney.', 'price': '219.00', 'category': 'Chutneys', 'image': 'images/mango_chutney.jpg', 'stock': 30, 'featured': True},
    {'id': 'p010', 'name': 'Mixture Namkeen', 'description': 'Classic Indian savory mix.', 'price': '159.00', 'category': 'Snacks', 'image': 'images/mixture_namkeen.jpg', 'stock': 55, 'featured': False},
]

for p in products:
    table.put_item(Item=p)
    print(f'Added: {p[\"name\"]}')

# Seed admin user
import hashlib
users_table = dynamodb.Table('HomemadePickles_Users')
users_table.put_item(Item={
    'id': 'admin',
    'username': 'admin',
    'email': 'admin@homemadepickles.com',
    'password': hashlib.sha256('admin123'.encode()).hexdigest(),
    'full_name': 'Admin User',
    'is_admin': True
})
print('Admin user seeded.')
"
```

---

## Step 10: Access Your Application

Open a browser and visit:

```
http://<EC2-Public-IP>
```

---

## ✅ Verification Checklist

| Step | Check |
|------|-------|
| DynamoDB tables created | 3 tables visible in AWS Console |
| EC2 instance running | Status: `running` in EC2 dashboard |
| Gunicorn running | `sudo systemctl status homemadepickles` shows `active` |
| Nginx running | `sudo systemctl status nginx` shows `active` |
| App accessible | Visit `http://<EC2-IP>` in browser |
| Admin login works | Login with `admin` / `admin123` |

---

## 🔄 How to Update the App

```bash
ssh -i your-key.pem ubuntu@<EC2-Public-IP>
cd /home/ubuntu/pickle-aws-project
git pull origin main
sudo systemctl restart homemadepickles
```

---

## 🛑 Common Issues

| Problem | Solution |
|---------|----------|
| 502 Bad Gateway | Check gunicorn: `sudo systemctl status homemadepickles` |
| DynamoDB AccessDenied | Verify IAM role is attached to EC2 |
| App not loading | Check security group allows port 80 |
| Static files not loading | Verify Nginx `location /static/` path |

---

## 💰 Estimated Cost (Free Tier Eligible)

| Service | Free Tier |
|---------|-----------|
| EC2 t2.micro | 750 hours/month free (12 months) |
| DynamoDB On-Demand | 25 GB storage + 25 WCU/RCU free |
| Data Transfer | 15 GB/month free |

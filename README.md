# Price Tracker Dashboard

![Project Banner](app/static/images/app_images/dashboard.png)

## 📌 Overview
A Flask-based web application that tracks product prices, displays historical trends, and predicts future prices using machine learning.

## ✨ Features
- **User Authentication**: Sign up, login, and logout functionality
- **Dashboard**: Interactive price visualization
  - 4-month historical price trends
  - 7-day price forecasts
- **Product Management**: View and track products

## 📊 Database Schema
```mermaid
erDiagram
    USERS {
        int id PK
        string username
        string email
        string password_hash
        datetime created_at
    }
    
    PRODUCTS ||--o{ PRICE_HISTORY : "1-to-Many"
    PRODUCTS {
        int id PK
        string name
        string category
        string image_url
        string last_update
    }
    
    PRICE_HISTORY {
        int id PK
        int product_id FK
        float price
        date date
    }
```
## 🛠️ Technologies
- **Backend**: 
  - Python 3.9
  - Flask 3.1.0
  - Flask-Login 0.6.3
  - SQLAlchemy 2.0.39
- **Frontend**:
  - HTML5, CSS3
  - Chart.js
- **Database**: PostgreSQL
- **Machine Learning**: scikit-learn 1.6.1

## 📂 Project Structure
```
price-tracker/
├── app/
│   ├── __init__.py
│   ├──  models.py
│   ├──  forms.py
│   ├──  routes.py
│   ├──  views.py
│   ├── scrapy_scrawler/
│   │   └── amazon_scraper.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── login/
│       ├── ├── base.html
│       │   ├── login.html
│       │   └── register.html
│       └── dashboard/
│           ├── base.html
│           └── dashboard.html
├── migrations/
├── ml/
├── scripts/
├── requirements.txt
├── config.py
├── run.py
└── .env
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 15+

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AliBakhshi274/price-tracker.git
   cd price-tracker
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   touch .env
   ```
   Edit `.env` with your credentials:
   ```ini
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://username:password@localhost:5000/price_tracker
   ```

5. Initialize database:
   ```bash
    python scripts/migrate.py migrate
    python scripts/migrate.py upgrade

   flask shell
   >> from scripts.seed_db_scrapy import *
   ```

6. Run the application:
   ```bash
   flask run
   ```
   
## 🌟 Usage
1. **Sign Up**: Create a new account at `/signup`
2. **Login**: Access your dashboard at `/login`
3. **Dashboard**:
   - View price history charts
   - See 7-day price predictions
   - Browse products

## 📈 Screenshots
| Sign Up Page                                        | Sgin In Page                                  |
|-----------------------------------------------------|-----------------------------------------------|
| ![Sign Up](app/static/images/app_images/signup.png/) | ![Sign In](app/static/images/app_images/signin.png) |

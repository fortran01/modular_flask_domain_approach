# modular_flask_domain_approach

This project implements a Customer Loyalty Program Management system, specifically addressing the Point Accrual Problem using a domain model approach. It features a modular Flask application that manages customer interactions, product catalog, and loyalty transactions to accrue and redeem points based on defined rules.

## Features

- User authentication (login and logout)
- Shopping cart management (add to cart, update cart display)
- Checkout process with points calculation
- Product catalog with detailed product information and categorization
- Loyalty account management to track and update customer points
- Point transactions recorded
- Dynamic point earning rules based on product categories and transaction dates
- Database seeding with initial data for customers, products, categories, and point rules

## Setup

- Clone the repository
- Create a virtual environment

```bash
python -m venv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

Activate the virtual environment:

```bash
source venv/bin/activate
```

### Test with a database

To create the SQLite database, you need to run the `loyalty_app.py` script directly. This is necessary because the Flask CLI does not automatically execute the code that initializes and seeds the database. By running the script directly, you ensure that the database setup code within the `app.app_context()` block is executed.

Here are the steps to run the script using the Python CLI:

1. Activate the virtual environment:

```bash
source venv/bin/activate
```

1. Run the script directly:

```bash
cd ../
ls # should see the loyalty_app.py file
python -m modular_flask.loyalty_app
```

To create the database and tables, the following code is used in `loyalty_app.py`:

```python
with app.app_context():
    db.create_all()
```

To seed the database with sample data, the `seed_database` function is used. This function is defined in the `seed_database.py` file and is responsible for adding sample customers, categories, products, loyalty accounts, and point earning rules to the database.

The `seed_database` function is called in the `loyalty_app.py` file when the Flask application starts, and it checks if the database is empty (e.g., no customers). If the database is empty, it seeds the database with the sample data.

Here is the relevant code snippet from `loyalty_app.py`:

```python
# Check if the database is empty (e.g., no customers)
if db.session.query(Customers).count() == 0:
    seed_database(db)
    print("Database seeded successfully")
```

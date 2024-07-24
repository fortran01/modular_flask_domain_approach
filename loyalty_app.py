from flask import Flask, request, jsonify, render_template, Response
from .models import (db, Customers, Products)
import os
from typing import List, Optional
# Import the seed_database function
from .seed_database import seed_database
from .repositories import (CustomerRepository, LoyaltyAccountRepository,
                           ProductRepository, PointTransactionRepository,
                           CategoryRepository)
from .services import LoyaltyService

app: Flask = Flask(__name__)
# Set a secret key for session handling
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# The SQLite database is located in the 'instance' folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loyalty_program.db'
db.init_app(app)

# Create the tables in the database if they don't exist and seed if necessary
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully")
        # Check if the database is empty (e.g., no customers)
        if db.session.query(Customers).count() == 0:
            seed_database(db)
            print("Database seeded successfully")

        # Initialize repositories and service
        customer_repo = CustomerRepository(db.session())
        loyalty_account_repo = LoyaltyAccountRepository(db.session())
        product_repo = ProductRepository(db.session())
        transaction_repo = PointTransactionRepository(db.session())
        category_repo = CategoryRepository(db.session())

        loyalty_service = LoyaltyService(
            customer_repo, loyalty_account_repo, product_repo,
            transaction_repo, category_repo)
    except Exception as e:
        print(f"Database creation or seeding failed: {e}")


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: Rendered HTML of the index page.
    """
    customer_id = request.cookies.get('customer_id', None)
    if customer_id:
        products: List[Products] = db.session.query(Products).all()
        return render_template('index.html', products=products, logged_in=True,
                               customer_id=customer_id)
    else:
        return render_template('index.html', logged_in=False)


@app.route('/login', methods=['POST'])
def login() -> Response:
    """
    Handle customer login.

    Returns:
        Response: JSON response indicating success or failure of login.
    """
    if not request.json or 'customer_id' not in request.json:
        app.logger.error("Login attempt without customer_id")
        response: Response = jsonify(
            {'success': False, 'error': 'Missing customer ID'})
        response.status_code = 400
        return response

    customer_id: str = request.json['customer_id']
    app.logger.debug(f"Attempting login for customer_id: {customer_id}")

    customer: Optional[Customers] = db.session.query(
        Customers).get(customer_id)
    if customer:
        response = jsonify({'success': True})
        response.set_cookie('customer_id', customer_id)
        app.logger.debug(f"Login successful for customer_id: {customer_id}")
        return response
    else:
        app.logger.error(
            f"Invalid login attempt for customer_id: {customer_id}")
        response = jsonify(
            {'success': False, 'error': 'Invalid customer ID'})
        response.status_code = 401
        return response


@app.route('/logout')
def logout() -> Response:
    """
    Handle customer logout.

    Returns:
        Response: JSON response indicating success of logout.
    """
    response: Response = jsonify({'success': True})
    response.delete_cookie('customer_id')
    return response


@app.route('/checkout', methods=['POST'])
def checkout() -> Response:
    """
    Handle checkout process.

    Returns:
        Response: JSON response with total points earned and a success message
        or an error message.
    """
    if 'customer_id' not in request.cookies:
        response = jsonify({"error": "Customer not logged in"})
        response.status_code = 401
        return response

    customer_id: int = int(request.cookies['customer_id'])
    product_ids: List[int] = request.json.get(
        'product_ids', []) if request.json else []

    response_data, status_code = loyalty_service.process_checkout(
        customer_id, product_ids)
    response = jsonify(response_data)
    response.status_code = status_code
    return response


if __name__ == '__main__':
    print("Debug mode is:", app.debug)
    app.run(debug=True)

from .models import (
    Customers,
    Products,
    Categories,
    LoyaltyAccounts,
    PointEarningRules,
)
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal


def seed_database(db: SQLAlchemy) -> None:
    """
    Seed the database with sample data including customers, categories,
    products, loyalty accounts, and point earning rules.
    """
    # Adding sample customers
    customer1: Customers = Customers(
        name="John Doe", email="john.doe@example.com")
    customer2: Customers = Customers(
        name="Jane Smith", email="jane.smith@example.com")

    # Adding sample categories
    category1: Categories = Categories(name="Electronics")
    category2: Categories = Categories(name="Books")

    # Adding a default category
    default_category: Categories = Categories(id=0, name="Default")

    # Adding sample products
    product1: Products = Products(
        name="Laptop",
        price=Decimal('1200.00'),
        category=category1,
        image_url=("https://upload.wikimedia.org/wikipedia/commons/e/e9/"
                   "Apple-desk-laptop-macbook-pro_%2823699397893%29.jpg")
    )
    product2: Products = Products(
        name="Science Fiction Book",
        price=Decimal('15.99'),
        category=category2,
        image_url=("https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/"
                   "Eric_Frank_Russell_-_Die_Gro%C3%9Fe_Explosion_-_Cover.jpg/"
                   "770px-Eric_Frank_Russell_-_Die_Gro%C3%9Fe_Explosion_-_Cove"
                   "r.jpg?20130713192345")
    )

    # Adding sample loyalty accounts
    loyalty_account1: LoyaltyAccounts = LoyaltyAccounts(
        customer=customer1, points=100)
    loyalty_account2: LoyaltyAccounts = LoyaltyAccounts(
        customer=customer2, points=200)

    # Adding a default point earning rule
    default_rule: PointEarningRules = PointEarningRules(
        category=default_category, points_per_dollar=1,
        start_date=date(1900, 1, 1), end_date=date(2099, 12, 31))

    # Adding sample point earning rules
    rule1: PointEarningRules = PointEarningRules(
        category=category1, points_per_dollar=2, start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31))
    rule2: PointEarningRules = PointEarningRules(
        category=category2, points_per_dollar=1, start_date=date(
            2024, 1, 1), end_date=date(2024, 12, 31))

    # Adding to session
    db.session.add_all([customer1, customer2, default_category, category1,
                        category2, product1, product2, loyalty_account1,
                        loyalty_account2, default_rule, rule1, rule2])

    # Committing the session to the database
    db.session.commit()

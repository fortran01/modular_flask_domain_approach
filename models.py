# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey

Base = declarative_base()

db = SQLAlchemy(model_class=Base)


class Customers(Base):
    """
    Represents a customer in the database.

    Attributes:
        id (int): The primary key.
        name (str): The name of the customer.
        email (str): The email address of the customer.
        loyalty_account (LoyaltyAccounts): A relationship to the customer's
            loyalty account.
    """
    __tablename__ = 'Customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    loyalty_account = relationship(
        'LoyaltyAccounts', uselist=False, back_populates='customer')


class LoyaltyAccounts(Base):
    """
    Represents a loyalty account in the database.

    Attributes:
        id (int): The primary key.
        customer_id (int): Foreign key to the associated customer.
        points (int): The current loyalty points balance.
        customer (Customers): A relationship to the associated customer.
        transactions (list of PointTransactions): A list of transactions
            associated with this account.
    """
    __tablename__ = 'LoyaltyAccounts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'))
    points = Column(Integer, default=0)
    customer = relationship('Customers', back_populates='loyalty_account')
    transactions = relationship(
        'PointTransactions', back_populates='loyalty_account')


class PointTransactions(Base):
    """
    Represents a transaction that affects loyalty points in the database.

    Attributes:
        id (int): The primary key.
        loyalty_account_id (int): Foreign key to the associated loyalty
            account.
        product_id (int): Foreign key to the associated product.
        points_earned (int): The number of points earned in this transaction.
        transaction_date (Date): The date of the transaction.
        loyalty_account (LoyaltyAccounts): A relationship to the associated
        loyalty account.
        product (Products): A relationship to the associated product.
    """
    __tablename__ = 'PointTransactions'
    id = Column(Integer, primary_key=True)
    loyalty_account_id = Column(Integer, ForeignKey('LoyaltyAccounts.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    points_earned = Column(Integer)
    transaction_date = Column(Date)
    loyalty_account = relationship(
        'LoyaltyAccounts', back_populates='transactions')
    product = relationship('Products', back_populates='transactions')


class Products(Base):
    """
    Represents a product in the database.

    Attributes:
        id (int): The primary key.
        name (str): The name of the product.
        price (Numeric): The price of the product.
        category_id (int): Foreign key to the associated category.
        image_url (str): URL to the product's image.
        category (Categories): A relationship to the associated category.
        transactions (list of PointTransactions): A list of transactions
        associated with this product.
    """
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Numeric(10, 2))
    category_id = Column(Integer, ForeignKey('Categories.id'))
    image_url = Column(String(255))
    category = relationship('Categories', back_populates='products')
    transactions = relationship('PointTransactions', back_populates='product')


class Categories(Base):
    """
    Represents a product category in the database.

    Attributes:
        id (int): The primary key.
        name (str): The name of the category.
        products (list of Products): A list of products in this category.
        point_earning_rules (list of PointEarningRules): A list of point
            earning rules associated with this category.
    """
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    products = relationship('Products', back_populates='category')
    point_earning_rules = relationship(
        'PointEarningRules', back_populates='category')


class PointEarningRules(Base):
    """
    Represents a rule for earning points based on purchases within a specific
    category in the database.

    Attributes:
        id (int): The primary key.
        category_id (int): Foreign key to the associated category.
        points_per_dollar (int): The number of points earned per dollar spent.
        start_date (Date): The start date of the rule's validity.
        end_date (Date): The end date of the rule's validity.
        category (Categories): A relationship to the associated category.
    """
    __tablename__ = 'PointEarningRules'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('Categories.id'))
    points_per_dollar = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    category = relationship('Categories', back_populates='point_earning_rules')

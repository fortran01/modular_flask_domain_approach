# repositories.py

from typing import Optional
from sqlalchemy.orm import Session
from .models import (
    Customers, LoyaltyAccounts, Products, Categories,
    PointEarningRules, PointTransactions
)
from .domain_models import (
    Customer, LoyaltyAccount, Product, Category,
    PointEarningRule, PointTransaction
)
from datetime import date


class CustomerRepository:
    """
    Repository for performing database operations on the Customers table.
    """

    def __init__(self, session: Session):
        """
        Initializes the CustomerRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Retrieves a customer by their ID.

        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns:
            Optional[Customer]: The retrieved customer or None if not found.
        """
        customer_model = self.session.query(Customers).get(customer_id)
        if customer_model:
            return Customer(
                customer_model.id,
                customer_model.name,
                customer_model.email
            )
        return None


class LoyaltyAccountRepository:
    """
    Repository for performing database operations on the LoyaltyAccounts table.
    """

    def __init__(self, session: Session):
        """
        Initializes the LoyaltyAccountRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_by_customer_id(self, customer_id: int) -> Optional[LoyaltyAccount]:
        """
        Retrieves a loyalty account by customer ID.

        Args:
            customer_id (int): The ID of the customer whose loyalty account
            to retrieve.

        Returns:
            Optional[LoyaltyAccount]: The retrieved loyalty account or None
            if not found.
        """
        account_model = self.session.query(LoyaltyAccounts).filter_by(
            customer_id=customer_id).first()
        if account_model:
            customer = Customer(
                account_model.customer.id,
                account_model.customer.name,
                account_model.customer.email
            )
            account_id = int(account_model.id)
            points = int(account_model.points)
            return LoyaltyAccount(
                account_id, customer, points
            )
        return None

    def update(self, loyalty_account: LoyaltyAccount) -> None:
        """
        Updates a loyalty account in the database.

        Args:
            loyalty_account (LoyaltyAccount): The loyalty account to update.
        """
        account_model = self.session.query(
            LoyaltyAccounts).get(loyalty_account.id)
        if account_model:
            account_model.points = loyalty_account.points
            self.session.commit()


class ProductRepository:
    """
    Repository for performing database operations on the Products table.
    """

    def __init__(self, session: Session):
        """
        Initializes the ProductRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Retrieves a product by its ID.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            Optional[Product]: The retrieved product or None if not found.
        """
        product_model = self.session.query(Products).get(product_id)
        if product_model:
            category = Category(product_model.category_id,
                                product_model.category.name)
            return Product(
                product_model.id,
                product_model.name,
                product_model.price,
                category,
                product_model.category_id,
                product_model.image_url
            )
        return None


class CategoryRepository:
    """
    Repository for performing database operations on the Categories table.
    """

    def __init__(self, session: Session):
        """
        Initializes the CategoryRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_by_id(self, category_id: Optional[int]) -> Optional[Category]:
        """
        Retrieves a category by its ID.

        Args:
            category_id (Optional[int]): The ID of the category to retrieve.

        Returns:
            Optional[Category]: The retrieved category or None if not found.
        """
        category_model = self.session.query(Categories).get(category_id)
        if category_model:
            category = Category(category_model.id, category_model.name)
            # Look up the applicable PointEarningRule for that category
            # Assuming for now only the latest rule is applicable
            point_earning_rule_model = self.session.query(
                PointEarningRules
            ).filter_by(
                category_id=category.id
            ).order_by(
                PointEarningRules.start_date.desc()
            ).first()
            if point_earning_rule_model:
                rule = PointEarningRule(
                    point_earning_rule_model.id,
                    category,
                    point_earning_rule_model.points_per_dollar,
                    point_earning_rule_model.start_date,
                    point_earning_rule_model.end_date
                )
                category.add_point_earning_rule(rule)
            return category
        return None


class PointTransactionRepository:
    """
    Repository for performing database operations on the
    PointTransactions table.
    """

    def __init__(self, session: Session):
        """
        Initializes the PointTransactionRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, transaction: PointTransaction) -> None:
        """
        Creates a new point transaction in the database.

        Args:
            transaction (PointTransaction): The transaction to create.
        """
        transaction_model = PointTransactions(
            loyalty_account_id=transaction.loyalty_account.id,
            product_id=transaction.product.id,
            points_earned=transaction.points_earned,
            transaction_date=transaction.transaction_date
        )
        self.session.add(transaction_model)
        self.session.commit()


class PointEarningRuleRepository:
    """
    Repository for performing database operations on the
    PointEarningRules table.
    """

    def __init__(self, session: Session):
        """
        Initializes the PointEarningRuleRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_active_rule(self, category_id: int,
                        transaction_date: date) -> Optional[PointEarningRule]:
        """
        Retrieves the active point earning rule for a category on a given date.

        Args:
            category_id (int): The ID of the category.
            transaction_date (date): The date for which the rule is applicable.

        Returns:
            Optional[PointEarningRule]: The active rule or None if not found.
        """
        rule_model = self.session.query(PointEarningRules).filter(
            PointEarningRules.category_id == category_id,
            PointEarningRules.start_date <= transaction_date,
            PointEarningRules.end_date >= transaction_date
        ).first()

        if rule_model:
            category = Category(rule_model.category.id,
                                rule_model.category.name)
            return PointEarningRule(int(rule_model.id), category,
                                    rule_model.points_per_dollar,
                                    rule_model.start_date,
                                    rule_model.end_date)
        return None

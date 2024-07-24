# domain_models.py

from datetime import date
from decimal import Decimal
from typing import List, Optional


class Customer:
    """Represents a customer with an optional loyalty account."""

    def __init__(self, id: int, name: Optional[str], email: Optional[str]):
        self.id: int = id
        self.name: Optional[str] = name
        self.email: Optional[str] = email
        self.loyalty_account: Optional[LoyaltyAccount] = None


class LoyaltyAccount:
    """Represents a loyalty account associated with a customer."""

    def __init__(self, id: int, customer: Customer, points: int = 0):
        self.id: int = id
        self.customer: Customer = customer
        self.points: int = points
        self.transactions: List[PointTransaction] = []

    def add_points(self, points: int) -> None:
        """Adds points to the loyalty account."""
        self.points += points

    def add_transaction(self, transaction: 'PointTransaction') -> None:
        """Adds a transaction to the list of transactions."""
        self.transactions.append(transaction)


class Product:
    """Represents a product with optional category and pricing information."""

    def __init__(self, id: int, name: Optional[str], price: Optional[Decimal],
                 category: Optional['Category'], category_id: Optional[int],
                 image_url: Optional[str]):
        self.id: int = id
        self.name: Optional[str] = name
        self.price: Optional[Decimal] = price
        self.category: Optional['Category'] = category
        self.category_id: Optional[int] = category_id
        self.image_url: Optional[str] = image_url


class Category:
    """Represents a product category with associated point earning rules."""

    def __init__(self, id: Optional[int], name: Optional[str]):
        self.id: Optional[int] = id
        self.name: Optional[str] = name
        self.point_earning_rules: List[PointEarningRule] = []

    def add_point_earning_rule(self, rule: 'PointEarningRule') -> None:
        """Adds a point earning rule to the category."""
        self.point_earning_rules.append(rule)

    def get_active_rule(self, date: date) -> Optional['PointEarningRule']:
        """
        Returns the active point earning rule for the category on a
        given date.
        """
        for rule in self.point_earning_rules:
            if (rule.start_date is None or rule.start_date <= date) and \
               (rule.end_date is None or date <= rule.end_date):
                return rule
        return None


class PointEarningRule:
    """
    Defines a rule for earning points based on purchases in a
    specificcategory.
    """

    def __init__(self, id: int, category: Category,
                 points_per_dollar: Optional[int],
                 start_date: Optional[date],
                 end_date: Optional[date]):
        self.id: int = id
        self.category: Category = category
        self.points_per_dollar: Optional[int] = points_per_dollar
        self.start_date: Optional[date] = start_date
        self.end_date: Optional[date] = end_date


class PointTransaction:
    """Represents a transaction where points are earned or spent."""

    def __init__(self, loyalty_account: LoyaltyAccount,
                 product: Product, points_earned: int,
                 transaction_date: date):
        self.loyalty_account: LoyaltyAccount = loyalty_account
        self.product: Product = product
        self.points_earned: int = points_earned
        self.transaction_date: date = transaction_date


class PointCalculator:
    """
    Provides functionality to calculate points based on product and
    transaction date.
    """
    @staticmethod
    def calculate_points(product: Product, transaction_date: date) -> int:
        """
        Calculates the points earned from a transaction based on the
        product and date.
        """
        if product.category is not None:
            rule = product.category.get_active_rule(transaction_date)
            if rule and rule.points_per_dollar and product.price:
                return int(product.price * rule.points_per_dollar)
        return 0

# domain_models.py

from datetime import date
from decimal import Decimal
from typing import List, Optional


class Customer:
    def __init__(self, id: int, name: Optional[str], email: Optional[str]):
        self.id = id
        self.name = name
        self.email = email
        self.loyalty_account: Optional[LoyaltyAccount] = None


class LoyaltyAccount:
    def __init__(self, id: int, customer: Customer, points: int = 0):
        self.id = id
        self.customer = customer
        self.points = points
        self.transactions: List[PointTransaction] = []

    def add_points(self, points: int) -> None:
        self.points += points

    def add_transaction(self, transaction: 'PointTransaction') -> None:
        self.transactions.append(transaction)


class Product:
    def __init__(self, id: int, name: Optional[str], price: Optional[Decimal],
                 category: Optional['Category'], category_id: Optional[int],
                 image_url: Optional[str]):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.category_id = category_id
        self.image_url = image_url


class Category:
    def __init__(self, id: Optional[int], name: Optional[str]):
        self.id = id
        self.name = name
        self.point_earning_rules: List[PointEarningRule] = []

    def add_point_earning_rule(self, rule: 'PointEarningRule') -> None:
        self.point_earning_rules.append(rule)

    def get_active_rule(self, date: date) -> Optional['PointEarningRule']:
        print(f"Getting active rule for {self.name} on {date}")
        for rule in self.point_earning_rules:
            print(f"Checking rule {rule.id} with start date {
                  rule.start_date} and end date {rule.end_date}")
            if (rule.start_date is None or rule.start_date <= date) and \
               (rule.end_date is None or date <= rule.end_date):
                return rule
        return None


class PointEarningRule:
    def __init__(self, id: int, category: Category,
                 points_per_dollar: Optional[int],
                 start_date: Optional[date],
                 end_date: Optional[date]):
        self.id = id
        self.category = category
        self.points_per_dollar = points_per_dollar
        self.start_date = start_date
        self.end_date = end_date


class PointTransaction:
    def __init__(self, loyalty_account: LoyaltyAccount,
                 product: Product, points_earned: int,
                 transaction_date: date):
        self.loyalty_account = loyalty_account
        self.product = product
        self.points_earned = points_earned
        self.transaction_date = transaction_date


class PointCalculator:
    @staticmethod
    def calculate_points(product: Product, transaction_date: date) -> int:
        if product.category is not None:
            rule = product.category.get_active_rule(transaction_date)
            if rule and rule.points_per_dollar and product.price:
                return int(product.price * rule.points_per_dollar)
        return 0

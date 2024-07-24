# services.py

from typing import List, Dict, Any, Tuple
from datetime import date
from .domain_models import (
    LoyaltyAccount, Product, PointTransaction, PointCalculator
)
from .repositories import (
    CustomerRepository, LoyaltyAccountRepository,
    ProductRepository, PointTransactionRepository, CategoryRepository
)


class LoyaltyService:
    def __init__(self,
                 customer_repo: CustomerRepository,
                 loyalty_account_repo: LoyaltyAccountRepository,
                 product_repo: ProductRepository,
                 transaction_repo: PointTransactionRepository,
                 category_repo: CategoryRepository):
        self.customer_repo = customer_repo
        self.loyalty_account_repo = loyalty_account_repo
        self.product_repo = product_repo
        self.transaction_repo = transaction_repo
        self.category_repo = category_repo

    def process_checkout(self, customer_id: int,
                         product_ids: List[int]) -> Tuple[Dict[str, Any], int]:
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            return {"error": "Customer not found"}, 404

        loyalty_account = self.loyalty_account_repo.get_by_customer_id(
            customer_id)
        if not loyalty_account:
            return {"error": "Loyalty account not found"}, 404

        results = self._process_products(loyalty_account, product_ids)
        (total_points_earned, invalid_products, products_missing_category,
         point_earning_rules_missing) = results

        self.loyalty_account_repo.update(loyalty_account)

        response_data = {
            "total_points_earned": total_points_earned,
            "invalid_products": invalid_products,
            "products_missing_category": products_missing_category,
            "point_earning_rules_missing": point_earning_rules_missing
        }

        return response_data, 200

    def _process_products(
        self, loyalty_account: LoyaltyAccount, product_ids: List[int]
    ) -> Tuple[int, List[int], List[int], List[int]]:
        total_points_earned = 0
        invalid_products = []
        products_missing_category = []
        point_earning_rules_missing = []

        for product_id in product_ids:
            product = self.product_repo.get_by_id(product_id)
            if not product:
                invalid_products.append(product_id)
                continue

            # Fetch the category with rules using the CategoryRepository
            product.category = self.category_repo.get_by_id(
                product.category_id)
            if not product.category:
                products_missing_category.append(product_id)
                continue

            points_earned = PointCalculator.calculate_points(
                product, date.today())
            if points_earned == 0:
                point_earning_rules_missing.append(product_id)
                continue

            self._create_transaction(loyalty_account, product, points_earned)
            loyalty_account.add_points(points_earned)
            total_points_earned += points_earned

        return (total_points_earned, invalid_products,
                products_missing_category, point_earning_rules_missing)

    def _create_transaction(
        self, loyalty_account: LoyaltyAccount, product: Product,
        points_earned: int
    ) -> None:
        transaction = PointTransaction(
            loyalty_account=loyalty_account,
            product=product,
            points_earned=points_earned,
            transaction_date=date.today()
        )
        self.transaction_repo.create(transaction)

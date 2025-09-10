from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.knowledge_base import KnowledgeBase
from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum


class IUserRepository(ABC):

    # User methods

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def create_user(self, new_user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def update_user(self, user_id: str, update_date: int, new_name: Optional[str], new_email: Optional[str], new_cellphone: Optional[str], new_address: Optional[str], new_cep: Optional[str]) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    # Transactions methods

    @abstractmethod
    def get_transactions_by_user(self, user_id: str) -> List[Transaction]:
        """
        Returns a list of transactions for the given user_id.
        """
        pass

    @abstractmethod
    def create_transaction(self, transaction: Transaction) -> Transaction:
        """
        Creates a new transaction record for the user.
        """
        pass

    # Subscription methods

    @abstractmethod
    def get_subscriptions_by_user(self, user_id: str) -> List[Subscription]:
        """
        Returns a list of subscriptions for the given user_id.
        """
        pass

    @abstractmethod
    def update_subscription(self, user_id: str, new_plan: PlanEnum) -> Subscription:
        """
        Creates a new record of subscription for the user with the new plan and updates the plan on the user entity.
        """
        pass

    @abstractmethod
    def create_subscription(self, subscription: Subscription) -> Subscription:
        """
        Creates a new subscription record for the user.
        """
        pass

    # Knowledge Base methods

    @abstractmethod
    def create_knowledge_base(self, user_id: str, kb: KnowledgeBase) -> KnowledgeBase:
        """
        Creates a new knowledge base for the user.
        """
        pass
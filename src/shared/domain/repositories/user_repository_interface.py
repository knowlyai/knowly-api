from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.user import User


class IUserRepository(ABC):

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
    def update_user(self, user_id: str, new_name: Optional[str], new_email: Optional[str], new_cellphone: Optional[str], new_address: Optional[str], new_cep: Optional[str]) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

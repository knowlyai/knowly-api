from typing import List

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetUserSubscriptionsUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str) -> List[Subscription]:
        if not isinstance(user_id, str):
            raise EntityError("user_id")

        # Check if the user exists
        self.repo.get_user(user_id)

        subs = self.repo.get_subscriptions_by_user(user_id)
        return subs

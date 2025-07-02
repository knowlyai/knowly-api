from typing import List
from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.repositories.subscription_repository_interface import ISubscriptionRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetUserSubscriptionsUsecase:
    def __init__(self, repo: ISubscriptionRepository, observability=None):
        self.repo = repo

    def __call__(self, user_id: str) -> List[Subscription]:
        if not isinstance(user_id, str):
            raise EntityError("user_id")

        subs = self.repo.get_all_by_user(user_id)
        if not subs:
            raise NoItemsFound(f"No subscriptions found for user {user_id}")
        return subs
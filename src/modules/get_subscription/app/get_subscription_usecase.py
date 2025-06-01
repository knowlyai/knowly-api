from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.repositories.subscription_repository_interface import ISubscriptionRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class GetSubscriptionUsecase:
    def __init__(self, repo: ISubscriptionRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability

    def __call__(self, subscription_id: str) -> Subscription:
        self.observability.log_usecase_in()

        if type(subscription_id) is not str:
            raise EntityError("subscription_id")

        subscription = self.repo.get_subscription(subscription_id)

        self.observability.log_usecase_out()
        return subscription
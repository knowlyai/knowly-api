from src.shared.domain.entities.subscription import Subscription


class GetSubscriptionViewmodel:
    id: str
    user_id: str
    previous_plan: str
    new_plan: str
    update_date: int

    def __init__(self, subscription: Subscription):
        self.id = subscription.id
        self.user_id = subscription.user_id
        # aqui usava .name
        self.previous_plan = subscription.previous_plan.name
        self.new_plan = subscription.new_plan.name
        self.update_date = subscription.update_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "previous_plan": self.previous_plan,
            "new_plan": self.new_plan,
            "update_date": self.update_date,
            "message": "subscription retrieved successfully"
        }
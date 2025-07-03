from src.shared.domain.entities.user import User

class GetUserViewmodel:
    def __init__(self, user: User):
        self.user = user

    def to_dict(self):
        return {
            "user": self.user.__to_dict__(),
            'message': "the user was retrieved successfully"
        }

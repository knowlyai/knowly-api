from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class DeleteUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str) -> User:

        if not User.validate_user_id(user_id):
            raise EntityError("user_id")

        user = self.repo.delete_user(user_id)

        return user

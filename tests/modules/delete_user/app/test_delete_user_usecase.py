import pytest

from src.modules.delete_user.app.delete_user_usecase import DeleteUserUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestDeleteUserUseCase:
    def test_delete_user(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUseCase(repo)

        before = len(repo.users)

        user = usecase("e4d3c2b1-a098-7654-3210-fedcba987654")

        assert len(repo.users) == before - 1

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUseCase(repo)

        with pytest.raises(NoItemsFound):
            user = usecase("607c8e68-69da-49d4-95e7-f0640345b459")

    def test_delete_user_invalid_id(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUseCase(repo)

        with pytest.raises(EntityError):
            user = usecase("invalid")

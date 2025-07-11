import pytest

from src.modules.get_user.app.get_user_usecase import GetUserUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetUserUseCase:

    def test_get_user(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)

        user = usecase(user_id="fdddafb9-687a-4982-a025-54fb12671932")

        assert repo.users[0] == user

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)

        with pytest.raises(NoItemsFound):
            user = usecase(user_id="d964660a-9d59-42eb-89f4-de1ad1e81f7c")

    def test_get_user_invalid_id(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)

        with pytest.raises(EntityError):
            user = usecase(user_id="invalid")

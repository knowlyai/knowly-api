import time

import pytest

from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user("fdddafb9-687a-4982-a025-54fb12671932")

        assert user.name == "Enzo Sakamoto"
        assert user.user_id == "fdddafb9-687a-4982-a025-54fb12671932"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user("22412cb0-ca31-4b53-ac53-e2d0b6f9bef9")

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            user_id="24255c3c-cfff-40ad-899a-f9331c5b0dd8",
            name="Vitor Soller",
            email="dohype@vitin.com",
            cellphone="11 99175-8098",
            p_type=PTypeEnum.PF,
            cpf_cnpj="37739658855",
            address="Rua Tres Pedras, 915",
            cep="04111111",
            plan=PlanEnum.BR,
            creation_date=1749079322,
            update_date=1749079323,
            birthdate=1022368922
        )

        repo.create_user(user)

        assert repo.users[6].user_id == "24255c3c-cfff-40ad-899a-f9331c5b0dd8"
        assert repo.users[6].name == "Vitor Soller"
        assert repo.users[6].email == "dohype@vitin.com"
        assert repo.users[6].cellphone == "11 99175-8098"
        assert repo.users[6].p_type == PTypeEnum.PF
        assert repo.users[6].cpf_cnpj == "37739658855"
        assert repo.users[6].address == "Rua Tres Pedras, 915"
        assert repo.users[6].cep == "04111111"
        assert repo.users[6].plan == PlanEnum.BR
        assert repo.users[6].creation_date == 1749079322
        assert repo.users[6].update_date == 1749079323
        assert repo.users[6].birthdate == 1022368922
        assert repo.user_counter == 7

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert user.name == "Enzo Sakamoto"
        assert user.user_id == "fdddafb9-687a-4982-a025-54fb12671932"

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_user("0bfa3e4d-ad8e-4735-963c-9463e8c6c9e2")

    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user("fdddafb9-687a-4982-a025-54fb12671932", update_date=int(time.time()), new_name="Maria da div", new_email="email@email.com", new_cellphone="11 99999-9999", new_address="Rua Nova, 123", new_cep="12345-678")

        assert user.name == "Maria da div"
        assert user.email == "email@email.com"
        assert user.cellphone == "11 99999-9999"
        assert user.address == "Rua Nova, 123"
        assert user.cep == "12345-678"

    def test_update_user_one_parameter(self):
        repo = UserRepositoryMock()
        user = repo.update_user("5042b518-83ca-4cbf-84fc-c992da2506e5", new_name="Instituto Mauá de Tecnologia Atualizado", update_date=int(time.time()))

        assert user.name == "Instituto Mauá de Tecnologia Atualizado"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.update_user("501bdc27-951e-40ff-8d11-863ab36eb16d", "Bruno Guirão")

    def test_get_users_counter(self):
        repo = UserRepositoryMock()

        assert repo.get_user_counter() == 6


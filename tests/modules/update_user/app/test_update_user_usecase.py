import pytest
import time

from src.modules.update_user.app.update_user_usecase import UpdateUserUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUpdateUserUsecase:
    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        updated_user = usecase(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_name="Novo Nome Teste"
        )

        assert updated_user.name == "Novo Nome Teste"
        assert updated_user.email == "saka@moto.com"

    def test_update_user_usecase_all_fields(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        updated_user = usecase(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_name="Nome Completo Atualizado",
            new_email="novo@email.com",
            new_cellphone="11 98765-4321",
            new_address="Rua Nova Atualizada, 456",
            new_cep="01234-567"
        )

        assert updated_user.name == "Nome Completo Atualizado"
        assert updated_user.email == "novo@email.com"
        assert updated_user.cellphone == "11 98765-4321"
        assert updated_user.address == "Rua Nova Atualizada, 456"
        assert updated_user.cep == "01234-567"

    def test_update_user_usecase_wrong_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="invalid-user-id",
                new_name="Teste"
            )
        assert str(exc_info.value) == "O campo user_id não é válido"

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id=None,
                new_name="Teste"
            )
        assert str(exc_info.value) == "O campo user_id não é válido"

    def test_update_user_usecase_wrong_new_name(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_name="AB"
            )
        assert str(exc_info.value) == "O campo new_name não é válido"

        updated_user = usecase(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_name=None
        )
        assert updated_user.name == "Enzo Sakamoto"

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_name=123
            )
        assert str(exc_info.value) == "O campo new_name não é válido"

    def test_update_user_usecase_wrong_new_email(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_email="email-invalido"
            )
        assert str(exc_info.value) == "O campo new_email não é válido"

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_email="emailsemat.com"
            )
        assert str(exc_info.value) == "O campo new_email não é válido"

    def test_update_user_usecase_wrong_new_cellphone(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_cellphone="123"
            )
        assert str(exc_info.value) == "O campo new_cellphone não é válido"

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_cellphone=11987654321
            )
        assert str(exc_info.value) == "O campo new_cellphone não é válido"

    def test_update_user_usecase_wrong_new_address(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_address="Rua"
            )
        assert str(exc_info.value) == "O campo new_address não é válido"

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_address=123
            )
        assert str(exc_info.value) == "O campo new_address não é válido"

    def test_update_user_usecase_wrong_new_cep(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_cep="123"
            )
        assert str(exc_info.value) == "O campo new_cep não é válido"

        with pytest.raises(EntityError) as exc_info:
            usecase(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                new_cep="123456789"
            )
        assert str(exc_info.value) == "O campo new_cep não é válido"

    def test_update_user_usecase_partial_updates(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        updated_user = usecase(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_email="email.novo@teste.com"
        )
        assert updated_user.email == "email.novo@teste.com"
        assert updated_user.name == "Enzo Sakamoto"

    def test_update_user_usecase_update_date_is_updated(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo)

        # Obter o update_date original do usuário
        original_user = repo.get_user("fdddafb9-687a-4982-a025-54fb12671932")
        original_update_date = original_user.update_date

        # Aguardar um momento para garantir que o timestamp seja diferente
        time.sleep(1)

        # Executar a atualização
        updated_user = usecase(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_name="Nome Atualizado"
        )

        # Verificar se o update_date foi atualizado
        assert updated_user.update_date > original_update_date
        assert updated_user.update_date <= int(time.time())  # Não deve ser futuro
        assert updated_user.name == "Nome Atualizado"

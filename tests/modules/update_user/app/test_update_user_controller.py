from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "fdddafb9-687a-4982-a025-54fb12671932",
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user']['user_id'] == repo.users[0].user_id
        assert response.body['user']['name'] == 'Branco do Branco Branco da Silva'
        assert response.body['user']['email'] == repo.users[0].email
        assert response.body['message'] == "Usuário atualizado com sucesso"

    def test_update_user_controller_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id está faltando"

    def test_update_user_controller_invalid_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': 3,
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id não está no tipo correto.\nRecebido: int.\nEsperado: str"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUseCase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "0e49cbfb-61bd-4f55-9517-9e639a0e504b",
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'Nenhum item encontrado para user_id'

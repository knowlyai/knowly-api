from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestDeleteUserController:
    def test_delete_user_controller(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': 'fdddafb9-687a-4982-a025-54fb12671932'
            })

            response = controller(request=request)

            assert response.status_code == 200
            assert response.body['user']['user_id'] == 'fdddafb9-687a-4982-a025-54fb12671932'
            assert response.body['message'] == 'O usuário foi excluído com sucesso'

    def test_delete_user_controller_wrong_type(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': 1
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'O campo user_id não está no tipo correto.\nRecebido: int.\nEsperado: str'

    def test_delete_user_controller_missing_parameter(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'id': '1'
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'O campo user_id está faltando'

    def test_delete_user_controller_invalid_user_id(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': 2
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == "O campo user_id não está no tipo correto.\nRecebido: int.\nEsperado: str"

    def test_delete_user_controller_no_items_found(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': 'ed0fc321-98eb-4ef9-b32b-7fd0bb081680'
            })

            response = controller(request=request)

            assert response.status_code == 404
            assert response.body == 'Nenhum item encontrado para user_id'



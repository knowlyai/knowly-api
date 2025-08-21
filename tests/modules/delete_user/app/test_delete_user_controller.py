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
                "requester_user": {
                    "sub": repo.users[0].user_id,
                    "name": repo.users[0].name,
                    "email": repo.users[0].email
                }
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
                "requester_user": {
                    "sub": 1,
                    "name": repo.users[0].name,
                    "email": repo.users[0].email
                }
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == "O campo user_id não está no tipo correto.\nRecebido: <class 'int'>.\nEsperado: str"

    def test_delete_user_controller_missing_parameter(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={})

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'O campo requester_user está faltando'

    def test_delete_user_controller_invalid_user_id(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                "requester_user": {
                    "sub": 'abc',
                    "name": repo.users[0].name,
                    "email": repo.users[0].email
                }
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'O campo user_id não é válido'

    def test_delete_user_controller_no_items_found(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUseCase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                "requester_user": {
                    "sub": 'ed0fc321-98eb-4ef9-b32b-7fd0bb081680',
                    "name": repo.users[0].name,
                    "email": repo.users[0].email
                }
            })

            response = controller(request=request)

            assert response.status_code == 404
            assert response.body == 'Nenhum item encontrado para user_id'

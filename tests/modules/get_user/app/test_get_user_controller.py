from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="get_user")

class Test_GetUserController:
    def test_get_user_controller(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo, observability=observability)
        controller = GetUserController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'user_id': str(repo.users[1].user_id)
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] == repo.users[1].user_id
        assert response.body['name'] == repo.users[1].name
        assert response.body['email'] == repo.users[1].email
        assert response.body['state'] == repo.users[1].state.value

    def test_get_user_controller_missing_parameters(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo, observability=observability)
        controller = GetUserController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'O campo user_id está faltando'

    def test_get_user_contoller_wrong_type_parameter(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo, observability=observability)
        controller = GetUserController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'user_id': 999
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id não está no tipo correto.\nRecebido: int.\nEsperado: str"

    def test_get_user_contoller_entity_error(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo, observability=observability)
        controller = GetUserController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'user_id': 'abc'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'O campo user_id não é válido'

    def test_get_user_controller_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo, observability=observability)
        controller = GetUserController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'user_id': str(999)
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'Nenhum item encontrado para user_id'

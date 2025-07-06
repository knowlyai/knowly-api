from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetUserController:
    def test_get_user_controller(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'user_id': str(repo.users[0].user_id)
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user']['user_id'] == "fdddafb9-687a-4982-a025-54fb12671932"
        assert response.body['user']['name'] == "Enzo Sakamoto"
        assert response.body['user']['email'] == "saka@moto.com"
        assert response.body['user']['cellphone'] == "11 95320-2088"
        assert response.body['user']['p_type'] == "PF"
        assert response.body['user']['cpf_cnpj'] == "37973280871"
        assert response.body['user']['address'] == "Rua das Flores, 123"
        assert response.body['user']['cep'] == "04111111"
        assert response.body['user']['plan'] == "Gold"
        assert response.body['user']['creation_date'] == 1749079322
        assert response.body['user']['update_date'] == 1749079323
        assert response.body['user']['birthdate'] == 1022368922

    def test_get_user_controller_missing_parameters(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(query_params={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'O campo user_id está faltando'

    def test_get_user_controller_wrong_type_parameter(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'user_id': 999
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id não está no tipo correto.\nRecebido: <class 'int'>.\nEsperado: str"

    def test_get_user_controller_entity_error(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'user_id': 'abc'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'O campo user_id não é válido'

    def test_get_user_controller_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'user_id': str("46ad137d-296e-4583-af8b-13a901d24036")
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'Nenhum item encontrado para user_id'

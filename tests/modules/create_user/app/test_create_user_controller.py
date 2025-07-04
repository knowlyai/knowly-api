from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest
import time


class TestCreateUserController:

    @pytest.fixture
    def create_user_usecase(self):
        """Fixture que retorna uma instância do usecase com repositório mock"""
        repo = UserRepositoryMock()
        return CreateUserUseCase(repo)

    @pytest.fixture
    def valid_request_data(self):
        """Fixture com dados válidos para requisição"""
        return {
            'user_id': '65443594-1f8d-4e2f-933e-f932baa5656f',
            'name': 'Virginia Cruz',
            'email': 'joao@teste.com',
            'cellphone': '11999999999',
            'p_type': 'PF',
            'cpf_cnpj': '71214584110',
            'address': 'Rua Teste, 123',
            'cep': '01234567',
            'birthdate': int(time.time() - (25 * 365.25 * 24 * 60 * 60)),  # 25 anos atrás
            'plan': 'Bronze'
        }

    def test_create_user_controller_success(self, create_user_usecase, valid_request_data):
        """Teste de caso de sucesso"""
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 201
        assert response.body['user']['user_id'] == '65443594-1f8d-4e2f-933e-f932baa5656f'
        assert response.body['user']['name'] == 'Virginia Cruz'
        assert response.body['user']['email'] == 'joao@teste.com'
        assert response.body['message'] == "Usuário criado com sucesso"

    # Testes de parâmetros obrigatórios ausentes
    def test_create_user_controller_missing_user_id(self, create_user_usecase, valid_request_data):
        """Teste erro: user_id ausente"""
        valid_request_data.pop('user_id')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'user_id' in response.body

    def test_create_user_controller_missing_name(self, create_user_usecase, valid_request_data):
        """Teste erro: name ausente"""
        valid_request_data.pop('name')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'name' in response.body

    def test_create_user_controller_missing_email(self, create_user_usecase, valid_request_data):
        """Teste erro: email ausente"""
        valid_request_data.pop('email')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'email' in response.body

    def test_create_user_controller_missing_cellphone(self, create_user_usecase, valid_request_data):
        """Teste erro: cellphone ausente"""
        valid_request_data.pop('cellphone')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'cellphone' in response.body

    def test_create_user_controller_missing_p_type(self, create_user_usecase, valid_request_data):
        """Teste erro: p_type ausente"""
        valid_request_data.pop('p_type')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'p_type' in response.body

    def test_create_user_controller_missing_cpf_cnpj(self, create_user_usecase, valid_request_data):
        """Teste erro: cpf_cnpj ausente"""
        valid_request_data.pop('cpf_cnpj')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'cpf_cnpj' in response.body

    def test_create_user_controller_missing_address(self, create_user_usecase, valid_request_data):
        """Teste erro: address ausente"""
        valid_request_data.pop('address')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'address' in response.body

    def test_create_user_controller_missing_cep(self, create_user_usecase, valid_request_data):
        """Teste erro: cep ausente"""
        valid_request_data.pop('cep')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'cep' in response.body

    def test_create_user_controller_missing_plan(self, create_user_usecase, valid_request_data):
        """Teste erro: plan ausente"""
        valid_request_data.pop('plan')
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'plan' in response.body

    # Testes de tipo de parâmetro incorreto
    def test_create_user_controller_wrong_type_user_id(self, create_user_usecase, valid_request_data):
        """Teste erro: user_id com tipo incorreto"""
        valid_request_data['user_id'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'user_id' in response.body

    def test_create_user_controller_wrong_type_name(self, create_user_usecase, valid_request_data):
        """Teste erro: name com tipo incorreto"""
        valid_request_data['name'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'name' in response.body

    def test_create_user_controller_wrong_type_email(self, create_user_usecase, valid_request_data):
        """Teste erro: email com tipo incorreto"""
        valid_request_data['email'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'email' in response.body

    def test_create_user_controller_wrong_type_cellphone(self, create_user_usecase, valid_request_data):
        """Teste erro: cellphone com tipo incorreto"""
        valid_request_data['cellphone'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'cellphone' in response.body

    def test_create_user_controller_wrong_type_cpf_cnpj(self, create_user_usecase, valid_request_data):
        """Teste erro: cpf_cnpj com tipo incorreto"""
        valid_request_data['cpf_cnpj'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'cpf_cnpj' in response.body

    def test_create_user_controller_wrong_type_address(self, create_user_usecase, valid_request_data):
        """Teste erro: address com tipo incorreto"""
        valid_request_data['address'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'address' in response.body

    def test_create_user_controller_wrong_type_cep(self, create_user_usecase, valid_request_data):
        """Teste erro: cep com tipo incorreto"""
        valid_request_data['cep'] = 123
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'cep' in response.body

    def test_create_user_controller_wrong_type_birthdate(self, create_user_usecase, valid_request_data):
        """Teste erro: birthdate com tipo incorreto"""
        valid_request_data['birthdate'] = "1990-01-01"
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'birthdate' in response.body

    # Testes de enum inválido
    def test_create_user_controller_invalid_p_type_enum(self, create_user_usecase, valid_request_data):
        """Teste erro: p_type com valor inválido"""
        valid_request_data['p_type'] = 'INVALID'
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'p_type' in response.body

    def test_create_user_controller_invalid_plan_enum(self, create_user_usecase, valid_request_data):
        """Teste erro: plan com valor inválido"""
        valid_request_data['plan'] = 'INVALID'
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'plan' in response.body

    # Teste de idade menor
    def test_create_user_controller_minor_age_error(self, create_user_usecase, valid_request_data):
        """Teste erro: usuário menor de idade"""
        # Data de nascimento para 15 anos atrás
        valid_request_data['birthdate'] = int(time.time() - (15 * 365.25 * 24 * 60 * 60))
        controller = CreateUserController(create_user_usecase)
        request = HttpRequest(body=valid_request_data)

        response = controller(request)

        assert response.status_code == 400
        assert 'age' in response.body or 'menor' in response.body.lower()

    # Teste de diferentes tipos de plano válidos
    def test_create_user_controller_different_valid_plans(self, create_user_usecase, valid_request_data):
        """Teste com diferentes planos válidos"""
        plans = ['Bronze', 'Silver', 'Gold']

        for plan in plans:
            valid_request_data['plan'] = plan
            valid_request_data['user_id'] = f'c8318707-cb41-4856-8798-1670b844ba20'
            controller = CreateUserController(create_user_usecase)
            request = HttpRequest(body=valid_request_data)

            response = controller(request)

            assert response.status_code == 201
            assert response.body['user']['user_id'] == f'c8318707-cb41-4856-8798-1670b844ba20'

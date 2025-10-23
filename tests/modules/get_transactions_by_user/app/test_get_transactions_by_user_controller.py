from src.modules.get_transactions_by_user.app.get_transactions_by_user_controller import GetTransactionsByUserController
from src.modules.get_transactions_by_user.app.get_transactions_by_user_usecase import GetTransactionsByUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetTransactionsByUserController:

    def test_get_transactions_by_user_success(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': repo.users[0].user_id,
                'name': repo.users[0].name,
                'email': repo.users[0].email
            }
        })

        response = controller(request)

        assert response.status_code == 200
        assert 'transactions' in response.body
        assert 'message' in response.body
        assert response.body['message'] == 'Transações do usuário foram retornadas'
        assert len(response.body['transactions']) == 3
        assert all(isinstance(t, dict) for t in response.body['transactions'])

    def test_get_transactions_by_user_missing_requester_user(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request)

        assert response.status_code == 400
        assert 'O campo requester_user está faltando' in response.body

    def test_get_transactions_by_user_invalid_user_id_type(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': 123,
                'name': repo.users[0].name,
                'email': repo.users[0].email
            }
        })

        response = controller(request)

        assert response.status_code == 400
        assert 'O campo user_id não está no tipo correto' in response.body

    def test_get_transactions_by_user_entity_error_empty(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': '   ',
                'name': repo.users[0].name,
                'email': repo.users[0].email
            }
        })

        response = controller(request)

        assert response.status_code == 400
        assert 'user_id' in response.body

    def test_get_transactions_by_user_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': 'nonexistent-user-id',
                'name': 'X',
                'email': 'x@example.com'
            }
        })

        response = controller(request)

        assert response.status_code == 404
        assert 'Nenhum item encontrado para user_id' in response.body

    def test_get_transactions_by_user_empty_transactions(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': repo.users[1].user_id,  # user sem transações
                'name': repo.users[1].name,
                'email': repo.users[1].email
            }
        })

        response = controller(request)

        assert response.status_code == 200
        assert 'transactions' in response.body
        assert len(response.body['transactions']) == 0
        assert response.body['message'] == 'Transações do usuário foram retornadas'

    def test_get_transactions_by_user_internal_error(self):
        class MockRepo:
            def get_user(self, user_id):
                raise Exception('Database connection error')
            def get_transactions_by_user(self, user_id):
                return []
        repo = MockRepo()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': 'fdddafb9-687a-4982-a025-54fb12671932',
                'name': 'Teste',
                'email': 'teste@example.com'
            }
        })

        response = controller(request)

        assert response.status_code == 500
        assert 'Database connection error' in response.body

from src.modules.get_subscriptions_by_user.app.get_subscriptions_by_user_controller import GetUserSubscriptionsController
from src.modules.get_subscriptions_by_user.app.get_subscriptions_by_user_usecase import GetUserSubscriptionsUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetUserSubscriptionsController:

    def test_get_user_subscriptions_success(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={
            'requester_user': {
                'sub': repo.users[0].user_id,
                'name': repo.users[0].name,
                'email': repo.users[0].email
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert len(body['subscriptions']) == 1
        assert body['subscriptions'][0]['user_id'] == repo.users[0].user_id
        assert body['message'] == 'Assinaturas do usuário encontradas com sucesso'

    def test_get_user_subscriptions_empty_list(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={
            'requester_user': {
                'sub': repo.users[2].user_id,  # user com 0 subscriptions
                'name': repo.users[2].name,
                'email': repo.users[2].email
            }
        })
        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert len(body['subscriptions']) == 0
        assert body['message'] == 'Assinaturas do usuário encontradas com sucesso'

    def test_get_user_subscriptions_missing_requester_user(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={})
        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'O campo requester_user está faltando'

    def test_get_user_subscriptions_invalid_user_id_type(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={
            'requester_user': {
                'sub': 123,
                'name': repo.users[0].name,
                'email': repo.users[0].email
            }
        })
        response = controller(request=request)

        assert response.status_code == 400
        assert 'O campo user_id não está no tipo correto' in response.body

    def test_get_user_subscriptions_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={
            'requester_user': {
                'sub': 'nonexistent-user-id',
                'name': 'X',
                'email': 'x@example.com'
            }
        })
        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'Nenhum item encontrado para user_id'

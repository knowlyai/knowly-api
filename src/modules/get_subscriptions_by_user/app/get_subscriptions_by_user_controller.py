from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from src.shared.infra.dto.user_api_gateway_dto import UserApiGatewayDTO
from .get_subscriptions_by_user_usecase import GetUserSubscriptionsUseCase


class GetUserSubscriptionsController:
    def __init__(self, usecase: GetUserSubscriptionsUseCase):
        self.get_user_subscriptions_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            # Authorizer obrigatório
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            user_id = requester_user.user_id
            if type(user_id) != str:
                raise WrongTypeParameter(
                    field_name="user_id",
                    field_type_expected="str",
                    field_type_received=type(user_id)
                )
            if not user_id.strip():
                raise EntityError("user_id")

            subscriptions = self.get_user_subscriptions_usecase(user_id=user_id)

            viewmodel = {
                'subscriptions': [s.to_dict() for s in subscriptions],
                'message': 'Assinaturas do usuário encontradas com sucesso'
            }

            return OK(viewmodel)

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=str(err))
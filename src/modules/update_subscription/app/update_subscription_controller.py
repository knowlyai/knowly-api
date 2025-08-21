from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, Forbidden, InternalServerError
from src.shared.infra.dto.user_api_gateway_dto import UserApiGatewayDTO
from .update_subscription_usecase import UpdateSubscriptionUseCase


class UpdateSubscriptionController:

    def __init__(self, usecase: UpdateSubscriptionUseCase):
        self.update_subscription_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            # Authorizer obrigatório
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))
            user_id_raw = requester_user.user_id
            if not isinstance(user_id_raw, str):
                raise WrongTypeParameter(
                    field_name='user_id',
                    field_type_expected='str',
                    field_type_received=type(user_id_raw).__name__
                )
            if user_id_raw.strip() == "":
                raise EntityError('user_id')

            new_plan_raw = request.data.get('new_plan')
            if new_plan_raw is None:
                raise MissingParameters('new_plan')
            if not isinstance(new_plan_raw, str):
                raise WrongTypeParameter(
                    field_name='new_plan',
                    field_type_expected='str',
                    field_type_received=type(new_plan_raw).__name__
                )
            if new_plan_raw not in PlanEnum.__members__:
                raise EntityError('new_plan')
            new_plan = PlanEnum[new_plan_raw]

            subscription = self.update_subscription_usecase(
                user_id=user_id_raw,
                new_plan=new_plan
            )

            viewmodel = {
                'subscription': subscription.to_dict(),
                'message': 'subscription updated successfully'
            }

            return OK(viewmodel)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))

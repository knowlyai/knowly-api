from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .update_subscription_usecase import UpdateSubscriptionUsecase
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

class UpdateSubscriptionController:

    def __init__(self, usecase: UpdateSubscriptionUsecase):
        self.update_subscription_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id_raw = request.data.get('user_id')
            if user_id_raw is None:
                raise MissingParameters('user_id')
            if not isinstance(user_id_raw, int):
                raise WrongTypeParameter(
                    fieldName='user_id',
                    fieldTypeExpected='int',
                    fieldTypeReceived=type(user_id_raw).__name__
                )
            if user_id_raw <= 0:
                raise EntityError('user_id')

            new_plan_raw = request.data.get('new_plan')
            if new_plan_raw is None:
                raise MissingParameters('new_plan')
            if not isinstance(new_plan_raw, str):
                raise WrongTypeParameter(
                    fieldName='new_plan',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(new_plan_raw).__name__
                )
            if new_plan_raw not in PLAN.__members__:
                raise EntityError('new_plan')
            new_plan = PLAN[new_plan_raw]

            subscription = self.update_subscription_usecase(
                subscription_id=user_id_raw,
                new_plan=new_plan
            )

            viewmodel = {
                'subscription': {
                    'id': subscription.id,
                    'user_id': subscription.user_id,
                    'plan': subscription.plan.name,
                    'start_date': subscription.start_date,
                    'end_date': subscription.end_date
                },
                'message': 'Assinatura atualizada com sucesso'
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
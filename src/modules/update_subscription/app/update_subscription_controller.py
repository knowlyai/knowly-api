from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .update_subscription_usecase import UpdateSubscriptionUsecase
from .update_subscription_viewmodel import UpdateSubscriptionViewmodel
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class UpdateSubscriptionController:

    def __init__(self, usecase: UpdateSubscriptionUsecase):
        self.UpdateSubscriptionUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            sub_id = request.data.get('id')
            if sub_id is None:
                raise MissingParameters('id')
            if type(sub_id) is not str:
                raise WrongTypeParameter(
                    fieldName="id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(sub_id).__name__
                )
            if len(sub_id.strip()) == 0:
                raise EntityError("id")

            new_plan_raw = request.data.get('new_plan')
            if new_plan_raw is None:
                raise MissingParameters('new_plan')
            if type(new_plan_raw) is not str:
                raise WrongTypeParameter(
                    fieldName="new_plan",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(new_plan_raw).__name__
                )
            if new_plan_raw not in PLAN.__members__:
                raise EntityError("new_plan")
            new_plan = PLAN[new_plan_raw]

            subscription = self.UpdateSubscriptionUsecase(
                subscription_id=sub_id,
                new_plan=new_plan
            )
            viewmodel = UpdateSubscriptionViewmodel(subscription=subscription)

            return OK(viewmodel.to_dict())

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
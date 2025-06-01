from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_subscription_usecase import GetSubscriptionUsecase
from .get_subscription_viewmodel import GetSubscriptionViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from aws_lambda_powertools import Logger


class GetSubscriptionController:

    def __init__(self, usecase: GetSubscriptionUsecase, observability: ObservabilityAWS):
        self.GetSubscriptionUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()

            sub_id = request.data.get("id")
            if sub_id is None:
                raise MissingParameters("id")
            if type(sub_id) is not str:
                raise WrongTypeParameter(
                    fieldName="id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(sub_id).__name__
                )
            if len(sub_id.strip()) == 0:
                raise EntityError("id")

            subscription = self.GetSubscriptionUsecase(subscription_id=sub_id)
            viewmodel = GetSubscriptionViewmodel(subscription)

            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=subscription.id)
            return response

        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=str(err))
            return InternalServerError(body=str(err))
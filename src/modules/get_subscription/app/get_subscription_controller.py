from typing import List
from .get_user_subscriptions_usecase import GetUserSubscriptionsUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

class GetUserSubscriptionsController:

    def __init__(self, usecase: GetUserSubscriptionsUsecase, observability=None):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = request.data.get("user_id")
            if user_id is None:
                raise MissingParameters("user_id")
            if not isinstance(user_id, str):
                raise WrongTypeParameter("user_id", "str", type(user_id).__name__)
            if not user_id.strip():
                raise EntityError("user_id")

            subscriptions = self.usecase(user_id=user_id)  
            result = [s.to_dict() for s in subscriptions]

            return OK(result)

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=str(err))
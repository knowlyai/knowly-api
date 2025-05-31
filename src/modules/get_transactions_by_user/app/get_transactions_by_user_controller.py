from .get_transactions_by_user_usecase import GetTransactionsByUserUsecase
from .get_transactions_by_user_viewmodel import GetTransactionsByUserViewmodel

from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class GetTransactionsByUserController:
    def __init__(self, usecase: GetTransactionsByUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get("user_id") is None:
                raise MissingParameters("user_id")

            user_id = request.data.get("user_id")

            transactions = self.usecase(user_id=user_id)

            viewmodel = GetTransactionsByUserViewmodel(transactions)

            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
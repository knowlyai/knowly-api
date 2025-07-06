from typing import List
from .get_transactions_by_user_usecase import GetTransactionsByUserUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

class GetTransactionsByUserController:

    def __init__(self, usecase: GetTransactionsByUserUseCase):
        self.get_transactions_by_user_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = request.data.get("user_id")
            if user_id is None:
                raise MissingParameters("user_id")
            if not isinstance(user_id, str):
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_id).__name__
                )
            if not user_id.strip():
                raise EntityError("user_id")

            transactions = self.get_transactions_by_user_usecase(user_id=user_id)
            result = [
                {
                    "id": t.id,
                    "user_id": t.user_id,
                    "plan": t.plan.name,
                    "value": t.value,
                    "create_date": t.create_date
                }
                for t in transactions
            ]

            viewmodel = {
                'transactions': result,
                'message': 'Transações do usuário recuperadas com sucesso'
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
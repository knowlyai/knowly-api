from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from .get_transactions_by_user_usecase import GetTransactionsByUserUseCase


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
                    field_name="user_id",
                    field_type_expected="str",
                    field_type_received=type(user_id).__name__
                )
            if not user_id.strip():
                raise EntityError("user_id")

            transactions = self.get_transactions_by_user_usecase(user_id=user_id)

            viewmodel = {
                'transactions': [t.to_dict() for t in transactions],
                'message': 'Transações do usuário foram retornadas'
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
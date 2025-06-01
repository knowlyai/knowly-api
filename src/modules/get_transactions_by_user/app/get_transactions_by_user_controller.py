from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_transactions_by_user_usecase import GetTransactionsByUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetTransactionsByUserController:

    def __init__(self, usecase: GetTransactionsByUserUsecase, observability: ObservabilityAWS):
        self.usecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()

            # Validar se veio user_id
            user_id = request.data.get("user_id")
            if user_id is None:
                raise MissingParameters("user_id")
            if type(user_id) is not str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_id).__name__
                )
            if len(user_id.strip()) == 0:
                raise EntityError("user_id")

            # Executa o use case para obter a lista de transações
            transactions = self.usecase(user_id=user_id)

            # Converte cada Transaction em dicionário
            result = []
            for t in transactions:
                result.append({
                    "id": t.id,
                    "user_id": t.user_id,
                    "plan": t.plan.name,
                    "value": t.value,
                    "create_date": t.create_date
                })

            self.observability.log_controller_out(input=user_id)
            return OK(result)

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
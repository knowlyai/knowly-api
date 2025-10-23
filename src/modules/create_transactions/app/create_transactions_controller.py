from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import Created, NotFound, BadRequest, InternalServerError
from src.shared.domain.enums.plan_enum import PlanEnum
from .create_transactions_usecase import CreateTransactionUsecase


class CreateTransactionController:
    def __init__(self, usecase: CreateTransactionUsecase):
        self.create_transaction_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            tran_id = request.data.get("tran_id")
            user_id = request.data.get("user_id")
            plan = request.data.get("plan")
            value = request.data.get("value")
            create_date = request.data.get("create_date")  

            if tran_id is None:
                raise MissingParameters("tran_id")
            if user_id is None:
                raise MissingParameters("user_id")
            if plan is None:
                raise MissingParameters("plan")
            if value is None:
                raise MissingParameters("value")

            if not isinstance(tran_id, str):
                raise WrongTypeParameter("tran_id", "str", type(tran_id).__name__)
            if not isinstance(user_id, str):
                raise WrongTypeParameter("user_id", "str", type(user_id).__name__)

            if isinstance(plan, str):
                try:
                    try:
                        plan = PlanEnum(plan)
                    except ValueError:
                        plan = PlanEnum[plan]
                except Exception:
                    raise WrongTypeParameter("plan", "PlanEnum | str", type(plan).__name__)
            elif not isinstance(plan, PlanEnum):
                raise WrongTypeParameter("plan", "PlanEnum | str", type(plan).__name__)

            if not isinstance(value, (int, float)):
                raise WrongTypeParameter("value", "float | int", type(value).__name__)
            value = float(value)

            if create_date is not None and not isinstance(create_date, int):
                raise WrongTypeParameter("create_date", "int", type(create_date).__name__)

            if not tran_id.strip():
                raise EntityError("tran_id")
            if not user_id.strip():
                raise EntityError("user_id")

            transaction = self.create_transaction_usecase(
                tran_id=tran_id,
                user_id=user_id,
                plan=plan,
                value=value,
                create_date=create_date,
            )

            viewmodel = {
                "transaction": transaction.to_dict(),
                "message": "Transação criada com sucesso",
            }

            return Created(viewmodel)

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except DuplicatedItem as err:
            return BadRequest(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=str(err))
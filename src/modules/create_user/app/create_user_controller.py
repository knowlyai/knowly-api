from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, EnumError
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, MinorAgeError
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.external_interfaces.http_codes import NotFound, BadRequest, InternalServerError, Created
from .create_user_usecase import CreateUserUseCase


class CreateUserController:

    def __init__(self, usecase: CreateUserUseCase):
        self.CreateUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')
            if type(request.data.get('user_id')) != str:
                raise WrongTypeParameter('user_id', 'str', f"{type(request.data.get('user_id'))}")

            if request.data.get('name') is None:
                raise MissingParameters('name')
            if type(request.data.get('name')) != str:
                raise WrongTypeParameter('name', 'str', f"{type(request.data.get('name'))}")

            if request.data.get('email') is None:
                raise MissingParameters('email')
            if type(request.data.get('email')) != str:
                raise WrongTypeParameter('email', 'str', f"{type(request.data.get('email'))}")

            if request.data.get('cellphone') is None:
                raise MissingParameters('cellphone')
            if type(request.data.get('cellphone')) != str:
                raise WrongTypeParameter('cellphone', 'str', f"{type(request.data.get('cellphone'))}")

            if request.data.get('p_type') is not None:
                p_type_str = request.data.get('p_type')
                if p_type_str not in [p_type.value for p_type in PTypeEnum]:
                    raise EnumError('p_type', 'PTypeEnum')
                p_type = PTypeEnum(p_type_str)
            else:
                raise MissingParameters('p_type')

            if request.data.get('cpf_cnpj') is None:
                raise MissingParameters('cpf_cnpj')
            if type(request.data.get('cpf_cnpj')) != str:
                raise WrongTypeParameter('cpf_cnpj', 'str', f"{type(request.data.get('cpf_cnpj'))}")

            if request.data.get('address') is None:
                raise MissingParameters('address')
            if type(request.data.get('address')) != str:
                raise WrongTypeParameter('address', 'str', f"{type(request.data.get('address'))}")

            if request.data.get('cep') is None:
                raise MissingParameters('cep')
            if type(request.data.get('cep')) != str:
                raise WrongTypeParameter('cep', 'str', f"{type(request.data.get('cep'))}")

            if request.data.get('birthdate') is not None:
                if type(request.data.get('birthdate')) != int:
                    raise WrongTypeParameter('birthdate', 'int', f"{type(request.data.get('birthdate'))}")
                birthdate = request.data.get('birthdate')

            if request.data.get('plan') is not None:
                plan_str = request.data.get('plan')
                if plan_str not in [plan.value for plan in PlanEnum]:
                    raise EnumError('plan', 'PlanEnum')
                plan = PlanEnum(plan_str)
            else:
                raise MissingParameters('plan')

            user = self.CreateUserUseCase(
                user_id=request.data.get('user_id'),
                name=request.data.get('name'),
                email=request.data.get('email'),
                cellphone=request.data.get('cellphone'),
                p_type=p_type,
                cpf_cnpj=request.data.get('cpf_cnpj'),
                address=request.data.get('address'),
                cep=request.data.get('cep'),
                birthdate=request.data.get('birthdate', None),
                plan=plan
            )

            viewmodel = {
                'user': user.__to_dict__(),
                'message': 'Usuário criado com sucesso'
            }

            return Created(viewmodel)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except EnumError as err:
            return BadRequest(body=err.message)

        except MinorAgeError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])

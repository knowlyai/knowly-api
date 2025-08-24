from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from src.shared.infra.dto.user_api_gateway_dto import UserApiGatewayDTO
from .update_user_usecase import UpdateUserUseCase


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUseCase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            # Authorizer obrigatório
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if type(requester_user.user_id) != str:
                raise WrongTypeParameter(
                    field_name='user_id',
                    field_type_expected='str',
                    field_type_received=type(requester_user.user_id)
                )

            new_name = request.data.get('new_name')
            new_email = request.data.get('new_email')
            new_cellphone = request.data.get('new_cellphone')
            new_address = request.data.get('new_address')
            new_cep = request.data.get('new_cep')

            if new_name is not None and type(new_name) != str:
                raise WrongTypeParameter(
                    field_name="new_name",
                    field_type_expected="str",
                    field_type_received=new_name.__class__.__name__
                )
            if new_email is not None and type(new_email) != str:
                raise WrongTypeParameter(
                    field_name="new_email",
                    field_type_expected="str",
                    field_type_received=new_email.__class__.__name__
                )
            if new_cellphone is not None and type(new_cellphone) != str:
                raise WrongTypeParameter(
                    field_name="new_cellphone",
                    field_type_expected="str",
                    field_type_received=new_cellphone.__class__.__name__
                )
            if new_address is not None and type(new_address) != str:
                raise WrongTypeParameter(
                    field_name="new_address",
                    field_type_expected="str",
                    field_type_received=new_address.__class__.__name__
                )
            if new_cep is not None and type(new_cep) != str:
                raise WrongTypeParameter(
                    field_name="new_cep",
                    field_type_expected="str",
                    field_type_received=new_cep.__class__.__name__
                )

            user = self.UpdateUserUsecase(user_id=requester_user.user_id, new_name=new_name, new_email=new_email,
                                          new_cellphone=new_cellphone, new_address=new_address, new_cep=new_cep)

            viewmodel = {
                'user': user.__to_dict__(),
                'message': 'Usuário atualizado com sucesso'
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
            return InternalServerError(body=err.args[0])

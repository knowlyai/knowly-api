from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from .get_user_usecase import GetUserUseCase


class GetUserController:

    def __init__(self, usecase: GetUserUseCase):
        self.GetUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')

            if type(request.data.get('user_id')) != str:
                raise WrongTypeParameter('user_id', 'str', type(request.data.get('user_id')))

            user = self.GetUserUsecase(
                user_id=request.data.get('user_id')
            )

            viewmodel = {
                'user': user.__to_dict__(),
                'message': 'Usuário encontrado com sucesso'
            }
            
            response = OK(viewmodel)
            return response

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

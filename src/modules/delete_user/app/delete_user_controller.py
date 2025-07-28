from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from .delete_user_usecase import DeleteUserUseCase


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUseCase):
        self.DeleteUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')

            if type(request.data.get('user_id')) != str:
                raise WrongTypeParameter(
                    field_name="user_id",
                    field_type_expected="str",
                    field_type_received=request.data.get('user_id').__class__.__name__
                )

            user = self.DeleteUserUsecase(
                user_id=request.data.get('user_id')
            )

            viewmodel = {
                'user': user.__to_dict__(),
                'message': "O usuário foi excluído com sucesso"
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

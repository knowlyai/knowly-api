from botocore.exceptions import ClientError

from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, Forbidden
from .get_token_usecase import GetTokenUseCase


class GetTokenController:

    def __init__(self, usecase: GetTokenUseCase):
        self.GetTokenUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')
            if type(request.data.get('email')) is not str:
                raise WrongTypeParameter('email', 'str', f"{type(request.data.get('email'))}")

            if request.data.get('password') is None:
                raise MissingParameters('password')
            if type(request.data.get('password')) is not str:
                raise WrongTypeParameter('password', 'str', f"{type(request.data.get('password'))}")

            result = self.GetTokenUseCase(
                email=request.data.get('email'),
                password=request.data.get('password')
            )

            return OK(result)

        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except ClientError as err:
            code = err.response.get('Error', {}).get('Code')
            message = err.response.get('Error', {}).get('Message', str(err))

            if code in ['NotAuthorizedException', 'UserNotFoundException']:
                return Forbidden(body={'message': 'Credenciais inválidas'})
            if code == 'UserNotConfirmedException':
                return Forbidden(body={'message': 'Usuário não confirmado'})
            if code == 'PasswordResetRequiredException':
                return Forbidden(body={'message': 'Redefinição de senha obrigatória'})
            if code in ['TooManyRequestsException', 'LimitExceededException']:
                return Forbidden(body={'message': 'Muitas tentativas. Tente novamente mais tarde'})
            if code in ['InvalidParameterException', 'InvalidSmsRoleAccessPolicyException', 'InvalidSmsRoleTrustRelationshipException']:
                return BadRequest(body=message)

            return InternalServerError(body=message)
        except Exception as err:
            return InternalServerError(body=str(err))

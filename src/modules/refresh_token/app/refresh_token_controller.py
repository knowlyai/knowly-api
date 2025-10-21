from botocore.exceptions import ClientError

from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, Forbidden
from .refresh_token_usecase import RefreshTokenUseCase


class RefreshTokenController:

    def __init__(self, usecase: RefreshTokenUseCase):
        self.RefreshTokenUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('refresh_token') is None:
                raise MissingParameters('refresh_token')
            if not isinstance(request.data.get('refresh_token'), str):
                raise WrongTypeParameter('refresh_token', 'str', f"{type(request.data.get('refresh_token'))}")

            result = self.RefreshTokenUseCase(
                refresh_token=request.data.get('refresh_token')
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
                return Forbidden(body={'message': 'Token de atualização inválido ou expirado'})
            if code == 'UserNotConfirmedException':
                return Forbidden(body={'message': 'Usuário não confirmado'})
            if code in ['TooManyRequestsException', 'LimitExceededException']:
                return Forbidden(body={'message': 'Muitas tentativas. Tente novamente mais tarde'})
            if code in ['InvalidParameterException', 'InvalidSmsRoleAccessPolicyException', 'InvalidSmsRoleTrustRelationshipException']:
                return BadRequest(body=message)

            return InternalServerError(body=message)
        except Exception as err:
            return InternalServerError(body=str(err))


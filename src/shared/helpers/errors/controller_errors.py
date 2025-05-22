from src.shared.helpers.errors.base_error import BaseError


class MissingParameters(BaseError):
    def __init__(self, message: str):
        super().__init__(f'O campo {message} está faltando')
class WrongTypeParameter(BaseError):
    def __init__(self, fieldName: str, fieldTypeExpected: str, fieldTypeReceived: str):
        super().__init__(f'O campo {fieldName} não está no tipo correto.\nRecebido: {fieldTypeReceived}.\nEsperado: {fieldTypeExpected}')
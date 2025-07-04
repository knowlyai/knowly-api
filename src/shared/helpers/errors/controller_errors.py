from src.shared.helpers.errors.base_error import BaseError


class MissingParameters(BaseError):
    def __init__(self, message: str):
        super().__init__(f'O campo {message} está faltando')
class WrongTypeParameter(BaseError):
    def __init__(self, field_name: str, field_type_expected: str, field_type_received: str):
        super().__init__(f'O campo {field_name} não está no tipo correto.\nRecebido: {field_type_received}.\nEsperado: {field_type_expected}')

class EnumError(BaseError):
    def __init__(self, field_name: str, expected_enum: str):
        super().__init__(f'O campo {field_name} não é um valor válido do tipo {expected_enum}.')
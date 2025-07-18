from src.shared.helpers.errors.base_error import BaseError


class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'O campo {message} não é válido')

class EntityParameterTypeError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message

class EntityParameterError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message

class UpdateToSamePlanError(EntityError):
    def __init__(self, message: str):
        super().__init__(f"Não é possível atualizar para o mesmo plano: {message}")
        self.__message = message
    @property
    def message(self):
        return self.__message
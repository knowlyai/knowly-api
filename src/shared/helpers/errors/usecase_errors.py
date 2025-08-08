from src.shared.helpers.errors.base_error import BaseError

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Nenhum item encontrado para {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'O item já existe para {message}')
        
class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Essa ação é proibida para {message}')

class MinorAgeError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Usuário é menor de idade: {message}')

class UserAlreadyExists(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Usuário já existe: {message}')
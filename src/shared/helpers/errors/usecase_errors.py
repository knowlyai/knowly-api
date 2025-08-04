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

class ExternalServiceError(BaseError):
    def __init__(self, service: str, message: str):
        super().__init__(f'Erro no serviço {service}: {message}')

class InfrastructureError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Erro de infraestrutura: {message}')

class DatabaseError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Erro de banco de dados: {message}')

class ConfigurationError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Erro de configuração: {message}')

from typing import Optional

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UpdateUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str, new_name: Optional[str] = None, new_email: Optional[str] = None, new_cellphone: Optional[str] = None, new_address: Optional[str] = None, new_cep: Optional[str] = None) -> User:

        if not User.validate_user_id(user_id):
            raise EntityError("user_id")

        if new_name is not None and not User.validate_name(new_name):
            raise EntityError("new_name")

        if new_email is not None and not User.validate_email(new_email):
            raise EntityError("new_email")

        if new_cellphone is not None and not User.validate_cellphone(new_cellphone):
            raise EntityError("new_cellphone")

        if new_address is not None and (type(new_address) != str or len(new_address) <= User.MIN_ADDRESS_LENGTH):
            raise EntityError("new_address")

        if new_cep is not None and not User.validate_cep(new_cep):
            raise EntityError("new_cep")

        updated_user = self.repo.update_user(
            user_id=user_id,
            new_name=new_name,
            new_email=new_email,
            new_cellphone=new_cellphone,
            new_address=new_address,
            new_cep=new_cep
        )

        return updated_user

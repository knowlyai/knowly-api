from typing import Optional
import time
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.type_enum import PTypeEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import MinorAgeError


class CreateUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str, name: str, email: str, cellphone: str, p_type: PTypeEnum, cpf_cnpj: str, address: str, cep: str, birthdate: Optional[int], plan: PlanEnum) -> User:

        current_time = int(time.time())

        if birthdate is not None:
            age_in_seconds = current_time - birthdate
            age_in_years = age_in_seconds / (365.25 * 24 * 60 * 60)

            if age_in_years < 18:
                raise MinorAgeError(str(age_in_years))

        # 18 years = 568024668

        creation_date = current_time
        update_date = current_time

        user = User(
            user_id=user_id,
            name=name,
            email=email,
            cellphone=cellphone,
            p_type=p_type,
            cpf_cnpj=cpf_cnpj,
            address=address,
            cep=cep,
            birthdate=birthdate,
            plan=plan,
            creation_date=creation_date,
            update_date=update_date,
        )

        return self.repo.create_user(user)

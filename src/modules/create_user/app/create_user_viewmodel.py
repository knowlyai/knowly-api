from typing import Optional

from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum


class CreateUserViewmodel:
    user_id: str
    name: str
    email: str
    cellphone: str
    p_type: PTypeEnum
    cpf_cnpj: str
    address: str
    cep: str
    birthdate: Optional[int] = None
    plan: PlanEnum
    creation_date: int
    update_date: int

    def __init__(self, user: User):
        self.user = user
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.cellphone = user.cellphone
        self.p_type = user.p_type
        self.cpf_cnpj = user.cpf_cnpj
        self.address = user.address
        self.cep = user.cep
        self.birthdate = user.birthdate
        self.plan = user.plan
        self.creation_date = user.creation_date
        self.update_date = user.update_date


    def to_dict(self):
        return {
            'user':
                self.user.__to_dict__()
            ,
            'message': "the user was created successfully"
        }

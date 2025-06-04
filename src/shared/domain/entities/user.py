import re
import uuid
from typing import Optional
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.type_enum import PTypeEnum
from src.shared.helpers.errors.domain_errors import EntityError


class User:
    user_id: str
    name: str
    email: str
    cellphone: str
    p_type: PTypeEnum
    cpf_cnpj: str
    address: str
    cep: str
    birthdate: Optional[int]
    plan: PlanEnum
    creation_date: int
    update_date: int
    MIN_NAME_LENGTH = 3

    def __init__(self, user_id: str, name: str, email: str, cellphone: str, p_type: PTypeEnum, cpf_cnpj: str, address: str, cep: str, plan: PlanEnum, creation_date: int, update_date: int, birthdate: Optional[int] = None):
        if not User.validate_user_id(user_id):
            raise EntityError("user_id")

        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email


        self.user_id = user_id


    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        elif type(name) != str:
            return False
        elif len(name) < User.MIN_NAME_LENGTH:
            return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        if email is None:
            return False

        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        return bool(re.fullmatch(regex, email))

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if user_id is None or type(user_id) != str:
            return False
        try:
            uuid.UUID(user_id)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_cellphone(cellphone: str) -> bool:
        if cellphone is None or type(cellphone) != str:
            return False
        regex = re.compile(r"(?:(\+|00)?(55)\s?)?\(?(\d{2})\)?\s?(|\d{2})(|-)?(9\d|[2-9])\d{3}[-|.\s]?(\d{4})")
        return bool(re.fullmatch(regex, cellphone))

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, user_id={self.user_id})"

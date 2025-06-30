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
    MIN_ADDRESS_LENGTH = 5

    def __init__(self, user_id: str, name: str, email: str, cellphone: str, p_type: PTypeEnum, cpf_cnpj: str, address: str, cep: str, plan: PlanEnum, creation_date: int, update_date: int, birthdate: Optional[int] = None):
        if not User.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if not User.validate_cellphone(cellphone):
            raise EntityError("cellphone")
        self.cellphone = cellphone

        if not isinstance(p_type, PTypeEnum):
            raise EntityError("p_type")
        self.p_type = p_type

        if not User.validate_cpf_cnpj(cpf_cnpj, p_type):
            raise EntityError("cpf_cnpj")
        self.cpf_cnpj = cpf_cnpj

        if type(address) != str or len(address) <= self.MIN_ADDRESS_LENGTH:
            raise EntityError("address")
        self.address = address

        if not User.validate_cep(cep):
            raise EntityError("cep")
        self.cep = cep

        if not isinstance(plan, PlanEnum):
            raise EntityError("plan")
        self.plan = plan

        if type(creation_date) != int:
            raise EntityError("creation_date")
        self.creation_date = creation_date

        if type(update_date) != int or update_date < creation_date:
            raise EntityError("update_date")
        self.update_date = update_date

        if birthdate is not None and type(birthdate) != int:
            raise EntityError("birthdate")
        self.birthdate = birthdate




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

    @staticmethod
    def validate_cpf_cnpj(cpf_cnpj: str, p_type: PTypeEnum) -> bool:
        only_numbers = re.sub(r"\D", "", cpf_cnpj)
        if p_type == PTypeEnum.PF:
            regex_cpf = re.compile(r"^\d{3}.?\d{3}.?\d{3}-?\d{2}$")
            if not re.fullmatch(regex_cpf, cpf_cnpj):
                return False

            if len(only_numbers) != 11:
                return False

            if only_numbers == only_numbers[0] * 11:
                return False

            nums = [int(d) for d in only_numbers]

            def digit_check_cpf(base: list[int], initial_weight: int) -> int:
                soma = 0
                weight = initial_weight
                for n in base:
                    soma += n * weight
                    weight -= 1
                rest = soma % 11
                return 0 if rest < 2 else 11 - rest

            base_cpf = nums[:9]
            first_dv = digit_check_cpf(base_cpf, 10)
            second_dv = digit_check_cpf(base_cpf + [first_dv], 11)

            return nums[9] == first_dv and nums[10] == second_dv
        elif p_type == PTypeEnum.PJ:
            regex_cnpj = re.compile(r"^(\d{2}.?\d{3}.?\d{3}/?\d{4}-?\d{2})$")
            if not re.fullmatch(regex_cnpj, cpf_cnpj):
                return False

            if len(only_numbers) != 14:
                return False

            if only_numbers == only_numbers[0] * 14:
                return False


            nums = [int(d) for d in only_numbers]

            def check_digit_cnpj(base: list[int], weights: list[int]) -> int:
                soma = sum(n * p for n, p in zip(base, weights))
                rest = soma % 11
                return 0 if rest < 2 else 11 - rest

            first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            second_weights = [6] + first_weights

            base_cnpj = nums[:12]
            first_dv = check_digit_cnpj(base_cnpj, first_weights)
            second_dv = check_digit_cnpj(base_cnpj + [first_dv], second_weights)

            return nums[12] == first_dv and nums[13] == second_dv

        else:
            return False

    @staticmethod
    def validate_cep(cep: str) -> bool:
        if cep is None:
            return False
        cep_regex = re.compile(r"(^\d{5})-?(\d{3}$)")
        return bool(re.fullmatch(cep_regex, cep))

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, user_id={self.user_id})"

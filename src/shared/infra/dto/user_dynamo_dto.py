from decimal import Decimal
from typing import Optional

from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum


class UserDynamoDTO:
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

    def __init__(self, user_id: str, name: str, email: str, cellphone: str, p_type: PTypeEnum,
                 cpf_cnpj: str, address: str, cep: str, plan: PlanEnum, creation_date: int,
                 update_date: int, birthdate: Optional[int] = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.cellphone = cellphone
        self.p_type = p_type
        self.cpf_cnpj = cpf_cnpj
        self.address = address
        self.cep = cep
        self.birthdate = birthdate
        self.plan = plan
        self.creation_date = creation_date
        self.update_date = update_date

    @staticmethod
    def from_entity(user: User) -> "UserDynamoDTO":
        """
        Parse data from User to UserDynamoDTO
        """
        return UserDynamoDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            cellphone=user.cellphone,
            p_type=user.p_type,
            cpf_cnpj=user.cpf_cnpj,
            address=user.address,
            cep=user.cep,
            birthdate=user.birthdate,
            plan=user.plan,
            creation_date=user.creation_date,
            update_date=user.update_date
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from UserDynamoDTO to dict
        """
        dynamo_dict = {
            "entity": "user",
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "cellphone": self.cellphone,
            "p_type": self.p_type.value,
            "cpf_cnpj": self.cpf_cnpj,
            "address": self.address,
            "cep": self.cep,
            "plan": self.plan.value,
            "creation_date": Decimal(self.creation_date),
            "update_date": Decimal(self.update_date)
        }

        if self.birthdate is not None:
            dynamo_dict["birthdate"] = Decimal(self.birthdate)

        return dynamo_dict

    @staticmethod
    def from_dynamo(user_data: dict) -> "UserDynamoDTO":
        """
        Parse data from DynamoDB to UserDynamoDTO
        @param user_data: dict from DynamoDB
        """
        birthdate = None
        if "birthdate" in user_data and user_data["birthdate"] is not None:
            birthdate = int(user_data["birthdate"])

        return UserDynamoDTO(
            user_id=user_data["user_id"],
            name=user_data["name"],
            email=user_data["email"],
            cellphone=user_data["cellphone"],
            p_type=PTypeEnum(user_data["p_type"]),
            cpf_cnpj=user_data["cpf_cnpj"],
            address=user_data["address"],
            cep=user_data["cep"],
            birthdate=birthdate,
            plan=PlanEnum(user_data["plan"]),
            creation_date=int(user_data["creation_date"]),
            update_date=int(user_data["update_date"])
        )

    def to_entity(self) -> User:
        """
        Parse data from UserDynamoDTO to User
        """
        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            cellphone=self.cellphone,
            p_type=self.p_type,
            cpf_cnpj=self.cpf_cnpj,
            address=self.address,
            cep=self.cep,
            birthdate=self.birthdate,
            plan=self.plan,
            creation_date=self.creation_date,
            update_date=self.update_date
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

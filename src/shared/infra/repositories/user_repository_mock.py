from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]
    user_counter: int

    def __init__(self):
        self.user_counter = 6
        self.users = [
            User(user_id="fdddafb9-687a-4982-a025-54fb12671932",
                 name="Enzo Sakamoto",
                 email="saka@moto.com",
                 cellphone="11 95320-2088",
                 p_type=PTypeEnum.PF,
                 cpf_cnpj="37973280871",
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 birthdate=1022368922),

            User(user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
                 name="Instituto Mauá de Tecnologia",
                 email="imt@maua.br",
                 cellphone="11 95320-2088",
                 p_type=PTypeEnum.PJ,
                 cpf_cnpj="60.749.736/0001-99",
                 address="Praça Mauá, 1",
                 cep="09580-900",
                 plan=PlanEnum.BR,
                 creation_date=1749079322,
                 update_date=1749079323,
                 ),

            User(user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
                 name="Maria Silva Santos",
                 email="maria.silva@email.com",
                 cellphone="21 98765-4321",
                 p_type=PTypeEnum.PF,
                 cpf_cnpj="123.456.789-09",
                 address="Avenida Copacabana, 456",
                 cep="22070-011",
                 plan=PlanEnum.BR,
                 creation_date=1749080000,
                 update_date=1749080100,
                 birthdate=694224000),

            User(user_id="9e8d7c6b-5a49-3827-1605-948372615038",
                 name="Antonio Sergio Ferreira Bonato",
                 email="antonio.bonato@maua.br",
                 cellphone="11 99453-4121",
                 p_type=PTypeEnum.PF,
                 cpf_cnpj="987.654.321-00",
                 address="Rua Augusta, 789",
                 cep="01305-100",
                 plan=PlanEnum.SI,
                 creation_date=1749081000,
                 update_date=1749081200,
                 birthdate=567993600),

            User(user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
                 name="TechCorp Soluções LTDA",
                 email="contato@techcorp.com.br",
                 cellphone="11 91234-5678",
                 p_type=PTypeEnum.PJ,
                 cpf_cnpj="60.749.736/0001-99",
                 address="Rua dos Desenvolvedores, 100",
                 cep="04567-890",
                 plan=PlanEnum.GO,
                 creation_date=1749082000,
                 update_date=1749082300),

            User(user_id="e4d3c2b1-a098-7654-3210-fedcba987654",
                 name="Inovação Digital PIRELLI",
                 email="admin@inovacaodigital.com",
                 cellphone="11 94567-8901",
                 p_type=PTypeEnum.PJ,
                 cpf_cnpj="60.749.736/0001-99",
                 address="Avenida Paulista, 2000",
                 cep="01310-100",
                 plan=PlanEnum.BR,
                 creation_date=1749083000,
                 update_date=1749083500),
        ]

    def get_user(self, user_id: str) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise NoItemsFound("user_id")

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        self.user_counter += 1
        return new_user

    def delete_user(self, user_id: str) -> User:
        for idx, user in enumerate(self.users):
            if user.user_id == user_id:
                return self.users.pop(idx)

        raise NoItemsFound("user_id")

    def update_user(self, user_id: str, new_name: str) -> User:
        for user in self.users:
            if user.user_id == user_id:
                user.name = new_name
                return user

        raise NoItemsFound("user_id")

    def get_user_counter(self) -> int:
        return self.user_counter

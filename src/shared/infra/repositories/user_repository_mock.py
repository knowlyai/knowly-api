import time
import uuid
from typing import List, Optional

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.entities.transaction import Transaction
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

        self.transactions = [
            Transaction(
                tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                plan=PlanEnum.BR,
                value=29.9,
                create_date=1717000000
            ),
            Transaction(
                tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c8",
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                plan=PlanEnum.SI,
                value=59.9,
                create_date=1717100000
            ),
            Transaction(
                tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c9",
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                plan=PlanEnum.GO,
                value=19.9,
                create_date=1717200000
            ),
        ]

        self.subscriptions: List[Subscription] = [
            Subscription(
                sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.GO,
                update_date=1700000000
            ),
            Subscription(
                sub_id="9cf4fdd7-f0d4-43cf-9603-e50a3033a6c3",
                user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
                previous_plan=PlanEnum.SI,
                new_plan=PlanEnum.BR,
                update_date=1700003600
            ),
            Subscription(
                sub_id="a1bb21da-b84b-4d0d-a32d-90c08a435729",
                user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.GO,
                update_date=1700007200
            ),
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

    def update_user(self, user_id: str, update_date: int, new_name: Optional[str] = None, new_email: Optional[str] = None, new_cellphone: Optional[str] = None, new_address: Optional[str] = None, new_cep: Optional[str] = None ) -> User:
        for user in self.users:
            if user.user_id == user_id:
                if new_name is not None:
                    user.name = new_name
                if new_email is not None:
                    user.email = new_email
                if new_cellphone is not None:
                    user.cellphone = new_cellphone
                if new_address is not None:
                    user.address = new_address
                if new_cep is not None:
                    user.cep = new_cep
                user.update_date = update_date
                return user

        raise NoItemsFound("user_id")

    def get_user_counter(self) -> int:
        return self.user_counter

    def get_transactions_by_user(self, user_id: str) -> List[Transaction]:
        return [tx for tx in self.transactions if tx.user_id == user_id]

    def create_transaction(self, transaction: Transaction) -> Transaction:
        self.transactions.append(transaction)
        return transaction

    def get_subscriptions_by_user(self, user_id: str) -> List[Subscription]:
        return [sub for sub in self.subscriptions if sub.user_id == user_id]

    def create_subscription(self, subscription: Subscription) -> Subscription:
        self.subscriptions.append(subscription)
        return subscription

    def update_subscription(self, user_id: str, new_plan: PlanEnum) -> Subscription:
        for user in self.users:
            if user.user_id == user_id:
                current_plan = user.plan
                # Atualiza o plano do usuário diretamente
                user.plan = new_plan

                # Cria nova subscription
                new_subscription = Subscription(
                    sub_id=str(uuid.uuid4()),
                    user_id=user_id,
                    previous_plan=current_plan,
                    new_plan=new_plan,
                    update_date=int(time.time())
                )
                self.subscriptions.append(new_subscription)
                return new_subscription
        raise NoItemsFound("user_id")

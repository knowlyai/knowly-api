import time
import uuid

import pytest

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.entities.user import User
from src.shared.domain.entities.knowledge_base import KnowledgeBase
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user("fdddafb9-687a-4982-a025-54fb12671932")

        assert user.name == "Enzo Sakamoto"
        assert user.user_id == "fdddafb9-687a-4982-a025-54fb12671932"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user("22412cb0-ca31-4b53-ac53-e2d0b6f9bef9")

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            user_id="24255c3c-cfff-40ad-899a-f9331c5b0dd8",
            name="Vitor Soller",
            email="dohype@vitin.com",
            cellphone="11 99175-8098",
            p_type=PTypeEnum.PF,
            cpf_cnpj="37739658855",
            address="Rua Tres Pedras, 915",
            cep="04111111",
            plan=PlanEnum.BR,
            creation_date=1749079322,
            update_date=1749079323,
            birthdate=1022368922
        )

        repo.create_user(user)

        assert repo.users[6].user_id == "24255c3c-cfff-40ad-899a-f9331c5b0dd8"
        assert repo.users[6].name == "Vitor Soller"
        assert repo.users[6].email == "dohype@vitin.com"
        assert repo.users[6].cellphone == "11 99175-8098"
        assert repo.users[6].p_type == PTypeEnum.PF
        assert repo.users[6].cpf_cnpj == "37739658855"
        assert repo.users[6].address == "Rua Tres Pedras, 915"
        assert repo.users[6].cep == "04111111"
        assert repo.users[6].plan == PlanEnum.BR
        assert repo.users[6].creation_date == 1749079322
        assert repo.users[6].update_date == 1749079323
        assert repo.users[6].birthdate == 1022368922
        assert repo.user_counter == 7

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert user.name == "Enzo Sakamoto"
        assert user.user_id == "fdddafb9-687a-4982-a025-54fb12671932"

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_user("0bfa3e4d-ad8e-4735-963c-9463e8c6c9e2")

    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user("fdddafb9-687a-4982-a025-54fb12671932", update_date=int(time.time()), new_name="Maria da div", new_email="email@email.com", new_cellphone="11 99999-9999", new_address="Rua Nova, 123", new_cep="12345-678")

        assert user.name == "Maria da div"
        assert user.email == "email@email.com"
        assert user.cellphone == "11 99999-9999"
        assert user.address == "Rua Nova, 123"
        assert user.cep == "12345-678"

    def test_update_user_one_parameter(self):
        repo = UserRepositoryMock()
        user = repo.update_user("5042b518-83ca-4cbf-84fc-c992da2506e5", new_name="Instituto Mauá de Tecnologia Atualizado", update_date=int(time.time()))

        assert user.name == "Instituto Mauá de Tecnologia Atualizado"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.update_user("501bdc27-951e-40ff-8d11-863ab36eb16d", update_date=int(time.time()), new_name="Bruno Guirão")

    def test_get_users_counter(self):
        repo = UserRepositoryMock()

        assert repo.get_user_counter() == 6

    def test_get_transactions_by_user(self):
        repo = UserRepositoryMock()
        transactions = repo.get_transactions_by_user(user_id="fdddafb9-687a-4982-a025-54fb12671932")

        assert len(transactions) == 3

    def test_get_transactions_by_user_empty(self):
        repo = UserRepositoryMock()
        transactions = repo.get_transactions_by_user(user_id="nonexistent-user-id")

        assert len(transactions) == 0

    def test_create_transaction(self):
        repo = UserRepositoryMock()

        # Verifica quantidade inicial de transações
        initial_count = len(repo.transactions)

        # Cria nova transação com UUID válido
        new_transaction = Transaction(
            tran_id=str(uuid.uuid4()),
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.SI,
            value=99.99,
            create_date=1717300000
        )

        created_transaction = repo.create_transaction(new_transaction)

        # Verifica se a transação foi criada corretamente
        assert created_transaction == new_transaction
        assert len(repo.transactions) == initial_count + 1

        # Verifica se a transação foi adicionada à lista
        assert repo.transactions[-1] == new_transaction

        # Verifica se a transação aparece nas consultas por usuário
        user_transactions = repo.get_transactions_by_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(user_transactions) == 4  # 3 existentes + 1 nova
        assert new_transaction in user_transactions

    def test_create_transaction_different_user(self):
        repo = UserRepositoryMock()

        # Cria transação para usuário diferente com UUID válido
        new_transaction = Transaction(
            tran_id=str(uuid.uuid4()),
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            plan=PlanEnum.GO,
            value=149.90,
            create_date=1717400000
        )

        created_transaction = repo.create_transaction(new_transaction)

        # Verifica se a transação foi criada
        assert created_transaction == new_transaction

        # Verifica se aparece apenas nas consultas do usuário correto
        user_transactions = repo.get_transactions_by_user("5042b518-83ca-4cbf-84fc-c992da2506e5")
        assert len(user_transactions) == 1
        assert user_transactions[0] == new_transaction

        # Verifica que não afeta as transações de outros usuários
        other_user_transactions = repo.get_transactions_by_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(other_user_transactions) == 3  # Mantém as 3 originais

    def test_create_subscription(self):
        repo = UserRepositoryMock()

        # Verifica quantidade inicial de subscriptions
        initial_count = len(repo.subscriptions)

        # Cria nova subscription com UUID válido
        new_subscription = Subscription(
            sub_id=str(uuid.uuid4()),
            user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.SI,
            update_date=1700500000
        )

        created_subscription = repo.create_subscription(new_subscription)

        # Verifica se a subscription foi criada corretamente
        assert created_subscription == new_subscription
        assert len(repo.subscriptions) == initial_count + 1

        # Verifica se a subscription foi adicionada à lista
        assert repo.subscriptions[-1] == new_subscription

        # Verifica se a subscription aparece nas consultas por usuário
        user_subscriptions = repo.get_subscriptions_by_user("a1b2c3d4-e5f6-7890-1234-567890abcdef")
        assert len(user_subscriptions) == 1  # Usuário não tinha subscriptions antes
        assert new_subscription in user_subscriptions

    def test_create_subscription_different_user(self):
        repo = UserRepositoryMock()

        # Cria subscription para usuário que já tem uma subscription
        new_subscription = Subscription(
            sub_id=str(uuid.uuid4()),
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.GO,
            new_plan=PlanEnum.BR,
            update_date=1700600000
        )

        created_subscription = repo.create_subscription(new_subscription)

        # Verifica se a subscription foi criada
        assert created_subscription == new_subscription

        # Verifica se aparece nas consultas do usuário correto
        user_subscriptions = repo.get_subscriptions_by_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(user_subscriptions) == 2  # 1 existente + 1 nova
        assert new_subscription in user_subscriptions

        # Verifica que não afeta as subscriptions de outros usuários
        other_user_subscriptions = repo.get_subscriptions_by_user("5042b518-83ca-4cbf-84fc-c992da2506e5")
        assert len(other_user_subscriptions) == 1  # Mantém a original

    def test_create_subscription_validates_same_plan(self):
        repo = UserRepositoryMock()

        # Tenta criar subscription com planos iguais (deve falhar)
        with pytest.raises(Exception):  # A entidade Subscription lança ForbiddenAction
            Subscription(
                sub_id=str(uuid.uuid4()),
                user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.BR,  # Mesmo plano
                update_date=1700700000
            )

    def test_get_subscriptions_by_user(self):
        repo = UserRepositoryMock()
        subscriptions = repo.get_subscriptions_by_user(user_id="fdddafb9-687a-4982-a025-54fb12671932")

        assert len(subscriptions) == 1
        assert subscriptions[0].sub_id == "fbf1af68-33c1-4f41-9290-5823158397a8"
        assert subscriptions[0].user_id == "fdddafb9-687a-4982-a025-54fb12671932"
        assert subscriptions[0].previous_plan == PlanEnum.BR
        assert subscriptions[0].new_plan == PlanEnum.GO

    def test_get_subscriptions_by_user_multiple(self):
        repo = UserRepositoryMock()
        subscriptions = repo.get_subscriptions_by_user(user_id="5042b518-83ca-4cbf-84fc-c992da2506e5")

        assert len(subscriptions) == 1
        assert subscriptions[0].previous_plan == PlanEnum.SI
        assert subscriptions[0].new_plan == PlanEnum.BR

    def test_get_subscriptions_by_user_empty(self):
        repo = UserRepositoryMock()
        subscriptions = repo.get_subscriptions_by_user(user_id="nonexistent-user-id")

        assert len(subscriptions) == 0

    def test_update_subscription(self):
        repo = UserRepositoryMock()

        # Verificar plano atual do usuário
        user_before = repo.get_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert user_before.plan == PlanEnum.GO

        # Atualizar subscription
        new_subscription = repo.update_subscription(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_plan=PlanEnum.SI
        )

        # Verificar que o plano do usuário foi atualizado
        user_after = repo.get_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert user_after.plan == PlanEnum.SI

        # Verificar dados da nova subscription
        assert new_subscription.user_id == "fdddafb9-687a-4982-a025-54fb12671932"
        assert new_subscription.previous_plan == PlanEnum.GO
        assert new_subscription.new_plan == PlanEnum.SI
        assert isinstance(new_subscription.update_date, int)
        assert new_subscription.update_date > 0

        # Verificar que a subscription foi adicionada à lista
        subscriptions = repo.get_subscriptions_by_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(subscriptions) == 2  # A original + a nova

    def test_update_subscription_user_not_found(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.update_subscription(
                user_id="nonexistent-user-id",
                new_plan=PlanEnum.SI
            )

    def test_create_knowledge_base(self):
        repo = UserRepositoryMock()
        initial_count = len(repo.kbs)

        kb = KnowledgeBase(
            id="Z9Y8X7W6V5",
            name="KB_Nova",
            description="KB para testes",
            created_at="2025-03-10T00:00:00Z",
            updated_at="2025-03-10T00:00:00Z",
            status="ACTIVE",
            documents_count=0,
            categories=["geral"],
            display_name="KB Nova",
            rds_table="embedding_Z9Y8X7W6V5",
        )

        created_kb = repo.create_knowledge_base(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            kb=kb,
        )

        assert created_kb == kb
        assert len(repo.kbs) == initial_count + 1
        assert repo.kbs[-1] == kb

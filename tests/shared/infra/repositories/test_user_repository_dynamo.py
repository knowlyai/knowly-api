import os
import time
import uuid

import pytest

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo


class TestUserRepositoryDynamo:
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        user = user_repository.get_user("fdddafb9-687a-4982-a025-54fb12671932")

        assert user.name == "Enzo Sakamoto"
        assert user.user_id == "fdddafb9-687a-4982-a025-54fb12671932"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user_not_found(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        with pytest.raises(NoItemsFound):
            user_repository.get_user("22412cb0-ca31-4b53-ac53-e2d0b6f9bef9")

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        test_user = User(
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

        created_user = user_repository.create_user(test_user)

        assert created_user.user_id == "24255c3c-cfff-40ad-899a-f9331c5b0dd8"
        assert created_user.name == "Vitor Soller"
        assert created_user.email == "dohype@vitin.com"
        assert created_user.cellphone == "11 99175-8098"
        assert created_user.p_type == PTypeEnum.PF
        assert created_user.cpf_cnpj == "37739658855"
        assert created_user.address == "Rua Tres Pedras, 915"
        assert created_user.cep == "04111111"
        assert created_user.plan == PlanEnum.BR
        assert created_user.creation_date == 1749079322
        assert created_user.update_date == 1749079323
        assert created_user.birthdate == 1022368922

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        test_user = User(
            user_id="c1cad83a-d406-4127-b828-b8045d699147",
            name="Edgar Kobayashi",
            email="saka@moto.com",
            cellphone="11 95320-2088",
            p_type=PTypeEnum.PF,
            cpf_cnpj="37973280871",
            address="Rua das Flores, 123",
            cep="04111111",
            plan=PlanEnum.GO,
            creation_date=1749079322,
            update_date=1749079323,
            birthdate=1022368922
        )

        user_repository.create_user(test_user)

        deleted_user = user_repository.delete_user("c1cad83a-d406-4127-b828-b8045d699147")

        assert deleted_user.name == "Edgar Kobayashi"
        assert deleted_user.user_id == "c1cad83a-d406-4127-b828-b8045d699147"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user_not_found(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        with pytest.raises(NoItemsFound):
            user_repository.delete_user("0bfa3e4d-ad8e-4735-963c-9463e8c6c9e2")

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        test_user = User(
            user_id="c1cad83a-d406-4127-b828-b8045d699147",
            name="Edgar Kobayashi",
            email="saka@moto.com",
            cellphone="11 95320-2088",
            p_type=PTypeEnum.PF,
            cpf_cnpj="37973280871",
            address="Rua das Flores, 123",
            cep="04111111",
            plan=PlanEnum.GO,
            creation_date=1749079322,
            update_date=1749079323,
            birthdate=1022368922
        )

        user_repository.create_user(test_user)

        updated_user = user_repository.update_user(
            "c1cad83a-d406-4127-b828-b8045d699147",
            update_date=int(time.time()),
            new_name="Maria da div",
            new_email="email@email.com",
            new_cellphone="11 99999-9999",
            new_address="Rua Nova, 123",
            new_cep="12345-678"
        )

        assert updated_user.name == "Maria da div"
        assert updated_user.email == "email@email.com"
        assert updated_user.cellphone == "11 99999-9999"
        assert updated_user.address == "Rua Nova, 123"
        assert updated_user.cep == "12345-678"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user_one_parameter(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        test_user = User(
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            name="Instituto Mauá de Tecnologia",
            email="imt@maua.br",
            cellphone="11 95320-2088",
            p_type=PTypeEnum.PJ,
            cpf_cnpj="60.749.736/0001-99",
            address="Praça Mauá, 1",
            cep="09580-900",
            plan=PlanEnum.BR,
            creation_date=1749079322,
            update_date=1749079323
        )

        user_repository.create_user(test_user)

        updated_user = user_repository.update_user(
            "5042b518-83ca-4cbf-84fc-c992da2506e5",
            new_name="Instituto Mauá de Tecnologia Atualizado",
            update_date=int(time.time())
        )

        assert updated_user.name == "Instituto Mauá de Tecnologia Atualizado"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user_not_found(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        with pytest.raises(NoItemsFound):
            user_repository.update_user(
                "501bdc27-951e-40ff-8d11-863ab36eb16d",
                update_date=int(time.time()),
                new_name="Bruno Guirão"
            )

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_transactions_by_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        transactions = user_repository.get_transactions_by_user(user_id="fdddafb9-687a-4982-a025-54fb12671932")

        assert len(transactions) == 3

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_transactions_by_user_empty(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        transactions = user_repository.get_transactions_by_user(user_id="nonexistent-user-id")

        assert len(transactions) == 0

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_transaction(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        # Cria nova transação com UUID válido
        new_transaction = Transaction(
            tran_id=str(uuid.uuid4()),
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.SI,
            value=99.99,
            create_date=1717300000
        )

        created_transaction = user_repository.create_transaction(new_transaction)

        assert created_transaction == new_transaction

        user_transactions = user_repository.get_transactions_by_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert any(t.tran_id == new_transaction.tran_id for t in user_transactions)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_subscription(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        new_subscription = Subscription(
            sub_id=str(uuid.uuid4()),
            user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.SI,
            update_date=1700500000
        )

        created_subscription = user_repository.create_subscription(new_subscription)

        assert created_subscription == new_subscription

        user_subscriptions = user_repository.get_subscriptions_by_user("a1b2c3d4-e5f6-7890-1234-567890abcdef")
        assert any(s.sub_id == new_subscription.sub_id for s in user_subscriptions)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_subscriptions_by_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        subscriptions = user_repository.get_subscriptions_by_user(user_id="fdddafb9-687a-4982-a025-54fb12671932")

        assert len(subscriptions) >= 1
        assert any(s.sub_id == "fbf1af68-33c1-4f41-9290-5823158397a8" for s in subscriptions)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_subscriptions_by_user_empty(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        subscriptions = user_repository.get_subscriptions_by_user(user_id="nonexistent-user-id")

        assert len(subscriptions) == 0

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_subscription(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        test_user = User(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
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
            birthdate=1022368922
        )

        user_repository.create_user(test_user)

        new_subscription = user_repository.update_subscription(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            new_plan=PlanEnum.SI
        )

        user_after = user_repository.get_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert user_after.plan == PlanEnum.SI

        assert new_subscription.user_id == "fdddafb9-687a-4982-a025-54fb12671932"
        assert new_subscription.previous_plan == PlanEnum.GO
        assert new_subscription.new_plan == PlanEnum.SI
        assert isinstance(new_subscription.update_date, int)
        assert new_subscription.update_date > 0

        subscriptions = user_repository.get_subscriptions_by_user("fdddafb9-687a-4982-a025-54fb12671932")
        assert any(s.sub_id == new_subscription.sub_id for s in subscriptions)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_subscription_user_not_found(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        with pytest.raises(NoItemsFound):
            user_repository.update_subscription(
                user_id="nonexistent-user-id",
                new_plan=PlanEnum.SI
            )

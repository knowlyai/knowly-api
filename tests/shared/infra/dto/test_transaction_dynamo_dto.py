from decimal import Decimal

from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.infra.dto.transaction_dynamo_dto import TransactionDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestTransactionDynamoDto:
    def test_from_entity(self):
        repo = UserRepositoryMock()
        transaction = repo.transactions[0]

        transaction_dto = TransactionDynamoDTO.from_entity(transaction=transaction)

        expected_transaction_dto = TransactionDynamoDTO(
            tran_id=transaction.tran_id,
            user_id=transaction.user_id,
            plan=transaction.plan,
            value=transaction.value,
            create_date=transaction.create_date
        )

        assert transaction_dto == expected_transaction_dto

    def test_to_dynamo(self):
        repo = UserRepositoryMock()
        transaction = repo.transactions[0]

        transaction_dto = TransactionDynamoDTO.from_entity(transaction=transaction)
        transaction_dynamo = transaction_dto.to_dynamo()

        expected_dict = {
            "entity": "transaction",
            "tran_id": transaction.tran_id,
            "user_id": transaction.user_id,
            "plan": transaction.plan.value,
            "value": Decimal(str(transaction.value)),
            "create_date": Decimal(transaction.create_date)
        }

        assert transaction_dynamo == expected_dict

    def test_from_dynamo(self):
        dynamo_dict = {
            "entity": "transaction",
            "tran_id": "a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
            "plan": "Bronze",
            "value": Decimal("29.9"),
            "create_date": Decimal("1717000000")
        }

        transaction_dto = TransactionDynamoDTO.from_dynamo(item=dynamo_dict)

        expected_transaction_dto = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        assert transaction_dto == expected_transaction_dto

    def test_to_entity(self):
        transaction_dto = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        transaction = transaction_dto.to_entity()

        assert transaction.tran_id == "a33e9c1d-8bb1-4634-9610-e09810f6e0c7"
        assert transaction.user_id == "fdddafb9-687a-4982-a025-54fb12671932"
        assert transaction.plan == PlanEnum.BR
        assert transaction.value == 29.9
        assert transaction.create_date == 1717000000

    def test_from_dynamo_to_entity(self):
        dynamo_item = {
            "entity": "transaction",
            "tran_id": "a33e9c1d-8bb1-4634-9610-e09810f6e0c8",
            "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
            "plan": "Silver",
            "value": Decimal("59.9"),
            "create_date": Decimal("1717100000")
        }

        transaction_dto = TransactionDynamoDTO.from_dynamo(item=dynamo_item)
        transaction = transaction_dto.to_entity()

        expected_transaction = Transaction(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.SI,
            value=59.9,
            create_date=1717100000
        )

        assert transaction.tran_id == expected_transaction.tran_id
        assert transaction.user_id == expected_transaction.user_id
        assert transaction.plan == expected_transaction.plan
        assert transaction.value == expected_transaction.value
        assert transaction.create_date == expected_transaction.create_date

    def test_from_entity_to_dynamo(self):
        repo = UserRepositoryMock()
        transaction = repo.transactions[1]

        transaction_dto = TransactionDynamoDTO.from_entity(transaction=transaction)
        transaction_dynamo = transaction_dto.to_dynamo()

        expected_dict = {
            "entity": "transaction",
            "tran_id": transaction.tran_id,
            "user_id": transaction.user_id,
            "plan": transaction.plan.value,
            "value": Decimal(str(transaction.value)),
            "create_date": Decimal(transaction.create_date)
        }

        assert transaction_dynamo == expected_dict

    def test_dto_equality(self):
        transaction_dto1 = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        transaction_dto2 = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        assert transaction_dto1 == transaction_dto2

    def test_dto_inequality(self):
        transaction_dto1 = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        transaction_dto2 = TransactionDynamoDTO(
            tran_id="different-id",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        assert transaction_dto1 != transaction_dto2

    def test_repr(self):
        transaction_dto = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.BR,
            value=29.9,
            create_date=1717000000
        )

        expected_repr = (
            "TransactionDynamoDTO("
            "tran_id='a33e9c1d-8bb1-4634-9610-e09810f6e0c7', "
            "user_id='fdddafb9-687a-4982-a025-54fb12671932', "
            "plan=PlanEnum.BR, "
            "value=29.9, "
            "create_date=1717000000"
            ")"
        )

        assert repr(transaction_dto) == expected_repr

    def test_value_decimal_conversion(self):
        """Testa se valores float são convertidos corretamente para Decimal no DynamoDB"""
        transaction_dto = TransactionDynamoDTO(
            tran_id="a33e9c1d-8bb1-4634-9610-e09810f6e0c7",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            plan=PlanEnum.GO,
            value=19.99,
            create_date=1717200000
        )

        dynamo_dict = transaction_dto.to_dynamo()

        assert isinstance(dynamo_dict["value"], Decimal)
        assert dynamo_dict["value"] == Decimal("19.99")

    def test_round_trip_conversion(self):
        """Testa conversão completa: entity -> dto -> dynamo -> dto -> entity"""
        repo = UserRepositoryMock()
        original_transaction = repo.transactions[2]

        # entity -> dto
        dto = TransactionDynamoDTO.from_entity(original_transaction)

        # dto -> dynamo
        dynamo_dict = dto.to_dynamo()

        # dynamo -> dto
        dto_from_dynamo = TransactionDynamoDTO.from_dynamo(dynamo_dict)

        # dto -> entity
        final_transaction = dto_from_dynamo.to_entity()

        # Verifica se os dados foram preservados
        assert final_transaction.tran_id == original_transaction.tran_id
        assert final_transaction.user_id == original_transaction.user_id
        assert final_transaction.plan == original_transaction.plan
        assert final_transaction.value == original_transaction.value
        assert final_transaction.create_date == original_transaction.create_date

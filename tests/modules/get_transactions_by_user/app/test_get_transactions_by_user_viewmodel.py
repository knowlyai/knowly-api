import pytest

from src.modules.get_transactions_by_user.app.get_transactions_by_user_viewmodel import (
    GetTransactionsByUserViewmodel
)
from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.enums.plan_enum import PLAN


class Test_GetTransactionsByUserViewmodel:

    def test_single_transaction(self):
        tx = Transaction(
            id="tx-1",
            user_id="user-1",
            plan=PLAN.BRONZE,
            value=50.0,
            create_date=1700000000
        )
        viewmodel = GetTransactionsByUserViewmodel([tx])
        result = viewmodel.to_dict()

        expected = {
            "transactions": [
                {
                    "id": "tx-1",
                    "user_id": "user-1",
                    "plan": "BRONZE",
                    "value": 50.0,
                    "create_date": 1700000000
                }
            ],
            "message": "transactions retrieved successfully"
        }
        assert result == expected

    def test_multiple_transactions(self):
        tx1 = Transaction(
            id="tx-1",
            user_id="user-1",
            plan=PLAN.SILVER,
            value=75.5,
            create_date=1700001000
        )
        tx2 = Transaction(
            id="tx-2",
            user_id="user-1",
            plan=PLAN.GOLD,
            value=120.0,
            create_date=1700002000
        )
        viewmodel = GetTransactionsByUserViewmodel([tx1, tx2])
        result = viewmodel.to_dict()

        expected = {
            "transactions": [
                {
                    "id": "tx-1",
                    "user_id": "user-1",
                    "plan": "SILVER",
                    "value": 75.5,
                    "create_date": 1700001000
                },
                {
                    "id": "tx-2",
                    "user_id": "user-1",
                    "plan": "GOLD",
                    "value": 120.0,
                    "create_date": 1700002000
                }
            ],
            "message": "transactions retrieved successfully"
        }
        assert result == expected

    def test_empty_list(self):
        viewmodel = GetTransactionsByUserViewmodel([])
        result = viewmodel.to_dict()

        expected = {
            "transactions": [],
            "message": "transactions retrieved successfully"
        }
        assert result == expected
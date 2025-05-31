from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.transaction_repository_mock import TransactionRepositoryMock
import pytest

class Test_TransactionRepositoryMock:

    def test_get_all_transactions_by_user_retorna_lista_correta(self):
        repo = TransactionRepositoryMock()

        # “user-1” possui duas transações no mock (tx-1 e tx-2)
        transacoes = repo.get_all_transactions_by_user("user-1")
        assert isinstance(transacoes, list)
        assert len(transacoes) == 2

        ids_retornados = {t.id for t in transacoes}
        assert "tx-1" in ids_retornados
        assert "tx-2" in ids_retornados

        # Verifica um dos campos de uma transação qualquer
        primeira = transacoes[0]
        assert isinstance(primeira, Transaction)
        assert primeira.user_id == "user-1"
        assert primeira.plan in (PLAN.BRONZE, PLAN.SILVER)

    def test_get_all_transactions_by_user_sem_resultados(self):
        repo = TransactionRepositoryMock()

        # Usuário “user-3” não existe no mock, logo não há transações
        transacoes = repo.get_all_transactions_by_user("user-3")
        assert isinstance(transacoes, list)
        assert transacoes == []  # lista vazia quando não encontra nada
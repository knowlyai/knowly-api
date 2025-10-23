from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.kb_key import KbKey


class IKeysRepository(ABC):

    @abstractmethod
    def create_kb_key(self, kb_key: KbKey) -> KbKey:
        """
        Creates a new API key for a knowledge base.
        """
        pass

    @abstractmethod
    def get_kb_keys(self, user_id: str, kb_id: str = None) -> List[KbKey]:
        """
        Retorna lista de KbKey do usuário.
        - Se kb_id for fornecido: retorna lista de chaves da KB específica
        - Caso contrário: retorna todas as chaves do usuário (lista possivelmente vazia)
        """
        pass

    @abstractmethod
    def delete_kb_key(self, user_id: str, kb_key: str) -> KbKey:
        """
        Deletes an API key.
        If key not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_kb_id_by_key(self, kb_key: str) -> str:
        """
        Retorna o kb_id associado à chave de API fornecida.
        Se a chave não for encontrada, levanta NoItemsFound.
        """
        pass

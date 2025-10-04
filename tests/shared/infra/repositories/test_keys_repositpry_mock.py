import pytest

from src.shared.domain.entities.kb_key import KbKey
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.keys_repository_mock import KeysRepositoryMock


class TestKeysRepositoryMock:
    def test_get_kb_keys_all_by_user(self):
        repo = KeysRepositoryMock()
        keys = repo.get_kb_keys(user_id="fdddafb9-687a-4982-a025-54fb12671932")

        assert len(keys) == 2
        assert all(key.user_id == "fdddafb9-687a-4982-a025-54fb12671932" for key in keys)

    def test_get_kb_keys_by_user_and_kb_id(self):
        repo = KeysRepositoryMock()
        keys = repo.get_kb_keys(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            kb_id="A1B2C3D4E5"
        )

        assert len(keys) == 2
        assert all(key.kb_id == "A1B2C3D4E5" for key in keys)
        assert keys[0].kb_key_alias == "Production API Key"
        assert keys[1].kb_key_alias == "Test API Key"

    def test_get_kb_keys_specific_kb(self):
        repo = KeysRepositoryMock()
        keys = repo.get_kb_keys(
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            kb_id="123456ABCD"
        )

        assert len(keys) == 1
        assert keys[0].kb_key == "mock_live_9f8e7d6c5b4a3e2d1c0b9a8f7e6d5c4b"
        assert keys[0].kb_key_alias == "IMT Main Key"

    def test_get_kb_keys_empty(self):
        repo = KeysRepositoryMock()
        keys = repo.get_kb_keys(user_id="nonexistent-user-id")

        assert len(keys) == 0

    def test_get_kb_keys_user_with_no_keys_for_specific_kb(self):
        repo = KeysRepositoryMock()
        keys = repo.get_kb_keys(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            kb_id="NONEXIST1"
        )

        assert len(keys) == 0

    def test_create_kb_key(self):
        repo = KeysRepositoryMock()
        initial_count = len(repo.kb_keys)

        new_key = KbKey(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            kb_id="A1B2C3D4E5",
            kb_key="mock_test_newkey123456789012345678901234",
            kb_key_alias="New Test Key"
        )

        created_key = repo.create_kb_key(new_key)

        assert created_key == new_key
        assert len(repo.kb_keys) == initial_count + 1
        assert repo.kb_keys[-1] == new_key

        # Verifica se a chave aparece nas consultas por usuário
        user_keys = repo.get_kb_keys("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(user_keys) == 3  # 2 existentes + 1 nova
        assert new_key in user_keys

    def test_create_kb_key_different_user(self):
        repo = KeysRepositoryMock()

        new_key = KbKey(
            user_id="9e8d7c6b-5a49-3827-1605-948372615038",
            kb_id="XYZ1234567",
            kb_key="mock_live_abcdefghijklmnopqrstuvwxyz1234",
            kb_key_alias="New User Key"
        )

        created_key = repo.create_kb_key(new_key)

        assert created_key == new_key

        # Verifica se aparece apenas nas consultas do usuário correto
        user_keys = repo.get_kb_keys("9e8d7c6b-5a49-3827-1605-948372615038")
        assert len(user_keys) == 1
        assert user_keys[0] == new_key

        # Verifica que não afeta as chaves de outros usuários
        other_user_keys = repo.get_kb_keys("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(other_user_keys) == 2  # Mantém as 2 originais

    def test_delete_kb_key(self):
        repo = KeysRepositoryMock()
        initial_count = len(repo.kb_keys)

        deleted_key = repo.delete_kb_key(
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            kb_key="mock_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        )

        assert deleted_key.kb_key == "mock_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        assert deleted_key.kb_key_alias == "Production API Key"
        assert len(repo.kb_keys) == initial_count - 1

        # Verifica se a chave foi removida das consultas
        user_keys = repo.get_kb_keys("fdddafb9-687a-4982-a025-54fb12671932")
        assert len(user_keys) == 1  # Tinha 2, removeu 1
        assert all(key.kb_key != "mock_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" for key in user_keys)

    def test_delete_kb_key_not_found(self):
        repo = KeysRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.delete_kb_key(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                kb_key="nonexistent_key"
            )

    def test_delete_kb_key_wrong_user(self):
        repo = KeysRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.delete_kb_key(
                user_id="wrong-user-id",
                kb_key="mock_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
            )

    def test_create_and_get_kb_key(self):
        repo = KeysRepositoryMock()

        new_key = KbKey(
            user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
            kb_id="abcDEF1234",
            kb_key="mock_test_createandget1234567890123456",
            kb_key_alias="Create and Get Test"
        )

        repo.create_kb_key(new_key)

        # Busca todas as chaves do usuário
        user_keys = repo.get_kb_keys("f7e6d5c4-b3a2-9180-7654-321098765432")
        assert len(user_keys) == 3  # 2 existentes + 1 nova

        # Busca chaves da KB específica
        kb_keys = repo.get_kb_keys(
            user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
            kb_id="abcDEF1234"
        )
        assert len(kb_keys) == 3
        assert any(key.kb_key == "mock_test_createandget1234567890123456" for key in kb_keys)

    def test_create_delete_create_sequence(self):
        repo = KeysRepositoryMock()

        # Cria uma nova chave
        new_key = KbKey(
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            kb_id="123456ABCD",
            kb_key="mock_temp_sequence_test_key_123456789012",
            kb_key_alias="Temporary Sequence Key"
        )
        repo.create_kb_key(new_key)

        # Verifica que foi criada
        keys = repo.get_kb_keys("5042b518-83ca-4cbf-84fc-c992da2506e5")
        assert len(keys) == 2

        # Deleta a chave
        repo.delete_kb_key(
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            kb_key="mock_temp_sequence_test_key_123456789012"
        )

        # Verifica que foi deletada
        keys = repo.get_kb_keys("5042b518-83ca-4cbf-84fc-c992da2506e5")
        assert len(keys) == 1

        # Cria novamente com o mesmo kb_key (agora é possível)
        new_key_2 = KbKey(
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            kb_id="123456ABCD",
            kb_key="mock_temp_sequence_test_key_123456789012",
            kb_key_alias="Recreated Key"
        )
        repo.create_kb_key(new_key_2)

        # Verifica que foi criada novamente
        keys = repo.get_kb_keys("5042b518-83ca-4cbf-84fc-c992da2506e5")
        assert len(keys) == 2
        assert any(key.kb_key_alias == "Recreated Key" for key in keys)

    def test_multiple_keys_same_kb(self):
        repo = KeysRepositoryMock()

        # Verifica usuário com múltiplas chaves na mesma KB
        keys = repo.get_kb_keys(
            user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
            kb_id="abcDEF1234"
        )

        assert len(keys) == 2
        aliases = {key.kb_key_alias for key in keys}
        assert "TechCorp Primary" in aliases
        assert "TechCorp Development" in aliases


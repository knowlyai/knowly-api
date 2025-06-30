import pytest
import time
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.type_enum import PTypeEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import MinorAgeError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


@pytest.fixture
def user_repository():
    """Fixture para criar uma instância do repositório mock"""
    return UserRepositoryMock()


@pytest.fixture
def create_user_usecase(user_repository):
    """Fixture para criar uma instância do use case"""
    return CreateUserUseCase(user_repository)


@pytest.fixture
def valid_pf_user_data():
    """Fixture com dados válidos para usuário pessoa física"""
    return {
        "user_id": "9750bdb8-9e02-4c32-b9f0-16c7bf466389",
        "name": "Vitor Soller",
        "email": "21.01444-2@maua.br",
        "cellphone": "11 991758098",
        "p_type": PTypeEnum.PF,
        "cpf_cnpj": "37739658855",
        "address": "Rua Três Pedras, 915",
        "cep": "03209-010",
        "birthdate": 1036795662,
        "plan": PlanEnum.BR
    }


@pytest.fixture
def valid_pj_user_data():
    """Fixture com dados válidos para usuário pessoa jurídica"""
    return {
        "user_id": "3eda6da8-4acb-474c-8806-904faae874d0",
        "name": "Empresa XYZ Ltda",
        "email": "contato@empresaxyz.com",
        "cellphone": "1134567890",
        "p_type": PTypeEnum.PJ,
        "cpf_cnpj": "60749736000199",
        "address": "Av. Paulista, 1000",
        "cep": "01310-100",
        "birthdate": None,
        "plan": PlanEnum.GO
    }


@pytest.fixture
def base_user_data():
    """Fixture com dados base para testes de erro"""
    return {
        "user_id": "5d76d01f-a10d-4acb-8c89-4f9df2413962",
        "name": "João Silva",
        "email": "joao@example.com",
        "cellphone": "11987654321",
        "p_type": PTypeEnum.PF,
        "cpf_cnpj": "71214584110",
        "address": "Rua das Flores, 123",
        "cep": "12345-678",
        "birthdate": int(time.time()) - (25 * 365 * 24 * 60 * 60),
        "plan": PlanEnum.BR
    }


@pytest.fixture
def adult_birthdate():
    """Fixture para data de nascimento de adulto (25 anos)"""
    return int(time.time()) - (25 * 365 * 24 * 60 * 60)


@pytest.fixture
def minor_birthdate():
    """Fixture para data de nascimento de menor (16 anos)"""
    return int(time.time()) - (16 * 365 * 24 * 60 * 60)


@pytest.fixture
def exactly_18_years_birthdate():
    """Fixture para data de nascimento de exatamente 18 anos"""
    return int(time.time()) - (18 * 365.25 * 24 * 60 * 60)


class TestCreateUserUseCase:

    def test_create_user_pf_success(self, create_user_usecase, valid_pf_user_data):
        result = create_user_usecase(**valid_pf_user_data)

        assert result.user_id == valid_pf_user_data["user_id"]
        assert result.name == valid_pf_user_data["name"]
        assert result.email == valid_pf_user_data["email"]
        assert result.cellphone == valid_pf_user_data["cellphone"]
        assert result.p_type == valid_pf_user_data["p_type"]
        assert result.cpf_cnpj == valid_pf_user_data["cpf_cnpj"]
        assert result.address == valid_pf_user_data["address"]
        assert result.cep == valid_pf_user_data["cep"]
        assert result.birthdate == valid_pf_user_data["birthdate"]
        assert result.plan == valid_pf_user_data["plan"]
        assert result.creation_date > 0
        assert result.update_date > 0

    def test_create_user_pj_success(self, create_user_usecase, valid_pj_user_data):
        result = create_user_usecase(**valid_pj_user_data)

        assert result.user_id == valid_pj_user_data["user_id"]
        assert result.name == valid_pj_user_data["name"]
        assert result.email == valid_pj_user_data["email"]
        assert result.cellphone == valid_pj_user_data["cellphone"]
        assert result.p_type == valid_pj_user_data["p_type"]
        assert result.cpf_cnpj == valid_pj_user_data["cpf_cnpj"]
        assert result.address == valid_pj_user_data["address"]
        assert result.cep == valid_pj_user_data["cep"]
        assert result.birthdate is None
        assert result.plan == valid_pj_user_data["plan"]
        assert result.creation_date > 0
        assert result.update_date > 0

    def test_create_user_minor_age_error(self, create_user_usecase, minor_birthdate):
        with pytest.raises(MinorAgeError):
            create_user_usecase(
                user_id="f8b1c2d3-4e5f-6a7b-8c9d-e0f1g2h3i4j5",
                name="Ning Caudhari",
                email="joao.jovem@example.com",
                cellphone="11987654321",
                p_type=PTypeEnum.PF,
                cpf_cnpj="71214584110",
                address="Rua das Flores, 123",
                cep="12345-678",
                birthdate=minor_birthdate,
                plan=PlanEnum.BR
            )

    def test_create_user_invalid_user_id_error(self, create_user_usecase, base_user_data):
        test_data = base_user_data.copy()
        test_data["user_id"] = "invalid-uuid"

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo user_id não é válido"

    def test_create_user_invalid_name_error(self, create_user_usecase, base_user_data):
        test_data = base_user_data.copy()
        test_data["name"] = "Jo"  # Nome muito curto

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo name não é válido"

    def test_create_user_invalid_email_error(self, create_user_usecase, base_user_data):
        test_data = base_user_data.copy()
        test_data["email"] = "email-inválido"

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo email não é válido"

    def test_create_user_invalid_cellphone_error(self, create_user_usecase, base_user_data):
        """Teste de erro para celular inválido"""
        test_data = base_user_data.copy()
        test_data["cellphone"] = "123"  # Celular inválido

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo cellphone não é válido"

    def test_create_user_invalid_address_error(self, create_user_usecase, base_user_data):
        """Teste de erro para endereço inválido"""
        test_data = base_user_data.copy()
        test_data["address"] = "Rua"  # Endereço muito curto

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo address não é válido"

    def test_create_user_invalid_cep_error(self, create_user_usecase, base_user_data):
        """Teste de erro para CEP inválido"""
        test_data = base_user_data.copy()
        test_data["cep"] = "123"  # CEP inválido

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo cep não é válido"

    def test_create_user_exactly_18_years_success(self, create_user_usecase, base_user_data, exactly_18_years_birthdate):
        """Teste para usuário com exatamente 18 anos (caso limite)"""
        test_data = base_user_data.copy()
        test_data["birthdate"] = int(exactly_18_years_birthdate)

        result = create_user_usecase(**test_data)
        assert result.birthdate == int(exactly_18_years_birthdate)

    def test_create_user_without_birthdate_success(self, create_user_usecase, base_user_data):
        """Teste para criação de usuário sem data de nascimento"""
        test_data = base_user_data.copy()
        test_data["birthdate"] = None
        test_data["cpf_cnpj"] = "712.145.841-10"

        result = create_user_usecase(**test_data)
        assert result.birthdate is None

    def test_create_user_invalid_cpf_error(self, create_user_usecase, base_user_data):
        """Teste de erro para CPF inválido"""
        test_data = base_user_data.copy()
        test_data["cpf_cnpj"] = "123.456.789-00"

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo cpf_cnpj não é válido"

    # noinspection PyTypeChecker
    def test_create_user_invalid_cnpj_error(self, create_user_usecase, base_user_data):
        test_data = base_user_data.copy()
        test_data.update({
            "name": "Maua Tecnologia",
            "p_type": PTypeEnum.PJ,
            "cpf_cnpj": "00000000000000",  # CNPJ inválido
            "birthdate": None
        })

        with pytest.raises(EntityError) as exc_info:
            create_user_usecase(**test_data)
        assert str(exc_info.value) == "O campo cpf_cnpj não é válido"

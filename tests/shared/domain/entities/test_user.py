from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.helpers.errors.domain_errors import EntityError
import pytest


class TestUser:
    def test_user(self):
        new_user = User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
             name="Enzo Sakamoto",
             email="umemail@email.com",
             cellphone="11999999999",
             p_type=PTypeEnum.PF,
             address="hk1h9RpDz",
             cep="04111111",
             plan=PlanEnum.GO,
             creation_date=1749079322,
             update_date=1749079323,
             cpf_cnpj="37973280871",
             birthdate=1022368922)

        assert new_user.user_id == "2ea1333c-4647-4ef9-a58a-4721ed293d08"
        assert new_user.name == "Enzo Sakamoto"
        assert new_user.email == "umemail@email.com"
        assert new_user.cellphone == "11999999999"
        assert new_user.p_type == PTypeEnum.PF
        assert new_user.address == "hk1h9RpDz"
        assert new_user.cep == "04111111"
        assert new_user.plan == PlanEnum.GO
        assert new_user.creation_date == 1749079322
        assert new_user.update_date == 1749079323
        assert new_user.cpf_cnpj == "37973280871"
        assert new_user.birthdate == 1022368922

    def test_user_pj(self):
        new_user = User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                        name="Instituto Mauá de Tecnologia",
                        email="random@email.com",
                        cellphone="11999999999",
                        p_type=PTypeEnum.PJ,
                        address="hk1h9RpDz",
                        cep="04111111",
                        plan=PlanEnum.GO,
                        creation_date=1749079322,
                        update_date=1749079323,
                        cpf_cnpj="60749736000199",
                        birthdate=None)

        assert new_user.user_id == "2ea1333c-4647-4ef9-a58a-4721ed293d08"
        assert new_user.p_type == PTypeEnum.PJ
        assert new_user.cpf_cnpj == "60749736000199"

    def test_user_name_is_none(self):
        with pytest.raises(EntityError):
            User(name=None,
                 email="21.01444-2@maua.br",
                 user_id="7fb750f3-fcd3-4fd0-b405-6c4a890f20bd",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922
                 )

    def test_user_name_is_not_str(self):
        with pytest.raises(EntityError):
            User(name=1,
                 email="21.01444-2@maua.br",
                 user_id="7fb750f3-fcd3-4fd0-b405-6c4a890f20bd",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922,
                 )

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(name="V",
                 email="21.01444-2@maua.br",
                 user_id="7fb750f3-fcd3-4fd0-b405-6c4a890f20bd",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922,
                 )

    def test_user_email_is_none(self):
        with pytest.raises(EntityError):
            User(name="Vitor Soller",
                 email=None,
                 user_id="7fb750f3-fcd3-4fd0-b405-6c4a890f20bd",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37739658855",
                 birthdate=1022368922,
                 )

    def test_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            User(name="Vitor",
                 email="21.01444-2maua.br",
                 user_id="7fb750f3-fcd3-4fd0-b405-6c4a890f20bd",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922,
                 )

    def test_user_user_id_is_not_str(self):
        with pytest.raises(EntityError):
            User(user_id=1,
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_user_id_is_not_uuid(self):
        with pytest.raises(EntityError):
            User(user_id="not_a_uuid",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_cellphone_is_not_str(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone=11999999999,
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_cellphone_is_not_valid_format(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="1234digit",
                 p_type=PTypeEnum.PF,
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_p_type_is_not_instance_of_ptype_enum(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type="not_a_p_type",
                 address="hk1h9RpDz",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922
                 )

    def test_user_address_is_none(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
             name="Enzo Sakamoto",
             email="umemail@email.com",
             cellphone="11999999999",
             p_type=PTypeEnum.PF,
             address=None,
             cep="04111111",
             plan=PlanEnum.GO,
             creation_date=1749079322,
             update_date=1749079323,
             cpf_cnpj="37973280871",
             birthdate=1022368922)

    def test_user_address_is_not_str(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address=123,  # Not a string
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_address_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="rua",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_cpf_cnpj_is_empty(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="",  # Empty string instead of None
                 birthdate=1022368922)

    def test_user_cpf_invalid_format(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="123456789",  # Invalid format (too short)
                 birthdate=1022368922)

    def test_user_cpf_invalid_verification_digits(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="12345678901",  # Valid format but invalid verification digits
                 birthdate=1022368922)

    def test_user_cpf_repeated_digits(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="11111111111",  # All repeated digits
                 birthdate=1022368922)

    def test_user_cnpj_invalid_format(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Empresa XYZ",
                 email="empresa@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PJ,
                 address="Rua das Empresas, 456",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="123456789",  # Invalid format (too short)
                 birthdate=None)

    def test_user_cnpj_invalid_verification_digits(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Empresa XYZ",
                 email="empresa@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PJ,
                 address="Rua das Empresas, 456",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="12345678901234",  # Valid format but invalid verification digits
                 birthdate=None)

    def test_user_cnpj_repeated_digits(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Empresa XYZ",
                 email="empresa@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PJ,
                 address="Rua das Empresas, 456",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="11111111111111",  # All repeated digits
                 birthdate=None)

    def test_user_cep_is_none(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep=None,
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_cep_invalid_format(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="123456",  # Invalid format (too short)
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_plan_is_not_instance_of_plan_enum(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan="not_a_plan",  # Not a PlanEnum instance
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_creation_date_is_not_int(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date="not_an_int",  # Not an integer
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_update_date_is_not_int(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date="not_an_int",  # Not an integer
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_update_date_not_greater_than_creation_date(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079321,  # Same as creation_date
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_update_date_less_than_creation_date(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079321,  # Less than creation_date
                 cpf_cnpj="37973280871",
                 birthdate=1022368922)

    def test_user_birthdate_is_not_int(self):
        with pytest.raises(EntityError):
            User(user_id="2ea1333c-4647-4ef9-a58a-4721ed293d08",
                 name="Enzo Sakamoto",
                 email="umemail@email.com",
                 cellphone="11999999999",
                 p_type=PTypeEnum.PF,
                 address="Rua das Flores, 123",
                 cep="04111111",
                 plan=PlanEnum.GO,
                 creation_date=1749079322,
                 update_date=1749079323,
                 cpf_cnpj="37973280871",
                 birthdate="not_an_int")  # Not an integer

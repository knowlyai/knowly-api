from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum


class TestCreateUserViewModel:
    def test_create_user_viewmodel(self):
        user = User(
            user_id="50b0f552-cae5-4cf8-9cee-ff832407f738",
            name="Eric Akhtar",
            email="vitinho@hype.com",
            cellphone="11999999999",
            p_type=PTypeEnum.PF,
            cpf_cnpj="71214584110",
            address="Rua das Flores, 123",
            cep="12345678",
            birthdate=None,
            plan=PlanEnum.GO,
            creation_date=1680000000,
            update_date=1680000000
        )
        user_viewmodel = CreateUserViewmodel(user=user).to_dict()

        print(user_viewmodel)
        print('teste')
        expected = {
            "user": {
                    'user_id': "50b0f552-cae5-4cf8-9cee-ff832407f738",
                    'name': 'Eric Akhtar',
                    'email': 'vitinho@hype.com',
                    'cellphone': '11999999999',
                    'p_type': PTypeEnum.PF.value,
                    'cpf_cnpj': '71214584110',
                    'address': 'Rua das Flores, 123',
                    'cep': '12345678',
                    'birthdate': None,
                    'plan': PlanEnum.GO.value,
                    'creation_date': 1680000000,
                    'update_date': 1680000000
            },
                    'message': 'the user was created successfully'}

        assert expected == user_viewmodel

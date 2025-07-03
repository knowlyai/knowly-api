from src.modules.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum


class TestGetUserViewModel:
    def test_get_user_viewmodel(self):
        user = User(
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
        user_viewmodel = GetUserViewmodel(user=user).to_dict()

        expected = {
            'user': {
                'user_id': 'fdddafb9-687a-4982-a025-54fb12671932',
                'name': 'Enzo Sakamoto',
                'email': 'saka@moto.com',
                'cellphone': '11 95320-2088',
                'p_type': 'PF',
                'cpf_cnpj': '37973280871',
                'address': 'Rua das Flores, 123',
                'cep': '04111111',
                'birthdate': 1022368922,
                'plan': 'Gold',
                'creation_date': 1749079322,
                'update_date': 1749079323
            },
            'message': 'the user was retrieved successfully'
        }

        assert expected == user_viewmodel

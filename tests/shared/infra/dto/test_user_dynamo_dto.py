from decimal import Decimal

from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.enums.ptype_enum import PTypeEnum
from src.shared.domain.enums.state_enum import STATE
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUserDynamoDto:
    def test_from_entity(self):
        repo = UserRepositoryMock()
        user = repo.users[0]

        user_dto = UserDynamoDTO.from_entity(user=user)

        expected_user_dto = UserDynamoDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            cellphone=user.cellphone,
            p_type=user.p_type,
            cpf_cnpj=user.cpf_cnpj,
            address=user.address,
            cep=user.cep,
            birthdate=user.birthdate,
            plan=user.plan,
            creation_date=user.creation_date,
            update_date=user.update_date
        )

        assert user_dto == expected_user_dto

    def test_to_dynamo(self):
        repo = UserRepositoryMock()
        user = repo.users[0]

        user_dto = UserDynamoDTO.from_entity(user=user)
        user_dynamo = user_dto.to_dynamo()

        expected_dict = {
            "entity": "user",
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "cellphone": user.cellphone,
            "p_type": user.p_type.value,
            "cpf_cnpj": user.cpf_cnpj,
            "address": user.address,
            "cep": user.cep,
            "birthdate": Decimal(user.birthdate),
            "plan": user.plan.value,
            "creation_date": Decimal(user.creation_date),
            "update_date": Decimal(user.update_date)
        }

        assert user_dynamo == expected_dict

    def test_to_dynamo_without_birthdate(self):
        repo = UserRepositoryMock()
        user = repo.users[1]  # User without birthdate

        user_dto = UserDynamoDTO.from_entity(user=user)
        user_dynamo = user_dto.to_dynamo()

        expected_dict = {
            "entity": "user",
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "cellphone": user.cellphone,
            "p_type": user.p_type.value,
            "cpf_cnpj": user.cpf_cnpj,
            "address": user.address,
            "cep": user.cep,
            "plan": user.plan.value,
            "creation_date": Decimal(user.creation_date),
            "update_date": Decimal(user.update_date)
        }

        assert user_dynamo == expected_dict
        assert "birthdate" not in user_dynamo

    def test_from_dynamo(self):
        dynamo_dict = {
            'user_id': 'fdddafb9-687a-4982-a025-54fb12671932',
            'name': 'Enzo Sakamoto',
            'email': 'saka@moto.com',
            'cellphone': '11 95320-2088',
            'p_type': 'PF',
            'cpf_cnpj': '37973280871',
            'address': 'Rua das Flores, 123',
            'cep': '04111111',
            'birthdate': Decimal('1022368922'),
            'plan': 'Gold',
            'creation_date': Decimal('1749079322'),
            'update_date': Decimal('1749079323'),
            'entity': 'user'
        }

        user_dto = UserDynamoDTO.from_dynamo(user_data=dynamo_dict)

        expected_user_dto = UserDynamoDTO(
            user_id='fdddafb9-687a-4982-a025-54fb12671932',
            name='Enzo Sakamoto',
            email='saka@moto.com',
            cellphone='11 95320-2088',
            p_type=PTypeEnum.PF,
            cpf_cnpj='37973280871',
            address='Rua das Flores, 123',
            cep='04111111',
            birthdate=1022368922,
            plan=PlanEnum.GO,
            creation_date=1749079322,
            update_date=1749079323
        )

        assert user_dto == expected_user_dto

    def test_from_dynamo_without_birthdate(self):
        dynamo_dict = {
            'user_id': '5042b518-83ca-4cbf-84fc-c992da2506e5',
            'name': 'Instituto Mauá de Tecnologia',
            'email': 'imt@maua.br',
            'cellphone': '11 95320-2088',
            'p_type': 'PJ',
            'cpf_cnpj': '60.749.736/0001-99',
            'address': 'Praça Mauá, 1',
            'cep': '09580-900',
            'plan': 'Bronze',
            'creation_date': Decimal('1749079322'),
            'update_date': Decimal('1749079323'),
            'entity': 'user'
        }

        user_dto = UserDynamoDTO.from_dynamo(user_data=dynamo_dict)

        expected_user_dto = UserDynamoDTO(
            user_id='5042b518-83ca-4cbf-84fc-c992da2506e5',
            name='Instituto Mauá de Tecnologia',
            email='imt@maua.br',
            cellphone='11 95320-2088',
            p_type=PTypeEnum.PJ,
            cpf_cnpj='60.749.736/0001-99',
            address='Praça Mauá, 1',
            cep='09580-900',
            birthdate=None,
            plan=PlanEnum.BR,
            creation_date=1749079322,
            update_date=1749079323
        )

        assert user_dto == expected_user_dto

    def test_to_entity(self):
        user_dto = UserDynamoDTO(
            user_id='fdddafb9-687a-4982-a025-54fb12671932',
            name='Enzo Sakamoto',
            email='saka@moto.com',
            cellphone='11 95320-2088',
            p_type=PTypeEnum.PF,
            cpf_cnpj='37973280871',
            address='Rua das Flores, 123',
            cep='04111111',
            birthdate=1022368922,
            plan=PlanEnum.GO,
            creation_date=1749079322,
            update_date=1749079323
        )

        user = user_dto.to_entity()

        assert user.user_id == 'fdddafb9-687a-4982-a025-54fb12671932'
        assert user.name == 'Enzo Sakamoto'
        assert user.email == 'saka@moto.com'
        assert user.cellphone == '11 95320-2088'
        assert user.p_type == PTypeEnum.PF
        assert user.cpf_cnpj == '37973280871'
        assert user.address == 'Rua das Flores, 123'
        assert user.cep == '04111111'
        assert user.birthdate == 1022368922
        assert user.plan == PlanEnum.GO
        assert user.creation_date == 1749079322
        assert user.update_date == 1749079323

    def test_from_dynamo_to_entity(self):
        dynamo_item = {
            'user_id': 'fdddafb9-687a-4982-a025-54fb12671932',
            'name': 'Enzo Sakamoto',
            'email': 'saka@moto.com',
            'cellphone': '11 95320-2088',
            'p_type': 'PF',
            'cpf_cnpj': '37973280871',
            'address': 'Rua das Flores, 123',
            'cep': '04111111',
            'birthdate': Decimal('1022368922'),
            'plan': 'Gold',
            'creation_date': Decimal('1749079322'),
            'update_date': Decimal('1749079323'),
            'entity': 'user'
        }

        user_dto = UserDynamoDTO.from_dynamo(user_data=dynamo_item)
        user = user_dto.to_entity()

        expected_user = User(
            user_id='fdddafb9-687a-4982-a025-54fb12671932',
            name='Enzo Sakamoto',
            email='saka@moto.com',
            cellphone='11 95320-2088',
            p_type=PTypeEnum.PF,
            cpf_cnpj='37973280871',
            address='Rua das Flores, 123',
            cep='04111111',
            birthdate=1022368922,
            plan=PlanEnum.GO,
            creation_date=1749079322,
            update_date=1749079323
        )

        assert user.user_id == expected_user.user_id
        assert user.name == expected_user.name
        assert user.email == expected_user.email
        assert user.cellphone == expected_user.cellphone
        assert user.p_type == expected_user.p_type
        assert user.cpf_cnpj == expected_user.cpf_cnpj
        assert user.address == expected_user.address
        assert user.cep == expected_user.cep
        assert user.birthdate == expected_user.birthdate
        assert user.plan == expected_user.plan
        assert user.creation_date == expected_user.creation_date
        assert user.update_date == expected_user.update_date

    def test_from_entity_to_dynamo(self):
        repo = UserRepositoryMock()
        user = repo.users[0]

        user_dto = UserDynamoDTO.from_entity(user=user)
        user_dynamo = user_dto.to_dynamo()

        expected_dict = {
            "entity": "user",
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "cellphone": user.cellphone,
            "p_type": user.p_type.value,
            "cpf_cnpj": user.cpf_cnpj,
            "address": user.address,
            "cep": user.cep,
            "birthdate": Decimal(user.birthdate),
            "plan": user.plan.value,
            "creation_date": Decimal(user.creation_date),
            "update_date": Decimal(user.update_date)
        }

        assert user_dynamo == expected_dict

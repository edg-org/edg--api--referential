from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.electrical.repositories.ConnectionPoleRepo import ConnectionPoleRepo

class TestConnectionPoleRepository(TestCase):
    session: Session
    poleRepository: ConnectionPoleRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.poleRepository = ConnectionPoleRepo(self.session)
        
    @patch("api.electrical.schemas.ConnectionPoleSchema.CreateConnectionPole", autospec=True)
    def test_create(self, CreateConnectionPole):
        fake = Faker()
        supply: List[CreateConnectionPole] = CreateConnectionPole(
            pole_number=fake,
            transformer_id=fake,
            area_id=fake,
            infos= dict(
                number=fake,
                name=fake,
                area_code=fake,
                electrical_code=fake,
                transformer_code=fake,
                address=fake,
                transformers=[
                    dict(
                        electrical_code=fake,
                        activation_dated=fake
                    )
                ],
                departure_area_code=fake,
                departure_address=fake,
                is_owner=fake,
                voltage_measurement_unit=fake
            )
        )
        a: List[CreateConnectionPole] = self.poleRepository.create(supply)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == supply)
    
    @patch("api.electrical.models.ConnectionPoleModel.ConnectionPoleModel", autospec=True)
    def test_delete(self, ConnectionPoleModel):
        pole = ConnectionPoleModel(id=1)
        self.poleRepository.delete(pole)
        self.session.delete.assert_called_once_with(pole)

    @patch("api.electrical.models.ConnectionPoleModel.ConnectionPoleModel", autospec=True)
    def test_get(self, ConnectionPoleModel):
        pole = ConnectionPoleModel(id=1)
        self.poleRepository.get(pole)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.poleRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.electrical.schemas.ConnectionPoleSchema.CreateConnectionPole", autospec=True)
    def test_update(self, CreateConnectionPole):
        fake = Faker()
        pole : CreateConnectionPole = CreateConnectionPole(
            infos= dict(
                number=fake,
                name=fake,
                area_code=fake,
                electrical_code=fake,
                transformer_code=fake,
                address=fake,
                transformers=[
                    dict(
                        electrical_code=fake,
                        activation_dated=fake
                    )
                ],
                departure_area_code=fake,
                departure_address=fake,
                is_owner=fake,
                voltage_measurement_unit=fake
            )
        )
        self.poleRepository.update(pole)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
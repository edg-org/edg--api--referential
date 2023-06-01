from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.electrical.repositories.ElectricMeterRepo import ElectricMeterRepo

class TestElectricMeterRepository(TestCase):
    session: Session
    meterRepository: ElectricMeterRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.meterRepository = ElectricMeterRepo(self.session)
        
    @patch("api.electrical.schemas.ElectricMeterSchema.CreateElectricMeter", autospec=True)
    def test_create(self, CreateElectricMeter):
        fake = Faker()
        supply: List[CreateElectricMeter] = CreateElectricMeter(
            meter_number=fake,
            infos= dict(
                brand=fake,
                meter_type=fake,
                supply_mode=fake,
                index_reading=fake,
                manufacturing_country=fake
            )
        )
        a: List[CreateElectricMeter] = self.meterRepository.create(supply)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == supply)
    
    @patch("api.electrical.models.ElectricMeterModel.ElectricMeterModel", autospec=True)
    def test_delete(self, ElectricMeterModel):
        pole = ElectricMeterModel(id=1)
        self.meterRepository.delete(pole)
        self.session.delete.assert_called_once_with(pole)

    @patch("api.electrical.models.ElectricMeterModel.ElectricMeterModel", autospec=True)
    def test_get(self, ElectricMeterModel):
        pole = ElectricMeterModel(id=1)
        self.meterRepository.get(pole)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.meterRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.electrical.schemas.ElectricMeterSchema.CreateElectricMeter", autospec=True)
    def test_update(self, CreateElectricMeter):
        fake = Faker()
        pole : CreateElectricMeter = CreateElectricMeter(
            infos= dict(
                brand=fake,
                meter_type=fake,
                supply_mode=fake,
                index_reading=fake,
                manufacturing_country=fake
            )
        )
        self.meterRepository.update(pole)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
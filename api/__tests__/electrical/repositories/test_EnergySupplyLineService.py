from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import Mock, create_autospec, patch
from api.electrical.repositories.EnergySupplyLineRepo import EnergySupplyLineRepo

class TestSupplyLineRepository(TestCase):
    session: Session
    supplylineRepository: EnergySupplyLineRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.supplylineRepository = EnergySupplyLineRepo(self.session)
        
    @patch("api.electrical.schemas.EnergySupplyLineSchema.CreateEnergySupplyLine", autospec=True)
    def test_create(self, CreateEnergySupplyLine):
        fake = Faker()
        supply: List[CreateEnergySupplyLine] = CreateEnergySupplyLine(
            code=fake,
            line_type_id=fake,
            voltage_type_id=fake,
            departure_area_id=fake,
            infos= dict(
                name=fake,
                line_type=fake,
                voltage_type=fake,
                real_voltage=fake,
                electrical_code=fake,
                maximum_power=fake,
                power_measurement_unit=fake,
                departure_area_code=fake,
                departure_address=fake,
                is_owner=fake,
                voltage_measurement_unit=fake
            )
        )
        a: List[CreateEnergySupplyLine] = self.supplylineRepository.create(supply)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == supply)
    
    @patch("api.electrical.models.EnergySupplyLineModel.EnergySupplyLineModel", autospec=True)
    def test_delete(self, EnergySupplyLineModel):
        supplyline = EnergySupplyLineModel(id=1)
        self.supplylineRepository.delete(supplyline)
        self.session.delete.assert_called_once_with(supplyline)

    @patch("api.electrical.models.EnergySupplyLineModel.EnergySupplyLineModel", autospec=True)
    def test_get(self, EnergySupplyLineModel):
        supplyline = EnergySupplyLineModel(id=1)
        self.supplylineRepository.get(supplyline)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.supplylineRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.electrical.schemas.EnergySupplyLineSchema.CreateEnergySupplyLine", autospec=True)
    def test_update(self, CreateEnergySupplyLine):
        fake = Faker()
        data : CreateEnergySupplyLine = CreateEnergySupplyLine(
            infos= dict(
                name=fake,
                line_type=fake,
                voltage_type=fake,
                real_voltage=fake,
                electrical_code=fake,
                maximum_power=fake,
                power_measurement_unit=fake,
                departure_area_code=fake,
                departure_address=fake,
                is_owner=fake,
                voltage_measurement_unit=fake
            )
        )
        self.supplylineRepository.update = Mock()
        self.supplylineRepository.update(1, data)
        self.supplylineRepository.update.assert_called_with(1, data)
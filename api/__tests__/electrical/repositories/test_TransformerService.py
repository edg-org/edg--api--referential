from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch, Mock
from api.electrical.repositories.TransformerRepo import TransformerRepo

class TestTransformerRepository(TestCase):
    session: Session
    transformerRepository: TransformerRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.transformerRepository = TransformerRepo(self.session)
        
    @patch("api.electrical.schemas.TransformerSchema.CreateTransformer", autospec=True)
    def test_create(self, CreateTransformer):
        fake = Faker()
        supply: List[CreateTransformer] = CreateTransformer(
            transformer_code=fake,
            area_id=fake,
            fixation_type_id=fake,
            infos= dict(
                name=fake,
                brand=fake,
                power_mesurement_unit=fake,
                fixation_type=fake,
                area_code=fake,
                electrical_code=fake,
                tranformer_serial_number=fake,
                manufacturing_country=fake,
                energy_supply_lines=[
                    dict(
                        electrical_code=fake,
                        is_actived=fake,
                        activation_dated=fake
                    )
                ]
            )
        )
        a: List[CreateTransformer] = self.transformerRepository.create(supply)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == supply)
    
    @patch("api.electrical.models.TransformerModel.TransformerModel", autospec=True)
    def test_delete(self, TransformerModel):
        pole = TransformerModel(id=1)
        self.transformerRepository.delete(pole)
        self.session.delete.assert_called_once_with(pole)

    @patch("api.electrical.models.TransformerModel.TransformerModel", autospec=True)
    def test_get(self, TransformerModel):
        pole = TransformerModel(id=1)
        self.transformerRepository.get(pole)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.transformerRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.electrical.schemas.TransformerSchema.CreateTransformer", autospec=True)
    def test_update(self, CreateTransformer):
        fake = Faker()
        data : CreateTransformer = CreateTransformer(
            infos= dict(
                name=fake,
                brand=fake,
                power_mesurement_unit=fake,
                fixation_type=fake,
                area_code=fake,
                electrical_code=fake,
                tranformer_serial_number=fake,
                manufacturing_country=fake,
                energy_supply_lines=[
                    dict(
                        electrical_code=fake,
                        is_actived=fake,
                        activation_dated=fake
                    )
                ]
            )
        )
        self.transformerRepository.update = Mock()
        self.transformerRepository.update(1, data)
        self.transformerRepository.update.assert_called_with(1, data)
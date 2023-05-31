import json
from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.ageographical.repositories.CityRepo import CityRepo

class TestCityRepository(TestCase):
    session: Session
    cityRepository: CityRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.cityRepository = CityRepo(self.session)

    @patch("api.ageographical.schemas.CitySchema.CreateCity", autospec=True)
    def test_create(self, CreateCity):
        fake = Faker()
        city: List[CreateCity] = CreateCity(
            code=fake,
            zipcode=fake,
            city_type_id=fake,
            city_level_id=fake,
            prefecture_id=fake,
            infos=fake
        )
        a: List[CreateCity] = self.cityRepository.create(city)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == city)

    @patch("api.ageographical.models.CityModel.CityModel", autospec=True)
    def test_delete(self, CityModel):
        city = CityModel(id=1)
        self.cityRepository.delete(city)
        self.session.delete.assert_called_once_with(city)

    @patch("api.ageographical.models.CityModel.CityModel", autospec=True)
    def test_get(self, CityModel):
        city = CityModel(id=1)
        self.cityRepository.get(city)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.cityRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.ageographical.schemas.CitySchema.CreateCity", autospec=True)
    def test_update(self, CreateCity):
        fake = Faker()
        city : CreateCity = CreateCity(
            code=fake,
            zipcode=fake,
            city_type_id=fake,
            city_level_id=fake,
            prefecture_id=fake,
            infos=fake
        )
        self.cityRepository.update(city)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
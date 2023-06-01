import json
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
        city = CreateCity(name=self.loadJson())
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
        city : CreateCity = CreateCity(
            code=201458,
            zipcode="02000",
            city_type_id=1,
            city_level_id=1,
            prefecture_id=10,
            infos=dict(
                prefecture="boké",
                name="Dabiss",
                city_type="Commune Urbaine",
                city_level="Sous-préfecture"
            )
        )
        self.cityRepository.update(city)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        
    #
    def loadJson(self):
        f = open("api/__tests__/json/cities_input.json")
        a = json.load(f)
        f.close()
        return a
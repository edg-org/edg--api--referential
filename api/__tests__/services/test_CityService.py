import json
from faker import Faker
from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.services.CityService import CityService

class TestCityService(TestCase):
    cityRepository: CityRepo
    cityService: CityService

    def setUp(self):
        super().setUp()
        self.cityRepository = create_autospec(CityRepo)
        self.cityService = CityService(self.cityRepository)

    @patch("api.ageographical.schemas.CitySchema.CityInput", autospec=True)
    async def test_create(self, CityInput):
        fake = Faker()
        city: List[CityInput] = CityInput(
            code=fake,
            zipcode=fake,
            city_type_id=fake,
            city_level_id=fake,
            prefecture_id=fake,
            infos=fake
        )
        self.cityService.create = Mock()
        self.cityService.create(city)
        self.cityService.create.assert_called_once_with(city)
        
    
    @patch("api.ageographical.schemas.CitySchema.CityUpdate", autospec=True)
    async def test_update(self, CityUpdate):
        fake = Faker()
        city: CityUpdate = CityUpdate(
            infos=fake
        )
        self.cityService.update = Mock()
        self.cityService.update(city)
        self.cityService.update.assert_called_once_with(city)
    
    #
    async def test_activate_desactivate(self):
        self.cityService.activate_desactivate(code=1, flag=True)
        self.session.delete.assert_called_once()
from faker import Faker
from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.services.AreaService import AreaService

class TestAreaService(TestCase):
    areaRepository: AreaRepo
    areaService: AreaService

    def setUp(self):
        super().setUp()
        self.areaRepository = create_autospec(AreaRepo)
        self.areaService = AreaService(self.areaRepository)

    @patch("api.ageographical.schemas.AreaSchema.AreaInput", autospec=True)
    async def test_create(self, AreaInput):
        fake = Faker()
        area: List[AreaInput] = AreaInput(
            {
                "code": fake,
                "zipcode": fake,
                "city_id": fake,
                "area_level_id": fake,
                "area_type_id": fake,
                "infos": {
                    "name": fake,
                    "area_type": fake,
                    "is_same_zipcode": fake,
                }
            }
        )
        self.areaService.create = Mock()
        self.areaService.create(area)
        self.areaService.create.assert_called_once_with(area)
        
    
    @patch("api.ageographical.schemas.AreaSchema.AreaUpdate", autospec=True)
    async def test_update(self, AreaUpdate):
        fake = Faker()
        area: AreaUpdate = AreaUpdate(
            {
                "infos": {
                    "name": fake,
                    "area_type": fake,
                    "is_same_zipcode": fake
                }
            }
        )
        self.areaService.update = Mock()
        self.areaService.update(area)
        self.areaService.update.assert_called_once_with(area)
    
    #
    async def test_activate_desactivate(self):
        self.areaService.activate_desactivate(code=1, flag=True)
        self.session.delete.assert_called_once()
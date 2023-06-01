from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.ageographical.repositories.RegionRepo import RegionRepo
from api.ageographical.services.RegionService import RegionService

class TestRegionService(TestCase):
    regionRepository: RegionRepo
    regionService: RegionService

    def setUp(self):
        super().setUp()
        self.regionRepository = create_autospec(RegionRepo)
        self.regionService = RegionService(self.regionRepository)

    @patch("api.ageographical.schemas.RegionSchema.RegionInput", autospec=True)
    async def test_create(self, RegionInput):
        region: List[RegionInput] = RegionInput(
            {
                "name": "Région de Mamou",
                "code": 1042,
                "zone_id": 10,
                "infos": {
                    "natural_zone": "moyenne guinée"
                }
            }
        )
        self.regionService.create = Mock()
        self.regionService.create(region)
        self.regionService.create.assert_called_once_with(region)
        
    @patch("api.ageographical.schemas.RegionSchema.RegionUpdate", autospec=True)
    async def test_update(self, RegionUpdate):
        region: RegionUpdate = RegionUpdate(
            {
                "name": "Région de Mamou",
                "infos": {
                    "natural_zone": "moyenne guinée"
                }
            }
        )
        self.regionService.update = Mock()
        self.regionService.update(region)
        self.regionService.update.assert_called_once_with(region)
    
    #
    async def test_activate_desactivate(self):
        self.regionService.activate_desactivate(code=1, flag=True)
        self.session.delete.assert_called_once()
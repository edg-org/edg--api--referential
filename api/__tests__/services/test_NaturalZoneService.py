from faker import Faker
from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.ageographical.repositories.NaturalZoneRepo import ZoneRepo
from api.ageographical.services.NaturalZoneService import ZoneService

class TestNaturalZoneService(TestCase):
    zoneRepository: ZoneRepo
    zoneService: ZoneService

    def setUp(self):
        super().setUp()
        self.zoneRepository = create_autospec(ZoneRepo)
        self.zoneService = ZoneService(self.zoneRepository)

    @patch("api.ageographical.schemas.NaturalZoneSchema.ZoneInput", autospec=True)
    async def test_create(self, ZoneInput):
        fake = Faker()
        zone: List[ZoneInput] = ZoneInput(
            {
                "code":fake,
                "name":fake
            }
        )
        self.zoneService.create = Mock()
        self.zoneService.create(zone)
        self.zoneService.create.assert_called_once_with(zone)
        
    
    @patch("api.ageographical.schemas.NaturalZoneSchema.ZoneUpdate", autospec=True)
    async def test_update(self, ZoneUpdate):
        fake = Faker()
        zone: ZoneUpdate = ZoneUpdate(
            {
                "name":fake
            }
        )
        self.zoneService.update = Mock()
        self.zoneService.update(zone)
        self.zoneService.update.assert_called_once_with(zone)
    
    #
    async def test_activate_desactivate(self):
        self.zoneService.activate_desactivate(code=1)
        self.session.delete.assert_called_once()
import json
from faker import Faker
from typing import List
from unittest import TestCase
from unittest.mock import create_autospec, patch
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
    def test_create(self, ZoneInput):
        fake = Faker()
        zone: List[ZoneInput] = ZoneInput(name=fake.name())
        self.zoneService.create(zone)
        self.zoneRepository.create.assert_called_one()
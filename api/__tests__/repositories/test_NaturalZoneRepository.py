import json
from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.ageographical.repositories.NaturalZoneRepo import ZoneRepo

class TestZoneRepository(TestCase):
    session: Session
    zoneRepository: ZoneRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.zoneRepository = ZoneRepo(self.session)

    @patch("api.ageographical.schemas.NaturalZoneSchema.CreateZone", autospec=True)
    def test_create(self, CreateZone):
        fake = Faker()
        zone: List[CreateZone] = CreateZone(name=fake.name())
        a: List[CreateZone] = self.zoneRepository.create(zone)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == zone)

    @patch("api.ageographical.models.NaturalZoneModel.ZoneModel", autospec=True)
    def test_delete(self, ZoneModel):
        zone = ZoneModel(id=1)
        self.zoneRepository.delete(zone)
        self.session.delete.assert_called_once_with(zone)

    @patch("api.ageographical.models.NaturalZoneModel.ZoneModel", autospec=True)
    def test_get(self, ZoneModel):
        zone = ZoneModel(id=1)
        self.zoneRepository.get(zone)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.zoneRepository.list(0, 100)
        # Should call query method on Session
        self.session.query.assert_called_once()
        # Should call filter_by method on QueryResponse

    @patch("api.ageographical.schemas.NaturalZoneSchema.CreateZone", autospec=True)
    def test_update(self, CreateZone):
        fake = Faker()
        zone : CreateZone = CreateZone(name=fake.name())
        self.zoneRepository.update(zone)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
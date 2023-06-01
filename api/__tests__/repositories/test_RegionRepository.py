from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.ageographical.repositories.RegionRepo import RegionRepo

class TestRegionRepository(TestCase):
    session: Session
    regionRepository: RegionRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.regionRepository = RegionRepo(self.session)

    @patch("api.ageographical.schemas.RegionSchema.CreateRegion", autospec=True)
    def test_create(self, CreateRegion):
        fake = Faker()
        region = CreateRegion(
            name=fake,
            code=fake,
            zone_id=fake,
            infos= dict(
                natural_zone=fake
            )
        )
        a: List[CreateRegion] = self.regionRepository.create(region)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == region)

    @patch("api.ageographical.models.RegionModel.RegionModel", autospec=True)
    def test_delete(self, RegionModel):
        region = RegionModel(id=1)
        self.regionRepository.delete(region)
        self.session.delete.assert_called_once_with(region)

    @patch("api.ageographical.models.RegionModel.RegionModel", autospec=True)
    def test_get(self, RegionModel):
        region = RegionModel(id=1)
        self.regionRepository.get(region)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.regionRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.ageographical.schemas.RegionSchema.CreateRegion", autospec=True)
    def test_update(self, CreateRegion):
        fake = Faker()
        region : CreateRegion = CreateRegion(
            name=fake,
            code=fake,
            zone_id=fake,
            infos= dict(
                natural_zone=fake
            )
        )
        self.regionRepository.update(region)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
    
    def loadJson(self):
        f = open("api/__tests__/json/regions_input.json")
        a = json.load(f)
        f.close()
        return a
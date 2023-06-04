from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.ageographical.repositories.AreaRepo import AreaRepo

class TestAreaRepository(TestCase):
    session: Session
    areaRepository: AreaRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.areaRepository = AreaRepo(self.session)

    @patch("api.ageographical.schemas.AreaSchema.CreateArea", autospec=True)
    def test_create(self, CreateArea):
        fake = Faker()
        area: List[CreateArea] = CreateArea(
            code=fake,
            zipcode=fake,
            city_id=fake,
            area_type_id=fake,
            infos=dict(
                name=fake,
                area_type=fake,
                is_same_zipcode=fake
            )
        )
        a: List[CreateArea] = self.areaRepository.create(area)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == area)

    @patch("api.ageographical.models.AreaModel.AreaModel", autospec=True)
    def test_delete(self, AreaModel):
        area = AreaModel(id=1)
        self.areaRepository.delete(area)
        self.session.delete.assert_called_once_with(area)

    @patch("api.ageographical.models.AreaModel.AreaModel", autospec=True)
    def test_get(self, AreaModel):
        area = AreaModel(id=1)
        self.areaRepository.get(area)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.areaRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.ageographical.schemas.AreaSchema.CreateArea", autospec=True)
    def test_update(self, CreateArea):
        fake = Faker()
        area : CreateArea = CreateArea(
            code=fake,
            zipcode=fake,
            city_id=fake,
            area_type_id=fake,
            infos=dict(
                name=fake,
                area_type=fake,
                is_same_zipcode=fake
            )
        )
        self.areaRepository.update(area)
        self.session.merge.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
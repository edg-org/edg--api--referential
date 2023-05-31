import json
from faker import Faker
from typing import List
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import create_autospec, patch
from api.ageographical.repositories.PrefectureRepo import PrefectureRepo

class TestPrefectureRepository(TestCase):
    session: Session
    prefectureRepository: PrefectureRepo

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.prefectureRepository = PrefectureRepo(self.session)

    @patch("api.ageographical.schemas.PrefectureSchema.CreatePrefecture", autospec=True)
    def test_create(self, CreatePrefecture):
        fake = Faker()
        prefecture: List[CreatePrefecture] = CreatePrefecture(
            name=fake,
            code=fake,
            is_capital=fake,
            prefecture_number=fake,
            region_id=fake,
            infos=fake
        )
        a: List[CreatePrefecture] = self.prefectureRepository.create(prefecture)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(a == prefecture)

    @patch("api.ageographical.models.PrefectureModel.PrefectureModel", autospec=True)
    def test_delete(self, PrefectureModel):
        prefecture = PrefectureModel(id=1)
        self.prefectureRepository.delete(prefecture)
        self.session.delete.assert_called_once_with(prefecture)

    @patch("api.ageographical.models.PrefectureModel.PrefectureModel", autospec=True)
    def test_get(self, PrefectureModel):
        prefecture = PrefectureModel(id=1)
        self.prefectureRepository.get(prefecture)
        self.session.query.assert_called_once()
    
    def test_list(self):
        self.prefectureRepository.list(0, 100)
        self.session.query.assert_called_once()

    @patch("api.ageographical.schemas.PrefectureSchema.CreatePrefecture", autospec=True)
    def test_update(self, CreatePrefecture):
        fake = Faker()
        prefecture : CreatePrefecture = CreatePrefecture(
            name=fake,
            code=fake,
            is_capital=fake,
            prefecture_number=fake,
            region_id=fake,
            infos=fake
        )
        self.prefectureRepository.update(prefecture)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.ageographical.repositories.PrefectureRepo import PrefectureRepo
from api.ageographical.services.PrefectureService import PrefectureService

class TestPrefectureService(TestCase):
    prefectureRepository: PrefectureRepo
    prefectureService: PrefectureService

    def setUp(self):
        super().setUp()
        self.prefectureRepository = create_autospec(PrefectureRepo)
        self.prefectureService = PrefectureService(self.prefectureRepository)

    @patch("api.ageographical.schemas.PrefectureSchema.PrefectureInput", autospec=True)
    async def test_create(self, PrefectureInput):
        prefecture: List[PrefectureInput] = PrefectureInput(
            {
                "name": "Mamou",
                "region_id": 10254,
                "prefecture_number": 10,
                "is_capital": True,
                "infos": {
                    "region": "région de mamou"
                }
            }
        )
        self.prefectureService.create = Mock()
        self.prefectureService.create(prefecture)
        self.prefectureService.create.assert_called_once_with(prefecture)
        
    
    @patch("api.ageographical.schemas.PrefectureSchema.PrefectureUpdate", autospec=True)
    async def test_update(self, PrefectureUpdate):
        prefecture: PrefectureUpdate = PrefectureUpdate(
            {
                "name": "Mamou",
                "is_capital": True,
                "infos": {
                    "region": "région de mamou"
                }
            }
        )
        self.prefectureService.update = Mock()
        self.prefectureService.update(prefecture)
        self.prefectureService.update.assert_called_once_with(prefecture)
    
    #
    async def test_activate_desactivate(self):
        self.prefectureService.activate_desactivate(code=1, flag=True)
        self.session.delete.assert_called_once()
from typing import List
from datetime import datetime
from api.tools.Helper import prefecture_basecode
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.RegionRepo import RegionRepo
from api.ageographical.models.PrefectureModel import PrefectureModel
from api.ageographical.repositories.PrefectureRepo import PrefectureRepo
from api.ageographical.schemas.PrefectureSchema import (
    PrefectureInput,
    PrefectureUpdate,
    CreatePrefecture,
)

#
class PrefectureService:
    prefecture: PrefectureRepo

    def __init__(
        self, prefecture: PrefectureRepo = Depends()
    ) -> None:
        self.prefecture = prefecture

    # get all prefectures function
    async def list(self, skip: int = 0, limit: int = 100) -> List[PrefectureModel]:
        return self.prefecture.list(skip=skip, limit=limit)

    # get prefecture by id function
    async def get(self, id: int) -> PrefectureModel:
        return self.prefecture.get(id=id)

    # get prefecture by code function
    async def getbycode(self, code: str) -> PrefectureModel:
        return self.prefecture.getbycode(code=code)

    # get prefecture by name function
    async def getbyname(self, name: str) -> PrefectureModel:
        return self.prefecture.getbyname(name=name)

    # create prefecture function
    async def create(self, data: List[PrefectureInput]) -> List[CreatePrefecture]:
        step = 0
        row_number = self.prefecture.countrows()
        if row_number is not None:
            step = row_number
        prefecturelist = []
        for item in data:
            count = self.prefecture.countbyname(name=item.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Prefecture already registered with name " + item.infos.name,
                )
            
            step += 1
            basecode = prefecture_basecode(item.infos.region_code)
            prefecture_code = basecode + step
            count = self.prefecture.countbycode(code=prefecture_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Prefecture already registered with code " + str(prefecture_code),
                )
            
            prefecture = CreatePrefecture(
                code = prefecture_code,
                name = item.name,
                is_capital = item.is_capital,
                prefecture_number = str((prefecture_code % 100)).zfill(2),
                region_id = RegionRepo.getidbycode(self.prefecture, item.infos.region_code),
                infos = item.infos
            )
            prefecturelist.append(prefecture)

        return self.prefecture.create(data=prefecturelist)

    # update prefecture function
    async def update(self, code: int, data: PrefectureUpdate) -> PrefectureModel:
        count = self.prefecture.countbycode(code=code)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prefecture not found",
            )

        prefecture = CreatePrefecture(
            code = code,
            name = data.name,
            is_capital = data.is_capital,
            prefecture_number = str((prefecture_code % 100)).zfill(2),
            region_id = RegionRepo.getidbycode(self.prefecture, data.infos.region_code),
            infos = data.infos
        )

        prefecturedict = prefecture.dict(exclude_unset=True)
        for key, val in prefecturedict.items():
            setattr(prefecture, key, val)
        return self.prefecture.update(prefecture)

    # activate or desactivate region function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        count = self.prefecture.countbycode(code=code)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prefecture not found",
            )
        region.is_activated = flag
        message = "Prefecture desactivated"
        region.deleted_at = datetime.utcnow().isoformat()
        if flag == True:
            region.deleted_at = None
            message = "Prefecture activated"

        self.prefecture.update(region)
        return HTTPException(
            status_code=status.HTTP_200_OK, detail=message
        )

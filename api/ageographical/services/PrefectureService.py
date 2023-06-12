from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
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
    log: LogService
    prefecture: PrefectureRepo

    def __init__(
        self, 
        log: LogService = Depends(),
        prefecture: PrefectureRepo = Depends()
    ) -> None:
        self.log = log
        self.prefecture = prefecture

    # get all prefectures function
    async def list(self, start: int = 0, size: int = 100) -> (int, List[PrefectureModel]):
        return self.prefecture.list(start=start, size=size)

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
                    detail=f"Prefecture already registered with name {item.infos.name}",
                )
            
            step += 1
            region = RegionRepo.getbyname(self.prefecture, item.infos.region)
            basecode = Helper.prefecture_basecode(region.code)
            prefecture_code = basecode + step
            count = self.prefecture.countbycode(code=prefecture_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Prefecture already registered with code {prefecture_code}",
                )
            
            prefecture = CreatePrefecture(
                code = prefecture_code,
                name = item.name,
                is_capital = item.is_capital,
                prefecture_number = str((prefecture_code % 100)).zfill(2),
                region_id = region.id,
                infos = item.infos
            )
            prefecturelist.append(prefecture)

        return self.prefecture.create(data=prefecturelist)

    # update prefecture function
    async def update(self, code: int, tokendata: dict, data: PrefectureUpdate) -> PrefectureModel:
        old_data = jsonable_encoder(self.prefecture.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prefecture not found",
            )
        
        data.region_id = RegionRepo.getidbyname(self.prefecture, data.infos.region)
        current_data = jsonable_encoder(self.prefecture.update(code=code, data=data.dict()))
        logs = [await Helper.build_log(f"/prefectures/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate region function
    async def activate_desactivate(self, code: int, flag: bool, tokendata: dict) -> None:
        old_data = jsonable_encoder(self.prefecture.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prefecture not found",
            )
        message = "Prefecture desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Prefecture activated"
        
        data = dict(
            is_activated = flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.prefecture.update(code=code, data=data))
        logs = [await Helper.build_log(f"/prefectures/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)
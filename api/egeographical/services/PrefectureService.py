from typing import List
from datetime import datetime
from api.tools.Helper import prefecture_basecode
from fastapi import Depends, HTTPException, status
from api.egeographical.repositories.RegionRepo import (
    RegionRepo,
)
from api.egeographical.models.PrefectureModel import (
    PrefectureModel,
)
from api.egeographical.repositories.PrefectureRepo import (
    PrefectureRepo,
)
from api.egeographical.schemas.PrefectureSchema import (
    PrefectureBase,
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
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[PrefectureModel]:
        return self.prefecture.list(skip=skip, limit=limit)

    # get prefecture by id function
    async def get(self, id: int) -> PrefectureModel:
        return self.prefecture.get(id=id)

    # get prefecture by code function
    async def getbycode(self, code: str) -> PrefectureBase:
        return self.prefecture.getbycode(code=code)

    # get prefecture by name function
    async def getbyname(self, name: str) -> PrefectureBase:
        return self.prefecture.getbyname(name=name)

    # create prefecture function
    async def create(
        self, data: List[CreatePrefecture]
    ) -> List[CreatePrefecture]:
        step = 0
        row_number = self.prefecture.countrows()
        if row_number is not None:
            step = row_number

        for item in data:
            step += 1
            item.region_id = RegionRepo.getidbycode(
                self.prefecture, item.infos.region_code
            )
            basecode = prefecture_basecode(
                item.infos.region_code
            )
            prefecture_code = basecode + step
            item.code = prefecture_code
            item.prefecture_number = str(
                (prefecture_code % 100)
            ).zfill(2)

            prefecture = self.prefecture.getbycode(
                code=prefecture_code
            )
            if prefecture:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Prefecture already registered with code "
                    + str(item.code),
                )

            prefecture = self.prefecture.getbyname(
                name=item.infos.name
            )
            if prefecture:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Prefecture already registered with name "
                    + item.infos.name,
                )

        return self.prefecture.create(data=data)

    # update prefecture function
    async def update(
        self, code: int, data: PrefectureBase
    ) -> PrefectureModel:
        prefecture = self.prefecture.getbycode(code=code)
        if prefecture is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prefecture not found",
            )

        prefecturedict = data.dict(exclude_unset=True)
        for key, val in prefecturedict.items():
            setattr(prefecture, key, val)
        return self.prefecture.update(prefecture)

    # activate or desactivate region function
    async def activate_desactivate(
        self, id: int, flag: bool
    ) -> None:
        region = self.naturalRegion.get(id=id)
        if region is None:
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

        self.naturalRegion.update(region)
        return HTTPException(
            status_code=status.HTTP_200_OK, detail=message
        )

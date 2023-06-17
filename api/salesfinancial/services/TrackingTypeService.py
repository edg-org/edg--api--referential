from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.TrackingTypeModel import TrackingTypeModel
from api.salesfinancial.schemas.TrackingTypeSchema import CreateTrackingType
from api.salesfinancial.repositories.TrackingTypeRepo import TrackingTypeRepo
from fastapi.encoders import jsonable_encoder
from api.tools.Helper import build_log
from api.logs.repositories.LogRepo import LogRepo

class TrackingTypeService:
    trackingtype: TrackingTypeRepo
    log: LogRepo

    def __init__(
        self, trackingtype: TrackingTypeRepo = Depends(), log: LogRepo = Depends()
    ) -> None:
        self.trackingtype = trackingtype
        self.log = log

    # get all tracking types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[TrackingTypeModel]:
        return self.trackingtype.list(
            skip=skip, limit=limit
        )

    # get tracking type by id function
    async def get(self, id: int) -> TrackingTypeModel:
        return self.trackingtype.get(id=id)

    # get tracking type by code function
    async def getbycode(self, code: int) -> TrackingTypeModel:
        return self.trackingtype.getbycode(code=code)

    # get tracking type by name function
    async def getbyname(self, name: str) -> TrackingTypeModel:
        return self.trackingtype.getbyname(name=name)

    # create tracking type function
    async def create(self, data: List[CreateTrackingType]) -> List[CreateTrackingType]:
        for item in data:
            trackingtype = self.trackingtype.getbycode(code=item.code)
            if trackingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tracking Type already registered with code "
                    + str(item.code),
                )

            trackingtype = self.trackingtype.getbyname(name=item.name)
            if trackingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tracking Type already registered with name "
                    + item.name,
                )

        return self.trackingtype.create(data=data)

    # update tracking type function
    # async def update(self, code: int, data: CreateTrackingType) -> TrackingTypeModel:
    #     trackingtype = self.trackingtype.getbycode(code=code)
    #     if trackingtype is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Tracking Type not found",
    #         )
    #
    #     typedict = data.dict(exclude_unset=True)
    #     for key, val in typedict.items():
    #         setattr(trackingtype, key, val)
    #     return self.trackingtype.update(trackingtype)

    async def update(self, code: int, data: CreateTrackingType) -> TrackingTypeModel:
        old_data = jsonable_encoder(self.trackingtype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tracking Type not found",
            )

        verif = self.trackingtype.verif_duplicate(data.name, "TrackingTypeModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.name})

        current_data = jsonable_encoder(self.trackingtype.update(code=code, data=data.dict()))
        logs = [await build_log(f"/trackingtype/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete tracking type %function
    async def delete(self, tracking: TrackingTypeModel) -> None:
        code = 0
        trackingtype = self.trackingtype.getbycode(code=code)
        if trackingtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tracking Type not found",
            )

        self.trackingtype.update(tracking)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Tracking Type deleted",
        )

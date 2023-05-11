from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.TrackingTypeModel import TrackingTypeModel
from api.salesfinancial.schemas.TrackingTypeSchema import CreateTrackingType
from api.salesfinancial.repositories.TrackingTypeRepo import TrackingTypeRepo

class TrackingTypeService:
    trackingtype: TrackingTypeRepo

    def __init__(
        self, trackingtype: TrackingTypeRepo = Depends()
    ) -> None:
        self.trackingtype = trackingtype

    # get all tracking types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[TrackingTypeModel]:
        return self.trackingtype.list(
            skip=skip, limit=limit
        )

    # get tracking type by id function
    async def get(self, id: int) -> TrackingTypeModel:
        return self.trackingtype.get(id=id)

    # get tracking type by code function
    async def getbycode(self, code: str) -> TrackingTypeModel:
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
    async def update(self, code: int, data: CreateTrackingType) -> TrackingTypeModel:
        trackingtype = self.trackingtype.getbycode(code=code)
        if trackingtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tracking Type not found",
            )

        typedict = data.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(trackingtype, key, val)
        return self.trackingtype.update(trackingtype)

    # delete tracking type %function
    async def delete(self, tracking: TrackingTypeModel) -> None:
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
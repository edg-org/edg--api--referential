from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.ConnectionPointModel import (
    ConnectionPointModel,
)
from api.electrical.repositories.ConnectionPointRepo import (
    ConnectionPointRepo,
)
from api.electrical.schemas.ConnectionPointSchema import (
    ConnectionPointBase,
    CreateConnectionPoint,
)


#
class ConnectionPointService:
    connectionpoint: ConnectionPointRepo

    def __init__(
        self,
        connectionpoint: ConnectionPointRepo = Depends(),
    ) -> None:
        self.connectionpoint = connectionpoint

    # get all connection points function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[ConnectionPointModel]:
        return self.connectionpoint.list(
            skip=skip, limit=limit
        )

    # get connection point by id function
    async def get(self, id: int) -> ConnectionPointModel:
        return self.connectionpoint.get(id=id)

    # get connection point by number function
    async def getbynumber(
        self, number: int
    ) -> ConnectionPointBase:
        return self.connectionpoint.getbynumber(
            number=number
        )

    # get connection point by name function
    async def getbyname(
        self, name: str
    ) -> ConnectionPointBase:
        return self.connectionpoint.getbyname(name=name)

    # create connection point function
    async def create(
        self, data: List[CreateConnectionPoint]
    ) -> List[CreateConnectionPoint]:
        for item in data:
            connectionpoint = (
                self.connectionpoint.getbycode(
                    code=item.code
                )
            )
            if connectionpoint:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Connection Point already registered with code "
                    + str(item.code),
                )

            connectionpoint = (
                self.connectionpoint.getbyname(
                    name=item.name
                )
            )
            if connectionpoint:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Connection Point already registered with name "
                    + item.name,
                )

        return self.connectionpoint.create(data=data)

    # update connection point function
    async def update(
        self, number: int, data: ConnectionPointBase
    ) -> ConnectionPointModel:
        connectionpoint = self.connectionpoint.getbynumber(
            number=number
        )
        if connectionpoint is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection Point not found",
            )

        connectionpointdict = data.dict(exclude_unset=True)
        for key, val in connectionpointdict.items():
            setattr(connectionpoint, key, val)
        return self.connectionpoint.update(connectionpoint)

    # delete connection point function
    async def delete(
        self, connectionpoint: ConnectionPointModel
    ) -> None:
        connectionpoint = self.connectionpoint.get(id=id)
        if connectionpoint is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection Point not found",
            )

        self.connectionpoint.update(connectionpoint)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Connection Point deleted",
        )

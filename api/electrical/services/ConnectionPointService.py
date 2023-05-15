from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.tools.Helper import connectionpoint_basecode, generate_code
from api.electrical.repositories.TransformerRepo import TransformerRepo
from api.electrical.models.ConnectionPointModel import ConnectionPointModel
from api.electrical.repositories.ConnectionPointRepo import ConnectionPointRepo
from api.electrical.schemas.ConnectionPointSchema import (
    ConnectionPointUpdate,
    CreateConnectionPoint
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
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ConnectionPointModel]:
        return self.connectionpoint.list(skip=skip, limit=limit)

    # get connection point by id function
    async def get(self, id: int) -> ConnectionPointModel:
        return self.connectionpoint.get(id=id)

    # get connection point by number function
    async def getbynumber(self, number: int) -> ConnectionPointModel:
        return self.connectionpoint.getbynumber(number=number)

    # get connection point by name function
    async def getbyname(self, name: str) -> ConnectionPointModel:
        return self.connectionpoint.getbyname(name=name)

    # create connection point function
    async def create(self, data: List[ConnectionPointUpdate]) -> List[CreateConnectionPoint]:
        #step = 0
        area_code = None
        connectionpointlist = []
        for item in data:
            if (area_code is not None) and  (area_code != item.infos.area_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of connection points for one area at a time"
                )
                
            #step += 1
            result = generate_code(
                init_codebase=connectionpoint_basecode(item.infos.area_code),
                maxcode=self.connectionpoint.maxnumberbyarea(item.infos.area_code),
                step=item.infos.number
            )
            connection_point_number = result["code"]

            count = self.connectionpoint.countbynumber(number=connection_point_number)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Connection Point already registered with code " + str(connection_point_number),
                )
                
            connectionpoint = CreateConnectionPoint(
                connection_point_number = str(connection_point_number),
                area_id = AreaRepo.getidbycode(self.connectionpoint, item.infos.area_code),
                transformer_id = TransformerRepo.getidbycode(self.connectionpoint, item.infos.transformer_code),
                infos = item.infos
            )
            connectionpointlist.append(connectionpoint)
            area_code = item.infos.area_code
            
        return self.connectionpoint.create(data=connectionpointlist)

    # update connection point function
    async def update(self, number: int, data: ConnectionPointModel) -> ConnectionPointModel:
        connectionpoint = self.connectionpoint.getbynumber(number=number)
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
    async def delete(self, connectionpoint: ConnectionPointModel) -> None:
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
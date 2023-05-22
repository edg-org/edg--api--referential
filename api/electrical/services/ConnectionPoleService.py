from typing import List
from fastapi import Depends, HTTPException, status
from api.tools.Helper import pole_basecode, generate_code
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.electrical.repositories.TransformerRepo import TransformerRepo
from api.electrical.models.ConnectionPoleModel import ConnectionPoleModel
from api.electrical.repositories.ConnectionPoleRepo import ConnectionPoleRepo
from api.electrical.schemas.ConnectionPoleSchema import (
    ConnectionPoleUpdate,
    CreateConnectionPole
)

#
class ConnectionPoleService:
    pole: ConnectionPoleRepo

    def __init__(
        self,
        pole: ConnectionPoleRepo = Depends(),
    ) -> None:
        self.pole = pole

    # get all connection poles function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ConnectionPoleModel]:
        return self.pole.list(skip=skip, limit=limit)

    # get connection pole by id function
    async def get(self, id: int) -> ConnectionPoleModel:
        return self.pole.get(id=id)

    # get connection pole by number function
    async def getbynumber(self, number: int) -> ConnectionPoleModel:
        return self.pole.getbynumber(number=number)

    # get connection pole by name function
    async def getbyname(self, name: str) -> ConnectionPoleModel:
        return self.pole.getbyname(name=name)

    # create connection pole function
    async def create(self, data: List[ConnectionPoleUpdate]) -> List[CreateConnectionPole]:
        #step = 0
        area_code = None
        polelist = []
        for item in data:
            if (area_code is not None) and  (area_code != item.infos.area_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of connection poles for one area at a time"
                )
                
            result = generate_code(
                init_codebase=pole_basecode(item.infos.area_code),
                maxcode=self.pole.maxnumberbyarea(item.infos.area_code),
                step=item.infos.number
            )
            pole_number = result["code"]

            count = self.pole.countbynumber(number=pole_number)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Connection Pole already registered with code " + str(pole_number),
                )
                
            pole = CreateConnectionPole(
                pole_number = str(pole_number),
                area_id = AreaRepo.getidbycode(self.pole, item.infos.area_code),
                transformer_id = TransformerRepo.getidbycode(self.pole, item.infos.transformer_code),
                infos = item.infos
            )
            polelist.append(pole)
            area_code = item.infos.area_code
            
        return self.pole.create(data=polelist)

    # update connection pole function
    async def update(self, number: int, data: ConnectionPoleModel) -> ConnectionPoleModel:
        pole = self.pole.getbynumber(number=number)
        if pole is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection Pole not found",
            )

        poledict = data.dict(exclude_unset=True)
        for key, val in poledict.items():
            setattr(pole, key, val)
        return self.pole.update(pole)

    # delete connection pole function
    async def delete(self, pole: ConnectionPoleModel) -> None:
        pole = self.pole.get(id=id)
        if pole is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection Pole not found",
            )

        self.pole.update(pole)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Connection Pole deleted",
        )
from typing import List
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.tools.Helper import build_log, pole_basecode, generate_code
from api.electrical.repositories.TransformerRepo import TransformerRepo
from api.electrical.models.ConnectionPoleModel import ConnectionPoleModel
from api.electrical.repositories.ConnectionPoleRepo import ConnectionPoleRepo
from api.electrical.schemas.ConnectionPoleSchema import (
    ConnectionPoleUpdate,
    CreateConnectionPole
)

class ConnectionPoleService:
    log: LogRepo
    pole: ConnectionPoleRepo

    def __init__(
        self,
        log: LogRepo = Depends(),
        pole: ConnectionPoleRepo = Depends()
    ) -> None:
        self.log = log
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
        step = 0
        area_code = None
        polelist = []
        for item in data:
            if (area_code is not None) and  (area_code != item.infos.area_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of connection poles for one area at a time"
                )
            step += 1
            result = generate_code(
                init_codebase=pole_basecode(item.infos.transformer_code),
                maxcode=int(self.pole.maxnumberbyarea(item.infos.area_code)),
                step=step
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
 # async def create(self, data: List[ConnectionPoleUpdate]) -> List[CreateConnectionPole]:
 #        #step = 0
 #        area_code = None
 #        polelist = []
 #        for item in data:
 #            if (area_code is not None) and  (area_code != item.infos.area_code):
 #                raise HTTPException(
 #                    status_code=status.HTTP_400_BAD_REQUEST,
 #                    detail="You should only have the list of connection poles for one area at a time"
 #                )
 #
 #            result = generate_code(
 #                init_codebase=pole_basecode(item.infos.area_code),
 #                maxcode=self.pole.maxnumberbyarea(item.infos.area_code),
 #                step=item.infos.number
 #            )
 #            pole_number = result["code"]
 #
 #            count = self.pole.countbynumber(number=pole_number)
 #            if count > 0:
 #                raise HTTPException(
 #                    status_code=status.HTTP_400_BAD_REQUEST,
 #                    detail="Connection Pole already registered with code " + str(pole_number),
 #                )
 #
 #            pole = CreateConnectionPole(
 #                pole_number = str(pole_number),
 #                area_id = AreaRepo.getidbycode(self.pole, item.infos.area_code),
 #                transformer_id = TransformerRepo.getidbycode(self.pole, item.infos.transformer_code),
 #                infos = item.infos
 #            )
 #            polelist.append(pole)
 #            area_code = item.infos.area_code
 #
 #        return self.pole.create(data=polelist)

    # update connection pole function
    async def update(self, number: int, data: ConnectionPoleModel) -> ConnectionPoleModel:
        old_data = jsonable_encoder(self.pole.getbynumber(number=number))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Electric Meter not found",
            )
        
        # if (hasattr(data.infos, "area_code") and data.infos.area_code is not None):
        #     data.area_id = AreaRepo.getidbycode(self.pole, data.infos.area_code)
        #
        # if (hasattr(data.infos, "transformer_code") and data.infos.transformer_code is not None):
        #     data.transformer_id = TransformerRepo.getidbycode(self.pole, data.infos.transformer_code)
            
        current_data = jsonable_encoder(self.pole.update(number=number, data=data.dict()))
        logs = [await build_log(f"/connectionpoles/{number}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # activate or desactivate connection pole function
    async def activate_desactivate(self, number: int, flag: bool) -> None:
        old_data = jsonable_encoder(self.pole.getbynumber(number=number))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection Pole not found",
            )
        message = "Connection Pole desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Connection Pole activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.pole.update(number=number, data=data))
        logs = [build_log(f"/connectionpoles/{number}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)
    
    # delete connection pole function
    async def delete(self, number: int) -> None:
        data = self.pole.getbynumber(number=number)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection Pole not found",
            )

        self.pole.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Connection Pole deleted",
        )
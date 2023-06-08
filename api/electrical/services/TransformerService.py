from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.repositories.CityRepo import CityRepo
from api.electrical.models.TransformerModel import TransformerModel
from api.electrical.repositories.TransformerRepo import TransformerRepo
from api.electrical.repositories.FixationTypeRepo import FixationTypeRepo
from api.electrical.schemas.TransformerSchema import (
    TransformerUpdate,
    CreateTransformer
)

#
class TransformerService:
    log: LogRepo
    transformer: TransformerRepo

    def __init__(
        self,
        logo: LogRepo = Depends(),
        transformer: TransformerRepo = Depends()
    ) -> None:
        self.logo = logo
        self.transformer = transformer

    # get all transformers function
    async def list(self, skip: int = 0, limit: int = 100) -> List[TransformerModel]:
        return self.transformer.list(skip=skip, limit=limit)

    # get transformer by id function
    async def get(self, id: int) -> TransformerModel:
        return self.transformer.get(id=id)

    # get transformer by code function
    async def getbycode(self, code: int) -> TransformerModel:
        return self.transformer.getbycode(code=code)

    # get transformer by name function
    async def getbyname(self, name: str) -> TransformerModel:
        return self.transformer.getbyname(name=name)

    # create transformer function
    async def create(self, data: List[CreateTransformer]) -> List[CreateTransformer]:
        step = 0
        transformerlist = []
        for item in data:
            multiple = 100
            input_code = item.infos.city_code
            count = self.transformer.checktransformername(place_code = input_code, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Transformer already registered with name {item.infos.name} in the city whose code is {item.infos.city_code}",
                )
            
            #area_id = None
            if (hasattr(item.infos, "area_code") and item.infos.area_code is not None):
                multiple = 10
                area_id = AreaRepo.getidbycode(self.transformer, item.infos.area_code)
                input_code = item.infos.area_code
                count = self.transformer.checktransformername(place_code = input_code, name=item.infos.name)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Transformer already registered with name {item.infos.name} in the area whose code is {item.infos.area_code}",
                    )
            
            if (hasattr(item.infos, "tranformer_serie_number") and item.infos.tranformer_serie_number is not None):
                transformer_code = item.infos.tranformer_serie_number
                count = self.transformer.countbynumber(number=item.transformer_code)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Transformer already registered with number {item.transformer_code}",
                    )
            else:
                step += 1
                result = Helper.generate_code(
                    init_codebase=Helper.transformer_basecode(input_code, multiple),
                    maxcode=self.transformer.maxcodebycity(item.infos.city_code),
                    step=step
                )
                step = result["step"]
                transformer_code = result["code"]
                count = self.transformer.countbycode(code=transformer_code)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Transformer already registered with code {transformer_code}",
                    )

                transformer = CreateTransformer(
                    transformer_code = transformer_code,
                    area_id = AreaRepo.getidbycode(self.transformer, item.infos.area_code),
                    fixation_type_id = CityRepo.getidbycode(self.transformer, item.infos.city_code),
                    infos = item.infos,
                    energy_supply_lines = item.energy_supply_lines
                )
                transformerlist.append(transformer)

        return self.transformer.create(data=transformerlist)

    # update transformer function
    async def update(self, code: int, data: TransformerUpdate) -> TransformerModel:
        old_data = jsonable_encoder(self.supply.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transformer not found",
            )

        if (hasattr(data.infos, "area_code") and data.infos.area_code is not None):
            data.area_id = AreaRepo.getidbycode(self.transformer, data.infos.area_code)
            
        if (hasattr(data.infos, "fixation_type") and data.infos.fixation_type is not None):
            data.fixation_type_id = FixationTypeRepo.getbyname(self.transformer, data.infos.fixation_type)
    
        current_data = jsonable_encoder(self.transformer.update(code=code, data=data.dict()))
        logs = [Helper.build_log(f"/transformers/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
            
        await self.log.create(logs)
        return current_data
    
    # activate or desactivate region function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        old_data = jsonable_encoder(self.transformer.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transformer not found",
            )
        message = "Transformer desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Transformer activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.transformer.update(code=code, data=data))
        logs = [Helper.build_log(f"/transformers/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)
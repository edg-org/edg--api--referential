from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.repositories.CityRepo import CityRepo
from api.tools.Helper import transformer_basecode, generate_code
from api.electrical.models.TransformerModel import TransformerModel
from api.electrical.repositories.TransformerRepo import TransformerRepo
from api.electrical.repositories.EnergySupplyLineRepo import EnergySupplyLineRepo
from api.electrical.schemas.TransformerSchema import (
    TransformerUpdate,
    CreateTransformer,
)


#
class TransformerService:
    transformer: TransformerRepo

    def __init__(
        self, transformer: TransformerRepo = Depends()
    ) -> None:
        self.transformer = transformer

    # get all transformers function
    async def list(self, skip: int = 0, limit: int = 100) -> List[TransformerModel]:
        return self.transformer.list(skip=skip, limit=limit)

    # get transformer by id function
    async def get(self, id: int) -> TransformerModel:
        return self.transformer.get(id=id)

    # get transformer by number function
    async def getbynumber(self, number: str) -> TransformerModel:
        return self.transformer.getbynumber(number=number)

    # get transformer by name function
    async def getbyname(self, name: str) -> TransformerModel:
        return self.transformer.getbyname(name=name)

    # create transformer function
    async def create(self, data: List[CreateTransformer]) -> List[CreateTransformer]:
        step = 0
        place_code = 0
        transformerlist = []
        for item in data:
            input_code = item.infos.city_code
            count = self.transformer.checktransformername(place_code = input_code, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transformer already registered with name " + item.infos.name + " in the city whose code is " + str(item.infos.city_code),
                )
            
            area_id = None
            if (hasattr(item.infos, "area_code") and item.infos.area_code is not None):
                area_id = AreaRepo.getidbycode(self.transformer, item.infos.area_code)
                input_code = item.infos.area_code
                count = self.transformer.checktransformername(place_code = input_code, name=item.infos.name)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Transformer already registered with name " + item.infos.name + " in the area whose code is " + str(item.infos.area_code),
                    )
            
            if (hasattr(item.infos, "tranformer_serie_number") and item.infos.tranformer_serie_number is not None):
                transformer_code = item.infos.tranformer_serie_number
                count = self.transformer.countbynumber(number=item.transformer_code)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Transformer already registered with number "+ str(item.transformer_code),
                    )
            else:
                step += 1
                transformer_code = generate_code(
                    init_codebase=transformer_basecode(input_code),
                    maxcode=self.transformer.maxcodebycity(item.infos.city_code),
                    input_code=input_code,
                    code=place_code,
                    current_step=step,
                    init_step=1
                )
                count = self.transformer.countbycode(code=transformer_code)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Transformer already registered with code " + str(transformer_code),
                    )
                
                area_id = None
                if (hasattr(item.infos, "area_code") and item.infos.area_code is not None):
                    area_id = AreaRepo.getidbycode(self.supply, item.infos.area_code)

                transformer = CreateTransformer(
                    transformer_code = transformer_code,
                    city_id = CityRepo.getidbycode(self.transformer, item.infos.city_code),
                    area_id = area_id,
                    supply_line_id = EnergySupplyLineRepo.getbycode(self.transformer, item.infos.supply_line_code).id,
                    infos = item.infos
                )
                transformerlist.append(transformer)
                place_code = input_code

        return self.transformer.create(data=transformerlist)

    # update transformer function
    async def update(self, code: str, data: TransformerUpdate) -> TransformerModel:
        count = self.transformer.countbycode(code=code)
        if count  == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transformer not found",
            )

        olddata = self.supply.getbycode(code=code)
        area_id = olddata.area_id
        if (hasattr(data.infos, "area_code") and data.infos.area_code is not None):
            area_id = AreaRepo.getidbycode(self.supply, data.infos.area_code)

        transformer = CreateTransformer(
            transformer_code = transformer_code,
            city_id = CityRepo.getidbycode(self.transformer, data.infos.city_code),
            area_id = area_id,
            supply_line_id = EnergySupplyLineRepo.getbycode(self.transformer, data.infos.supply_line_code).id,
            infos = data.infos
        )

        transformerdict = transformer.dict(exclude_unset=True)
        for key, val in transformerdict.items():
            setattr(transformer, key, val)
        return self.transformer.update(transformer)

    # delete transformer function
    async def delete(self, transformer: TransformerModel) -> None:
        transformer = self.transformer.get(id=id)
        if transformer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transformer not found",
            )

        self.transformer.update(transformer)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Transformer deleted",
        )

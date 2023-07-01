from typing import List
from api.configs.Environment import get_env_var
from fastapi import Depends, HTTPException, status, Cookie
from api.salesfinancial.models.HousingTypeModel import HousingTypeModel
from api.salesfinancial.repositories.HousingTypeRepo import HousingTypeRepo
from api.salesfinancial.schemas.HousingTypeSchema import CreateHousingType, HousingTypeUpdate
from api.tools.Helper import build_log
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo

class HousingTypeService:
    housingtype: HousingTypeRepo
    log: LogRepo
    # username: str = Cookie(None)

    def __init__(
        self, housingtype: HousingTypeRepo = Depends(), log: LogRepo = Depends(),
    ) -> None:
        self.housingtype = housingtype
        self.log = log

    # get all housing types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[HousingTypeModel]:
        return self.housingtype.list(
            skip=skip, limit=limit
        )

    # get housing type by id function
    async def get(self, id: int) -> HousingTypeModel:
        return self.housingtype.get(id=id)

    # get housing type by code function
    async def getbycode(self, code: str) -> HousingTypeModel:
        return self.housingtype.getbycode(code=code)

    # get housing type by name function
    async def getbyname(self, name: str) -> HousingTypeModel:
        return self.housingtype.getbyname(name=name)

    # create housing type function
    async def create(self, data: List[CreateHousingType]) -> List[CreateHousingType]:
        for item in data:
            housingtype = self.housingtype.getbycode(code=item.code)
            if housingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Housing Type already registered with code "
                    + str(item.code),
                )

            housingtype = self.housingtype.getbyname(name=item.name)
            if housingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Housing Type already registered with name "
                    + item.name,
                )

        return self.housingtype.create(data=data)

    async def verif_duplicate(self, housingtype: CreateHousingType):
        # id = housingtype.id if hasattr(housingtype, 'id') else 0
        name = housingtype.name if hasattr(housingtype, 'name') else ""
        req = "HousingTypeModel.id != " + str(id)
        # name = housingtype.infos.name if hasattr(housingtype.infos, 'name') else ""

        housingtype = self.housingtype.verif_duplicate(name, req)

        return self.housingtype.verif_duplicate(name=name)
        # return self.housingtype.verif_duplicate(name= name, req=req)

        # try:
        #     stmt = (
        #         select(RefNaturalRegions)
        #         .filter(RefNaturalRegions.infos['name'].as_string().ilike(name))
        #         .filter(eval(req))
        #     )
        #
        #     ref_natural_region = self.db.scalars(stmt).all()
        #
        # except Exception as e:
        #     raise HTTPException(status_code=400, detail={})
        #
        # return ref_natural_region

    async def update(self, code: int, data: HousingTypeUpdate, username: str = Cookie(None)) -> HousingTypeModel:
        old_data = jsonable_encoder(self.housingtype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Housing Type not found",
            )

        verif = self.housingtype.verif_duplicate(data.name, "HousingTypeModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.name})

        current_data = jsonable_encoder(self.housingtype.update(code=code, data=data.dict()))
        print("+++++++++++++++++++++++++++++ username token -----------------------------------------, ", username)
        logs = [await build_log(f"/housingtype/{code}", "PUT", "username", old_data, current_data)]
        # logs = [await build_log(f"/housingtype/{code}", "PUT", "diatas2@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete housing type %function
    async def delete(self, code: int) -> None:
        housingtype = self.housingtype.getbycode(code=code)
        if housingtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Housing Type not found",
            )

        self.housingtype.update(housingtype)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Housing Type deleted",
        )

from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.models.CityModel import CityModel
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.repositories.CityTypeRepo import CityTypeRepo
from api.ageographical.repositories.CityLevelRepo import CityLevelRepo
from api.ageographical.repositories.PrefectureRepo import PrefectureRepo
from api.tools.Helper import city_basecode, generate_zipcode, generate_code
from api.ageographical.schemas.CitySchema import (
    CityInput,
    CityUpdate,
    CreateCity,
    CitySearchParams
)

#
class CityService:
    city: CityRepo

    def __init__(self, city: CityRepo = Depends()) -> None:
        self.city = city

    # get all citys function
    async def list(self, skip: int = 0, limit: int = 100) -> List[CityModel]:
        return self.city.list(skip=skip, limit=limit)

    # get city by id function
    async def get(self, id: int) -> CityModel:
        return self.city.get(id=id)

    # get city by code function
    async def getbycode(self, code: str) -> CityModel:
        return self.city.getbycode(code=code)

    # get city by name function
    async def getbyname(self, name: str) -> CityModel:
        return self.city.getbyname(name=name)

    # get city by name function
    async def getbyzipcode(self, zip_code: str) -> CityModel:
        return self.city.getbyzipcode(zip_code=zip_code)

    # get city by code function
    async def search(self, query_params: CitySearchParams) -> CityModel:
        return self.city.search(query_params=query_params)

    # create city function
    async def create(self, data: List[CityInput]) -> List[CreateCity]:
        step = 0
        zipcode_step = 0
        citylist = []
        city_level = None
        prefecture_code = None
        
        for item in data:
            
            count = self.city.checkcityname(prefecture_code = item.infos.prefecture_code, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="City already registered with name " + item.infos.name
                    + " inside the prefecture with code "+ str(item.infos.prefecture_code),
                )
            
            if (prefecture_code is not None) and  (prefecture_code != item.infos.prefecture_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of cities for one prefecture at a time"
                )
            
            if (city_level is not None) and  (city_level != item.infos.city_level):
                step = 0

            step += 1
            prefecture_code = item.infos.prefecture_code
            city_level_id = CityLevelRepo.getbyname(self.city, item.infos.city_level).id
            #suffix = (prefecture_code*10)+city_level_id
            maxzipcode = self.city.maxzipcodebypref(prefecture_code)
            result = generate_code(
                init_codebase=city_basecode(prefecture_code),
                maxcode=self.city.maxcodebypref(prefecture_code),
                step=step
            )
            step = result["step"]
            city_code = result["code"]

            if maxzipcode > 0 :
                zipcode_step += 1
                zipcode_base = maxzipcode
            else:
                #suffix = prefecture_code*100
                zipcode_base = ((prefecture_code % 10000) // 100) * 1000

                if (str(item.infos.city_level).lower() == "préfecture"):
                    zipcode_step = 0
                else:
                    if (hasattr(item, "zipcode") is False) or (hasattr(item, "zipcode") and item.zipcode is None):
                        if zipcode_step == 0:
                            zipcode_step = 110
                        else:
                            zipcode_step += 10
                            if (zipcode_step) % 100 == 0:
                                zipcode_step += 10

            count = self.city.countbycode(code=city_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="City already registered with code " + str(city_code),
                )
            
            zipcode = generate_zipcode(zipcode_base, zipcode_step)
            count = self.city.countbyzipcode(zipcode=zipcode)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="City already registered with zip code " + str(item.zipcode),
                )
            
            city = CreateCity(
                code = city_code,
                city_type_id = CityTypeRepo.getbyname(self.city, item.infos.city_type).id,
                city_level_id = city_level_id,
                prefecture_id = PrefectureRepo.getbycode(self.city, prefecture_code).id,
                zipcode = zipcode,
                infos = item.infos
            )
            citylist.append(city)
            city_level = item.infos.city_level
            prefecture_code = item.infos.prefecture_code
            
        return self.city.create(data=citylist)

    # update city function
    async def update(self, code: int, data: CityUpdate) -> CityModel:
        count = self.city.countbycode(code=code)
        if count ==  0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )
        
        olddata = self.city.getbycode(code=code)
        city = CreateCity(
            code = code,
            city_type_id = CityTypeRepo.getbyname(self.city, data.infos.city_type).id,
            city_level_id = CityLevelRepo.getbyname(self.city, data.infos.city_level).id,
            prefecture_id = PrefectureRepo.getbycode(self.city, data.infos.prefecture_code).id,
            zipcode = olddata.zipcode,
            infos = data.infos
        )
        citydict = data.city(exclude_unset=True)
        for key, val in citydict.items():
            setattr(city, key, val)
        return self.city.update(city)

    # delete city function
    async def delete(self, city: CityModel) -> None:
        count = self.city.countbycode(code=code)
        if count > 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

        del city["is_deleted"]
        city["is_deleted"] = 1

        self.city.update(city)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="City deleted",
        )

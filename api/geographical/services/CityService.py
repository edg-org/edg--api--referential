from typing import List
from fastapi import Depends, HTTPException, status
from api.geographical.models.CityModel import CityModel
from api.geographical.repositories.CityRepo import CityRepo
from api.tools.Helper import city_basecode, generate_zipcode
from api.geographical.repositories.CityTypeRepo import CityTypeRepo
from api.geographical.schemas.CitySchema import CityBase, CreateCity
from api.geographical.repositories.CityLevelRepo import CityLevelRepo
from api.geographical.repositories.PrefectureRepo import PrefectureRepo

#
class CityService:
    city: CityRepo

    def __init__(
        self, city: CityRepo = Depends()
    ) -> None:
        self.city = city

    # get all citys function
    async def list(self, skip: int = 0, limit: int = 100) -> List[CityModel]:
        return self.city.list(skip=skip, limit=limit)

    # get city by id function
    async def get(self, id: int) -> CityModel:
        return self.city.get(id=id)
    
    # get city by code function
    async def getbycode(self, code: str) -> CityBase:
        return self.city.getbycode(code=code)
    
    # get city by name function
    async def getbyname(self, name: str) -> CityBase:
        return self.city.getbyname(name=name)
    
     # get city by name function
    async def getbyzipcode(self, zip_code: str) -> CityBase:
        return self.city.getbyzipcode(zip_code=zip_code)

    # create city function
    async def create(self, data: List[CreateCity]) -> List[CreateCity]:
        step = 0
        zipcode_step = 0
        prefecture_code = 0
        for item in data:
            maxcode = self.city.maxcode_byzone(item.infos.prefecture_code)
            maxzipcode = self.city.maxzipcode_byzone(item.infos.prefecture_code)
            
            if maxcode is None:
                maxcode = 0
            
            item.type_id = CityTypeRepo.getbyname(self.city, item.infos.type).id
            item.level_id = CityLevelRepo.getbyname(self.city, item.infos.level).id
            item.prefecture_id = PrefectureRepo.getidbycode(self.city, item.infos.prefecture_code)
            
            if maxcode > 0:
                step +=1
                basecode = maxcode
            else:
                basecode = city_basecode(item.infos.prefecture_code)
                step +=1
                if prefecture_code != item.infos.prefecture_code:
                    step = 0
            
            city_code = basecode+step

            if maxzipcode is not None:
                zipcode_step +=1
                zipcode_base=maxzipcode
            else:
                zipcode_base=((city_code%10000)//100)*1000

                if str(item.infos.level).lower() == "préfecture":
                    zipcode_step = 0
                else:
                    if (hasattr(item, 'zipcode') is False) or (hasattr(item, 'zipcode') and item.zipcode is None):
                        if zipcode_step == 0:
                            zipcode_step = 110
                        else:
                            zipcode_step += 10
                            if (zipcode_step)%100 == 0:
                                zipcode_step +=10


            item.code = city_code
            prefecture_code = item.infos.prefecture_code

            zipcode = generate_zipcode(zipcode_base, zipcode_step)

            item.zipcode = zipcode
            
            city = self.city.getbycode(code=city_code)
            if city:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City already registered with code "+ str(item.code))
            
            city = self.city.getbyname(name=item.infos.name)
            if city:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City already registered with name "+ item.infos.name)
            
            city = self.city.getbyzipcode(zipcode=item.zipcode)
            if city:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City already registered with zip code "+ str(item.zipcode))

        return self.city.create(data=data)

    # update city function
    async def update(self, id: int, data: CityBase) -> CityModel:
        city = self.city.get(id=id)
        if city is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
        
        citydict = data.dict(exclude_unset=True)
        for key, val in citydict.items():
            setattr(city, key, val)
        return self.city.update(city)

    # delete city function
    async def delete(self, city: CityModel) -> None:
        city = self.city.get(id=id)
        if city is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
        
        del city['is_deleted']
        city["is_deleted"] = 1
        
        self.city.update(city)
        return HTTPException(status_code=status.HTTP_200_OK, detail="City deleted")
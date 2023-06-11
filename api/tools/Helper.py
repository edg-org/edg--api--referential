from typing import Any
from httpx import AsyncClient
from fastapi import HTTPException
from fastapi.openapi.models import Response
from api.configs.Environment import get_env_var
from api.logs.schemas.LogSchema import CreateLog

env = get_env_var()

class Helper:
    
    # Function to generate geographical natural zone code
    @classmethod
    def generate_zone_code(cls, code: int):
        return code + 10

    # Function to generate administrative region base code
    @classmethod
    def region_basecode(cls, code: int) -> int:
        return code * 10

    # Function to generate prefecture base code
    @classmethod
    def prefecture_basecode(cls, code: int) -> int:
        return code * 100

    # Function to generate city base code
    @classmethod
    def city_basecode(cls, code: int):
        return code * 100

    # Function to generate area base code
    @classmethod
    def area_basecode(cls, code: int) -> int:
        return code * 100

    # Function to generate agency base code
    @classmethod
    def agency_basecode(cls, code: int) -> int:
        return code * 100

    # Function to generate street code
    @classmethod
    def street_basecode(cls, code: int) -> int:
        return code * 100

    # Function to generate address code
    @classmethod
    def address_basecode(cls, code: int) -> int:
        return code * 100

    # Function to generate delivery point code
    @classmethod
    def deliverypoint_basecode(cls, code: int) -> int:
        return code * 10000

    # Function to generate energy supply line base code
    @classmethod
    def energy_supply_basecode(cls, code: int) -> int:
        return code * 100

    # Function to generate transformer base code
    @classmethod
    def transformer_basecode(cls, code: int, multiple: int) -> int:
        return code * multiple

    # Function to generate connection point base code
    @classmethod
    def pole_basecode(code: int) -> int:
        return code * 1000

    # Function to generate zipcode
    @classmethod
    def generate_zipcode(zipcode_base: int, step: int) -> str:
        return str(zipcode_base + step).zfill(5)

    # function to generate code
    @classmethod
    def generate_code(
        init_codebase: int, 
        maxcode: int, 
        step: int
    ) -> int:
        if maxcode > 0:
            basecode = maxcode
        else:
            basecode = init_codebase

        return dict(step=step, code=(basecode + step))

    # add logs function
    @classmethod
    async def get_request(cls, url: str, token: str) -> Response:
        header = {"Authorization": token}
        client = AsyncClient()
        response = await client.get(url, headers=header)
        status_code=response.status_code 
        
        if status_code != 200:
            if status_code == 401:
                detail=f"{response.text} : Please you have to authenticate, login please"
            elif status_code == 403:
                detail=f"{response.text} : The access to this resource is forbidden"
            else:
                detail=response.text                
            
            raise HTTPException(
                    status_code=status_code,
                    detail=detail
                )
        return response.text            
    
    #
    @classmethod
    async def build_log(
        cls,
        endpoint_name: str,
        verb: str,
        user_email: str,
        previous_metadata: Any,
        current_metadata: Any
    ) -> CreateLog:
        root_endpoint = env.api_routers_prefix + env.api_version
        return CreateLog(
            infos=dict(
                microservice_name="Referential",
                endpoint=root_endpoint+endpoint_name,
                verb=verb,
                user_email=user_email,
                previous_metadata=previous_metadata,
                current_metadata=current_metadata
            )
        )
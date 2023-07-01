from fastapi.openapi.models import Response
from fastapi import HTTPException, status
import  requests


class RequestMaster:
    # @classmethod
    @staticmethod
    async def generic_request_query(url: str, token: str) -> Response:
        header = {
            "Authorization": token
        }
        response = requests.get(url, headers=header)
        
        # logging.warning("response status code ", response.status_code)
        if response.status_code == 403:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The access to this resource is forbidden",
            )
        if response.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please you have to authenticate, login please"
            )
        return response.text



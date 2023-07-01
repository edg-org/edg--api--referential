import logging
from fastapi import Request, HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.configs.Environment import get_env_var
import json
from api.tools import RequestMaster
from fastapi.responses import JSONResponse
import requests

env = get_env_var()

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, response: Response):
        authorization = request.headers.get("Authorization")
        logging.error(f" token %s ", authorization)
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")

            # response = await RequestMaster.generic_request_query("http://localhost:8085/v1/token/introspect", authorization)

            resp = requests.get(f"{env.auth_domaine_name}/v1/token/introspect", headers={"Authorization": authorization})

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

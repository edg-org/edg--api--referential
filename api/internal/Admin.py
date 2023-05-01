from typing import List, Optional
import requests
from fastapi.encoders import jsonable_encoder

from enum import Enum

class MicroService(Enum):
    REFGEOGRAPHIQUE = "d708875ae3bb11ed9a85ad976c280eaf"
    REFELECTRIQUE = "e1c67846e3bb11ed9a85ad976c280eaf"
    REFCOMMERCIALE = "e6273f6ae3bb11ed9a85ad976c280eaf"

    USER = {}
    PREVDATA = {}
    DATA = {}
    STATUS = "201"

def add_log(micro_service_uid: str, endpoint : str = "/", verb : str = "GET", user: Optional[dict] = {}, prev_data: Optional[dict] = {}, data: Optional[dict] = {}, status_code : str = "001"):    
    json_data = {
        "micro_service_uid": micro_service_uid,
        "infos": {
            "endpoint": endpoint,
            "verb": verb,
            "user": jsonable_encoder(user),
            "prev_data": jsonable_encoder(prev_data),
            "data": jsonable_encoder(data),
            "status_code": status_code
        }
    }   
    r = requests.post('http://127.0.0.1:8000/v1/logs/', json = json_data)

    return r.status_code # 201




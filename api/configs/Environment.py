from os import getenv
from functools import lru_cache
from pydantic import BaseSettings

@lru_cache
def get_env_filename():
    runtime_env = getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"

class __EnvironmentSettings(BaseSettings):
    app_name: str
    app_desc: str
    api_version: str
    db_dialect: str
    db_hostname: str
    db_username: str
    db_password:str
    db_name: str
    db_port: int
    api_routers_prefix: str
    debug_mode: bool

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_env_var():
    return __EnvironmentSettings()
from os import getenv
from dotenv import load_dotenv
from functools import lru_cache
from pydantic import BaseSettings
from pydantic.main import ModelMetaclass

load_dotenv()

class __EnvironmentSettings(BaseSettings):
    app_name: str = getenv("APP_NAME")
    app_desc: str = getenv("APP_DESC")
    api_version: str = getenv("API_VERSION")
    database_dialect: str = getenv("DATABASE_DIALECT")
    database_hostname: str = getenv("DATABASE_HOSTNAME")
    database_username: str = getenv("DATABASE_USERNAME")
    database_password: str = getenv("DATABASE_PASSWORD")
    database_name: str = getenv("DATABASE_NAME")
    database_port: int = int(getenv("DATABASE_PORT"))
    api_routers_prefix: str = getenv("API_ROUTERS_PREFIX")
    debug_mode: bool = bool(getenv("DEBUG_MODE"))
    domaine_name: str = getenv("DOMAINE_NAME")

    class Config:
        runtime_env = getenv("ENV")
        env_file = (f".env.{runtime_env}" if runtime_env else ".env")
        env_file_encoding = "utf-8"

class HideFields(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        fields_hided = getattr(namespaces.get("Config", {}), "fields_hided", {})
        fields = namespaces.get('__fields__', {})
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            fields.update(base.__fields__)
            annotations.update(base.__annotations__)
        merged_keys = fields.keys() & annotations.keys()
        [merged_keys.add(field) for field in fields]
        new_fields = {}
        new_annotations = {}
        for field in merged_keys:
            if not field.startswith('__') and field not in fields_hided:
                new_annotations[field] = annotations.get(field, fields[field].type_)
                new_fields[field] = fields[field]
        namespaces['__annotations__'] = new_annotations
        namespaces['__fields__'] = new_fields
        return super().__new__(self, name, bases, namespaces, **kwargs)

@lru_cache
def get_env_var():
    return __EnvironmentSettings()

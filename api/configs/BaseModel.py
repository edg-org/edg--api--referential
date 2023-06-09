from typing import Set
from functools import lru_cache
from pydantic.schema import datetime
from pydantic import BaseModel, validator
from api.configs.Database import Engine, EntityMeta

#
class BaseSchema(BaseModel):
    class Config:
        fields_to_hide: Set[str] = set()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        fields_to_hide = getattr(cls.Config, "fields_to_hide", set())
        fields = cls.__fields__
        new_fields = {}
        for field_name, field in fields.items():
            if field_name not in fields_to_hide:
                new_fields[field_name] = field
        cls.__fields__ = new_fields
        super().__init_subclass__(**kwargs)
    
# create database function
@lru_cache()
def init():
    EntityMeta.metadata.create_all(bind=Engine)
from functools import lru_cache
from api.configs.Database import Engine, EntityMeta

# create database function
@lru_cache()
def init():
    EntityMeta.metadata.create_all(bind=Engine)
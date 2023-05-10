from functools import lru_cache
from sqlalchemy import create_engine
from api.configs.Environment import get_env_var
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Engine = create_engine(
    "{0}://{1}:{2}@{3}:{4}/{5}".format(
        get_env_var().database_dialect,
        get_env_var().database_username,
        get_env_var().database_password,
        get_env_var().database_hostname,
        get_env_var().database_port,
        get_env_var().database_name,
    ),
    echo=get_env_var().debug_mode,
    future=True,
)

EntityMeta = declarative_base()
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


# Getting database function
def get_db():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()

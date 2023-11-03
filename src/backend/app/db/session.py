from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
 
from app.core import config
import orjson

def orjson_serializer(obj):
    """
    Note that `orjson.dumps()` return byte array, while sqlalchemy expects string, thus `decode()` call.
    This function helped to solve JSON datetime conversion issue on JSONB column
    """
    return orjson.dumps(
        obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC
    ).decode()
    
engine = create_engine(
    config.settings.SQLALCHEMY_DATABASE_URI,
    json_serializer=orjson_serializer,
    json_deserializer=orjson.loads,    
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async_engine = create_async_engine(   
    config.settings.SQLALCHEMY_ASYNC_DATABASE_URI,
    json_serializer=orjson_serializer,
    json_deserializer=orjson.loads,    
    pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session

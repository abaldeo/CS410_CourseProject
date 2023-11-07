from fastapi import APIRouter
from app.api.api_v1.services.embedding.core import (
                                                    get_embedding_model, 
                                                    create_vectorstore)
from app.api.api_v1.services.embedding.utils import Timer 
from app.api.api_v1.services.embedding.token_count import num_tokens_from_string

# from langchain.storage.upstash_redis import UpstashRedisStore
# from upstash_redis import Redis
import functools
from langchain.storage.redis import RedisStore
import redis
from langchain.embeddings import CacheBackedEmbeddings

# from dotenv import load_dotenv
# import os 
from pydantic import BaseModel
from app.core.config import settings, get_settings
from loguru import logger


# load_dotenv()

router = r = APIRouter()

REDIS_URL = settings.EMBEDDING_REDIS_URL
REDIS_TOKEN = settings.EMBEDDING_REDIS_TOKEN
REDIS_HOST = settings.EMBEDDING_REDIS_HOST
REDIS_PORT = settings.EMBEDDING_REDIS_PORT 
REDIS_PASSWD = settings.EMBEDDING_REDIS_PASSWD


@functools.lru_cache()
def get_redis_instance():
    # redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN, rest_retries=5, rest_retry_interval=3, allow_telemetry=False)    
    redis_client = redis.Redis( host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWD)
    return redis_client

redis_instance = get_redis_instance()
REDIS_STORE  = RedisStore(client= redis_instance, ttl=None, namespace="embedding_service")

GPT_MODEL_NAME = settings.GPT_MODEL_NAME

EMEDDING_MODEL  = get_embedding_model(settings.EMBEDDING_MODEL_NAME)
# EMBEDDING_CACHE = UpstashRedisStore(client=redis_client, ttl=None, namespace="embedding_service")

EMBEDDER = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=EMEDDING_MODEL, 
    document_embedding_cache=REDIS_STORE, 
    namespace=GPT_MODEL_NAME
)

VECTOR_DB =  create_vectorstore(embedding_model=EMBEDDER)


@r.get("/query")
def query(query_text: str):
    # text_splitter = get_token_splitter(MODEL_NAME)
    # chunks = chunk_texts(query_text, text_splitter)
    # model = get_embedding_model()
    # model = EMEDDING_MODEL
    with Timer() as t:
        pass

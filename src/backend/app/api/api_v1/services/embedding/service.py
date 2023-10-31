from fastapi import APIRouter
from dotenv import load_dotenv
import os 
from app.api.api_v1.services.embedding.core import (get_token_splitter,
                                                    get_text_splitter,
                                                    get_embedding_model, 
                                                    create_doc_embeddings,
                                                    create_query_embeddings,
                                                    create_text_embeddings,
                                                    load_s3_file, 
                                                    chunk_docs,
                                                    chunk_texts,
                                                    create_vectorstore)
from app.api.api_v1.services.embedding.utils import Timer 
from app.api.api_v1.services.embedding.token_count import num_tokens_from_string

# from langchain.storage.upstash_redis import UpstashRedisStore
# from upstash_redis import Redis
import functools
from langchain.storage.redis import RedisStore

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
S3_BUCKET_NAME = settings.S3_BUCKET_NAME
EMEDDING_MODEL  = get_embedding_model(settings.EMBEDDING_MODEL_NAME)
# EMBEDDING_CACHE = UpstashRedisStore(client=redis_client, ttl=None, namespace="embedding_service")

EMBEDDER = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=EMEDDING_MODEL, 
    document_embedding_cache=REDIS_STORE, 
    namespace=GPT_MODEL_NAME
)

VECTOR_DB =  create_vectorstore(embedding_model=EMBEDDER)


@r.get("/computeQueryEmbedding")
def compute_query_embedding(query_text: str):
    # text_splitter = get_token_splitter(MODEL_NAME)
    # chunks = chunk_texts(query_text, text_splitter)
    # model = get_embedding_model()
    # model = EMEDDING_MODEL
    with Timer() as t:
        vectors = create_query_embeddings(query_text, EMBEDDER)
    token_count = num_tokens_from_string(query_text, GPT_MODEL_NAME)
    output = {"text": query_text, "embedding": vectors, "token_count": token_count, "time_taken": t.elapsed() }
    return output 

@r.post("/storeDocEmbedding")
def store_document_embedding(S3Path:str):
    document = load_s3_file(S3Path, S3_BUCKET_NAME)
    text_splitter = get_text_splitter()
    # text_splitter = get_token_splitter(MODEL_NAME)
    chunks = chunk_docs(document, text_splitter)
    # model = get_embedding_model()
    # model  = EMEDDING_MODEL
    token_count = sum([num_tokens_from_string(doc.page_content, GPT_MODEL_NAME) for doc in chunks])
    with Timer() as t:
        vectors = create_doc_embeddings(chunks, EMBEDDER)
    VECTOR_DB.add_documents(chunks)
    token_count = sum([num_tokens_from_string(doc.page_content, MODEL_NAME) for doc in chunks])
    output = {"document": document, 
              "chunks": chunks,
              "embedding": vectors, 
              "token_count": token_count, 
              "time_taken": t.elapsed() }
    return output     

from pydantic import BaseModel

class Item(BaseModel):
    text: str


@r.post("/storeTextEmbedding")
def store_text_embedding(request: Item):
    text = request.text
    text_splitter = get_text_splitter()
    chunks = chunk_texts(text, text_splitter)
    for chunk in chunks:
        chunk.metadata['source'] = "user_input"
    token_count = sum([num_tokens_from_string(chunk.page_content, GPT_MODEL_NAME) for chunk in chunks])        
    with Timer() as t:
        vectors = create_text_embeddings(chunks, EMBEDDER)
    token_count = sum([num_tokens_from_string(chunk, MODEL_NAME) for chunk in chunks])
    VECTOR_DB.add_texts(chunks)
    output = {"text": text, 
              "chunks": chunks,
              "embedding": vectors, 
              "token_count": token_count, 
              "time_taken": t.elapsed() }
    return output     


@r.get("/fetchDocEmbeddings/{S3Path}")
async def fetch_stored_document_embedding(S3Path: str):
    #similarity_search_with_score
    pass
    

@r.get("/fetchTextEmbeddings/{text}")
async def fetch_stored_text_embedding(text: str):
    #similarity_search_with_score_by_vector
    pass

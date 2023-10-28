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

from langchain.storage.upstash_redis import UpstashRedisStore
from langchain.storage.redis import RedisStore

from langchain.embeddings import CacheBackedEmbeddings
from upstash_redis import Redis
import redis
from pydantic import BaseModel



load_dotenv()

router = r = APIRouter()

REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
REDIS_HOST = os.getenv("UPSTASH_REDIS_HOST")
REDIS_PORT = os.getenv("UPSTASH_REDIS_PORT")
REDIS_PASSWD = os.getenv("UPSTASH_REDIS_PASSWORD")
# print(REDIS_URL)
# print(REDIS_TOKEN)
# redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN, rest_retries=5, rest_retry_interval=3, allow_telemetry=False)
redis_instance = redis.Redis(
  host=REDIS_HOST, 
  port=REDIS_PORT,
  password=REDIS_PASSWD 
)


REDIS_STORE  = RedisStore(client=redis_instance, ttl=None, namespace="embedding_service")

MODEL_NAME = os.getenv("MODEL_NAME")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "coursebuddy")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
EMEDDING_MODEL  = get_embedding_model(EMBEDDING_MODEL_NAME)
# EMBEDDING_CACHE = UpstashRedisStore(client=redis_client, ttl=None, namespace="embedding_service")

EMBEDDER = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=EMEDDING_MODEL, 
    document_embedding_cache=REDIS_STORE, 
    namespace=MODEL_NAME
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
    token_count = num_tokens_from_string(query_text, MODEL_NAME)
    output = {"text": query_text, "embedding": vectors, "token_count": token_count, "time_taken": t.elapsed() }
    return output 


class FileItem(BaseModel):
    S3Path: str
    
@r.post("/storeDocEmbedding")
def store_document_embedding(request:FileItem):
    S3Path = request.S3Path
    document = load_s3_file(S3Path, S3_BUCKET_NAME)
    text_splitter = get_text_splitter()
    # text_splitter = get_token_splitter(MODEL_NAME)
    chunks = chunk_docs(document, text_splitter)
    # model = get_embedding_model()
    # model  = EMEDDING_MODEL
    token_count = sum([num_tokens_from_string(doc.page_content, MODEL_NAME) for doc in chunks])
    with Timer() as t:
        vectors = create_doc_embeddings(chunks, EMBEDDER)
        VECTOR_DB.add_documents(chunks)
    output = {"document": document, 
              "chunks": chunks,
              "embedding": vectors, 
              "token_count": token_count, 
              "time_taken": t.elapsed() }
    return output     


class Item(BaseModel):
    text: str


@r.post("/storeTextEmbedding")
def store_text_embedding(request: Item):
    text = request.text
    text_splitter = get_text_splitter()
    chunks = chunk_texts(text, text_splitter)
    for chunk in chunks:
        chunk.metadata['source'] = "user_input"
    token_count = sum([num_tokens_from_string(chunk.page_content, MODEL_NAME) for chunk in chunks])        
    with Timer() as t:
        vectors = create_doc_embeddings(chunks, EMBEDDER)
        VECTOR_DB.add_documents(chunks)
    output = {"text": text, 
              "chunks": chunks,
              "embedding": vectors, 
              "token_count": token_count, 
              "time_taken": t.elapsed() }
    return output     


@r.post("/fetchDocEmbeddings")
async def fetch_stored_document_embedding(request: FileItem):
    #similarity_search_with_score
    S3Path = request.S3Path
    document = load_s3_file(S3Path, S3_BUCKET_NAME)
    text_splitter = get_text_splitter()
    # text_splitter = get_token_splitter(MODEL_NAME)
    chunks = chunk_docs(document, text_splitter)    
    with Timer() as t:
        vectors = create_doc_embeddings(chunks, EMBEDDER)
    results = []
    for vector in vectors:
        results.extend(VECTOR_DB.similarity_search_by_vector(vector,k=1))
    return results

@r.post("/fetchTextEmbeddings")
async def fetch_stored_text_embedding(request: Item):
    #similarity_search_with_score_by_vector
    text = request.text
    text_splitter = get_text_splitter()
    chunks = chunk_texts(text, text_splitter)
    with Timer() as t:
        vectors = create_doc_embeddings(chunks, EMBEDDER)
    results = []
    for vector in vectors:
        results.extend(VECTOR_DB.similarity_search_by_vector(vector,k=1))
    return results
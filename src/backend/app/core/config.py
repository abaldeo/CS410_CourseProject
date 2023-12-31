from functools import lru_cache
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(object):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "CourseBuddyAI")
    SQLALCHEMY_DATABASE_URI: str  = os.getenv("DATABASE_URL")
    SQLALCHEMY_ASYNC_DATABASE_URI: str  = os.getenv("DATABASE_URL_ASYNC")
    SUPERUSER_EMAIL: str  = os.getenv("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")
    SECRET_KEY: str =os.getenv("SECRET_KEY")

    ZILLIZ_CLOUD_COLLECTION_NAME: str = os.getenv("ZILLIZ_CLOUD_COLLECTION_NAME")
    ZILLIZ_CLOUD_URI: str = os.getenv("ZILLIZ_CLOUD_URI") 
    ZILLIZ_CLOUD_API_KEY: str = os.getenv("ZILLIZ_CLOUD_API_KEY")

    AWS_REGION_NAME: str = os.getenv("REGION_NAME")   #ToDo renmae in env file
    AWS_SECRET_ACCESS_KEY: str= os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    S3_BUCKET_NAME: str = os.getenv("BUCKET_NAME", "coursebuddy") #TODO rename in env file
    S3_ENDPOINT_URL: str = os.getenv("ENDPOINT_URL") #TODO Rename in env file
    
    EMBEDDING_REDIS_URL: str = os.getenv("UPSTASH_REDIS_REST_URL")
    EMBEDDING_REDIS_TOKEN: str = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    EMBEDDING_REDIS_HOST: str = os.getenv("UPSTASH_REDIS_HOST")
    EMBEDDING_REDIS_PORT: int = os.getenv("UPSTASH_REDIS_PORT")
    EMBEDDING_REDIS_PASSWD: str = os.getenv("UPSTASH_REDIS_PASSWORD")

    SUMM_REDIS_URL: str = os.getenv("UPSTASH_REDIS_SUMM_REST_URL")
    SUMM_REDIS_TOKEN: str = os.getenv("UPSTASH_REDIS_SUMM_REST_TOKEN")
    SUMM_REDIS_HOST: str = os.getenv("UPSTASH_REDIS_SUMM_HOST")
    SUMM_REDIS_PORT: int = os.getenv("UPSTASH_REDIS_SUMM_PORT")
    SUMM_REDIS_PASSWD: str = os.getenv("UPSTASH_REDIS_SUMM_PASSWORD")

    GPT_MODEL_NAME: str = os.getenv("MODEL_NAME")   #TODO rename in env file 
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE")
    OPENAI_API_VERSION: str =  os.getenv("OPENAI_API_VERSION")
    
    AZURE_OPENAI_API_KEY: str = OPENAI_API_KEY
    AZURE_OPENAI_API_ENDPOINT: str = OPENAI_API_BASE
    AZURE_OPENAI_MODEL_VERSION: str = os.getenv("AZURE_OPENAI_MODEL_VERSION")
    
    SEARCH_TYPE: str = os.getenv("RAG_SEARCH_TYPE") 
    TOP_K: int = os.getenv("RAG_TOP_K")
    FETCH_K: int = os.getenv("RAG_FETCH_K")
    ENABLE_HYBRID_SEARCH: bool = bool(int(os.getenv("RAG_ENABLE_HYBRID_SEARCH")))
    MMR_SIMILARITY: float = os.getenv("RAG_MMR_SIMILARITY")
    BM25_WEIGHT: float = os.getenv("RAG_BM25_WEIGHT")
    BM25_K1: float = os.getenv("RAG_BM25_K1")
    BM25_B: float = os.getenv("RAG_BM25_B")
    BM25_EPSILON: float = os.getenv("RAG_BM25_EPSILON")


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
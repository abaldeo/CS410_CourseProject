from fastapi import APIRouter

router = r = APIRouter()

@r.get("/computeQueryEmbedding")
async def example():
    return {"message": "Hello from Embedding Service"}


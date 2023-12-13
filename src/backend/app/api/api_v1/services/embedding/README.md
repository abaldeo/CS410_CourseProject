**Document Embedding Service**

The document embedding service is used to generate text embeddings for uploaded lecture transcripts.
It first splits the documents into smaller chunks of 500 tokens to fit the context window.
The HuggingFace BGE text embedding model maps the text chunks into dense-vectors (768 dimensions)
The BAAI/bge-base-en-v1.5  model has shown state of the art performance in the MTEB leaderboard for semantic search and is small enough to be run locally.
After the document vectors are generated, the embedding service stores and indexes in cloud-hosted Milvus vector database instance.  

Endpoints:


*Compute Query Embedding*
- Http method - GET
- url /api/v1/embedding/computeQueryEmbedding
- params - query_text: str
- Response: {
  "text": "Test query",
  "embedding": [
    0.02058139070868492,
    0.03663616254925728,
    0.008633185178041458,
    0.034844063222408295,
    0.09318087995052338,
    0.035393308848142624,
    ...,
    0.0572730116546154,
   ],
  "token_count": 2,
  "time_taken": 0.7942631244659424
}

*Store Document Embedding*
- Http method POST
- url /api/v1/embedding/storeDocEmbedding
- params { "S3Path": "string" }


*Store Text Embedding*
- Http method POST
- url /api/v1/embedding/storeTextEmbedding
- params { "text": "string" }

*Fetch Stored Document Embedding*
- Http method POST
 url /api/v1/embedding/fetchDocEmbeddings
- params { "S3Path": "string" }


*Fetch Stored Text Embedding*
- Http method POST
- url /api/v1/embedding/fetchTextEmbeddings
- params { "text": "string" }



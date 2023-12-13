## Getting Started

First install dependencies and create a virtual environment:

```bash
cd src/backend
pdm install
```

To run an individual service assuming you are located in src/backend:

```bash
pdm run python app/api_v1/services/{service_to_run}/main.py
e.g pdm run python app/api_v1/services/summarization/main.py
```

To run an the entire backend and all services assuming you are located in src/backend:

```bash
pdm run python app/main.py

```

## File Upload Service

The file upload service is a service that allows for files of many different types, pdf, ppt, and txt to be uploaded and downloaded from our s3 buckets. The files are uploaded and downloaded using aioboto3. This service allows the frontend to send files to be stored and processed as well allow for other services to access saved files.

## Summarization Service

The summarization service is a service that ingest a transcript from a coursera lecture vvideo and produces concise bullet point summarizations of the lecture. The service can either receive the transcript as a string from the frontend or from an s3 path if the transcript is already saved in the s3 bucket. From there the transcript is cleaned and split into chunks so that the OpenAI model can summarize the chunks before we finally concatenate the individual summaries into a final bullet point list.

## Embedding Service

The  Embedding Service then takes the uploaded documents and generates text embeddings using the HuggingFace (HF) BAAI/bge-base-en-v1.5 model to map the lecture texts to dense-vectors (768 dimensions). This model has shown state of the art performance in the HF leaderboards for semantic search and is free for us to use (OpenAI’s ada embedding model is not). After generating the vectors using this model, the embedding service stores them into a cloud hosted vector database which indexes them. This allows our RAG Service to quickly retrieve the relevant documents for a user's question based on the similarity measure (euclidean distance).

## RAG Q&A Service

The RAG Service is used by our Q&A chatbot interface to provide ChatGPT with the users’ questions and the relevant lecture documents in order for it to synthesize an answer that is contextually relevant and based on the course material.


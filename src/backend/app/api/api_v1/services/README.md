## Summarization Service

The summarization service is a service that ingest a transcript from a coursera lecture and produces concise bullet point summarizations of the lecture. The service can either receive the transcript as a string from the front end or from an s3 path if the transcript is already saved in the s3 bucket. From there the transcript is cleaned and split into chunks so tha Langchain leveraging an OpenAi model can summarize the chunks and concat the individual summaries into a final bullet point list.

## File Upload Service

The file upload service is a service that allows for files of many different types, pdf, ppt, and txt to be uploaded and downloaded from our s3 buckets. The files are uploaded and downloaded using aioboto3 to allow for asynchronous functionality. This service allows the front end to send files to be stored and processed as well allow for other services to access saved files.

## Embedding Service

The Embedding service is a service that...

## RAG Service

The RAG service is a service that...



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

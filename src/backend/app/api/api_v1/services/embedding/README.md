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
- Response [
  {
    "page_content": "this lecture is the first one about the text clustering. in this lecture we are going to talk about the text clustering. this is a very important technique for doing topic mining and analysis. in particular in this lecture were going to start with some basic questions about the clustering. and that is what is text clustering and why we are interested in text clustering. in the following lectures we are going to talk about how to do text clustering. how to evaluate the clustering results so what is text clustering well clustering actually is a very general technique for data mining as you might have learned in some other courses. the idea is to discover natural structures in the data. in another words we want to group similar objects together. in our case these objects are of course text objects. for example they can be documents terms passages sentences or websites and then ill go group similar text objects together. so lets see an example well here you dont really see text objects but i just used some shapes to denote objects that can be grouped together. now if i ask you what are some natural structures or natural groups where you if you look at it and you might agree that we can group these objects based on chips or their locations on this two dimensional space. so we got the three clusters in this case. and they may not be so much this agreement about these three clusters but it really depends on the perspective to look at the objects. maybe some of you have also seen thing in a different way so we might get different clusters. and youll see another example about this ambiguity more clearly. but the main point of here is the problem is actually not so well defined. and the problem lies in how to define similarity. and what do you mean by similar objects now this problem has to be clearly defined in order to have a well defined clustering problem. and the problem is in general that any two objects can be similar depending on how you look at them. so for example this will kept the two words like car and horse. so are the two words similar well it depends on how if we look at the physical properties of car and horse they are very different but if you look at them functionally a car and a horse can both be transportation tools. so in that sense they may be similar. so as we can see it really depends on our perspective to look at the objects",
    "metadata": {
      "source": "/workspace/CS410_CourseProject/src/backend/data/transcripts/01_10-1-text-clustering-motivation.en.txt",
      "document_id": "3d49345751a5f1b84dc2311e994bdff4",
      "week_number": "10",
      "lecture_number": "10.1",
      "lecture_title": "Text Clustering Motivation",
      "start_index": 0,
      "chunk_id": "02bceac880efddf525223e3aa4f63bc1",
      "chunk_number": 1
    },
    "type": "Document"
  }]

*Fetch Stored Text Embedding*
- Http method POST
- url /api/v1/embedding/fetchTextEmbeddings
- params { "text": "string" }
- Response [
  {
    "page_content": "this lecture is the first one about the text clustering. in this lecture we are going to talk about the text clustering. this is a very important technique for doing topic mining and analysis. in particular in this lecture were going to start with some basic questions about the clustering. and that is what is text clustering and why we are interested in text clustering. in the following lectures we are going to talk about how to do text clustering. how to evaluate the clustering results so what is text clustering well clustering actually is a very general technique for data mining as you might have learned in some other courses. the idea is to discover natural structures in the data. in another words we want to group similar objects together. in our case these objects are of course text objects. for example they can be documents terms passages sentences or websites and then ill go group similar text objects together. so lets see an example well here you dont really see text objects but i just used some shapes to denote objects that can be grouped together. now if i ask you what are some natural structures or natural groups where you if you look at it and you might agree that we can group these objects based on chips or their locations on this two dimensional space. so we got the three clusters in this case. and they may not be so much this agreement about these three clusters but it really depends on the perspective to look at the objects. maybe some of you have also seen thing in a different way so we might get different clusters. and youll see another example about this ambiguity more clearly. but the main point of here is the problem is actually not so well defined. and the problem lies in how to define similarity. and what do you mean by similar objects now this problem has to be clearly defined in order to have a well defined clustering problem. and the problem is in general that any two objects can be similar depending on how you look at them. so for example this will kept the two words like car and horse. so are the two words similar well it depends on how if we look at the physical properties of car and horse they are very different but if you look at them functionally a car and a horse can both be transportation tools. so in that sense they may be similar. so as we can see it really depends on our perspective to look at the objects",
    "metadata": {
      "source": "/workspace/CS410_CourseProject/src/backend/data/transcripts/01_10-1-text-clustering-motivation.en.txt",
      "document_id": "3d49345751a5f1b84dc2311e994bdff4",
      "week_number": "10",
      "lecture_number": "10.1",
      "lecture_title": "Text Clustering Motivation",
      "start_index": 0,
      "chunk_id": "02bceac880efddf525223e3aa4f63bc1",
      "chunk_number": 1
    },
    "type": "Document"
  }
]


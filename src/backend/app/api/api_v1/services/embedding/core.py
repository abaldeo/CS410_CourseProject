import functools
import g4f
from g4f import Provider, models
from langchain.llms.base import LLM

from langchain_g4f import G4FLLM
print(g4f.Provider.Ails.params)  # supported args

from langchain.document_loaders import (UnstructuredPDFLoader,
                                        UnstructuredPowerPointLoader,
                                        TextLoader,
                                        DirectoryLoader)
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import Zilliz


# from dotenv import load_dotenv
# import os
from app.core.config import settings, get_settings 
# load_dotenv()

ZILLIZ_CLOUD_COLLECTION_NAME = settings.ZILLIZ_CLOUD_COLLECTION_NAME
ZILLIZ_CLOUD_URI = settings.ZILLIZ_CLOUD_URI
ZILLIZ_CLOUD_API_KEY = settings.ZILLIZ_CLOUD_API_KEY

# print(ZILLIZ_CLOUD_COLLECTION_NAME)
# print(ZILLIZ_CLOUD_URI)
# print(ZILLIZ_CLOUD_API_KEY)

AWS_REGION_NAME = settings.AWS_REGION_NAME
S3_ENDPOINT_URL = settings.S3_ENDPOINT_URL
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID

@functools.lru_cache()
def create_vectorstore(embedding_model):
    vectorstore = Zilliz(
        embedding_model,
        collection_name=ZILLIZ_CLOUD_COLLECTION_NAME,
        drop_old=False,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            # "user": ZILLIZ_CLOUD_USERNAME,
            # "password": ZILLIZ_CLOUD_PASSWORD,
            "token": ZILLIZ_CLOUD_API_KEY,            
            "secure": False,
        },
        # On Zilliz Cloud
        # index_params = {
        #     # Always set this to AUTOINDEX or just omit it.
        #     "index_type": "AUTOINDEX",            
        #     # Default to IP. This is the only parameter you should think about.
        #     "metric_type": "COSINE",
        #     # No need to set `params` 
        #     # "params": {},
        # },
    )


    return vectorstore


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".pdf": (UnstructuredPDFLoader, {}),
	#".pdf": (PyMuPDFLoader, {}),
    # ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}

# Loading pdf, docx, and txt files 
def load_document(file):
    import os 
    name, ext = os.path.splitext(file)

    if ext == ".pdf":
        from langchain.document_loaders import UnstructuredPDFLoader 
        loader = UnstructuredPDFLoader(file)
    elif ext == ".ppt" or ext == ".pptx":
        from langchain.document_loaders import UnstructuredPowerPointLoader
        loader = UnstructuredPowerPointLoader(file)
    elif ext == ".txt":
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file, encoding="utf-8")
    else:
        return None

    data = loader.load()
    return data

def create_directory_loader(file_type, directory_path):
    loader_class, loader_kwargs = LOADER_MAPPING[file_type]    
    return DirectoryLoader(
        path=directory_path,
        glob=f"**/*{file_type}",
        loader_cls=loader_class,
        loader_kwargs=loader_kwargs,
        use_multithreading=True, 
        show_progress=True
    )

def get_loaders(dir):
  extensions=LOADER_MAPPING.keys()
  return [create_directory_loader(extension,dir) for extension in extensions]

    return vectorstore


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".pdf": (UnstructuredPDFLoader, {}),
	#".pdf": (PyMuPDFLoader, {}),
    # ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}

# Loading pdf, docx, and txt files 
def load_document(file):
    import os 
    name, ext = os.path.splitext(file)

    if ext == ".pdf":
        from langchain.document_loaders import UnstructuredPDFLoader 
        loader = UnstructuredPDFLoader(file)
    elif ext == ".ppt" or ext == ".pptx":
        from langchain.document_loaders import UnstructuredPowerPointLoader
        loader = UnstructuredPowerPointLoader(file)
    elif ext == ".txt":
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file, encoding="utf-8")
    else:
        return None

    data = loader.load()
    return data

def create_directory_loader(file_type, directory_path):
    loader_class, loader_kwargs = LOADER_MAPPING[file_type]    
    return DirectoryLoader(
        path=directory_path,
        glob=f"**/*{file_type}",
        loader_cls=loader_class,
        loader_kwargs=loader_kwargs,
        use_multithreading=True, 
        show_progress=True
    )

def get_loaders(dir):
  extensions=LOADER_MAPPING.keys()
  return [create_directory_loader(extension,dir) for extension in extensions]


def load_s3_file(file_name, bucket_name):
    from langchain.document_loaders import S3FileLoader
    loader = S3FileLoader(bucket_name, file_name, 
                          region_name=AWS_REGION_NAME, endpoint_url=S3_ENDPOINT_URL,
                          aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return loader.load()


def clean_text(text):

    import string, re 
    # from nltk.corpus import stopwords
    # Lowercase the text
    text = text.lower()
    text =  text.replace('[sound]','')
    text =  text.replace('[music]','')
    text =  text.replace('[inaudible]','')
    
   # Remove extra spaces
    text = re.sub(r'[ |\t]', ' ', text).strip()
    
    # remove punctuations
    text = ''.join(c for c in text if c not in string.punctuation)
    
    # # Remove stop words
    # stop_words = set(stopwords.words('english'))
    # text = ' '.join([word for word in text.split() if word not in stop_words])
    
    return text

def get_text_splitter( chunk_size=1000, chunk_overlap=100, **kwargs):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
                                                   	length_function = len, add_start_index = True, **kwargs)
    return text_splitter

def get_token_splitter(model_name, chunk_size=500, chunk_overlap=20, **kwargs): 
    from langchain.text_splitter import TokenTextSplitter 
    from app.api.api_v1.services.embedding.token_count import get_encoder_for_model
    encoder = get_encoder_for_model(model_name)
    encoding_name = encoder.name 
    token_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,encoding_name=encoding_name, **kwargs )
    return token_splitter

# Chunk data
def chunk_docs(docs,text_splitter, clean=True):
    if not isinstance(docs, list): docs = [docs]  
    if clean:  clean_documents(docs)          
    chunks = text_splitter.split_documents(docs)
    # if clean:  clean_documents(chunks)    
    return chunks

def chunk_texts(texts, text_splitter, clean=True):
    if clean: texts = clean_text(texts)        
    if not isinstance(texts, list): texts = [texts]            
    chunks = text_splitter.create_documents(texts)
    # if clean: chunks = clean_texts(texts)        
    return chunks

# def clean_texts(texts):
#     texts = [clean_text(text) for text in texts]
#     return texts

def clean_documents(documents):
    # Iterate over texts page_content category with this cleaning method.
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

@functools.lru_cache()
def get_embedding_model(model_name="BAAI/bge-base-en-v1.5" ):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    hf = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf

def create_doc_embeddings(doc_chunks, embedding_model):
    doc_text = [doc.page_content for doc in doc_chunks]
    return embedding_model.embed_documents(doc_text)
 
def create_text_embeddings(text_chunks, embedding_model):
    return [embedding_model.embed_query(chunk) for chunk in text_chunks]
 
def create_query_embeddings(query_text, embedding_model):
    return embedding_model.embed_query(query_text)

def create_qa_chain(llm, vectorstore):
    from langchain.chains import RetrievalQA
    QA_CHAIN_PROMPT=""
    qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    return qa_chain 

def create_conversation_chain(llm, vectorstore, memory):
    from langchain.chains import ConversationalRetrievalChain    
    return ConverationalRetrievalChain.from_llm(llm=llm, retriever= vectorstore.as_retriever(), memory=memory)

def create_memory():
    from langchain.memory import ConversationBufferMemory
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def main():
    file='/workspace/CS410_CourseProject/src/backend/data/transcripts/01_10-1-text-clustering-motivation.en.txt'
    doc = load_document(file)
    # print(doc)
    text_splitter = get_text_splitter()
    # text_splitter = get_token_splitter("gpt-3.5-turbo")
    # chunks = chunk_texts(doc[0].page_content, text_splitter)
    chunks = chunk_docs(doc, text_splitter)
    # [print(len(chunk.page_content)) for chunk in chunks]
    model = get_embedding_model()
    print(model.model_name)
    # from app.api.api_v1.services.embedding.utils import timer
    # with timer() as t:
    #     vectors = create_doc_embeddings(chunks, model)
 
    # print(len(vectors))
    vector_db = create_vectorstore(embedding_model=model)
    # vector_db.add_documents(chunks)
    print(vector_db.similarity_search("text clustering", top_k=2))
    # llm: LLM = G4FLLM(
    #     model=models.gpt_35_turbo,
    #     provider=Provider.ChatForAi,
    # )

    # res = llm("hello")
    # print(res)  # Hello! How can I assist you today?
    

def load_s3_file(file_name, bucket_name):
    from langchain.document_loaders import S3FileLoader
    loader = S3FileLoader(bucket_name, file_name, 
                          region_name=AWS_REGION_NAME, endpoint_url=S3_ENDPOINT_URL,
                          aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return loader.load()


def clean_text(text):

    import string, re 
    # from nltk.corpus import stopwords
    # Lowercase the text
    text = text.lower()
    text =  text.replace('[sound]','')
    text =  text.replace('[music]','')
    text =  text.replace('[inaudible]','')
    
   # Remove extra spaces
    text = re.sub(r'[ |\t]', ' ', text).strip()
    
    # remove punctuations
    text = ''.join(c for c in text if c not in string.punctuation)
    
    # # Remove stop words
    # stop_words = set(stopwords.words('english'))
    # text = ' '.join([word for word in text.split() if word not in stop_words])
    
    return text

def get_text_splitter( chunk_size=1000, chunk_overlap=100, **kwargs):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
                                                   	length_function = len, add_start_index = True, **kwargs)
    return text_splitter

def get_token_splitter(model_name, chunk_size=500, chunk_overlap=20, **kwargs): 
    from langchain.text_splitter import TokenTextSplitter 
    from app.api.api_v1.services.embedding.token_count import get_encoder_for_model
    encoder = get_encoder_for_model(model_name)
    encoding_name = encoder.name 
    token_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,encoding_name=encoding_name, **kwargs )
    return token_splitter

# Chunk data
def chunk_docs(docs,text_splitter, clean=True):
    if not isinstance(docs, list): docs = [docs]  
    if clean:  clean_documents(docs)          
    chunks = text_splitter.split_documents(docs)
    # if clean:  clean_documents(chunks)    
    return chunks

def chunk_texts(texts, text_splitter, clean=True):
    if clean: texts = clean_text(texts)        
    if not isinstance(texts, list): texts = [texts]            
    chunks = text_splitter.create_documents(texts)
    # if clean: chunks = clean_texts(texts)        
    return chunks

# def clean_texts(texts):
#     texts = [clean_text(text) for text in texts]
#     return texts

def clean_documents(documents):
    # Iterate over texts page_content category with this cleaning method.
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

@functools.lru_cache()
def get_embedding_model(model_name="BAAI/bge-base-en-v1.5" ):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    hf = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf

def create_doc_embeddings(doc_chunks, embedding_model):
    doc_text = [doc.page_content for doc in doc_chunks]
    return embedding_model.embed_documents(doc_text)
 
def create_text_embeddings(text_chunks, embedding_model):
    return [embedding_model.embed_query(chunk) for chunk in text_chunks]
 
def create_query_embeddings(query_text, embedding_model):
    return embedding_model.embed_query(query_text)

def create_qa_chain(llm, vectorstore):
    from langchain.chains import RetrievalQA
    QA_CHAIN_PROMPT=""
    qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    return qa_chain 

def create_conversation_chain(llm, vectorstore, memory):
    from langchain.chains import ConversationalRetrievalChain    
    return ConverationalRetrievalChain.from_llm(llm=llm, retriever= vectorstore.as_retriever(), memory=memory)

def create_memory():
    from langchain.memory import ConversationBufferMemory
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def main():
    file='/workspace/CS410_CourseProject/src/backend/data/transcripts/01_10-1-text-clustering-motivation.en.txt'
    doc = load_document(file)
    # print(doc)
    text_splitter = get_text_splitter()
    # text_splitter = get_token_splitter("gpt-3.5-turbo")
    # chunks = chunk_texts(doc[0].page_content, text_splitter)
    chunks = chunk_docs(doc, text_splitter)
    # [print(len(chunk.page_content)) for chunk in chunks]
    model = get_embedding_model()
    print(model.model_name)
    # from app.api.api_v1.services.embedding.utils import timer
    # with timer() as t:
    #     vectors = create_doc_embeddings(chunks, model)
 
    # print(len(vectors))
    vector_db = create_vectorstore(embedding_model=model)
    # vector_db.add_documents(chunks)
    print(vector_db.similarity_search("text clustering", top_k=2))
    # llm: LLM = G4FLLM(
    #     model=models.gpt_35_turbo,
    #     provider=Provider.ChatForAi,
    # )

    # res = llm("hello")
    # print(res)  # Hello! How can I assist you today?
    

if __name__ == "__main__":
    main() 
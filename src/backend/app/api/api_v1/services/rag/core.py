
from langchain.chains import RetrievalQA
from loguru import logger

def local_retriever(db, llm, persona="default"):
    """
    Fn: local_retriever
    Description: The function sets up the local retrieval-based question-answering system.
    Args:
        db (object): The database object
        llm (object): The LLM model object
    return:
        chain (object): The chain object
    """
    try:
        prompt, memory = get_prompt(persona=persona)
        # Create a retriever object
        local_retriever = db.as_retriever()
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=local_retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt, "memory": memory},
            return_source_documents=True,
        )
        logging.info("Loaded Local Retriever Successfully 🔍")
    except Exception as e:
        logging.info("Error {}", e)

    return chain


from langchain.chains import RetrievalQA
from langchain.retrievers import BM25Retriever, EnsembleRetriever


def hybrid_retriever(db, llm, persona="default"):
    """
    Fn: hybrid_retriever
    Description: The function sets up the hybrid retrieval-based question-answering system.
    Args:
        db (object): The database object
        llm (object): The LLM model object
    return:
        chain (object): The chain object
    """
    prompt, memory = get_prompt(persona=persona)
    # Create a retriever object
    bm_retriever = BM25Retriever.from_texts(db.get())
    local_retriver = db.as_retriever()
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm_retriever, local_retriver], weights=[0.5, 0.5]
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=ensemble_retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt, "memory": memory},
        return_source_documents=True,
    )
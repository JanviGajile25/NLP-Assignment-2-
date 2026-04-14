import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.embeddings import get_embedding_model

def create_and_save_index(chunks: list[str], save_path: str = "vectorstore") -> FAISS:
    """
    Creates a FAISS vector store from the text chunks and saves it locally.
    """
    if not chunks:
        raise ValueError("No chunks provided to create the index.")
        
    embeddings = get_embedding_model()
    # Convert string chunks into Langchain Document objects
    docs = [Document(page_content=chunk) for chunk in chunks]
    
    # Create the vector store
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Ensure directory exists
    os.makedirs(save_path, exist_ok=True)
    
    # Save locally
    vectorstore.save_local(save_path)
    return vectorstore

def load_index(load_path: str = "vectorstore") -> FAISS:
    """
    Loads an existing FAISS vector store from the local directory.
    Returns None if the directory doesn't exist.
    """
    if not os.path.exists(os.path.join(load_path, "index.faiss")):
        return None
        
    embeddings = get_embedding_model()
    vectorstore = FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

def retrieve_context(query: str, vectorstore: FAISS, top_k: int = 3) -> list[Document]:
    """
    Performs a similarity search to retrieve the top_k most relevant chunks.
    """
    if vectorstore is None:
        raise ValueError("Vectorstore is not initialized.")
        
    docs = vectorstore.similarity_search(query, k=top_k)
    return docs

from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model(model_name: str = 'all-MiniLM-L6-v2'):
    """
    Initializes and returns the HuggingFace sentence transformer embedding model.
    """
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'}, # Use CPU by default, change to 'cuda' if GPU is available
            encode_kwargs={'normalize_embeddings': False}
        )
        return embeddings
    except Exception as e:
        print(f"Error initializing embedding model: {e}")
        raise e

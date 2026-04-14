import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_text(text: str) -> str:
    """
    Cleans the raw text by removing extra whitespaces, newlines, 
    and unwanted characters to improve embedding quality.
    """
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Strip leading and trailing whitespace
    text = text.strip()
    return text

def split_text_into_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    Splits the cleaned text into manageable chunks using Langchain's text splitter.
    """
    cleaned_text = clean_text(text)
    
    if not cleaned_text:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(cleaned_text)
    return chunks

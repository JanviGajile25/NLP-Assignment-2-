from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Strictly bind to context explicitly
prompt_template = """
You are a highly analytical technical assistant. Answer the question STRICTLY using the context provided below. 
Do not use any outside knowledge or hallucinate. If the context does not contain the answer, say "I cannot find the answer in the provided documents."

Context:
{context}

Question: {question}

Answer:
"""

def get_llm(model_type="Groq (Free)", api_key=None, ollama_model="llama3"):
    """
    Initialize and return the selected LLM.
    """
    if model_type == "Groq (Free)":
        if not api_key:
            raise ValueError("Groq API key is required.")
        return ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=api_key)
    elif model_type == "Ollama":
        # Requires Ollama to be running locally
        return Ollama(model=ollama_model, temperature=0)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

def generate_answer(query: str, retrieved_docs: list, model_type="Groq (Free)", api_key=None) -> str:
    """
    Generate an answer using the selected LLM and strict RAG prompt.
    """
    if not retrieved_docs:
        return "Answer not found in provided documents."
        
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
    prompt = PromptTemplate.from_template(prompt_template)
    llm = get_llm(model_type, api_key)
    
    chain = (
        {"context": lambda x: context_text, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(query)

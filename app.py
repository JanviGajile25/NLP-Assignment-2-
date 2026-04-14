import streamlit as st
import os

from utils.loader import load_document
from utils.splitter import split_text_into_chunks
from utils.retriever import create_and_save_index, load_index, retrieve_context
from utils.generator import generate_answer

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

col1, col2 = st.columns([8, 2])
with col1:
    st.title("🤖 RAG Chatbot for Technical Documentation")
    st.markdown("Upload technical documents (PDF, DOCX, TXT) and ask questions exactly strictly based on their content.")
with col2:
    st.write("") # Spacer
    theme = st.radio("Appearance", ["Dark", "Light"], horizontal=True)

if theme == "Dark":
    bg_color = "#0B0F19"
    text_color = "#E2E8F0"
    sidebar_bg = "#111827"
    source_bg = "#1F2937"
    chat_bg = "#1F2937"
    border_col = "#374151"
else:
    bg_color = "#F8FAFC"
    text_color = "#1E293B"
    sidebar_bg = "#FFFFFF"
    source_bg = "#F1F5F9"
    chat_bg = "#FFFFFF"
    border_col = "#E2E8F0"

# Apply completely revamped premium aesthetic CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Main Backgrounds */
    .stApp {{
        background-color: {bg_color} !important;
        font-family: 'Outfit', sans-serif !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_col};
    }}
    
    /* Ensure all text assumes primary color and font */
    .stMarkdown, .stText, p, span, label, div {{
        color: {text_color} !important;
        font-family: 'Outfit', sans-serif !important;
    }}
    
    /* Gorgeous Gradient Headers */
    h1 {{
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        padding-bottom: 0.5rem;
    }}
    h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
    }}
    
    /* Premium Button Stylings */
    .stButton>button {{
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4);
    }}

    /* Elevated Chat Messages */
    .stChatMessage {{
        background-color: {chat_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    
    /* Document Reference blocks */
    .source-doc {{
        background-color: {source_bg};
        border-left: 4px solid #a855f7;
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
        font-size: 0.95em;
        line-height: 1.6;
        color: {text_color} !important;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
    }}
    
    /* Inputs */
    .stTextInput>div>div>input {{
        border-radius: 10px;
        border: 1px solid {border_col};
        background-color: {source_bg} !important;
        color: {text_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "index_loaded" not in st.session_state:
    st.session_state.index_loaded = load_index() is not None

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    llm_type = st.selectbox("Select LLM", ["Groq (Free)", "Ollama"])
    api_key = ""
    if llm_type == "Groq (Free)":
        default_key = os.environ.get("GROQ_API_KEY", "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")
        if default_key:
            api_key = default_key
            st.success("✅ Groq API Key auto-loaded securely.")
        else:
            api_key = st.text_input("Groq API Key", type="password")
            if not api_key:
                st.warning("Please enter your Groq API key.")
                st.markdown("[Get a completely free key here (no credit card required)](https://console.groq.com/keys)")
    else:
        st.info("Make sure Ollama is running locally with the active model.")
    
    st.divider()
    
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    
    if st.button("Process Documents"):
        if not uploaded_files:
            st.error("Please upload at least one file first.")
        else:
            with st.spinner("Processing documents..."):
                all_text = ""
                # Save and load files temporarily
                temp_dir = "data"
                os.makedirs(temp_dir, exist_ok=True)
                
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    try:
                        text = load_document(file_path)
                        all_text += text + "\n"
                    except Exception as e:
                        st.error(f"Error loading {uploaded_file.name}: {e}")
                
                if all_text.strip():
                    # Split into chunks
                    chunks = split_text_into_chunks(all_text)
                    st.info(f"Split documents into {len(chunks)} chunks.")
                    
                    # Create and save FAISS index
                    create_and_save_index(chunks)
                    st.session_state.index_loaded = True
                    st.success("Documents processed and index built successfully!")
                else:
                    st.error("No valid text could be extracted from the files.")

# --- MAIN CHAT INTERFACE ---
if not st.session_state.index_loaded:
    st.info("👈 Please upload and process documents from the sidebar to begin chatting.")
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("View Source Context"):
                    for idx, doc in enumerate(message["sources"]):
                        st.markdown(f'<div class="source-doc"><b>Chunk {idx+1}:</b><br>{doc.page_content}</div>', unsafe_allow_html=True)
    
    # Handle user input
    user_query = st.chat_input("Ask a question about your documents...")
    if user_query:
        if llm_type == "Groq (Free)" and not api_key:
            st.error(f"{llm_type} API key is missing. Add it in the sidebar.")
        else:
            # Display user message
            st.chat_message("user").markdown(user_query)
            # Add to history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            with st.chat_message("assistant"):
                with st.spinner("Generating answer..."):
                    try:
                        vectorstore = load_index()
                        retrieved_docs = retrieve_context(user_query, vectorstore)
                        
                        answer = generate_answer(user_query, retrieved_docs, model_type=llm_type, api_key=api_key)
                        
                        st.markdown(answer)
                        
                        source_docs = []
                        if answer != "Answer not found in provided documents.":
                            source_docs = retrieved_docs
                            with st.expander("View Source Context"):
                                for idx, doc in enumerate(source_docs):
                                    st.markdown(f'<div class="source-doc"><b>Chunk {idx+1}:</b><br>{doc.page_content}</div>', unsafe_allow_html=True)
                        
                        # Add to history
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": answer,
                            "sources": source_docs
                        })
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

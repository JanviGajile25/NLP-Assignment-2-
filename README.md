# 🤖 RAG Chatbot for Technical Documentation

A beautiful, production-ready Retrieval-Augmented Generation (RAG) chatbot built with Streamlit that allows you to upload technical documents and ask questions based strictly on their content.

## ✨ Features

- **Multi-Format Support**: Upload PDF, DOCX, and TXT files
- **Intelligent Document Processing**: Automatic text extraction, cleaning, and chunking
- **Vector Search**: FAISS-powered semantic search for accurate context retrieval
- **Dual LLM Support**: 
  - Groq API (free, no credit card required)
  - Ollama (local deployment)
- **Premium UI**: Modern gradient design with dark/light theme toggle
- **Source Transparency**: View exact document chunks used to generate answers
- **Chat History**: Persistent conversation tracking within sessions
- **Sentence Transformers**: High-quality embeddings for semantic understanding

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd rag-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
python -m streamlit run app.py
```

4. **Get your free Groq API key** (optional)
   - Visit [console.groq.com/keys](https://console.groq.com/keys)
   - No credit card required

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS
- **LLM Integration**: LangChain, Groq, Ollama
- **Vector Store**: FAISS
- **Embeddings**: Sentence Transformers
- **Document Processing**: PyPDF2, python-docx

## 📦 Project Structure

```
rag-chatbot/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
│
├── utils/                      # Core utility modules
│   ├── loader.py              # Document loading (PDF, DOCX, TXT)
│   ├── splitter.py            # Text chunking and cleaning
│   ├── embeddings.py          # Sentence transformer embeddings
│   ├── retriever.py           # FAISS vector store operations
│   └── generator.py           # LLM answer generation
│
├── data/                       # Uploaded documents storage
│   └── BIG DATA.docx          # Sample document
│
└── vectorstore/                # FAISS index storage
    ├── index.faiss            # Vector embeddings index
    └── index.pkl              # Metadata and document store
```

## 🎯 Use Cases

- Technical documentation Q&A
- Research paper analysis
- Internal knowledge base queries
- Educational material exploration
- Legal document review

## 🔧 Configuration

### Using Groq (Recommended)
1. Get a free API key from [Groq Console](https://console.groq.com/keys)
2. Enter it in the sidebar when running the app
3. Or set as environment variable: `GROQ_API_KEY=your_key_here`

### Using Ollama
1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama2`
3. Ensure Ollama is running locally
4. Select "Ollama" in the app sidebar

## 📝 How It Works

1. **Upload Documents**: Add PDF, DOCX, or TXT files via the sidebar
2. **Process**: Documents are extracted, cleaned, and split into chunks
3. **Embed**: Chunks are converted to vector embeddings using Sentence Transformers
4. **Index**: Embeddings are stored in FAISS for fast similarity search
5. **Query**: Ask questions in natural language
6. **Retrieve**: Most relevant chunks are retrieved using semantic search
7. **Generate**: LLM generates answers based only on retrieved context

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

# 🤖 Langchain RAG Tutorial - Enhanced Edition

A comprehensive tutorial for building a **RAG (Retrieval Augmented Generation)** chatbot using LangChain, ChromaDB, OpenAI, and n8n workflow automation.

> **New!** 🚀 Complete the [60-minute Lightning Tutorial](LIGHTNING_TUTORIAL.md) to get up and running fast!

## 🌟 What's New in This Version

This enhanced version includes:

- ✅ **Improved Python scripts** with better error handling and progress indicators
- ✅ **Enhanced n8n workflow** with robust error handling and source citations
- ✅ **Comprehensive 60-minute tutorial** for complete beginners
- ✅ **Automated setup script** for one-command installation
- ✅ **Better documentation** with troubleshooting guides
- ✅ **Production-ready code** with proper error handling

## 🎯 What You'll Build

- A vector database for semantic search over your documents
- A RAG pipeline that retrieves relevant context for questions
- An AI chatbot interface powered by n8n
- Integration with OpenAI's GPT models
- Source citations for every answer

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd langchain-rag-tutorial

# Run the setup script
chmod +x setup.sh
./setup.sh
```

The script will:
1. Check prerequisites
2. Create virtual environment
3. Install dependencies
4. Set up environment variables
5. Create the vector database
6. Test the installation

### Option 2: Manual Setup

See detailed instructions in [LIGHTNING_TUTORIAL.md](LIGHTNING_TUTORIAL.md)

## 📋 Prerequisites

- **Python 3.9+** ([download](https://www.python.org/downloads/))
- **Node.js 18.17+** ([download](https://nodejs.org/)) - for n8n
- **OpenAI API Key** ([get one](https://platform.openai.com/api-keys))

## 📚 Documentation

- **[Lightning Tutorial](LIGHTNING_TUTORIAL.md)** - Complete 60-minute walkthrough
- **[n8n Setup Guide](N8N_SETUP.md)** - Detailed n8n installation and configuration
- **[Troubleshooting](#-troubleshooting)** - Common issues and solutions

## 🏗️ Project Structure

```
langchain-rag-tutorial/
├── create_database.py              # Original database creation script
├── create_database_improved.py     # Enhanced version with progress indicators
├── query_data.py                   # Original query script
├── query_data_improved.py          # Enhanced version with better error handling
├── compare_embeddings.py           # Compare different embedding strategies
├── n8n_workflow.json              # Original n8n workflow
├── n8n_workflow_improved.json     # Enhanced workflow with better error handling
├── setup.sh                       # Automated setup script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── LIGHTNING_TUTORIAL.md          # 60-minute comprehensive tutorial
├── N8N_SETUP.md                   # n8n installation guide
├── README.md                      # This file
├── data/
│   └── books/
│       └── alice_in_wonderland.md # Sample document
└── chroma/                        # Vector database (created after setup)
```

## 🔧 Installation

### Step 1: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Create Vector Database

```bash
# Use improved version (recommended)
python create_database_improved.py

# Or use original version
python create_database.py
```

### Step 4: Test RAG Query

```bash
# Use improved version (recommended)
python query_data_improved.py "Who is Alice?"

# Or use original version
python query_data.py "Who is Alice?"
```

Expected output:
```
Response: Alice is the main character...
Sources: [{"file": "data/books/alice_in_wonderland.md", "score": 0.89}]
```

### Step 5: Set Up n8n Workflow

```bash
# Install and start n8n
npx n8n

# Open http://localhost:5678
# Import n8n_workflow_improved.json
# Configure nodes as described in LIGHTNING_TUTORIAL.md
```

## 💻 Usage

### Command Line Interface

```bash
# Query your documents
python query_data_improved.py "Your question here"

# Recreate database (after adding new documents)
python create_database_improved.py

# Compare different embedding strategies
python compare_embeddings.py
```

### n8n Chat Interface

1. Start n8n: `npx n8n`
2. Open http://localhost:5678
3. Activate the workflow
4. Click "Chat" button
5. Start asking questions!

### Adding Your Own Documents

1. Add `.md`, `.txt`, or `.pdf` files to `data/books/`
2. Regenerate database: `python create_database_improved.py`
3. Query your new content: `python query_data_improved.py "Question about new content"`

## 🎓 Learning Path

**Beginners** (1 hour):
- Follow [LIGHTNING_TUTORIAL.md](LIGHTNING_TUTORIAL.md)
- Complete all 5 modules
- Build your first RAG chatbot

**Intermediate** (2-3 hours):
- Customize the RAG pipeline parameters
- Experiment with different chunk sizes
- Add conversation memory
- Try different AI models

**Advanced** (1 day):
- Implement streaming responses
- Add multiple data sources
- Create custom embeddings
- Deploy to production

## 🔍 How It Works

### RAG Pipeline Overview

```
User Question
    ↓
1. Embedding Creation (Convert question to vector)
    ↓
2. Similarity Search (Find relevant document chunks)
    ↓
3. Context Retrieval (Get top matching chunks)
    ↓
4. Prompt Construction (Combine question + context)
    ↓
5. LLM Generation (GPT generates answer)
    ↓
Response + Sources
```

### Key Components

1. **Document Loader**: Reads files from `data/books/`
2. **Text Splitter**: Breaks documents into chunks (800 chars, 200 overlap)
3. **Embeddings**: OpenAI embeddings convert text to vectors
4. **Vector Store**: ChromaDB stores and searches vectors
5. **LLM**: OpenAI GPT-4o-mini generates answers
6. **n8n**: Orchestrates the workflow and provides chat UI

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"

```bash
# Make sure .env file exists
ls -la .env

# Check contents (don't commit this file!)
cat .env

# Should contain:
OPENAI_API_KEY=sk-your-key-here
```

### "Database not found"

```bash
# Create the database first
python create_database_improved.py

# Verify it was created
ls -la chroma/
```

### "ModuleNotFoundError"

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### n8n Connection Issues

1. Check Execute Command node path is correct
2. Verify virtual environment activation in command
3. Test Python script independently first
4. Check n8n logs for detailed errors

See [LIGHTNING_TUTORIAL.md](LIGHTNING_TUTORIAL.md#-troubleshooting) for more solutions.

## 🚀 Advanced Features

### Conversation Memory

Add memory to remember chat history:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
# Integrate with your agent
```

### Streaming Responses

Enable real-time response streaming:

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

model = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)
```

### Multiple Data Sources

Combine different document types:

```bash
data/
├── books/       # Markdown files
├── pdfs/        # PDF documents
├── web/         # Scraped web pages
└── notes/       # Plain text notes
```

### Custom Embeddings

Use different embedding models:

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# OpenAI (default, best quality)
embeddings = OpenAIEmbeddings()

# HuggingFace (free, local)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 📊 Performance Tuning

### Chunk Size vs Context

| Chunk Size | Pros | Cons |
|------------|------|------|
| 300-500 | Precise matching | Less context |
| 800-1000 | Good balance | ⭐ Recommended |
| 1500-2000 | More context | Less precise |

### Relevance Threshold

```python
# Strict (fewer results, higher quality)
threshold = 0.75

# Balanced (recommended)
threshold = 0.5

# Relaxed (more results, may include noise)
threshold = 0.3
```

### Number of Results (k)

```python
# Fast, focused
k = 3

# Balanced (recommended)
k = 5

# Comprehensive
k = 10
```

## 🔐 Security Notes

- Never commit `.env` file to version control (already in `.gitignore`)
- Rotate API keys regularly
- Use environment variables for sensitive data
- Consider rate limiting for production use
- Review n8n workflow permissions

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain** - Framework for LLM applications
- **OpenAI** - GPT models and embeddings
- **ChromaDB** - Vector database
- **n8n** - Workflow automation
- Original tutorial inspired by [Pixegami's RAG Tutorial](https://www.youtube.com/watch?v=tcqEUSNCn8I)

## 📞 Support

- 📖 [Full Tutorial](LIGHTNING_TUTORIAL.md)
- 💬 [Open an Issue](https://github.com/your-repo/issues)
- 📧 [Contact the maintainers](mailto:your-email)

## 🗺️ Roadmap

- [ ] Add support for more document types (PDF, DOCX)
- [ ] Implement conversation memory persistence
- [ ] Create web UI with Streamlit/Gradio
- [ ] Add multi-language support
- [ ] Implement hybrid search (keyword + semantic)
- [ ] Add authentication and user management
- [ ] Deploy to cloud (Docker, AWS, etc.)
- [ ] Add analytics and monitoring

---

**Built with ❤️ using LangChain, OpenAI, and n8n**

**Happy Building! 🚀**

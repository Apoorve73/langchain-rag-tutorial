# 🚀 n8n + RAG Lightning Learning Path

**Learn n8n workflows and RAG pipelines in just 1 hour!**

This project has been transformed from a basic RAG tutorial into a comprehensive learning experience that teaches you how to build professional AI chatbots using n8n automation and vector search.

## 🎯 What You'll Learn

- **n8n Workflow Automation**: Build AI-powered workflows
- **RAG Systems**: Implement retrieval-augmented generation
- **Conversational AI**: Add memory and context awareness
- **Professional UX**: Create streaming chat interfaces

## 🚀 Quick Start (1 Hour Learning Path)

**Option 1: Automated Setup**
```bash
python setup.py
```

**Option 2: Manual Setup**
See [README_LEARNING.md](README_LEARNING.md) for the complete step-by-step guide.

## 📁 Project Structure

```
├── README_LEARNING.md     # 🚀 1-hour learning guide
├── setup.py              # Automated setup script
├── main.py               # Basic RAG API wrapper
├── enhanced_rag.py       # RAG with conversation memory
├── streaming_rag.py      # Streaming responses
├── workflows/            # n8n workflow templates
│   ├── basic_rag.json
│   └── professional_chat.json
├── tests/               # Test suite
└── data/books/          # Knowledge base
    └── alice_in_wonderland.md
```

## 🛠️ Tech Stack

- **n8n**: Workflow automation platform
- **LangChain**: RAG framework
- **ChromaDB**: Vector database
- **OpenAI**: Language models
- **Python**: Backend scripting

## 📚 Learning Phases

### Phase 1: Foundation (15 min)
- Environment setup
- Basic RAG system
- n8n installation

### Phase 2: Integration (15 min)
- n8n workflow creation
- API communication
- Basic chatbot

### Phase 3: Enhancement (15 min)
- Conversation memory
- Context awareness
- Advanced RAG features

### Phase 4: Professional (15 min)
- Streaming responses
- Rich formatting
- Production-ready interface

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
# or
python tests/test_rag.py
```

## 🔧 Manual Setup (Alternative)

### Install Dependencies

**MacOS (with onnxruntime workaround):**
```bash
conda install onnxruntime -c conda-forge
pip install -r requirements.txt
pip install "unstructured[md]"
```

**Windows:**
Follow the [C++ Build Tools guide](https://github.com/bycloudai/InstallVSBuildToolsWindows) first.

### Create Database
```bash
python create_database.py
```

### Query Database
```bash
python query_data.py "How does Alice meet the Mad Hatter?"
```

> You'll need an OpenAI API key in your `.env` file.

## 📖 Resources

- **[Complete Learning Guide](README_LEARNING.md)** - Step-by-step 1-hour tutorial
- **[n8n Documentation](https://docs.n8n.io/)** - Workflow automation
- **[LangChain Docs](https://python.langchain.com/)** - RAG framework
- **Tutorial Video**: [RAG+Langchain Python Project](https://www.youtube.com/watch?v=tcqEUSNCn8I)

## 🤝 Contributing

This project is designed for learning! Feel free to:
- Improve the learning guide
- Add more test cases
- Create additional workflows
- Enhance the RAG system

## 📄 License

MIT License - feel free to use this for learning and teaching.

# Langchain RAG Tutorial with n8n Integration

A complete RAG (Retrieval-Augmented Generation) pipeline using LangChain, ChromaDB, and OpenAI, integrated with n8n for an interactive chatbot experience.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18.17.0+ (for n8n)
- OpenAI API key

### Installation

1. **Install Python dependencies:**

   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install "unstructured[md]"
   ```

2. **Handle onnxruntime dependency:**

   - **MacOS users:** Install via conda before installing requirements:
     ```bash
     conda install onnxruntime -c conda-forge
     ```
     See this [thread](https://github.com/microsoft/onnxruntime/issues/11037) for additional help.

   - **Windows users:** Follow the guide [here](https://github.com/bycloudai/InstallVSBuildToolsWindows?tab=readme-ov-file) to install Microsoft C++ Build Tools.

3. **Set up environment variables:**

   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Basic Usage

1. **Create the vector database:**
   ```bash
   python create_database.py
   ```

2. **Query the database:**
   ```bash
   python query_data.py "How does Alice meet the Mad Hatter?"
   ```

   The script now outputs structured JSON with answer, sources, and confidence scores.

3. **Query with conversation memory:**
   ```bash
   python query_data.py "Who is Alice?" --session-id "my-session" --save-memory
   python query_data.py "What happened to her?" --session-id "my-session" --save-memory
   ```

## 🤖 n8n Chatbot Integration

### Setup n8n

1. **Install n8n:**
   ```bash
   # Option 1: Using npx (no installation needed)
   npx n8n
   
   # Option 2: Global installation
   npm install n8n -g
   n8n start
   ```

2. **Access n8n:** Open `http://localhost:5678` in your browser

3. **Import the workflow:**
   - Click **"+"** → **"Import from File"**
   - Select `n8n_workflow.json`
   - Activate the workflow (toggle switch)

4. **Start chatting:**
   - Click on the Chat Trigger node
   - Click **"Open Chat"**
   - Ask questions about Alice in Wonderland!

### Workflow Features

- ✅ Interactive chat interface
- ✅ Conversation memory (remembers context)
- ✅ Source citations
- ✅ Error handling
- ✅ Structured JSON responses

## 📚 Learning Resources

### Comprehensive Tutorial

For a complete **1-hour learning path**, see **[LEARNING_PATH.md](./LEARNING_PATH.md)** which covers:
- RAG concepts and architecture
- Step-by-step setup guide
- Building the pipeline
- Creating n8n workflows
- Best practices and troubleshooting

### Additional Resources

- Video Tutorial: [RAG+Langchain Python Project: Easy AI/Chat For Your Docs](https://www.youtube.com/watch?v=tcqEUSNCn8I&ab_channel=pixegami)
- [LangChain Documentation](https://python.langchain.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📁 Project Structure

```
.
├── create_database.py      # Build vector database from documents
├── query_data.py           # Query RAG pipeline (improved with JSON output)
├── compare_embeddings.py   # Compare embedding vectors
├── n8n_workflow.json       # n8n workflow for chatbot interface
├── requirements.txt        # Python dependencies
├── LEARNING_PATH.md        # Comprehensive tutorial guide
├── N8N_SETUP.md           # Detailed n8n setup instructions
├── data/
│   └── books/
│       └── alice_in_wonderland.md
└── chroma/                 # Vector database (created after running create_database.py)
```

## 🔧 Advanced Features

### Conversation Memory

The pipeline supports conversation memory through:
- Session-based tracking (`--session-id`)
- Persistent storage (`conversation_memory.json`)
- Automatic context inclusion in prompts

### Structured Output

All queries return JSON with:
```json
{
  "answer": "The answer text...",
  "sources": ["path/to/source.md"],
  "confidence": 0.85,
  "error": null
}
```

### Customization

- **Adjust chunk size:** Modify `chunk_size` in `create_database.py`
- **Change model:** Update `model` parameter in `query_data.py`
- **Custom prompts:** Edit `PROMPT_TEMPLATE` in `query_data.py`

## 🐛 Troubleshooting

- **onnxruntime errors:** Use conda installation method (see above)
- **n8n can't find Python:** Use full path to Python executable
- **No responses:** Check OpenAI API key, verify database exists
- **Memory not working:** Ensure `--save-memory` flag is used

## 📝 License

This project is open source and available for learning and modification.

---

**Happy Learning! 🎉**

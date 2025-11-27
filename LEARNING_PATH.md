# 🎓 Learn RAG + n8n in 1 Hour

Build a conversational AI chatbot that answers questions about "Alice in Wonderland" using:
- **RAG (Retrieval-Augmented Generation)** - Find relevant content from documents
- **n8n** - Visual workflow automation
- **OpenAI** - Generate natural language responses
- **ChromaDB** - Vector database for semantic search

---

## 🎯 What You'll Build

A chat interface where you can ask questions like:
- "Who is the Mad Hatter?"
- "What happens at the tea party?"
- "How does Alice change size?"

And get accurate, contextual answers pulled from the actual book!

---

## ⏱️ Learning Path Overview

| Phase | Topic | Duration | What You'll Learn |
|-------|-------|----------|-------------------|
| 🎯 | Prerequisites & Setup | 5 min | Environment setup |
| 📚 | Module 1: Understanding RAG | 5 min | Core concepts |
| 🔧 | Module 2: Building the RAG Pipeline | 20 min | Python + LangChain |
| 🔗 | Module 3: Setting Up n8n | 15 min | Workflow automation |
| 💬 | Module 4: Connecting Everything | 15 min | Integration & testing |

**Total Time: ~60 minutes**

---

## 🎯 Prerequisites (5 minutes)

### Required Software

| Software | Version | Check Command |
|----------|---------|---------------|
| Python | 3.9+ | `python --version` |
| Node.js | 18.17+ | `node --version` |
| pip | Latest | `pip --version` |

### Get Your OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy it for the next step

### Quick Setup

```bash
# 1. Clone the repository (if you haven't already)
git clone <your-repo-url>
cd langchain-rag-tutorial

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your environment file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

> ⚠️ **Important:** Replace `sk-your-key-here` with your actual OpenAI API key

---

## 📚 Module 1: Understanding RAG (5 minutes)

### What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique that makes AI responses more accurate by:

1. **Retrieving** relevant information from your documents
2. **Augmenting** the AI's prompt with this context
3. **Generating** grounded, factual responses

### Why RAG?

| Without RAG | With RAG |
|-------------|----------|
| AI might hallucinate facts | AI uses actual document content |
| Generic responses | Specific, accurate answers |
| No source attribution | Can cite sources |

### The RAG Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Question  │────▶│   Search    │────▶│   Build     │────▶│  Generate   │
│  "Who is    │     │  Vector DB  │     │   Prompt    │     │  Response   │
│  the Mad    │     │  (ChromaDB) │     │  + Context  │     │  (OpenAI)   │
│  Hatter?"   │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │  Relevant   │
                    │  Passages   │
                    │  from Book  │
                    └─────────────┘
```

### What is n8n?

n8n is a **visual workflow automation tool**. Think of it as connecting building blocks:

- **Triggers** start the workflow (chat message received)
- **Nodes** process data (HTTP requests, code execution)
- **Connections** define the data flow between nodes

---

## 🔧 Module 2: Building the RAG Pipeline (20 minutes)

### Step 2.1: Explore the Data (2 min)

Open `data/books/alice_in_wonderland.md` to see our knowledge base - the complete text of Alice's Adventures in Wonderland!

```bash
# Preview the first 50 lines
head -50 data/books/alice_in_wonderland.md
```

### Step 2.2: Create the Vector Database (5 min)

Run the database creation script:

```bash
python create_database.py
```

**What happens behind the scenes:**

1. 📄 **Load** - Reads the markdown file
2. ✂️ **Split** - Breaks text into ~500-character chunks
3. 🔢 **Embed** - Creates vector embeddings using OpenAI
4. 💾 **Store** - Saves to ChromaDB (local vector database)

You should see output like:
```
📚 Starting database creation...
📄 Split 1 documents into 150+ chunks.
💾 Saved chunks to chroma.
✅ Database ready!
```

### Step 2.3: Test the Query System (3 min)

Test the CLI query tool:

```bash
python query_data.py "Who is the White Rabbit?"
```

You should see:
- The context used (passages from the book)
- A generated response about the White Rabbit
- Source attribution

### Step 2.4: Start the RAG API Server (5 min)

Start the Flask API server that n8n will connect to:

```bash
python rag_api.py
```

You should see:
```
==================================================
🐰 Alice in Wonderland RAG API
==================================================
Starting server on http://localhost:5000

Available endpoints:
  POST /query  - Ask questions about Alice in Wonderland
  GET  /health - Health check
  POST /reset  - Clear conversation memory
==================================================
```

### Step 2.5: Test the API (5 min)

**Option A: Using curl**
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the Cheshire Cat look like?"}'
```

**Option B: Using Python**
```python
import requests

response = requests.post(
    "http://localhost:5000/query",
    json={"question": "What does the Cheshire Cat look like?"}
)
print(response.json())
```

**Expected Response:**
```json
{
  "response": "The Cheshire Cat is described as having a very wide grin...",
  "sources": ["data/books/alice_in_wonderland.md"],
  "confidence": 0.85
}
```

✅ **Checkpoint:** Your RAG API is running on `localhost:5000`

---

## 🔗 Module 3: Setting Up n8n (15 minutes)

### Step 3.1: Start n8n (2 min)

In a **new terminal** (keep the RAG API running!):

```bash
npx n8n
```

Open your browser to: **http://localhost:5678**

### Step 3.2: Import the Workflow (3 min)

1. Click **"New Workflow"** (or **+** icon)
2. Click the **"..."** menu (top right)
3. Select **"Import from File"**
4. Choose `n8n_rag_workflow.json` from this project

You should see a workflow with 3 connected nodes:
- **Chat Input** → **Query RAG API** → **Format Response**

### Step 3.3: Understanding the Workflow (5 min)

**Node 1: Chat Input**
- Type: `chatTrigger`
- Purpose: Provides a chat interface to receive user questions

**Node 2: Query RAG API**
- Type: `httpRequest`
- Purpose: Sends the question to your Python RAG server
- URL: `http://localhost:5000/query`

**Node 3: Format Response**
- Type: `code` (JavaScript)
- Purpose: Beautifies the response with confidence scores and emojis

### Step 3.4: Save the Workflow (2 min)

1. Click **"Save"** button
2. Name it: "RAG Chat: Alice in Wonderland"

### Step 3.5: Alternative - Build from Scratch (Optional)

If you want to build the workflow manually:

1. **Add Chat Trigger:**
   - Click **+** → Search "Chat Trigger"
   - Set Title: "Ask about Alice 🐰"

2. **Add HTTP Request:**
   - Click **+** → Search "HTTP Request"
   - Method: POST
   - URL: `http://localhost:5000/query`
   - Body Type: JSON
   - JSON Body: `{{ JSON.stringify({ question: $json.chatInput }) }}`

3. **Add Code Node:**
   - Click **+** → Search "Code"
   - Language: JavaScript
   - Paste the formatting code from `n8n_rag_workflow.json`

4. **Connect the nodes** by dragging from output to input

---

## 💬 Module 4: Connecting Everything (15 minutes)

### Step 4.1: Verify Both Services are Running (2 min)

**Terminal 1 (RAG API):**
```bash
curl http://localhost:5000/health
# Should return: {"status": "healthy", ...}
```

**Terminal 2 (n8n):**
- Open http://localhost:5678
- You should see your workflow

### Step 4.2: Test the Chat Interface (5 min)

1. In n8n, click the **"Chat"** button (bottom right corner)
2. Type: **"Who is the Mad Hatter?"**
3. Press Enter

You should see a response like:
```
The Mad Hatter is a character Alice meets at a tea party...

🎯 Confidence: 85%
📖 Source: Alice in Wonderland
```

### Step 4.3: Try Different Questions (5 min)

Test these questions:

| Question | What it Tests |
|----------|---------------|
| "What happens when Alice drinks the potion?" | Event recall |
| "Describe the Queen of Hearts" | Character description |
| "Who attended the tea party?" | Multiple characters |
| "What is the moral of the story?" | Abstract understanding |

### Step 4.4: Test Conversation Memory (3 min)

The RAG API maintains conversation context:

1. Ask: "Who is Alice?"
2. Then ask: "How old is she?"
3. The system remembers you're talking about Alice!

To reset memory:
```bash
curl -X POST http://localhost:5000/reset
```

---

## 🎉 Congratulations!

You've built a complete RAG chatbot with:

- ✅ **Vector Database** (ChromaDB) storing document embeddings
- ✅ **RAG Pipeline** (LangChain + OpenAI) for intelligent retrieval
- ✅ **REST API** (Flask) for easy integration
- ✅ **Chat Interface** (n8n) for user interaction
- ✅ **Conversation Memory** for contextual chat

---

## 🚀 Next Steps

### Add More Documents

1. Add PDF or text files to `data/books/`
2. Rebuild the database:
   ```bash
   python create_database.py
   ```

### Customize the AI Behavior

Edit the `PROMPT_TEMPLATE` in `rag_api.py` to change how the AI responds.

### Deploy to Production

| Component | Deployment Option |
|-----------|-------------------|
| RAG API | Railway, Render, AWS Lambda |
| n8n | n8n Cloud, self-hosted Docker |
| Database | Pinecone, Weaviate (cloud vector DBs) |

### Add More Data Sources

```python
# PDF support
from langchain_community.document_loaders import PyPDFLoader

# Web scraping
from langchain_community.document_loaders import WebBaseLoader
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" on port 5000 | Start the RAG API: `python rag_api.py` |
| "Connection refused" on port 5678 | Start n8n: `npx n8n` |
| "No matching results" | Rebuild database: `python create_database.py` |
| OpenAI errors | Check your API key in `.env` file |
| n8n won't start | Ensure Node.js 18.17+ is installed |
| Import fails in n8n | Check JSON file format |

### Common Error Messages

**"Unable to find matching results"**
- The question might be too unrelated to the book
- Try more specific questions about characters or events

**"OPENAI_API_KEY not set"**
- Create a `.env` file with your API key
- Make sure the key starts with `sk-`

---

## 📁 Project Structure

```
langchain-rag-tutorial/
├── data/
│   └── books/
│       └── alice_in_wonderland.md    # Knowledge base document
├── chroma/                           # Vector database (auto-generated)
├── create_database.py                # Script to build vector DB
├── query_data.py                     # CLI query tool
├── rag_api.py                        # Flask API for n8n integration
├── n8n_rag_workflow.json             # n8n workflow (import this!)
├── requirements.txt                  # Python dependencies
├── LEARNING_PATH.md                  # This guide!
└── .env                              # Your API keys (create this)
```

---

## 📚 Learn More

- [LangChain Documentation](https://python.langchain.com/docs/)
- [n8n Documentation](https://docs.n8n.io/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

---

## 🤝 Contributing

Found an issue or have an improvement? Open a PR!

---

*Happy Learning! 🐰✨*


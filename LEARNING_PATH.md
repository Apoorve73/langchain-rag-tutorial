# 🚀 1-Hour Learning Path: Build a RAG Chatbot with n8n

**Estimated Time:** 60-70 minutes  
**Difficulty:** Beginner to Intermediate  
**Prerequisites:** Basic Python knowledge, familiarity with command line

---

## 📋 Learning Objectives

By the end of this tutorial, you will:
- ✅ Understand RAG (Retrieval-Augmented Generation) concepts
- ✅ Set up and configure n8n workflows
- ✅ Build a production-ready RAG pipeline with LangChain
- ✅ Create an interactive chatbot interface
- ✅ Implement conversation memory
- ✅ Handle errors gracefully

---

## 🎯 Phase 1: Foundation & Setup (15 minutes)

### Step 1.1: Prerequisites Check (5 min)

Verify you have the required tools installed:

```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 18.17.0+)
node --version

# Check if OpenAI API key is set
echo $OPENAI_API_KEY
```

**If missing:**
- **Python:** Download from [python.org](https://www.python.org/downloads/)
- **Node.js:** Download from [nodejs.org](https://nodejs.org/) (minimum v18.17.0)
- **OpenAI API Key:** Get from [platform.openai.com](https://platform.openai.com/api-keys)

### Step 1.2: Environment Setup (10 min)

1. **Clone or navigate to the project:**
   ```bash
   cd langchain-rag-tutorial
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   # Install main dependencies
   pip install -r requirements.txt
   
   # Install markdown processing dependencies
   pip install "unstructured[md]"
   ```

4. **For MacOS users (if onnxruntime fails):**
   ```bash
   conda install onnxruntime -c conda-forge
   ```

5. **Create `.env` file:**
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```
   Replace `your_key_here` with your actual OpenAI API key.

6. **Test the setup:**
   ```bash
   # Create the vector database
   python create_database.py
   
   # Test a query
   python query_data.py "Who is Alice?"
   ```

   **Expected output:** You should see a JSON response with an answer and sources.

---

## 🧠 Phase 2: Understanding RAG (10 minutes)

### Step 2.1: RAG Concepts Explained (5 min)

**RAG (Retrieval-Augmented Generation)** combines three steps:

1. **Retrieval** 🔍
   - Converts documents into embeddings (vector representations)
   - Stores them in a vector database (ChromaDB)
   - Searches for relevant chunks when a question is asked

2. **Augmentation** 📚
   - Takes the user's question
   - Finds the most relevant document chunks
   - Combines them into a context prompt

3. **Generation** ✨
   - Sends the augmented prompt to an LLM (GPT-3.5/GPT-4)
   - LLM generates an answer based on the provided context

**Why RAG?**
- Provides factual answers from your documents
- Reduces hallucinations
- Allows you to "chat with your documents"

### Step 2.2: Explore the Code (5 min)

**`create_database.py`** - The indexing pipeline:
```python
Documents → Load → Chunk → Embed → Store in ChromaDB
```

**`query_data.py`** - The query pipeline:
```python
Question → Embed → Search → Retrieve Context → Generate Answer
```

**Key components:**
- **ChromaDB:** Vector database for storing embeddings
- **OpenAI Embeddings:** Converts text to vectors
- **LangChain:** Orchestrates the RAG pipeline
- **ChatOpenAI:** Generates answers using GPT

---

## 🔧 Phase 3: Building the RAG Pipeline (15 minutes)

### Step 3.1: Understanding the Improved Pipeline

The improved `query_data.py` includes:

✅ **JSON Output** - Structured responses for n8n  
✅ **Conversation Memory** - Remembers previous messages  
✅ **Better Error Handling** - Graceful failures  
✅ **Improved Prompts** - More natural responses  
✅ **Source Citations** - Shows where answers come from  

### Step 3.2: Test the Pipeline (5 min)

Try these queries to test different scenarios:

```bash
# Simple question
python query_data.py "Who is Alice?"

# Follow-up question (tests memory)
python query_data.py "What happened to her?" --session-id "test" --save-memory

# Complex question
python query_data.py "Tell me about the tea party"

# Question with low relevance
python query_data.py "What is quantum physics?"
```

**Observe:**
- How sources are included
- Confidence scores
- Error handling for edge cases

---

## 🎨 Phase 4: Building the n8n Workflow (20 minutes)

### Step 4.1: Start n8n (2 min)

**Option 1: Using npx (Recommended):**
```bash
npx n8n
```

**Option 2: Global Installation:**
```bash
npm install n8n -g
n8n start
```

**Access:** Open `http://localhost:5678` in your browser

### Step 4.2: Import the Workflow (3 min)

1. In n8n UI, click **"+"** → **"Import from File"**
2. Select `n8n_workflow.json`
3. The workflow will be imported with all nodes configured

### Step 4.3: Configure the Workflow (10 min)

**Workflow Structure:**
```
Chat Trigger → Set Variables → Execute Command → Parse Response
```

**Node Details:**

1. **Chat Trigger** (`When chat message received`)
   - Receives messages from the chat interface
   - No configuration needed

2. **Set Variables**
   - Extracts `chatInput` and `sessionId`
   - Prepares data for the command

3. **Execute Command**
   - Runs: `python query_data.py "{query}" --session-id "{sessionId}" --save-memory`
   - **Important:** Ensure Python path is correct in your environment

4. **Parse Response**
   - Parses JSON output from Python script
   - Formats response for chat
   - Adds source citations
   - Handles errors gracefully

### Step 4.4: Test the Workflow (5 min)

1. **Activate the workflow** (toggle switch in top-right)
2. **Open the chat interface** (click the Chat Trigger node → "Open Chat")
3. **Test queries:**
   - "Who is Alice?"
   - "Tell me about the Mad Hatter"
   - "What happened at the tea party?"

**Check:**
- ✅ Responses are generated
- ✅ Sources are shown
- ✅ Conversation flows naturally
- ✅ Errors are handled gracefully

---

## ✨ Phase 5: Enhancements & Polish (10 minutes)

### Step 5.1: Add Conversation Memory (5 min)

The pipeline now supports conversation memory:

- **Automatic:** Uses `sessionId` to track conversations
- **Persistent:** Saved to `conversation_memory.json`
- **Limited:** Keeps last 10 messages per session

**Test it:**
1. Ask: "Who is Alice?"
2. Follow up: "What happened to her?"
3. Notice how context is maintained

### Step 5.2: Customize the Experience (3 min)

**Modify the prompt** in `query_data.py`:
```python
PROMPT_TEMPLATE = """
Your custom prompt here...
"""
```

**Adjust chunk size** in `create_database.py`:
```python
chunk_size=300,  # Increase for more context
chunk_overlap=100,  # Overlap between chunks
```

**Change model** in `query_data.py`:
```python
model = ChatOpenAI(temperature=0.7, model="gpt-4")  # Use GPT-4
```

### Step 5.3: Final Testing (2 min)

**Test scenarios:**
- ✅ Simple questions
- ✅ Complex multi-part questions
- ✅ Questions outside the book's scope
- ✅ Error handling (e.g., database not found)

---

## 🎓 Key Concepts Learned

### RAG Architecture
```
User Question
    ↓
Embedding Model
    ↓
Vector Search (ChromaDB)
    ↓
Retrieve Top-K Chunks
    ↓
Build Context Prompt
    ↓
LLM Generation
    ↓
Answer + Sources
```

### n8n Workflow Pattern
```
Trigger → Process → Execute → Parse → Respond
```

### Best Practices
- ✅ Always validate inputs
- ✅ Handle errors gracefully
- ✅ Include source citations
- ✅ Use conversation memory
- ✅ Structure outputs (JSON)
- ✅ Test edge cases

---

## 🚀 Next Steps

### Enhancements to Try:
1. **Add more documents** - Expand beyond Alice in Wonderland
2. **Improve chunking** - Use semantic chunking instead of fixed-size
3. **Add reranking** - Improve result quality with reranking models
4. **Stream responses** - Show answers as they're generated
5. **Add authentication** - Secure your chatbot
6. **Deploy** - Host on cloud (n8n Cloud, Railway, etc.)

### Resources:
- [LangChain Documentation](https://python.langchain.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## 🐛 Troubleshooting

### Common Issues:

**Issue:** `onnxruntime` installation fails
- **Solution:** Use conda: `conda install onnxruntime -c conda-forge`

**Issue:** n8n can't find Python
- **Solution:** Use full path: `/usr/bin/python3` or `C:\Python\python.exe`

**Issue:** No responses from chatbot
- **Solution:** Check OpenAI API key, verify database exists, check n8n execution logs

**Issue:** Memory not working
- **Solution:** Ensure `--save-memory` flag is used, check file permissions

---

## 📝 Summary

You've successfully built:
- ✅ A production-ready RAG pipeline
- ✅ An n8n workflow for chat interface
- ✅ Conversation memory system
- ✅ Error handling and source citations

**Time invested:** ~60-70 minutes  
**Skills gained:** RAG, n8n workflows, LangChain, Vector databases

**Congratulations! 🎉** You're now ready to build your own RAG applications!

---

*This tutorial was generated by Composer (AI Assistant) to help you learn RAG and n8n workflows quickly and effectively.*


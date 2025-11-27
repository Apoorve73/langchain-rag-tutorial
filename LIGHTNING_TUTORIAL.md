# 🚀 RAG Chatbot in 60 Minutes - Lightning Tutorial

Build your own AI chatbot that can answer questions about any document using RAG (Retrieval Augmented Generation)!

## 🎯 What You'll Build

By the end of this tutorial, you'll have:
- ✅ A vector database of your documents (using ChromaDB)
- ✅ A smart RAG pipeline that retrieves relevant information
- ✅ A chat interface powered by n8n
- ✅ Integration with OpenAI GPT models
- ✅ Source citations for every answer

## ⏱️ Time Breakdown

- **Prerequisites Check**: 5 minutes
- **Environment Setup**: 10 minutes  
- **RAG Backend Setup**: 10 minutes
- **n8n Installation & Import**: 10 minutes
- **Workflow Configuration**: 15 minutes
- **Testing & Customization**: 10 minutes

**Total: ~60 minutes**

---

## 📋 Module 00: Prerequisites Check (5 minutes)

### What You Need

Before starting, ensure you have:

- [ ] **Python 3.9+** installed
  ```bash
  python --version  # Should show 3.9 or higher
  ```

- [ ] **Node.js 18.17+** installed
  ```bash
  node --version  # Should show 18.17 or higher
  ```

- [ ] **OpenAI API Key**
  - Sign up at [platform.openai.com](https://platform.openai.com)
  - Create an API key
  - Have it ready to paste

- [ ] **Text Editor** (VS Code recommended)

- [ ] **Terminal/Command Line** access

### Quick Verification

Run this one-liner to verify your setup:

```bash
python --version && node --version && echo "✅ Prerequisites OK!"
```

If both commands work, you're ready to proceed!

---

## 🔧 Module 01: Environment Setup (10 minutes)

### Step 1.1: Clone and Navigate to Project

If you haven't already:

```bash
git clone <repository-url>
cd langchain-rag-tutorial
```

### Step 1.2: Create Python Virtual Environment

This keeps your dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 1.3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` - Framework for LLM applications
- `langchain-openai` - OpenAI integration
- `langchain-chroma` - Vector database
- `chromadb` - Vector storage
- `python-dotenv` - Environment variable management
- And other dependencies

**Expected time:** 2-3 minutes

### Step 1.4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit it with your API key
# On macOS: open .env
# On Windows: notepad .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

⚠️ **Important:** Never commit this file to git! It's already in `.gitignore`.

---

## 🤖 Module 02: RAG Backend Setup (10 minutes)

### Understanding RAG

**What is RAG?**
- **R**etrieval: Find relevant document chunks
- **A**ugmented: Add them to the prompt
- **G**eneration: Generate answer with context

**Why use RAG?**
- Answers based on YOUR documents
- No hallucinations about your content
- Source citations for transparency
- Works with any text documents

### Step 2.1: Explore the Data

Look at what's in `data/books/`:

```bash
ls -la data/books/
```

You should see `alice_in_wonderland.md` - this is your initial knowledge base!

**💡 Pro Tip:** You can add your own documents here:
- Supported formats: `.md`, `.txt`, `.pdf`
- Just drop files in `data/books/`
- Re-run the database creation

### Step 2.2: Create Vector Database

Run the improved database creation script:

```bash
python create_database_improved.py
```

**What's happening?**
1. 📚 Loading documents from `data/books/`
2. ✂️ Splitting into chunks (800 chars each)
3. 🧮 Creating embeddings (vector representations)
4. 💾 Saving to ChromaDB

**Expected output:**
```
🚀 Starting database creation...
============================================================
📚 Step 1: Loading documents from data/books...
   ✓ Loaded 1 documents
     • alice_in_wonderland.md
✂️  Step 2: Splitting documents into chunks...
   ✓ Split 1 documents into 45 chunks
💾 Step 3: Saving to ChromaDB...
   ✓ Saved 45 chunks to chroma
============================================================
✅ Database created successfully!
```

### Step 2.3: Test RAG Query

Let's test the query system:

```bash
python query_data_improved.py "Who is Alice?"
```

**Expected output:**
```
Response: Alice is the main character of the story...
Sources: [{"file": "data/books/alice_in_wonderland.md", "score": 0.89}]
```

**Try more queries:**
```bash
python query_data_improved.py "What is the Mad Hatter like?"
python query_data_improved.py "Tell me about the Cheshire Cat"
```

### 🎓 Learning Moment

**How does this work?**

1. **Your question** → Converted to embedding (vector)
2. **Vector search** → Find similar document chunks
3. **Context retrieval** → Get top 3-5 most relevant chunks
4. **LLM generation** → GPT uses context to answer
5. **Response** → Answer + sources returned

**Key concepts:**
- **Embeddings**: Numbers representing text meaning
- **Similarity search**: Find text with similar meaning
- **Chunk size**: Balance between context and precision
- **k parameter**: How many chunks to retrieve

---

## 🔄 Module 03: n8n Installation & Import (10 minutes)

### What is n8n?

n8n is a workflow automation tool that connects different services together. Think of it as:
- Visual programming for APIs
- IFTTT/Zapier but self-hosted
- Perfect for AI agent workflows

### Step 3.1: Install and Start n8n

**Option A: Quick Start (No Installation)**
```bash
npx n8n
```

**Option B: Global Installation**
```bash
npm install n8n -g
n8n start
```

**What happens:**
- n8n starts on http://localhost:5678
- Browser opens automatically (or open manually)
- First-time setup screen appears

### Step 3.2: Initial n8n Setup

1. **Create Account** (local only, no signup needed)
   - Email: your@email.com (any email works locally)
   - Password: Your choice
   - Click "Create account"

2. **Welcome Screen**
   - You'll see the n8n dashboard
   - Click "Create new workflow" or skip tour

### Step 3.3: Import the RAG Workflow

1. **In n8n UI:**
   - Click "..." menu (top right)
   - Select "Import from file"

2. **Select Workflow File:**
   - Navigate to your project folder
   - Choose `n8n_workflow_improved.json`
   - Click "Open"

3. **Verify Import:**
   - You should see the workflow canvas
   - Multiple nodes connected together
   - Don't worry if there are warnings yet!

### 🎓 Understanding the Workflow

The workflow has 6 nodes:

```
📥 Chat Trigger → 🤖 AI Agent → 🐍 Execute Python → 📝 Parse Output
                      ↓
                  🧠 OpenAI Model
```

1. **Chat Trigger**: Receives user messages
2. **AI Agent**: Orchestrates the conversation
3. **OpenAI Model**: Powers the AI responses
4. **Execute Python**: Runs your RAG query
5. **Parse Output**: Formats the response
6. **Sticky Notes**: Instructions and config

---

## ⚙️ Module 04: Workflow Configuration (15 minutes)

### Step 4.1: Add OpenAI Credentials

1. **Open OpenAI Model node**
   - Double-click "OpenAI Model" node
   - You'll see credential dropdown

2. **Create New Credential**
   - Click "Create New Credential"
   - Name: "OpenAI RAG"
   - API Key: Paste your OpenAI key
   - Click "Save"

3. **Verify Connection**
   - Node should show green checkmark
   - If red X, check your API key

### Step 4.2: Configure Execute Command Node

This is the critical step connecting n8n to your RAG backend!

1. **Double-click "Query RAG Pipeline" node**

2. **Update Command:**
   ```bash
   cd /Users/YOUR_USERNAME/path/to/langchain-rag-tutorial && source venv/bin/activate && python query_data_improved.py "{{ $('When chat message received').item.json.chatInput }}"
   ```

   **Replace:**
   - `/Users/YOUR_USERNAME/path/to/langchain-rag-tutorial` with your actual project path
   - On Windows, use: `call venv\Scripts\activate` instead of `source venv/bin/activate`

3. **Get your project path:**
   ```bash
   # In your project directory, run:
   pwd  # macOS/Linux
   cd   # Windows
   ```

4. **Click "Save"**

### Step 4.3: Test Individual Nodes

Before testing the whole workflow, test each node:

1. **Test Chat Trigger**
   - Click "Test Node" button
   - Type a message: "Hello"
   - Should pass through successfully

2. **Test Execute Command**
   - Click "Test Node" 
   - Should execute Python script
   - Check for errors in output

3. **Test Parse Output**
   - Should format the response nicely

**Troubleshooting:**
- ❌ "Command not found" → Check path in Execute Command
- ❌ "ModuleNotFoundError" → Virtual environment not activated
- ❌ "OPENAI_API_KEY not found" → Check .env file location

### Step 4.4: Activate and Test Chat

1. **Save the Workflow**
   - Click "Save" button (top right)
   - Name it: "RAG Chatbot"

2. **Activate the Workflow**
   - Toggle "Active" switch (top right)
   - Should turn blue/green

3. **Open Chat Interface**
   - Click "Chat" button (top right)
   - Chat window opens

4. **Test Queries:**
   ```
   You: Who is Alice?
   Bot: [Should provide answer with sources]
   
   You: What happens in the story?
   Bot: [Should provide answer with sources]
   ```

**Success looks like:**
```
Bot: Alice is the main character who falls down a rabbit hole...

📚 Sources:
1. alice_in_wonderland.md (confidence: 89%)
2. alice_in_wonderland.md (confidence: 87%)
```

---

## 🧪 Module 05: Testing & Customization (10 minutes)

### Comprehensive Testing

Try these different types of queries:

**1. Factual Questions**
```
- Who is Alice?
- What is the Mad Hatter known for?
- Describe the Cheshire Cat
```

**2. Plot Questions**
```
- What happens at the tea party?
- How does Alice grow and shrink?
- How does the story end?
```

**3. Analysis Questions**
```
- What themes are in the story?
- Who are the main characters?
- What is this book about?
```

**4. Edge Cases**
```
- [Empty message]
- What is quantum physics? (should say "not in knowledge base")
- [Very long question]
```

### Quick Customizations

#### Option A: Change Chat Personality

1. Open "AI Agent" node
2. Find "System Message"
3. Try different personalities:

**Friendly Librarian:**
```
You are an enthusiastic librarian who LOVES Alice in Wonderland! 
Answer questions with excitement and encourage readers to explore more. 
Use emojis occasionally. 🎩📚
```

**Academic Scholar:**
```
You are a literature professor specializing in Victorian children's literature.
Provide detailed, analytical responses with context about the time period and author.
```

**Kid-Friendly Guide:**
```
You are a friendly storyteller explaining Alice in Wonderland to children.
Use simple words, be encouraging, and make it fun!
```

#### Option B: Add Conversation Memory

Make the bot remember previous messages:

1. Click on "AI Agent" node
2. Click the "+" button
3. Select "Memory" → "Window Buffer Memory"
4. Configure:
   - Context Window Size: 5
   - Memory Key: "chat_history"
5. Save and test:
   ```
   You: Who is Alice?
   Bot: [Answers]
   
   You: What happens to her? (Notice: "her" reference works!)
   Bot: [Continues conversation context]
   ```

#### Option C: Add Your Own Documents

**Add new knowledge:**

1. **Prepare documents:**
   - Save as `.md`, `.txt`, or `.pdf`
   - Put in `data/books/` folder

2. **Regenerate database:**
   ```bash
   python create_database_improved.py
   ```

3. **Test new knowledge:**
   ```bash
   python query_data_improved.py "Question about your new doc"
   ```

4. **Works in n8n automatically!**

**Example documents to try:**
- Company documentation
- Research papers
- Meeting notes
- Product manuals
- Blog posts

### Performance Tuning

Edit `query_data_improved.py` to adjust:

**More context (slower, more comprehensive):**
```python
results = db.similarity_search_with_relevance_scores(query_text, k=10)
context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results[:5]])
```

**Stricter relevance (more "I don't know" responses):**
```python
if len(results) == 0 or results[0][1] < 0.75:  # Raised from 0.5
```

**Different model (cheaper/faster):**
```python
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
```

---

## 🎉 Congratulations!

You've built a complete RAG chatbot! 

### What You've Learned

✅ How RAG works (Retrieval Augmented Generation)  
✅ Vector databases and embeddings  
✅ Document chunking strategies  
✅ n8n workflow automation  
✅ Integrating AI with custom backends  
✅ Error handling and testing  

### Next Steps

**Beginner:**
- Add more documents to your knowledge base
- Try different chat personalities
- Experiment with chunk sizes

**Intermediate:**
- Add streaming responses for real-time output
- Implement conversation memory persistence
- Add multiple data sources (PDFs, websites)
- Create a web UI instead of n8n chat

**Advanced:**
- Fine-tune embeddings for your domain
- Implement hybrid search (keyword + semantic)
- Add citation with page numbers
- Deploy to production with Docker
- Add user authentication
- Implement conversation branching

---

## 🐛 Troubleshooting

### Common Issues

**1. "OPENAI_API_KEY not found"**
- Check `.env` file exists in project root
- Verify the key is correct
- Make sure no spaces around `=`
- Restart terminal after creating `.env`

**2. "Database not found"**
- Run `python create_database_improved.py` first
- Check `chroma/` folder exists
- Verify you're in the right directory

**3. "Command not found" in n8n**
- Check the path in Execute Command node
- Use absolute paths, not relative
- On Windows, use backslashes: `C:\Users\...`
- Make sure virtual environment activates

**4. "ModuleNotFoundError"**
- Verify virtual environment is activated
- Re-install requirements: `pip install -r requirements.txt`
- Check you're using the right Python: `which python`

**5. Slow responses**
- Reduce `k` parameter (fewer chunks to process)
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Check internet connection (API calls)

**6. Poor answer quality**
- Increase `k` parameter (more context)
- Adjust chunk size in `create_database_improved.py`
- Lower relevance threshold
- Check source documents are relevant

**7. n8n port already in use**
```bash
n8n start --port 5679
```

### Getting Help

- 📖 [LangChain Documentation](https://python.langchain.com/)
- 📖 [n8n Documentation](https://docs.n8n.io/)
- 💬 [n8n Community Forum](https://community.n8n.io/)
- 🐛 [Report issues on GitHub](https://github.com/your-repo/issues)

---

## 📚 Additional Resources

### Learn More About RAG

- [What is RAG? - AWS Guide](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### Learn More About n8n

- [n8n Quickstart](https://docs.n8n.io/getting-started/quickstart/)
- [n8n AI Nodes](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain/)
- [Building AI Agents with n8n](https://blog.n8n.io/tag/ai-agents/)

### Expand Your Project

- **Add Web Scraping**: Automatically scrape and index websites
- **Schedule Updates**: Use n8n cron to re-index periodically
- **Multi-modal RAG**: Add images, audio transcripts
- **Custom UI**: Build with React, Streamlit, or Gradio
- **Analytics**: Track popular questions, response quality

---

## 📝 Summary

In just 60 minutes, you've built a production-ready RAG chatbot that:

- 🔍 Searches through document collections semantically
- 🤖 Generates accurate answers with GPT
- 📚 Provides source citations
- 💬 Offers a chat interface
- 🔧 Is fully customizable and extensible

**Keep experimenting and building!** 🚀

---

## 📄 License

This tutorial is part of the langchain-rag-tutorial project.

## 🙏 Credits

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- Automated with [n8n](https://n8n.io/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)

---

**Happy Building! 🎉**

*Have questions or improvements? Open an issue or PR on GitHub!*


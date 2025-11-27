# 🚀 n8n + RAG Lightning Learning Path

**Learn n8n workflows and RAG pipelines in just 1 hour!**

This guide transforms a basic RAG demo into a comprehensive learning experience. You'll build a professional chatbot that can answer questions about *Alice in Wonderland* using n8n automation and vector search.

## 🎯 Learning Objectives

By the end of this hour, you'll know how to:
- Set up n8n workflows for AI automation
- Build a RAG (Retrieval-Augmented Generation) system
- Create conversational AI with memory
- Deploy a professional chat interface

## ⏰ Time Breakdown (60 minutes)

- **0-15 min**: Foundation Setup
- **15-30 min**: Basic RAG Integration
- **30-45 min**: Conversational Memory
- **45-60 min**: Professional Chat Interface

---

## Phase 1: Foundation Setup (15 minutes)

### Step 1: Environment Setup

**1.1 Install Dependencies**
```bash
# Clone this repository
git clone <repository-url>
cd langchain-rag-tutorial

# Install Python dependencies
pip install -r requirements.txt
pip install "unstructured[md]"

# For Mac users with onnxruntime issues:
conda install onnxruntime -c conda-forge
```

**1.2 Set up OpenAI API Key**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**1.3 Create Knowledge Base**
```bash
python create_database.py
```

**1.4 Install and Start n8n**
```bash
# Option 1: Quick start (recommended)
npx n8n

# Option 2: Install globally
npm install n8n -g
n8n start

# Option 3: Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**1.5 Verify Setup**
- Open http://localhost:5678
- Test RAG system: `python main.py "Who is the Mad Hatter?"`

---

## Phase 2: Basic RAG Integration (15 minutes)

### Step 2: Create Your First n8n Workflow

**2.1 Import Basic Workflow**
1. In n8n UI, click the **"+"** button
2. Choose **"Import from File"**
3. Select `workflows/basic_rag.json`
4. Click **"Import workflow"**

**2.2 Understand the Workflow**
The workflow has 4 nodes:
- **Chat Trigger**: Receives messages from users
- **Execute Command**: Runs your RAG script
- **Set**: Parses the JSON response
- **Chat**: Sends response back to user

**2.3 Configure the Path**
Edit the "Execute RAG Query" node:
```bash
# Replace /path/to/your/project with your actual path
cd /Users/your-username/path/to/langchain-rag-tutorial && python main.py --json "{{ $json.chatInput }}"
```

**2.4 Test Your Chatbot**
1. Save the workflow (Ctrl+S)
2. Click **"Test workflow"**
3. Open the chat interface
4. Ask: *"What happens when Alice falls down the rabbit hole?"*

**Expected Result**: You should get a response about Alice's adventure!

---

## Phase 3: Conversational Memory (15 minutes)

### Step 3: Add Conversation Context

**3.1 Import Enhanced Workflow**
1. Create a new workflow
2. Import `workflows/professional_chat.json`

**3.2 The Enhanced RAG Script**
The `enhanced_rag.py` adds:
- **Conversation Memory**: Remembers previous messages
- **Context Awareness**: Provides more natural responses
- **Session Management**: Tracks conversation threads

**3.3 Test Conversation Flow**
1. Save and activate the workflow
2. Start a conversation:
   - *"Who is the Cheshire Cat?"*
   - *"What does he say to Alice?"*
   - *"Tell me more about his character"*

Notice how the bot remembers the context!

**3.4 Understanding Memory**
The system maintains conversation history and uses it to provide more contextual responses.

---

## Phase 4: Professional Chat Interface (15 minutes)

### Step 4: Streaming & Rich Responses

**4.1 The Streaming System**
The `streaming_rag.py` provides:
- **Real-time Responses**: Words appear as they're generated
- **Rich Metadata**: Sources and confidence scores
- **Professional UX**: Formatted responses with emojis

**4.2 Customize Your Chatbot**
Edit the Chat Trigger node:
```javascript
// Change the system message
"You are a literary expert specializing in Alice in Wonderland.
You have access to the full text and can provide detailed analysis."
```

**4.3 Add Response Formatting**
The workflow includes:
- 📚 **Sources**: Which parts of the book were referenced
- 🎯 **Confidence**: How sure the system is about the answer
- 💬 **Streaming**: Real-time text generation

**4.4 Advanced Features**
Try asking complex questions:
- *"Compare the Mad Hatter and March Hare"*
- *"What themes does the book explore?"*
- *"How does Alice change throughout the story?"*

---

## 🎉 Congratulations!

You've built a professional RAG chatbot! Here's what you accomplished:

### ✅ What You Built
- **RAG Pipeline**: Vector search + LLM generation
- **n8n Workflow**: Automated AI processing
- **Conversation Memory**: Contextual chat experience
- **Streaming Interface**: Professional UX

### 🛠️ Technical Skills Learned
- n8n workflow creation and automation
- LangChain RAG implementation
- Vector database integration (ChromaDB)
- API design and JSON communication
- Python scripting for AI applications

### 🚀 Next Steps
- **Deploy**: Host on Railway, Vercel, or your server
- **Enhance**: Add more documents to your knowledge base
- **Customize**: Modify prompts for different use cases
- **Scale**: Add user authentication and analytics

---

## 📚 Additional Resources

### n8n Learning
- [n8n Documentation](https://docs.n8n.io/)
- [n8n University](https://university.n8n.io/)
- [Community Forum](https://community.n8n.io/)

### RAG & LangChain
- [LangChain Docs](https://python.langchain.com/)
- [RAG Tutorial](https://www.youtube.com/watch?v=tcqEUSNCn8I)
- [Vector Databases Guide](https://www.pinecone.io/learn/vector-database/)

### Troubleshooting
- **n8n not starting**: Check if port 5678 is available
- **RAG errors**: Verify your OpenAI API key
- **Import fails**: Ensure workflow JSON is valid

---

## 🏆 Challenge Projects

**Beginner**: Add a web search capability
**Intermediate**: Implement user authentication
**Advanced**: Create a multi-document RAG system

Happy learning! 🎓
